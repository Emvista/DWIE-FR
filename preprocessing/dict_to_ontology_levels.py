"""
Author: Sylvain Verdy @ Fev 2023

"""

import logging
import argparse
import os
import json
import pickle
import spacy
import re

from tqdm import tqdm
import pandas as pd


class ReverseDict:
    def __init__(self, path_dict, i, save_file) -> None:
        self.json_data = open(path_dict, "r")
        self.df = pd.read_csv("./onto_deep_dwie.csv", sep=",")
        self.data = json.loads(self.json_data.read())
        self.i = i
        
        self.new_deep_parents = self.df[['Deep4','Deep'+ str(self.i)]]
        self.save_file = save_file

    def transforme(self, ):
        for key, value in self.data.items():
            for k, v in value.items():
                try:    
                    if self.i == "4":
                        new_value = self.new_deep_parents.loc[(self.new_deep_parents['Deep4']== v).values, 'Deep'+ str(self.i)].iloc[0]
                        new_value = new_value[0]
                    else:
                        new_value = self.new_deep_parents.loc[(self.new_deep_parents['Deep4']== v).values, 'Deep'+ str(self.i)].iloc[0]

                    self.data[str(key)][str(k)] = new_value
                except:
                    self.data[str(key)][str(k)] = {}
                    # not in vocab -> print("not in vocab", k, v )

        with open(self.save_file, "w", encoding='utf8')  as outfile:
            json.dump(self.data, outfile, ensure_ascii=False, indent=2)


def main():

    get_dict_levels = ReverseDict(params['input_path'] +'train_fr_NER.json', params["deep_ontologie"], params["input_path"]+'train_fr_NER.json')
    get_dict_levels.transforme()
    
    get_dict_levels = ReverseDict(params['input_path'] +'test_fr_NER.json', params["deep_ontologie"], params["input_path"]+'test_fr_NER.json')
    get_dict_levels.transforme()



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
        "-d",
        "--deep_ontologie",
        help="Path to the dwie content directory",
        default="./new_data_translate/",
    )

    
    args = parser.parse_args()
    params = vars(args)

    main()
