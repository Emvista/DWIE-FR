import logging
import argparse
import os
import json
from tqdm import tqdm
import re, string
from transformers import AutoTokenizer, AutoModel
from torch.nn.functional import cosine_similarity
import torch
from collections import deque
import numpy as np
from math import floor, ceil

import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize


model_translate = torch.hub.load('pytorch/fairseq', 'transformer.wmt14.en-fr', checkpoint_file='model.pt', tokenizer='moses', bpe='fastbpe')
model_translate.cuda()
model_translate.eval()

logger = logging.getLogger("fairseq.tasks.fairseq_task")
logger.disabled = True
stopwords = open('./stopwords.txt', 'r').read().splitlines() 


def prepare_data(data):
    list_elements = deque()
    list_labels = deque()
    list_labels_by_sentences = []
    list_sentences = []
    dict_labels_origin = {}
    dict_sentences_fr = {}
    past_entity = None
    group_entity = []
    count = 0
    for row in tqdm(data):
        
        if row != '\n':
            sentence = row.split('\t')
            list_elements.append(sentence[0])
            
            if sentence[1].split("\n")[0] != "O" and past_entity == sentence[1].split("\n")[0]:
                group_entity.append(sentence[0])
                past_entity = sentence[1].split("\n")[0]
            elif (past_entity == "O" or past_entity != sentence[1].split("\n")[0] ) and len(group_entity) == 0 and "O" != sentence[1].split("\n")[0]: 
                group_entity.append(sentence[0])
                past_entity = sentence[1].split("\n")[0]

            elif past_entity != None and len(group_entity)> 0 and  (sentence[1].split("\n")[0] == "O" or past_entity != sentence[1].split("\n")[0]):
                en_bpe = model_translate.apply_bpe(" ".join(group_entity).replace("'", " ' "))
                en_bin = model_translate.binarize(en_bpe)
                a = model_translate.generate(en_bin, verbose=False, beam=10 , sampling=True, sampling_topk=20)
                fr_sentences = []
                for i in a:
                    fr_bpe = model_translate.string(i['tokens'])
                    fr_toks = model_translate.remove_bpe(fr_bpe)
                    fr_sentences.append(' '.join(word_tokenize(model_translate.detokenize(fr_toks), language="french")).replace("'", " ' "))
                    if not any([word for word in stopwords if fr_sentences[-1] == word]):
                        dict_labels_origin.update({fr_sentences[-1]: past_entity})
                
                past_entity = sentence[1].split('\n')[0]
                if sentence[1].split("\n")[0] != "O":
                    group_entity = []
                    group_entity.append(sentence[0])
                else:
                    group_entity = []
            else:
                past_entity = sentence[1].split('\n')[0]

            
        if row == '\n':
            list_sentences.append(' '.join(list_elements))
            list_labels.clear(), list_elements.clear()
            dict_sentences_fr.update({str(count): dict_labels_origin})
            dict_labels_origin = {}
            count +=1
    return list_labels_by_sentences, list_sentences, dict_sentences_fr

class DictBuilder:
    def __init__(self, path_file_origin, save_file) -> None:
        self.path_file_origin = self.read_file(path_file_origin)
        self.labels, self.origin, self.dict_fr = prepare_data(self.path_file_origin)
        self.save_file = save_file
        self.save_file_data(self.dict_fr, self.save_file)
        
        
    def read_file(self, path):
        data = open(path, 'r').readlines()
        return data

    def save_file_data(self, dict_fr, save_file):
        with open(save_file, "w", encoding='utf8')  as outfile:
            json.dump(dict_fr, outfile, ensure_ascii=False, indent=2)


def main():

    builder = DictBuilder(params['input_path'] + 'train.txt',  params['output_path'] +'train_fr_NER.json')

    builder = DictBuilder(params['input_path'] + 'test.txt', params['output_path'] +'test_fr_NER.json')



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




        