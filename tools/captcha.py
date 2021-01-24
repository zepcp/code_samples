import os
import shutil
import random
import string
import json
import datetime
from PIL import Image
from claptcha import Claptcha


class Captcha:
    """Captcha Interface"""
    def __init__(self, length=7, validity=180,
                 blacklist=["0", "1", "h", "i", "j", "l", "n", "o"],
                 root=os.getcwd() + "/captchas/{}",
                 font_path=os.getcwd() + "/DejaVuSerif-Bold.ttf",
                 noise=0.0, resample=Image.BICUBIC):
        self.length = length
        self.validity = validity
        self.blacklist = blacklist

        self.root = root
        self.img_path = root + "/captcha.png"
        self.answer_path = root + "/answer.json"

        self.font_path = font_path
        self.noise = noise
        self.resample = resample

    def _random_string(self):
        letters_list = list(string.digits + string.ascii_lowercase)
        for k in self.blacklist:
            letters_list.remove(k)
        rnd_letters = (random.choice(letters_list) for _ in range(self.length))
        return "".join(rnd_letters)

    def _read_answerfile(self, user_id):
        """Read answer Random Captcha String"""
        if not os.path.exists(self.root.format(user_id)):
            return None
        with open(self.answer_path.format(user_id)) as f_handler:
            answer = json.loads(f_handler.read())
            answer["ts"] = datetime.datetime.strptime(answer["ts"], "%Y-%m-%d %H:%M:%S")
        return answer

    def _write_answerfile(self, user_id, text):
        ts_str = str(datetime.datetime.utcnow()).rsplit(".", 1)[0]
        answer = {"captcha": text, "ts": ts_str}
        answer_json = json.dumps(answer)

        with open(self.answer_path.format(user_id), "w") as f_handler:
            f_handler.write(answer_json)

    def create(self, user_id):
        if not os.path.exists(self.root.format(user_id)):
            os.makedirs(self.root.format(user_id))

        text = self._random_string()
        claptcha = Claptcha(text,
                            self.font_path,
                            resample=self.resample,
                            noise=self.noise)

        claptcha.write(self.img_path.format(user_id))
        self._write_answerfile(user_id, text)
        return self.img_path.format(user_id).rsplit("/", 1)

    def validate_answer(self, user_id, user_answer):
        answer = self._read_answerfile(user_id)
        if answer is None or user_answer != answer["captcha"]:
            return False
        return True

    def validate_timediff(self, user_id):
        utc_now = datetime.datetime.utcnow()
        answer = self._read_answerfile(user_id)
        if answer is None:
            return False

        if (utc_now - answer["ts"]).seconds > self.validity:
            return False
        return True

    def delete(self, user_id):
        if not os.path.exists(self.root.format(user_id)):
            return True
        shutil.rmtree(self.root.format(user_id))
