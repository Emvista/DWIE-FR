"""
Author: Sylvain Verdy @ Fev 2023
"""

import argparse
from tqdm import tqdm
from collections import deque
import numpy as np
from math import floor, ceil
from unidecode import unidecode
import pandas as pd


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

def dist_jaro_words(word, list_words):
    
    return np.argmax([jaro_distance(word, w) for w in list_words]), max([jaro_distance(word, w) for w in list_words])


def prepare_data_en(data):
    list_elements = deque()
    list_labels = deque()
    list_labels_by_sentences = []
    list_sentences = []
    index_footer_sentences = []
    count = 0
    list_labels_none = ['footer','none', 'skip', 'INVALID', 'derived', 'per_x'] # list of entities not used in our corpus (own choice)

    for row in tqdm(range(0, len(data)), disable=True):
        if data[row] != '\n':
            sentence = data[row].split('\t')
            list_elements.append(sentence[0])
            list_labels.append(sentence[1].split('\n')[0])
        if data[row] == '\n':
            list_sentences.append(' '.join(list_elements))
            list_labels_by_sentences.append(' '.join(list_labels))

            if any([item for item in list_labels_none if item in list_labels]):
                index_footer_sentences.append(count)
            
            list_labels.clear(), list_elements.clear()

            count +=1
    return list_labels_by_sentences, list_sentences, index_footer_sentences


def prepare_data_fr(data):
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
    return list_labels_by_sentences, list_sentences,



class RemoveFooter:
    def __init__(self, path_file_fr, path_file, save_file, remove_only_footer_en) -> None:
        self.path_file_fr = self.read_file(path_file_fr)
        self.path_file_en = self.read_file(path_file)
        self.save_file = save_file
        self.labels, self.origin = prepare_data_fr(self.path_file_fr)
        self.labels_en, self.origin_en, self.index_footer_sentences = prepare_data_en(self.path_file_en)
        self.en = remove_only_footer_en


    def read_file(self, path):
        data = open(path, 'r').readlines()
        return data

    def footer_remove_and_preprocessing(self, niv):
        use_countries_csv = True
        list_pays = []
        if use_countries_csv:
            df = pd.read_csv("./etats_capital.csv",sep=";", engine = 'python')
            list_pays = df["NOM"].values.tolist()
            list_capitale = df["CAPITALE"].values.astype(str).tolist()

            list_pays = [x.lower() for x in list_pays]
            list_capitale = [x.lower() for x in list_capitale]

            df = pd.read_csv("./onto_deep_dwie.csv", sep=",")
            new_deep_parents = df[['Deep4', 'Deep'+ str(niv)]]

        sentences = [item for idx, item in enumerate(self.origin) if idx not in self.index_footer_sentences]

        labels = [item for idx, item in enumerate(self.labels) if idx not in self.index_footer_sentences]


        list_word_tag = []
        prev_label = "O"
        for i in tqdm(range(0,len(sentences))):
            labels_list = labels[i].split()
            for a,word in enumerate(sentences[i].split()):
                if self.en:
                    list_word_tag.append(word +"\t"+ labels_list[a])
                else:
                    if word not in [ ",", ".", "!", "?" , "^", "[", "]", "{", "}"]: #,"(", ")"]:
                        
                        if use_countries_csv:
                            if any([x for x in list_pays if unidecode(word.strip().lower()) == unidecode(x.strip().lower())]):
                                if str(niv) == '4':
                                    list_word_tag.append(word +"\t"+ "gpe0")
                                    prev_label = "gpe0"

                                else:

                                    new_value = new_deep_parents.loc[(new_deep_parents['Deep4']== "gpe0").values, 'Deep'+ str(niv)].iloc[0]    
                                    list_word_tag.append(word +"\t"+ str(new_value))
                                    prev_label = new_value
                                
                            elif dist_jaro_words(word, list_pays)[1]> 0.9 and any([x for x in list_pays if x.lower()[0:4] == word.lower()[0:4]]):
                                
                                if str(niv) == '4':
                                        list_word_tag.append(word +"\t"+ "gpe0-x")
                                        prev_label = "gpe0-x"
                                else:
                                    new_value = new_deep_parents.loc[(new_deep_parents['Deep4']== "gpe0-x").values, 'Deep'+ str(niv)].iloc[0]    

                                    list_word_tag.append(word +"\t"+ str(new_value))
                                    prev_label = new_value
                                    
                                        
                            else:
                                if any([x for x in list_capitale if unidecode(word.strip().lower()) == unidecode(x.strip().lower())]):     
                                        
                                    if str(niv) == '4':
                                        list_word_tag.append(word +"\t"+ "gpe2")
                                        prev_label = "gpe2"


                                    else:

                                        new_value = new_deep_parents.loc[(new_deep_parents['Deep4']== "gpe2").values, 'Deep'+ str(niv)].iloc[0]    
                                        list_word_tag.append(word +"\t"+ new_value)
                                        prev_label = new_value

                                elif dist_jaro_words(word, list_capitale)[1]> 0.9  and any([x for x in list_pays if x.lower()[0:4] == word.lower()[0:4]]):
                                    if str(niv) == '4':
                                        list_word_tag.append(word +"\t"+ "gpe2-x")
                                        prev_label = "gpe2-x"
                                    else:

                                        new_value = new_deep_parents.loc[(new_deep_parents['Deep4']== "gpe2-x").values, 'Deep'+ str(niv)].iloc[0]    
                                        list_word_tag.append(word +"\t"+ str(new_value))
                                        prev_label = new_value

                                else:
                                    if  any([x for x in ["La", "L", "l", "d", "Le", "'"] if word.lower() == x.lower()]) and (prev_label == "O" or prev_label==""):
                                        list_word_tag.append(word +"\t"+ "O")
                                        prev_label = "O"

                                    else:
                                        list_word_tag.append(word +"\t"+ str(labels_list[a]))
                                        prev_label = labels_list[a]

                        else:
                            list_word_tag.append(word +"\t"+ str(labels_list[a]))
                            prev_label = labels_list[a]

                    else:
                        list_word_tag.append(word +"\t"+ "O")
                        prev_label = "O"
            list_word_tag.append("")
            prev_label = ""


        n_names = ["{}\n".format(i) for i in list_word_tag]

        with open(self.save_file, "w") as file:
            file.writelines(n_names)
            file.close()
    
    

def main():

    remover = RemoveFooter(params['base_path'],  params['input_path'], params['output_path'], params['remove_only_footer_en_data'])
    remover.footer_remove_and_preprocessing(params["deep_ontologie"])





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
        "-b",
        "--base_path",
        help="Path to the dwie content directory",
        default="./new_data_translate/",
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
        "-r",
        "--remove_only_footer_en_data",
        help="Remove footer entities for English = True or remove footer entities for French and preprocessing between  = False ",
        default=False,
    )


    args = parser.parse_args()
    params = vars(args)
    
    main()



        