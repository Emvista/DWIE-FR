import os
import json
import logging
import argparse
from tqdm import tqdm
import re, string
from transformers import AutoTokenizer, AutoModel
from torch.nn.functional import cosine_similarity
import torch
from collections import deque
import numpy as np
from math import floor, ceil
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
    return list_labels_by_sentences, list_sentences


class KeepAlign:
    def __init__(self, path_file_fr, path_file, save_file, dictionnary_path, path_onto_4) -> None:
        self.path_file_fr = self.read_file(path_file_fr)
        self.path_file = self.read_file(path_file)
        self.dictionnary = json.loads(open(dictionnary_path,'r').read())
        if path_onto_4 != "":
            self.path_onto_4 = self.read_file(path_onto_4)
            self.labels_deep4, self.origin_deep4 = prepare_data(self.path_onto_4)
        self.labels, self.origin = prepare_data(self.path_file_fr)
        self.save_file = save_file
        self.stopwords = open('./stopwords.txt', 'r').read().splitlines() 

    def read_file(self, path):
        data = open(path, 'r').readlines()
        return data
    def dict_and_replace(self, deep_ontologie):
        list_word_tag = []
        
        df = pd.read_csv("./onto_deep_dwie.csv", sep=",")
        new_deep_parents = df[['Deep4', 'Deep'+ str(deep_ontologie)]]

        count = 0
        for i in tqdm(range(0, len(self.origin))):
            for a, word in enumerate(self.origin[i].split()):
                if deep_ontologie != "4":
                    if self.labels_deep4[i].split()[a] != "O":
                        new_value = new_deep_parents.loc[(new_deep_parents['Deep4']== self.labels_deep4[i].split()[a]).values, 'Deep'+ str(deep_ontologie)].iloc[0]    
                        list_word_tag.append(word + '\t' + new_value)
                    else:
                        list_word_tag.append(word + '\t' + "O")
                else:
                    list_word_tag.append(word + '\t' + self.labels[i].split()[a])

            list_word_tag.append("")
            count +=1                    

        n_names = ["{}\n".format(i) for i in list_word_tag]

        with open(self.save_file, "w") as file:
            file.writelines(n_names)
            file.close()


def main():

    aligner = KeepAlign(params['input_path'],  params['base_path'], params['output_path'], params['json_dictionnary'],  params["ontologie_4"])
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
    parser.add_argument(
        "-j",
        "--json_dictionnary",
        help="Path to the dwie content directory",
        default="./new_data_translate/",
    )

    parser.add_argument(
        "-o4",
        "--ontologie_4",
        help="Path to the dwie content directory",
        default="./new_data_translate/",
    )

    args = parser.parse_args()
    params = vars(args)

    main()



        