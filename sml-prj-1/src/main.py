from generate_text import generate_text
from analyze_text import analyze_text
from make_model import make_model

from voice_synthesis import voice_synthesis


def main():
    excepted_subject = input("主語を入力してください: ")
    excepted_predicate = input("述語を入力してください: ")

    filename = "figures/aozora-small/aozora-small-wakachiL.txt"
    modelname = "figures/aozora-small/BetterRnnlm-small.pkl"
    model, word_to_id, id_to_word = make_model(filename, modelname)
    for i in range(10):
        text = generate_text(
            model, word_to_id, id_to_word, filename, modelname, excepted_subject
        )
        text = text.split("。")[0]
        print("Generated text:", text)
        subject, predicate = analyze_text(text)
        print("Subject:", subject)
        print("Predicate:", predicate)
        print("-" * 50)
        if subject == excepted_subject and predicate == excepted_predicate:
            print("Success!")
            voice_synthesis(text)
            break
        elif i == 9:
            print("Failed!")
            voice_synthesis("失敗しました")


if __name__ == "__main__":
    main()
