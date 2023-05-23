"""
Authors: Sylvain Verdy and Maxime Prieur @ Fev 2023
"""

"""Process the DWIE dataset to build files for the FLAIR NER model training.
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

DWIE_NER_TYPES = pd.read_csv("./onto_deep_dwie.csv", sep=",")

SENTENCE_NER_END_CHAR = [". O", '" O', "? O", "! O"]


def get_concepts_types(concepts: list) -> dict:
    """Return the types of each concept.

    Args:
        concepts (list): entities in the doc

    Returns:
        dict: types for each concepts
    """
    footer = False
    concepts_types = {}
    for concept in concepts:
        selected_tag = None
        if concept["tags"] is not None:
            tags_type = []
            for tag in concept["tags"]:
                tag_type, value = tag.split("::")
                value = value
                if 'footer' == value:
                    footer = True
                if tag_type == "type":
                    if value in DWIE_NER_TYPES and (
                        selected_tag is None
                        or DWIE_NER_TYPES[value]> DWIE_NER_TYPES[selected_tag]
                    ):                      
                        selected_tag = value                  

        if selected_tag is not None:
            if footer:
                concepts_types[concept["concept"]] = 'footer'
            else:    
                concepts_types[concept["concept"]] = selected_tag.lower()
    return concepts_types


def is_in_other_span(spans: tuple, i: int) -> bool:
    """Check if a span is included in another.

    Args:
        spans (tuple): begin, end char position and type
        i (int): index of the span to check

    Returns:
        bool: wheter the span is included in another
    """
    (begin, end, _) = spans[i]
    length = end - begin
    for j, (s_begin, s_end, _) in enumerate(spans):
        s_length = s_end - s_begin
        if i != j and length < s_length and s_begin <= begin <= end <= s_end:
            return True
    return False


def get_spans(doc, mentions, concept_types):
    """Filter the spans.

    Args:
        doc (Spacy.doc): a Spacy document
        mentions (list): annotated mentions
        type_of_concepts (dict): concepts with their type

    Returns:
        list: filtered spans
    """
    spans = []

    for mention in mentions:
        if mention["concept"] in concept_types:
            m_type = concept_types[mention["concept"]]
            m_begin, m_end = mention["begin"], mention["end"]
            char_span = doc.char_span(m_begin, m_end, m_type)
            if char_span is not None:
                spans.append((m_begin, m_end, m_type))

    return [
        doc.char_span(begin, end, tag)
        for i, (begin, end, tag) in enumerate(spans)
        if not is_in_other_span(spans, i)
    ]


def get_spacy_docs(path_dwie: str) -> dict:
    """Transform raw texts to annotated sentences.

    Args:
        path_dwie (str): path to the DWIE annotated data

    Returns:
        docs in the train set, docs in the test set
    """
    nlp = spacy.load("en_core_web_sm", exclude=['ner'])
    spacy_train = []
    spacy_test = []
    for filename in tqdm(os.listdir(path_dwie)):
        with open(os.path.join(path_dwie, filename), encoding="utf-8") as dwie_file:
            data = json.load(dwie_file)
        doc = nlp(data["content"])
        if len(data['mentions'])> 0:
            type_of_concepts = get_concepts_types(data["concepts"])
            spans = get_spans(doc, data["mentions"], type_of_concepts)
            if len(spans) > 0:
                doc.set_ents(spans)

            if data["tags"][1] == "train":
                spacy_train.append(doc)
            else:
                spacy_test.append(doc)
        else:
            print('empty!', filename)

    return spacy_train, spacy_test


def spacy_to_flair_token(token) -> str:
    """Format spacy tokens to flair.

    Args:
        token ): a spacy token

    Returns:
        str: formated flair token
    """
    line = token.text
    line = line.strip()
    if line != "\n" and len(line) != 0:
        line += "\t"  #+ token.ent_iob_

        if token.ent_iob_ != "O":
            line += token.ent_type_ # "-" + token.ent_type_
        #elif len(line) != 0 and line != "\n" or line != "":
        else:
            line += "O"

        return line.replace("\n", "")

    #return "\n"

def spacy_to_flair_sent(sent) -> list:
    """Translate a spacy sentence to a flair one.
    Args:
        sent (_type_): Spacy sentence.

    Returns:
        list[str]:list of flair token
    """
    
    return [spacy_to_flair_token(token) for token in sent if token.text != ""] + ["\n"] 


def spacy_to_flair_doc(doc) -> list:
    """Transform spacy doc to flair format

    Args:
        doc: a spacy document

    Returns:
        list: list of flair token
    """
    sents = []
    for i, sent in enumerate(doc.sents):
        #if 'Euromaxx' in str(list(doc.sents)) and 'Trump' in str(list(doc.sents)):
        sents += spacy_to_flair_sent(sent)
    return sents


def spacy_to_flair(docs: list) -> list[str]:
    """Transform spacy documents to comply with flair format.

    Args:
        docs (list): list fo spacy documents

    Returns:
        list[str]: flair dataset
    """
    dataset = []
    for doc in tqdm(docs):
        dataset += spacy_to_flair_doc(doc)
    return dataset


def clean_spaces(data: list) -> list:
    """Remove unnecessary tokens

    Args:
        data (list[str]): Flair dataset

    Returns:
        list[str]: Cleaned Flair dataset
    """
    cleaned_data = []
    for i in range(0, len(data) - 1):
        if not data[i] == data[i + 1] == "":
            cleaned_data.append(data[i])
            if (not data[i] in SENTENCE_NER_END_CHAR) and data[i + 1] == "":
                cleaned_data.append(". O")
    cleaned_data.append(data[-1])
    return cleaned_data


def get_data(spacy_docs, dataset):
    """Process training data.

    Args:
        spacy_docs (list): list of spacy document
        dataset (str): type of dataset
    """

    flair_datasets = clean_spaces(spacy_to_flair(spacy_docs))
    with open(
        os.path.join(params["output_path"], dataset + ".txt"),
        mode="w",
        encoding="utf-8",
    ) as flair_file:
        for token in flair_datasets:
            try:
                flair_file.write(token + "\n")
            except:
                pass
                #print("not a token", token)


    with open(
        os.path.join(params["output_path"], dataset + ".txt"),
        mode="r",
        encoding="utf-8",
    ) as flair_file:
        text = flair_file.read()

    text = re.sub("\n\n", "\n", text)
    
    with open(
        os.path.join(params["output_path"], dataset + ".txt"),
        mode="w",
        encoding="utf-8",
    ) as flair_file:
        flair_file.write(text)

def main():
    """Preprocess DWIE texts to train a FLAIR NER model."""
    if not os.path.exists(params["output_path"]):
        os.makedirs(params["output_path"])
    if os.path.exists(params["output_path"] + "spacy_docs.pickle"):
        with open(params["output_path"] + "spacy_docs.pickle", "rb") as spacy_files:
            train_docs, test_docs = pickle.load(spacy_files)

    else:
        train_docs, test_docs = get_spacy_docs(params["input_path"])
        with open(params["output_path"] + "spacy_docs.pickle", "wb") as spacy_files:
            pickle.dump((train_docs, test_docs), spacy_files)
    #train_docs, test_docs = get_spacy_docs(params["input_path"])

    get_data(train_docs, "train")
    get_data(test_docs, "test")


def read_file(file_path):
    data = open(file_path, 'r').readlines()
    return data

def prepare_data(data):
    list_elements = []
    list_labels = []
    list_labels_by_sentences = []
    list_sentences = []
    count = 0
    count_sentences = 0
    for row in tqdm(data):
        if row != '\n':
            sentence = row.split('\t') 
            list_elements.append(sentence[0])
            list_labels.append(sentence[1].split('\n')[0])
        if row == '\n':
            list_sentences.append(' '.join(list_elements))
            list_labels_by_sentences.append(' '.join(list_labels))
            
            list_labels, list_elements = [],[]
            count_sentences+=1
            
        if count == len(data)-1:
            list_sentences.append(' '.join(list_elements))
            list_labels_by_sentences.append(' '.join(list_labels))
            list_labels, list_elements = [],[]

        
        count +=1
    
    return list_labels_by_sentences, list_sentences



def get_sentences_file():
    path = params["output_path"] + "train.txt"
    path_2 = params["output_path"] + "train_origin_2.txt"

    data = read_file(path)
    _, list_sentences = prepare_data(data)

    n_names = ["{}\n".format(i) for i in list_sentences]


    with open(path_2, "w") as file:
        file.writelines(n_names[:-1])
        file.close()

    path = params["output_path"] + "test.txt"
    path_2 = params["output_path"] + "test_origin_2.txt"

    data = read_file(path)
    _, list_sentences = prepare_data(data)

    n_names = ["{}\n".format(i) for i in list_sentences]


    with open(path_2, "w") as file:
        file.writelines(n_names[:-1])
        file.close()


if __name__ == "__main__":
    logging.basicConfig(
        filename="data_preprocessing.log", encoding="utf-8", level=logging.DEBUG
    )
    parser = argparse.ArgumentParser(
        description="Arguments for the FLAIR Preprocessing.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-i",
        "--input_path",
        help="Path to the dwie content directory",
        default="./annos_with_content_2",
    )
    parser.add_argument(
        "-o",
        "--output_path",
        help="Path to save flair preprocessed files",
        default="/home/sylvain/POPCORN/datasets/DWIE_FR/",
    )

    parser.add_argument(
        "-d",
        "--deep_ontologie",
        help="Path to save flair preprocessed files",
        default="1",
    )

    args = parser.parse_args()
    params = vars(args)
    
    DWIE_NER_TYPES = DWIE_NER_TYPES[DWIE_NER_TYPES["Levels"] <= int(params["deep_ontologie"])]

    DWIE_NER_TYPES = DWIE_NER_TYPES.set_index('Labels')['Levels'].to_dict()
    print(DWIE_NER_TYPES)
    main()
    get_sentences_file()

