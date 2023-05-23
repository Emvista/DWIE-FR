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
import spacy

nlp = spacy.load('fr_core_news_sm')


def find_substring_positions(string, substring):

    positions = []
    start = 0
    while True:
        start = string.find(substring, start)
        if start == -1:
            break
        positions.append(start)
        start += len(substring)
    return positions



def prepare_data(data):
    list_elements = deque()
    list_labels = deque()
    list_labels_by_sentences = []
    list_sentences = []
    for row in tqdm(range(0, len(data)), disable=True):
        if data[row] != '\n':
            sentence = data[row].split('\t')
            list_elements.append(sentence[0])
            list_labels.append(sentence[1].split('\n')[0]) 
        if data[row] == '\n':
            list_sentences.append(' '.join(list_elements))
            list_labels_by_sentences.append(' '.join(list_labels))
            list_labels.clear(), list_elements.clear()
    return list_labels_by_sentences, list_sentences


class DictMoreAlign:
    def __init__(self, path_file_fr, path_file, save_file, dictionnary_path) -> None:
        self.path_file_fr = self.read_file(path_file_fr)
        self.path_file = self.read_file(path_file)
        self.dictionnary_path = dictionnary_path
        self.dictionnary = json.loads(open(dictionnary_path,'r').read())
        
        self.labels, self.origin = prepare_data(self.path_file_fr)
        self.save_file = save_file
        self.stopwords = open('./stopwords.txt', 'r').read().splitlines() 

    def read_file(self, path):
        data = open(path, 'r').readlines()
        return data
    def dict_and_replace(self,):
        list_word_tag = []
        
        count = 0
        for i in tqdm(range(0, len(self.origin))):
            etiquettes = self.labels[i].split()
            sentence = self.origin[i]

            positions_debut_mots = [m.start() for m in re.finditer(r"\S+", unidecode(self.origin[i]).strip().lower())]
            for cle, valeur in list(self.dictionnary[str(i)].items()):
                
    
                if len(cle.split()) > 0 and len(cle)> 1:
                    if 'footer' not in valeur:
                        debut_cle = unidecode(sentence.strip().lower()).find(unidecode(cle.strip().lower()))
                        fin_cle = debut_cle + len(unidecode(cle.strip().lower()))

                        if debut_cle != -1:
                            # La clé a été trouvée dans la phrase, donc on met à jour les étiquettes correspondantes
                            for a, position in enumerate(positions_debut_mots):
                                if position >= debut_cle and position < fin_cle:
                                    etiquettes[a] = valeur

            tokens = self.origin[i].split()
            for o, label in enumerate(etiquettes):
                list_word_tag.append(tokens[o] + '\t' + label)
            list_word_tag.append("")
            count +=1                    

        n_names = ["{}\n".format(i) for i in list_word_tag]

        with open(self.save_file, "w") as file:
            file.writelines(n_names)
            file.close()
    
def main():

    aligner = DictMoreAlign(params['input_path'],  params['base_path'], params['output_path'], params['json_dictionnary'])
    aligner.dict_and_replace()


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

    args = parser.parse_args()
    params = vars(args)

    main()