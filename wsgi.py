from random import choice
from string import ascii_uppercase, digits
import os
from flask import Flask, send_file, request
from captcha import Captcha

for file in os.scandir("captchas"):
    os.remove(file)

codes = []
captchas = []

app = Flask(__name__)


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/success")
def success():
    return send_file("success.html")


@app.route("/api/new")
def api_new():
    code = new_code()
    codes.append(code)
    captcha = Captcha(size=(200, 100), bounds=(4, 8))
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


@app.route("/api/check/<code>")
def api_check(code):
    for c in range(len(codes)):
        if codes[c] == code:
            captcha = captchas[c]
            if request.args.get("number") == str(captcha.number):
                return "Good"
    return "Bad"


def new_code() -> str:
    code = "".join(choice(ascii_uppercase + digits) for _ in range(10))
    if code in codes:
        return new_code()
    return code
