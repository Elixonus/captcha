from random import randint
from PIL import Image


class Captcha:
    number: int
    width: int
    height: int

    def __init__(self, width: int, height: int) -> None:
        self.number = 10
        self.width = width
        self.height = height

        image = Image.new("RGBA", (200, 100), (0, 0, 0))

        for n in range(self.number):
            emoji = Image.open("hugging_face.png").resize((50, 50))
            position = (randint(-50, self.width), randint(-50, self.height))
            image.paste(emoji, position, emoji)

        image.show()


captcha = Captcha(width=200, height=100)