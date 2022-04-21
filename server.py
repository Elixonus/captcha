from random import choice
from string import ascii_uppercase, digits
from io import StringIO
from flask import Flask, send_file
from captcha import Captcha

codes = []
captchas = []

app = Flask(__name__)

@app.route("/api/new")
def api_new():
    code = new_code()
    codes.append(code)
    captcha = Captcha(size=(1000, 500), bounds=(4, 8))
    captchas.append(captcha)
    return code


@app.route("/api/image/<code>")
def api_image(code):
    for c in range(len(codes)):
        if codes[c] == code:
            captcha = captchas[c]
            path = f"captchas/{code}.png"
            captcha.image.save(path)
            return send_file(path)


@app.route("/api/check/<code>/<number>")
def api_check(code, number):
    for c in range(len(codes)):
        if codes[c] == code:
            captcha = captchas[c]
            if number == str(captcha.number):
                return "Good"
    return "Bad"


def new_code() -> str:
    code = "".join(choice(ascii_uppercase + digits) for _ in range(10))
    if code in codes:
        return new_code()
    return code
