

from library.banco_de_dados.banco import dtb


def ink_random(the_text: str) -> str:
    from random import choice

    box: tuple = (
        '\033[1:30m', '\033[1:31m', '\033[1:32m', '\033[1:33m', '\033[1:34m', '\033[1:35m', '\033[1:36m',
        '\033[1:37m', '\033[1:38m',
    )

    return f"{choice(box)}{the_text}{box[-1]}"


def ink(color: str = 'blue', text: str = 'texto') -> str:
    # keys = conditions / values = actions of the conditions
    colors = {
        'black': '\033[1:30m' + text + '\033[m',
        'red': '\033[1:31m' + text + '\033[m',
        'green': '\033[1:32m' + text + '\033[m',
        'yellow': '\033[1:33m' + text + '\033[m',
        'blue': '\033[1:34m' + text + '\033[m',
        'purple': '\033[1:35m' + text + '\033[m',
        'cyan': '\033[1:36m' + text + '\033[m',
        'gray': '\033[1:37m' + text + '\033[m',
    }

    for key in colors:
        if color == key:
            return colors[key]


# Converte todos os números do bdd em strings
class GameStr:
    def __init__(self, game_tuple):
        self.all_numbers = tuple(range(1, 26))
        self.symbols = list('abcdefghijklmnopqrstuvwxy')
        self.game = game_tuple
        self.game_copy = list(self.game)
        self.game_str_code = self.build_game_str_code()
        self.translations = self.set_key_number_value_string()
        self.game_str_code_translation = self.translation()

        # self.print_data()

    def increase_game_copy_length(self):
        for index in range(10):
            self.game_copy.append(0)

    def build_game_str_code(self):
        box = []
        for _, index in enumerate(self.all_numbers):
            for number in self.game_copy:
                if number == self.all_numbers[_]:
                    box.append(self.symbols[_])
        self.game_str_code = "".join(box)
        return self.game_str_code

    def set_key_number_value_string(self):
        box = {}
        for _, index in enumerate(self.symbols):
            box[index] = self.all_numbers[_]
        self.translations = box
        return self.translations

    def translation(self):
        box = []
        for key in self.translations.keys():
            for number in self.game_str_code:
                if key in number:
                    box.append(self.translations[key])
        self.game_str_code_translation = box
        return self.game_str_code_translation

    def print_data(self):
        print(f'{self.game_copy = }')
        print(f'{self.game_str_code = }')
        print(f'{self.translations = }')
        print(f'{self.game_str_code_translation = }')


# Converte todos os códigos string em números
class GameInt:
    def __init__(self, game_string):
        self.all_numbers = tuple(range(1, 26))
        self.symbols = list('abcdefghijklmnopqrstuvwxy')
        self.game_string = game_string
        self.translations = self.set_key_number_value_string()
        self.game = self.translation()

    def set_key_number_value_string(self):
        box = {}
        for _, index in enumerate(self.symbols):
            box[index] = self.all_numbers[_]
        self.translations = box
        return self.translations

    def translation(self):
        box = []
        for key in self.translations.keys():
            for number in self.game_string:
                if key in number:
                    box.append(self.translations[key])
        self.game = box
        return self.game


# game = '1 2 4 6 7 8 10 11 14 15 16 17 20 21 24'
# game_shaped = tuple([int(integer) for integer in game.split(' ')])
# print('[A]', game_shaped)
# game_string = GameStr(game_tuple=game_shaped).game_str_code

"Último registro do banco"
# game_string = 'bcdghinpqrstvxy'

"Protótipo"
# game_string = ''

"Consulta"
# print(GameInt(game_string=game_string).game,
#       tuple(GameInt(game_string=game_string).game) in dtb,
#       dtb.index(tuple(GameInt(game_string=game_string).game))
#       )
