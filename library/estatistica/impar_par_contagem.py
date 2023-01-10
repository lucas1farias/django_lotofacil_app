

from library.estatistica.sequencias_seguidas_v2_poo import odd_even_sequences
from collections import Counter


class OddEvenCounter:
    def __init__(self, db):
        self.db = db
        self.odd_even_ = self.odd_even()
        self.odd_even_rank_ = self.odd_even_rank()
        self.odd_even_rank_tuple_into_array_ = self.odd_even_rank_tuple_into_array()
        self.include_percentage()
        self.arrange_data()
        self.good_odd_even = self.get_data_above_percentage_ten()
        # self.print_data()

    def odd_even(self):
        box = []
        odd_ = 0
        even_ = 0
        for odd_even_str in self.db:
            for letter in odd_even_str:
                if letter == 'i':
                    odd_ += 1
                else:
                    even_ += 1
            box.append(f'{odd_}/{even_}')
            odd_ = 0
            even_ = 0
        self.odd_even_ = box
        return self.odd_even_

    def odd_even_rank(self):
        box = list(Counter(self.odd_even_).items())
        self.odd_even_rank_ = box
        return self.odd_even_rank_

    def odd_even_rank_tuple_into_array(self):
        box = []
        [box.append(list(index)) for index in self.odd_even_rank_]
        self.odd_even_rank_tuple_into_array_ = box
        return self.odd_even_rank_tuple_into_array_

    def include_percentage(self):
        for index in self.odd_even_rank_tuple_into_array_:
            calculus = float(f'{(index[1] * 100) / len(self.db):.2f}')
            index.append(calculus)

    def arrange_data(self):
        self.odd_even_rank_tuple_into_array_ = sorted(self.odd_even_rank_tuple_into_array_, key=lambda index: index[2], reverse=True)

    def get_data_above_percentage_ten(self):
        box = []
        [box.append(index[0]) if index[2] >= 10 else None for index in self.odd_even_rank_tuple_into_array_]
        self.good_odd_even = box
        return self.good_odd_even

    def print_data(self):
        print(f'{self.odd_even_}')
        print(f'{self.odd_even_rank_}')
        print(f'{self.odd_even_rank_tuple_into_array_}')
        print(f'{self.good_odd_even}')


# odd_even_sequences = ['piipipiippppipi', 'ipipiiipiipipip', 'ippipipipppipip', ...]
good_odd_even_distribution = OddEvenCounter(db=odd_even_sequences).good_odd_even
# print(good_odd_even_distribution)
