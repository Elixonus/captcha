from math import hypot
from random import random, randint, shuffle
from PIL import Image, ImageFilter
import numpy as np


class Captcha:
    number: int
    size: tuple[int, int]
    image: Image
    stack: list[tuple[int, int]]

    def __init__(self, size: tuple[int, int], bounds: tuple[int, int]) -> None:
        self.number = randint(bounds[0], bounds[1])
        self.size = size
        self.image = Image.new("RGBA", size, (255, 255, 255))
        self.stack = []
        emoji_names = []
        for n in range(self.number):
            emoji_names.append("hugging")
        for n in range(randint(bounds[0] // 2, bounds[1] // 2)):
            emoji_names.append("crying")
        for n in range(randint(bounds[0] // 2, bounds[1] // 2)):
            emoji_names.append("money")
        self.add_emojis(emoji_names)
        r1 = random() - 0.5
        r2 = random() - 0.5
        r3 = random() - 0.5
        for i in range(size[0]):
            for j in range(size[1]):
                pixel = self.image.getpixel((i, j))
                self.image.putpixel((i, j), (min(pixel[0] + round(100 * r1), 255),
                                             min(pixel[1] + round(100 * r2), 255),
                                             min(pixel[2] + round(100 * r3), 255)))
        for i in range(size[0]):
            for j in range(size[1]):
                r1 = random() - 0.5
                r2 = random() - 0.5
                r3 = random() - 0.5
                pixel = self.image.getpixel((i, j))
                self.image.putpixel((i, j), (min(pixel[0] + round(50 * r1), 255),
                                             min(pixel[1] + round(50 * r2), 255),
                                             min(pixel[2] + round(50 * r3), 255)))
        ri = random() - 0.5
        rj = random() - 0.5
        for i in range(size[0]):
            for j in range(size[1]):
                ir = rj * i / size[0]
                jr = ri * i / size[1]
                r1 = random() - 0.5
                r2 = random() - 0.5
                r3 = random() - 0.5
                pixel = self.image.getpixel((i, j))
                self.image.putpixel((i, j), (min(pixel[0] + round(50 * r1 * ir * jr), 255),
                                             min(pixel[1] + round(50 * r2 * ir * jr), 255),
                                             min(pixel[2] + round(50 * r3 * ir * jr), 255)))

    def add_emojis(self, names: list[str]) -> None:
        names_shuffled = names.copy()
        shuffle(names_shuffled)
        for name in names_shuffled:
            self.add_emoji(name)

    def add_emoji(self, name: str) -> None:
        emoji_size = randint(0.1 * max(*self.size), 0.2 * max(*self.size))
        emoji_center = (randint(0, self.size[0]), randint(0, self.size[1]))
        for s in self.stack:
            if hypot(emoji_center[0] - s[0], emoji_center[1] - s[1]) < 0.1 * max(*self.size):
                self.add_emoji(name)
                return
        self.stack.append(emoji_center)
        emoji_position = (emoji_center[0] - emoji_size // 2, emoji_center[1] - emoji_size // 2)
        emoji = Image.open(f"static/emojis/{name}.png").resize((emoji_size, emoji_size)).rotate(360 * random())
        r1 = random() - 0.5
        r2 = random() - 0.5
        r3 = random() - 0.5
        for i in range(emoji_size):
            for j in range(emoji_size):
                pixel = emoji.getpixel((i, j))
                emoji.putpixel((i, j), (min(pixel[0] + round(80 * r1), 255),
                                        min(pixel[1] + round(80 * r2), 255),
                                        min(pixel[2] + round(80 * r3), 255),
                                        pixel[3]))
        self.image.alpha_composite(emoji, emoji_position)
