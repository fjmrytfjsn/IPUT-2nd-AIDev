# coding: utf-8
import numpy as np
import sys

sys.path.append("..")
from common.np import *
from rnnlm_gen import BetterRnnlmGen
from dataset import ptb

texts = []


def load_text(filename):
    with open(filename, encoding="utf-8") as f:
        i = 0
        j = 0
        for line in f:
            if filename.endswith("csv"):
                line = line.replace('"', "")  # 「”」を削除
                line = line.replace("　", "")  # 「全角スペース」を削除
                line = line.replace(",,", ",")  # 削除の結果、空になる部分を削除
            texts.append(line.split(",")[:-1])
            i = i + 1
            j = j + len(line.split(",")[:-1])
            # if i % 100000 == 1:
            # print(i, texts[-1])
            # if(i==10):
            #    break

    # print(i, "lines", j, "words loaded")


def text_to_id(texts):
    # words = text.split(' ')
    word_to_id = {}
    id_to_word = {}
    allwords = []
    for words in texts:
        allwords.extend(words)
        # print("ALL",allwords)
        for word in words:
            if word not in word_to_id:
                new_id = len(word_to_id)
                word_to_id[word] = new_id
                id_to_word[new_id] = word
    corpus = np.array([word_to_id[w] for w in allwords])
    return corpus, word_to_id, id_to_word


def init(modelname):
    # print(texts[:5])
    corpus_all, word_to_id, id_to_word = text_to_id(texts)
    # corpus, corpus_val, corpus_test = np.split(
    #     corpus_all, [int(len(corpus_all) * 0.8), int(len(corpus_all) * 0.9)]
    # )
    # print(id_to_word,text_to_id)
    # print(len(word_to_id), "kind of words in the corpus,")
    # print(
    #     len(corpus_all),
    #     "words",
    #     len(corpus),
    #     "in train",
    #     len(corpus_val),
    #     "in val",
    #     len(corpus_test),
    #     "in test",
    # )

    vocab_size = len(word_to_id)

    wordvec_size = 650
    hidden_size = 650

    # print(vocab_size)
    model = BetterRnnlmGen(vocab_size, wordvec_size, hidden_size)
    model.load_params(modelname)

    return model, word_to_id, id_to_word


def make_model(filename, modelname):
    load_text(filename)
    model, word_to_id, id_to_word = init(modelname)
    return model, word_to_id, id_to_word
