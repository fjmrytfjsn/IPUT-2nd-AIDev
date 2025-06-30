from gtts import gTTS

import vlc
import time

storepath = "C:/work/"


def voice_synthesis(text):
    language = "ja"

    output = gTTS(text=text, lang=language, slow=False)
    storefile = storepath + "output.mp3"
    output.save(storefile)
    print("done")

    p = vlc.MediaPlayer("c:/work/output.mp3")
    p.play()

    while p.get_state() != vlc.State.Ended:
        time.sleep(0.1)


if __name__ == "__main__":
    text = "こんにちは"
    voice_synthesis(text)
