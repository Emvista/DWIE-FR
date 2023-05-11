
"""
Author: Sylvain Verdy @ Jan 2023
translate.py
"""


import os
from tqdm import tqdm
import torch
import logging
import argparse

def read_file(file_path):
    data = open(file_path, 'r').readlines()
    return data

def prepare_data(data):
    list_elements = []
    list_labels = []
    list_labels_by_sentences = []
    list_sentences = []
    count = 0
    for row in tqdm(data):
        if row != '\n':
            sentence = row.split('\t') 
            list_elements.append(sentence[0])
            list_labels.append(sentence[1].split('\n')[0])
        if row == '\n':
            list_sentences.append(' '.join(list_elements))
            list_labels_by_sentences.append(' '.join(list_labels))
            list_labels, list_elements = [],[]
        if count == len(data)-1:
            list_sentences.append(' '.join(list_elements))
            list_labels_by_sentences.append(' '.join(list_labels))
            list_labels, list_elements = [],[]
        count +=1
    return list_labels_by_sentences, list_sentences



class Translator:
    def __init__(self, file_path, file_saver, file_path_origin):
        super().__init__()
        self.file_path_saver = file_saver
        self.file_path =  file_path 
        self.file_path_origin = file_path_origin
        self.data = read_file(self.file_path)
        self.labels, self.text = prepare_data(self.data)
        self.model = torch.hub.load('pytorch/fairseq', 'transformer.wmt14.en-fr', checkpoint_file='model.pt', tokenizer='moses', bpe='fastbpe')
        self.model.eval()
        self.model.cuda()


    def translate_sentence(self, sentence):
        return self.model.translate(sentence)

    def translate_file(self,):
        file = open(self.file_path_saver, 'w')
        file.close()

        file = open(self.file_path_origin, 'w')
        file.close()
        with open(self.file_path_origin, 'a') as file:
            for sentence in tqdm(self.text):
                if len(sentence) > 1:
                    file.write('{}\n'.format(sentence))
        file.close()
        
        with open(self.file_path_saver, 'a') as file:
            for sentence in tqdm(self.text):
                sentence = sentence.replace(" 's ", "'s ")
                file.write('{}\n'.format(self.translate_sentence(sentence)))
        file.close()



def main():

    translator = Translator(params['input_path'] + 'train.txt', params["output_path"] +'train_fr.txt', params["output_path"] +'train_origin_2.txt')
    translator.translate_file()

    translator = Translator(params['input_path'] + 'test.txt', params["output_path"] +'test_fr.txt', params["output_path"] +'test_origin_2.txt')
    translator.translate_file()


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

    
    args = parser.parse_args()
    params = vars(args)
    if not os.path.exists(params["output_path"]):
        os.makedirs(params["output_path"])
    main()

