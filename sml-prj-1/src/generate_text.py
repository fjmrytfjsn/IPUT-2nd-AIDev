# coding: utf-8
import numpy as np
import sys

sys.path.append("..")
from common.np import *
from rnnlm_gen import BetterRnnlmGen
from dataset import ptb


def generate_text(model, word_to_id, id_to_word, filename, modelname, subject):
    start_word = subject
    start_id = word_to_id[start_word]
    skip_words = ["　"]
    skip_ids = [word_to_id[w] for w in skip_words]
    # 文章生成
    word_ids = model.generate(start_id, skip_ids, sample_size=25)
    txt = "".join([id_to_word[i] for i in word_ids])
    txt = txt.replace(" <eos>", ".\n")

    return txt


if __name__ == "__main__":
    filename = "figures\KenziMiyazawa\宮沢賢治.txt.wakachiL.txt"
    modelname = "figures\KenziMiyazawa\myBetterRnnlm.pkl"
    subject = "私"
    while True:
        generate_text(filename, modelname, subject)
        if input("もう一度生成しますか？(y/n)") != "y":
            break
