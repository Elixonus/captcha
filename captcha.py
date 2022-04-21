from math import hypot
from random import randint, shuffle
from PIL import Image


class Captcha:
    number: int
    size: tuple[int, int]
    image: Image
    stack: list[tuple[int, int]]

    def __init__(self, size: tuple[int, int], bounds: tuple[int, int]) -> None:
        self.number = randint(bounds[0], bounds[1])
        self.size = size
        self.image = Image.new("RGBA", size, (0, 0, 0))
        self.stack = []
        emoji_names = []
        for n in range(self.number):
            emoji_names.append("hugging")
        for n in range(randint(bounds[0] // 2, bounds[1] // 2)):
            emoji_names.append("crying")
        for n in range(randint(bounds[0] // 2, bounds[1] // 2)):
            emoji_names.append("money")
        self.add_emojis(emoji_names)

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
        emoji = Image.open(f"emojis/{name}.png").resize((emoji_size, emoji_size))
        self.image.alpha_composite(emoji, emoji_position)
