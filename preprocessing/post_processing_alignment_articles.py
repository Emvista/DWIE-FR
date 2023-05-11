import argparse
from tqdm import tqdm
from collections import deque
from unidecode import unidecode
import pandas as pd


def prepare_data(data):
    list_elements = deque()
    list_labels = deque()
    list_labels_by_sentences = []
    list_sentences = []
    for row in tqdm(range(0, len(data)), disable=True):
        if data[row] != '\n':
            sentence = data[row].split('\t')
            list_elements.append(sentence[0])
            list_labels.append(sentence[1].split('\n')[0]) #.split('\n')[0])
        if data[row] == '\n':
            list_sentences.append(' '.join(list_elements))
            list_labels_by_sentences.append(' '.join(list_labels))
            list_labels.clear(), list_elements.clear()
    assert len(list_labels_by_sentences) == len(list_sentences)
    return list_labels_by_sentences, list_sentences


class KeepAlign:
    def __init__(self, path_file_fr, path_file, save_file) -> None:
        self.path_file_fr = self.read_file(path_file_fr)
        self.path_file = self.read_file(path_file)
        self.labels, self.origin = prepare_data(self.path_file_fr)
        self.save_file = save_file
        self.stopwords = open('./stopwords.txt', 'r').read().splitlines() 

    def read_file(self, path):
        data = open(path, 'r').readlines()
        return data
    def dict_and_replace(self, deep_ontologie):
        list_word_tag = []
        list_articles_between = ["du", "de", 'd', "'", "des", "-"]
        list_articles = ["le", "l", "l'","la", "les"]
        list_articles_between_two_tokens = ['l', 'd', '-', "'"]

        df = pd.read_csv("./onto_deep_dwie.csv", sep=",")
        new_deep_parents = df[['Deep4', 'Deep'+ str(deep_ontologie)]]

        count = 0
        footer = True
        for i in tqdm(range(0, len(self.origin))):

            a = 0
            if 'footer' not in self.labels[i].split() and footer != True:
                while a != len(self.origin[i].split()):
                    word = self.origin[i].split()[a]
                    if self.labels[i].split()[a] != ("CARDINAL" or "justice_misc"):
                        if word == "Pays-Bas":
                            if deep_ontologie == "4":
                                new_value = new_deep_parents.loc[(new_deep_parents['Deep4']== "gpe0").values, 'Deep'+ str(deep_ontologie)].iloc[0]
                                new_value = new_value[0]
                            else:
                                new_value = new_deep_parents.loc[(new_deep_parents['Deep4']== "gpe0").values, 'Deep'+ str(deep_ontologie)].iloc[0]

                            list_word_tag.append(word + '\t' + str(new_value))
                        
                        elif word in list_articles or word in list_articles_between:
                            if a < len(self.origin[i].split())-1 and a > 1 and self.labels[i].split()[a+1] == self.labels[i].split()[a-1] and self.labels[i].split()[a-1] != "O":
                                
                                list_word_tag.append(word + '\t' + self.labels[i].split()[a+1])

                            elif word in list_articles_between_two_tokens and a < len(self.origin[i].split())-2 and a >= 1 and self.labels[i].split()[a+2] == self.labels[i].split()[a-1] and self.labels[i].split()[a-1] != "O":
                                list_word_tag.append(word + '\t' + self.labels[i].split()[a-1])

                            elif word in list_articles_between_two_tokens and a < len(self.origin[i].split())-1 and a >= 2 and self.labels[i].split()[a+1] == self.labels[i].split()[a-2] and self.labels[i].split()[a-2] != "O":
                                list_word_tag.append(word + '\t' + self.labels[i].split()[a-2])

                            elif a < len(self.origin[i].split())-2 and a > 2  and word in list_articles_between_two_tokens and self.labels[i].split()[a-1] in list_articles_between and self.labels[i].split()[a+1] in list_articles_between_two_tokens and self.labels[i].split()[a-2] != "O" and self.labels[i].split()[a-2] == self.labels[i].split()[a+2]:
                                list_word_tag.append(word + '\t' + self.labels[i].split()[a-2])
                                
                            elif a < len(self.origin[i].split())-3 and self.origin[i].split()[a+1] == ('l' or 'd') and self.origin[i].split()[a+2] == "'" and word =="de" and self.labels[i].split()[a+3] != "O" and self.labels[i].split()[a-1] == self.labels[i].split()[a+3]:

                                list_word_tag.append(word + '\t' + self.labels[i].split()[a+3])
                                list_word_tag.append(self.origin[i].split()[a+1] + '\t' + self.labels[i].split()[a+3])
                                list_word_tag.append(self.origin[i].split()[a+2] + '\t' + self.labels[i].split()[a+3])
                                a +=2
                            elif a < len(self.origin[i].split())-1 and a > 1 and self.labels[i].split()[a+1] != self.labels[i].split()[a-1] and self.labels[i].split()[a-1] == "O":
                                list_word_tag.append(word + '\t' + 'O')

                            else:
                                list_word_tag.append(word + '\t' + self.labels[i].split()[a])
                            
                        else:
                            list_word_tag.append(word + '\t' + self.labels[i].split()[a])
                    elif self.labels[i].split()[a] == "justice_misc":
                        list_word_tag.append(word + '\t' + "case")
                    else:
                        list_word_tag.append(word + '\t' + "O")

                    a +=1     
                list_word_tag.append("")
                count +=1                    
            
            elif footer:
                a = 0
                while a != len(self.origin[i].split()):
                    word = self.origin[i].split()[a]
                    if self.labels[i].split()[a] != ("CARDINAL" or "justice_misc"):
                        if word == "Pays-Bas":
                            if deep_ontologie == "4":
                                new_value = new_deep_parents.loc[(new_deep_parents['Deep4']== "gpe0").values, 'Deep'+ str(deep_ontologie)].iloc[0]
                                new_value = new_value[0]
                            else:
                                new_value = new_deep_parents.loc[(new_deep_parents['Deep4']== "gpe0").values, 'Deep'+ str(deep_ontologie)].iloc[0]

                            list_word_tag.append(word + '\t' + str(new_value))
                        
                        elif word in list_articles or word in list_articles_between:
                            if a < len(self.origin[i].split())-1 and a > 1 and self.labels[i].split()[a+1] == self.labels[i].split()[a-1] and self.labels[i].split()[a-1] != "O":
                                
                                list_word_tag.append(word + '\t' + self.labels[i].split()[a+1])

                            elif word in list_articles_between_two_tokens and a < len(self.origin[i].split())-2 and a >= 1 and self.labels[i].split()[a+2] == self.labels[i].split()[a-1] and self.labels[i].split()[a-1] != "O":
                                list_word_tag.append(word + '\t' + self.labels[i].split()[a-1])

                            elif word in list_articles_between_two_tokens and a < len(self.origin[i].split())-1 and a >= 2 and self.labels[i].split()[a+1] == self.labels[i].split()[a-2] and self.labels[i].split()[a-2] != "O":
                                list_word_tag.append(word + '\t' + self.labels[i].split()[a-2])

                            elif a < len(self.origin[i].split())-2 and a > 2  and word in list_articles_between_two_tokens and self.labels[i].split()[a-1] in list_articles_between and self.labels[i].split()[a+1] in list_articles_between_two_tokens and self.labels[i].split()[a-2] != "O" and self.labels[i].split()[a-2] == self.labels[i].split()[a+2]:
                                list_word_tag.append(word + '\t' + self.labels[i].split()[a-2])
                                
                            elif a < len(self.origin[i].split())-3 and self.origin[i].split()[a+1] == ('l' or 'd') and self.origin[i].split()[a+2] == "'" and word =="de" and self.labels[i].split()[a+3] != "O" and self.labels[i].split()[a-1] == self.labels[i].split()[a+3]:

                                list_word_tag.append(word + '\t' + self.labels[i].split()[a+3])
                                list_word_tag.append(self.origin[i].split()[a+1] + '\t' + self.labels[i].split()[a+3])
                                list_word_tag.append(self.origin[i].split()[a+2] + '\t' + self.labels[i].split()[a+3])
                                a +=2
                            elif a < len(self.origin[i].split())-1 and a > 1 and self.labels[i].split()[a+1] != self.labels[i].split()[a-1] and self.labels[i].split()[a-1] == "O":
                                list_word_tag.append(word + '\t' + 'O')

                            else:
                                list_word_tag.append(word + '\t' + self.labels[i].split()[a])
                            
                        else:
                            list_word_tag.append(word + '\t' + self.labels[i].split()[a])
                    elif self.labels[i].split()[a] == "justice_misc":
                        list_word_tag.append(word + '\t' + "case")
                    else:
                        list_word_tag.append(word + '\t' + "O")

                    a +=1     
                list_word_tag.append("")
                count +=1        
        n_names = ["{}\n".format(i) for i in list_word_tag]
        with open(self.save_file, "w") as file:
            file.writelines(n_names)
            file.close()
    

def main():
    
    aligner = KeepAlign(params['input_path'],  params['base_path'], params['output_path'])
    aligner.dict_and_replace(params["deep_ontologie"])

    aligner = KeepAlign(params['input_path'],  params['base_path'], params['output_path'])
    aligner.dict_and_replace(params["deep_ontologie"])




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
        default="./new_data_translate/",
    )

    parser.add_argument(
        "-d",
        "--deep_ontologie",
        help="Path to the dwie content directory",
        default="./new_data_translate/",
    )

    parser.add_argument(
        "-b",
        "--base_path",
        help="Path to the dwie content directory",
        default="./new_data_translate/",
    )

    args = parser.parse_args()
    params = vars(args)
    # if not os.path.exists(params["output_path"]):
    #     os.makedirs(params["output_path"])
    main()



        