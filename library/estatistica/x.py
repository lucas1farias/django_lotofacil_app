

from banco_de_dados.banco import dtb
from collections import Counter


class XNumbers:
    def __init__(self, db):
        self.database = db
        self.x_values = (1, 5, 7, 9, 13, 17, 19, 21, 25)
        self.x_numbers = self.get_x_numbers()
        self.convert_data_into_string()
        self.convert_data_into_list()
        self.perform_data_countage()
        self.x_numbers_array = self.turn_nested_tuples_into_arrays()
        self.include_percentage()
        self.arrange_data()
        self.x_numbers_most_common_combinations = self.get_data_above_percentage_half_one()
        self.x_numbers_most_common_amounts = self.get_x_numbers_amount()
        self.print_vars()

    def get_x_numbers(self):
        box = []
        for data in self.database:
            for index in data:
                if index in self.x_values:
                    target_index = self.x_values.index(index)
                    number = self.x_values[target_index]
                    box.append(number)
                if index == data[-1]:
                    box.append('/')
        return box

    def get_x_numbers_amount(self):
        box = []
        for index_, _ in enumerate(self.database):
            temp_box = [self.database[index_].count(data) for data in self.x_values]
            for index in range(10):
                if sum(temp_box) == index: box.append(index)
            # if sum(temp_box) == 0: box.append(0)
            # if sum(temp_box) == 1: box.append(1)
            # if sum(temp_box) == 2: box.append(2)
            # if sum(temp_box) == 3: box.append(3)
            # if sum(temp_box) == 4: box.append(4)
            # if sum(temp_box) == 5: box.append(5)
            # if sum(temp_box) == 6: box.append(6)
            # if sum(temp_box) == 7: box.append(7)
            # if sum(temp_box) == 8: box.append(8)
            # if sum(temp_box) == 9: box.append(9)

        report = {
            0: box.count(0), 1: box.count(1), 2: box.count(2), 3: box.count(3), 4: box.count(4),
            5: box.count(5), 6: box.count(6), 7: box.count(7), 8: box.count(8), 9: box.count(9)
        }

        report_tuple = tuple(report.items())

        report_array = [list(tuple_) for tuple_ in report_tuple]

        for index in report_array:
            calculus = float(f'{(index[1] * 100) / len(self.database):.2f}')
            index.append(calculus)

        report_array = sorted(report_array, key=lambda the_index: the_index[2], reverse=True)

        # Imprimir "report_array" para ver os valores alvo comparados com 10 (índice aninhado 2)
        good_amounts_x_numbers = []
        [good_amounts_x_numbers.append(index[0]) if index[2] >= 10 else None for index in report_array]

        return good_amounts_x_numbers

    def convert_data_into_string(self):
        self.x_numbers = "".join([str(index) for index in self.x_numbers])

    def convert_data_into_list(self):
        self.x_numbers = self.x_numbers.split('/')

    def perform_data_countage(self):
        self.x_numbers = list(Counter(self.x_numbers).items())

    def turn_nested_tuples_into_arrays(self):
        self.x_numbers_array = []
        [self.x_numbers_array.append(list(index)) for index in self.x_numbers]
        return self.x_numbers_array

    def include_percentage(self):
        for index in self.x_numbers_array:
            calculus = float(f'{(index[1] * 100) / len(self.database):.2f}')
            index.append(calculus)

    def arrange_data(self):
        self.x_numbers_array = sorted(self.x_numbers_array, key=lambda index: index[2], reverse=True)

    def get_data_above_percentage_half_one(self):
        self.x_numbers_most_common_combinations = []
        [self.x_numbers_most_common_combinations.append(index[0]) if index[2] >= 0.5 else None for index in self.x_numbers_array]
        return self.x_numbers_most_common_combinations

    def print_vars(self):
        print(f'{self.x_numbers = }')
        print(f'{self.x_numbers_array = }')
        print(f'{self.x_numbers_most_common_combinations = }')
        print(f'{self.x_numbers_most_common_amounts = }')


sample = XNumbers(db=dtb)
