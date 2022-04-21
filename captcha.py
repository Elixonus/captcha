from math import floor, ceil, hypot
from random import randint
from PIL import Image
from numpy.random import standard_normal


class Captcha:
    number: int
    size: tuple[int, int]

    def __init__(self, size: tuple[int, int], mean: float, sd: float) -> None:
        self.number = min(max(round(mean + sd * standard_normal(1)[0]), ceil(0.5 * mean)), floor(1.5 * mean))
        self.size = size

        image = Image.new("RGBA", size, (0, 0, 0))
        stack = []

        for n in range(self.number):
            emoji_size = randint(0.1 * max(*size), 0.2 * max(*size))
            emoji_center = (randint(0, size[0]), randint(0, size[1]))

            for s in stack:
                if hypot(emoji_center[0] - s[0], emoji_center[1] - s[1]) < 0.075 * max(*size):
                    n -= 1
                    continue

            emoji_position = (emoji_center[0] - emoji_size // 2, emoji_center[1] - emoji_size // 2)
            emoji = Image.open("hugging_face.png").resize((emoji_size, emoji_size))
            image.alpha_composite(emoji, emoji_position)

        image.show()


captcha = Captcha(size=(1000, 500), mean=10, sd=2)
print(captcha.number)