"""Script to evaluate a flair NER Model."""

import argparse
import logging
import flair
from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.embeddings import TransformerWordEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer


import time

import flair
flair.set_seed(123)


def test_other_dataset(input_path):
    columns = {0: "text", 1: "ner"}  # define columns

    # init a corpus using column format, data folder and the names of the train, dev and test files
    corpus: Corpus = ColumnCorpus(
        input_path,
        columns,
        test_file="Jules_Verne_aligne_avec_DWIE_bio.txt", # "./enp_FR.bnf.txt",
    )
    tagger = SequenceTagger.load(params["output_path"]+"best-model.pt")
    tagger.label_dictionary.add_unk = True
    print(tagger.evaluate(corpus.test, gold_label_type="ner", mini_batch_size=16, out_path=f"predictions.txt")) 
    

def main():
    """Test a FLAIR Ner model."""

    # test(corpus)

    start = time.time()
    test_other_dataset(params["input_path"])

    done = time.time()
    elapsed = done - start
    print(elapsed, f" seconds from exp : ", params["output_path"])
    

if __name__ == "__main__":
    logging.basicConfig(
        filename="data_preprocessing.log", encoding="utf-8", level=logging.DEBUG
    )
    parser = argparse.ArgumentParser(
        description="Arguments to generate the tests sequences.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--input_path",
        help="Path to the flair formated DWIE datasets",
        default="../",
    )
    parser.add_argument(
        "-o",
        "--output_path",
        help="Path to the flair formated DWIE models",
        default="./",
    )
    parser.add_argument("-r", "--resume", action="store_true", default=False)
    args = parser.parse_args()
    params = vars(args)
    main()
