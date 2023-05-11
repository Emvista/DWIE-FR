"""
Author: Sylvain Verdy @ Fev 2023
"""

import argparse
from tqdm import tqdm
from collections import deque


def prepare_data(data):
    list_elements = deque()
    list_labels = deque()
    list_labels_by_sentences = []
    list_sentences = []
    count = 0

    for row in tqdm(range(0, len(data)), disable=True):
        if data[row] != '\n':
            sentence = data[row].split('\t')
            list_elements.append(sentence[0])
            list_labels.append(sentence[1].split('\n')[0])
        if data[row] == '\n':
            list_sentences.append(' '.join(list_elements))
            list_labels_by_sentences.append(' '.join(list_labels))
            list_labels.clear(), list_elements.clear()
            count +=1

    return list_labels_by_sentences, list_sentences



class BIO_convertor:
    def __init__(self, path_file_origin, save_file) -> None:
        self.path_file_origin = self.read_file(path_file_origin)
        self.labels, self.origin = prepare_data(self.path_file_origin)
        self.save_file = save_file
        self.save_file_data()
        
        
    def read_file(self, path):
        data = open(path, 'r').readlines()
        return data

    def save_file_data(self,):
        
        list_word_tag = []
        prev_label = "O"
        for i in tqdm(range(0, len(self.origin))):
            for a, word in enumerate(self.origin[i].split()):
                label = self.labels[i].split()[a]
                if label == 'O':
                    list_word_tag.append(word + '\t' + 'O')
                    prev_label = label

                else:
                    if prev_label == 'O' or label != prev_label.split("-")[1]:
                        label = f'B-{label}'
                        list_word_tag.append(word + '\t' + label)
                    else:
                        label = f'I-{label}'
                        list_word_tag.append(word + '\t' + label)

                    prev_label = label

            list_word_tag.append("")

        n_names = ["{}\n".format(i) for i in list_word_tag]

        with open(self.save_file, "w") as file:
            file.writelines(n_names)
            file.close()    

def main():

    convert = BIO_convertor(params['input_path'] , params['output_path'])
    convert.save_file_data()


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="Arguments for the DWIE Preprocessing.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-i",
        "--input_path",
        help="Path to the dwie content directory",
        default="./new_data/",
    )

    parser.add_argument(
        "-o",
        "--output_path",
        help="Path to the dwie content directory",
        default="./new_data/",
    )
    args = parser.parse_args()
    params = vars(args)
    # if not os.path.exists(params["output_path"]):
    #     os.makedirs(params["output_path"])
    main()




        