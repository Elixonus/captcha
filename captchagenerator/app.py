from os import remove, path, makedirs
from glob import glob
from random import choice
from string import ascii_uppercase, digits
from flask import Flask, send_file, request, send_from_directory, abort
from captcha import Captcha


files = glob("captchas/*")
for file in files:
    remove(file)

if not path.exists("captchas"):
    makedirs("captchas")

codes = []
captchas = []

app = Flask(__name__)


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/favicon.ico")
def favicon():
    return send_file("favicon.ico")


@app.route("/stars.jpg")
def stars():
    return send_file("stars.jpg")


@app.route("/api/new")
def api_new():
    code = new_code()
    codes.append(code)
    captcha = Captcha(size=(200, 100), bounds=(4, 8))
    captcha.image.save(f"captchas/{code}.png")
    captchas.append(captcha)
    return code


@app.route("/api/image")
def api_image():
    code = request.args.get("code")
    for c in range(len(codes)):
        if code == codes[c]:
            return send_file(f"captchas/{code}.png")
    abort(404)

@app.route("/api/check")
def api_check():
    code = request.args.get("code")
    number = request.args.get("number")
    for c in range(len(codes)):
        if code == codes[c]:
            captcha = captchas[c]
            if number == str(captcha.number):
                return "Good"
    return "Bad"


def new_code() -> str:
    code = "".join(choice(ascii_uppercase + digits) for _ in range(10))
    if code in codes:
        return new_code()
    return code
