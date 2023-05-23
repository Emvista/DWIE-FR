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

device = torch.device('cuda')

MODEL_NAME =  "bert-base-multilingual-cased" #'AIDA-UPM/MSTSb_stsb-xlm-r-multilingual'
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME).to(device)
model.eval()


def jaro_distance(s1, s2):
	
	# If the s are equal
	if (s1 == s2):
		return 1.0

	# Length of two s
	len1 = len(s1)
	len2 = len(s2)

	# Maximum distance upto which matching
	# is allowed
	max_dist = floor(max(len1, len2) / 2) - 1

	# Count of matches
	match = 0

	# Hash for matches
	hash_s1 = [0] * len(s1)
	hash_s2 = [0] * len(s2)

	# Traverse through the first
	for i in range(len1):

		# Check if there is any matches
		for j in range(max(0, i - max_dist),
					min(len2, i + max_dist + 1)):
			
			if (s1[i] == s2[j] and hash_s2[j] == 0):
				hash_s1[i] = 1
				hash_s2[j] = 1
				match += 1
				break

	if (match == 0):
		return 0.0

	t = 0
	point = 0

	for i in range(len1):
		if (hash_s1[i]):

			while (hash_s2[point] == 0):
				point += 1

			if (s1[i] != s2[point]):
				t += 1
			point += 1
	t = t//2

	# Return the Jaro Similarity
	return (match/ len1 + match / len2 +
			(match - t) / match)/ 3.0


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] 
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


def prepare_data(data):
    list_elements = deque()
    list_labels = deque()
    list_labels_by_sentences = []
    list_sentences = []
    for row in tqdm(data, disable=False):
        if row != '\n':
            sentence = row.split('\t')
            list_elements.append(sentence[0])
            list_labels.append(sentence[1].split('\n')[0]) #.split('\n')[0])
        if row == '\n':
            list_sentences.append(' '.join(list_elements))
            list_labels_by_sentences.append(' '.join(list_labels))
            list_labels.clear(), list_elements.clear()

    assert len(list_sentences) == len(list_labels_by_sentences)



    return list_labels_by_sentences, list_sentences


class KeepAlign:
    def __init__(self, path_file_origin, path_file, translated_file, save_file) -> None:
        self.path_file_origin = self.read_file(path_file_origin)
        self.labels, self.origin = prepare_data(self.path_file_origin)
        self.data_file = self.read_file(path_file)
        self.translated_file = self.read_file(translated_file)
        self.save_file = save_file
        self.stopwords = open('./stopwords.txt', 'r').readlines()

    def read_file(self, path):
        data = open(path, 'r').readlines()
        return data

    def list_vocab(self, sentence_origin, labels_sentence, i):
        try:
            dict_vocab = np.array([])        

            new_labels = word_tokenize(labels_sentence, language='english')
            new_sentence_origin = word_tokenize(sentence_origin, language='english')
            for a, word in enumerate(new_sentence_origin):
                assert len(new_sentence_origin) == len(new_labels)
                if a == 0:
                    dict_vocab = np.append([(str(word), str(new_labels[a]))], dict_vocab)
                else:
                    dict_vocab = np.vstack([dict_vocab, np.array((str(word), str(new_labels[a])))])
            if len(dict_vocab) <2:
                dict_vocab = dict_vocab[np.newaxis, :]
            
            if dict_vocab.ndim == 1:
                dict_vocab = dict_vocab[np.newaxis, :]

        
        except:
            dict_vocab = np.array([])        
            labels = labels_sentence.split()
            

            sentence_origin = sentence_origin.split()
            for a, word in enumerate(sentence_origin):

                if a == 0:
                    dict_vocab = np.append([(str(word), str(labels[a]))], dict_vocab)
                else:
                    dict_vocab = np.vstack([dict_vocab, np.array((str(word), str(labels[a])))])
            if len(dict_vocab) <2:
                dict_vocab = dict_vocab[np.newaxis, :]
            
            if dict_vocab.ndim == 1:
                dict_vocab = dict_vocab[np.newaxis, :]

        return dict_vocab

    def keep_labels(self, dict_vocab, i, file):

        if dict_vocab is not None:
            sentence = self.translated_file[i]
            sentence = sentence.replace("\\,", " , ")
            sentence = sentence.replace("\\!", " ! ")
            sentence = sentence.replace("\\?", " ? ")
            sentence = sentence.replace("\\'", "' ")
            sentence = sentence.replace("\\(", " ( ")
            sentence = sentence.replace("\\)", " ) ")
            sentence = sentence.replace("\"", " \" ")
            sentence = sentence.replace("'", " ' ")
            sentence = sentence.replace('"', ' " ')
            
            sentence = sentence.replace("aujourd' hui", "aujourd'hui")
            sentence = sentence.replace("rendez -vous", "rendez-vous")
            sentence = sentence.replace("est-ce", "est -ce")

            sentence = word_tokenize(sentence, language='french')
            
            
            vocab = list(dict_vocab[:, 0])

            stopwords = set(self.stopwords)
            for _, word in enumerate(sentence):
                if word in string.punctuation:
                    file.write(word + '\t' + 'O' + '\n')

                elif word not in string.punctuation and word +'\n' not in stopwords:

                    nbr_corrects = vocab.count(word)

                    if  nbr_corrects >= 1: 

                        if nbr_corrects == 1: 
                            index_val = vocab.index(word) 
                        elif nbr_corrects > 1:
                            index_val = [i for i, x in enumerate(vocab) if x == word][0]

                        file.write(word + '\t' + dict_vocab[index_val, 1] + '\n')
                        dict_vocab = np.delete(dict_vocab, index_val,axis=0)
                        vocab = list(dict_vocab[:, 0])
                    elif len(vocab) == 0:
                        file.write(word + '\t' + 'O' + '\n')
                    else:

                        tokens = tokenizer(word, return_tensors='pt').to(device)
                        out1 = model(tokens['input_ids'], tokens['attention_mask'])
                        out1 = mean_pooling(out1, tokens['attention_mask'].to(device))
                        tokens_2 = tokenizer.batch_encode_plus(vocab, padding=True, truncation=True, return_tensors='pt').to(device)
                        
                        out2 = model(tokens_2['input_ids'], tokens_2['attention_mask'])
                        
                        out2 = mean_pooling(out2, tokens_2['attention_mask'].to(device))
                        similarities = cosine_similarity(out1, out2, dim=-1)
                        max_index = torch.argmax(similarities).to(device)
                        
                        if similarities[max_index] > 0.7 or round(jaro_distance(word, dict_vocab[max_index, 0]),6) > 0.6:
                            file.write(word + '\t' + dict_vocab[max_index, 1] + '\n')

                        else:
                            file.write(word + '\t' + 'O' + '\n')
                else:
                    file.write(word + '\t' + 'O' + '\n')

            file.write('\n')
        else:
            print("continue")

    def alignement(self, ):
        file_save = open(self.save_file, 'w')
        file_save.close()
        file_save = open(self.save_file, 'a')
        for i in tqdm(range(0, len(self.origin))):
            
            dict_vocab = {}
            dict_vocab = self.list_vocab(self.origin[i], self.labels[i], i)
            self.keep_labels(dict_vocab, i, file_save)
        file_save.close()


def main():
    print('align test file')
    aligner = KeepAlign(params['input_path'] + 'test.txt', params['input_path'] +'test_origin_2.txt', params['output_path'] +'test_fr.txt', params['output_path'] +'test_fr_NER.txt')
    aligner.alignement()
    print('align train file')
    aligner = KeepAlign(params['input_path'] + 'train.txt', params['input_path'] +'train_origin_2.txt', params['output_path'] +'train_fr.txt', params['output_path'] +'train_fr_NER.txt')
    aligner.alignement()


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




        