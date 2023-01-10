

from django.views.generic import TemplateView, FormView
from library.funcoes.banco_de_dados import GameInt

from library.estatistica.primeiros_numeros_poo import allowed_at_start
from library.estatistica.sequencias_seguidas_v2_poo import worst_sequences
from library.estatistica.numeros_seguidos_v2_poo import impropers
from library.estatistica.tipo_de_jogo_v2_poo import game_types
from library.estatistica.contar_numeros_primos_v2_poo import (prime_numbers_amount_allowed, most_common_primes)
from library.estatistica.frequencia_numeros_poo import (most_frequent_numbers, percentages)
from library.estatistica.grupos_de_numeros_poo import most_common_sequences_of_3_amount
from library.estatistica.borda_centro_poo import (most_frequent_edges, most_frequent_centers)
from library.estatistica.grupos_horizontais_poo import common_horizontal_thread_groups
from library.estatistica.grupos_verticais_poo import common_vertical_thread_groups
from library.estatistica.historico_numeros import (proper_numbers_by_position, tolerable_mistakes)
from library.estatistica.impar_par_contagem import good_odd_even_distribution

from library.banco_de_dados.banco import dtb, ten_last
from .models import Game

# Adicionar novo jogo (dados tratados até estar nos moldes para ser add ao modelo "Game")
from .forms import NewGameModelForm
from .models import NewGame
from library.funcoes.banco_de_dados import GameStr
from django.urls import reverse_lazy


class LotofacilView(TemplateView):
    template_name = 'index.html'
    model = Game

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Jogos em formato string e tupla de inteiros
        self.games = LotofacilView.model.objects.all()
        self.db = [GameInt(game_string=string_code.code).game for string_code in self.games]
        self.card = tuple(range(1, 26))

        self.last_game = self.db[-1]

        self.last_game_edge = self.get_border_or_center_size(
            target_game=self.last_game,
            site='edges',
            references=[most_frequent_edges, most_frequent_centers]
        )

        self.last_game_center = self.get_border_or_center_size(
            target_game=self.last_game,
            site='center',
            references=[most_frequent_edges, most_frequent_centers]
        )

        self.last_game_horizontal_code = self.horizontal_code(
            reference=common_horizontal_thread_groups,
            target_game=self.last_game
        )

        self.last_game_vertical_code = self.vertical_code(
            reference=common_vertical_thread_groups,
            target_game=self.last_game
        )

        self.last_game_prime_numbers = self.prime_numbers_counter(
            target_game=self.last_game,
            references=[prime_numbers_amount_allowed, most_common_primes]
        )

        self.game = self.create_game(length=15)
        self.game_horizontal_blank_free = self.sequence_horizontal()
        self.game_vertical_blank_free = self.sequence_vertical()
        self.game_gap = self.proper_gap(reference=allowed_at_start)
        self.game_odd_even_sequence = self.avoid_large_odd_even_sequence(reference=worst_sequences)
        self.game_row_pattern = self.row_repetition()
        self.game_column_pattern = self.column_repetition()
        self.game_sequence_in_row = self.avoid_long_sequences(reference=impropers)
        self.game_split = self.game_type(reference=game_types)
        self.game_prime_numbers = self.prime_numbers_counter(
            target_game=self.game,
            references=[prime_numbers_amount_allowed, most_common_primes]
        )
        self.game_score_15_void = self.score_admin(single_score=True, score=15, has_comparison=True)
        self.game_score_14_void = self.score_admin(single_score=True, score=14, has_comparison=True)
        self.game_score_13_one_or_plus = self.score_admin(
            single_score=True,
            score=13,
            has_comparison=True,
            operator='greater',
            repeated=1
        )
        self.good_numbers = self.numbers_frequency(references=[most_frequent_numbers, percentages])
        self.proper_intersections = self.ten_last_comparison(reference=ten_last)
        self.sequence_group = self.three_in_a_row_counter(reference=most_common_sequences_of_3_amount)
        self.game_edges = self.get_border_or_center_size(
            target_game=self.game,
            site='edges',
            references=[most_frequent_edges, most_frequent_centers]
        )
        self.game_center = self.get_border_or_center_size(
            target_game=self.game,
            site='center',
            references=[most_frequent_edges, most_frequent_centers]
        )
        self.game_horizontal_code = self.horizontal_code(
            reference=common_horizontal_thread_groups,
            target_game=self.game
        )
        self.game_vertical_code = self.vertical_code(
            reference=common_vertical_thread_groups,
            target_game=self.game
        )
        self.game_history_numbers = self.game_numbers_position(
            references=[proper_numbers_by_position, tolerable_mistakes]
        )

        self.game_odd_even_countage = self.odd_even_countage(reference=good_odd_even_distribution)

        self.report = None
        self.result = []
        self.conditions = {
            1: self.result.append(True) if self.game_horizontal_blank_free['ok'] else self.result.append(False),
            2: self.result.append(True) if self.game_vertical_blank_free['ok'] else self.result.append(False),
            3: self.result.append(True) if self.game_gap['ok'] else self.result.append(False),
            # 4: self.result.append(True) if self.game_odd_even_sequence['ok'] else self.result.append(False),
            5: self.result.append(True) if self.game_row_pattern['ok'] else self.result.append(False),
            6: self.result.append(True) if self.game_column_pattern['ok'] else self.result.append(False),
            7: self.result.append(True) if self.game_sequence_in_row['ok'] else self.result.append(False),
            8: self.result.append(True) if self.game_split['ok'] else self.result.append(False),
            9: self.result.append(True) if self.game_prime_numbers['ok'] else self.result.append(False),
            10: self.result.append(True) if self.game_score_15_void['ok'] else self.result.append(False),
            11: self.result.append(True) if self.game_score_14_void['ok'] else self.result.append(False),
            12: self.result.append(True) if self.game_score_13_one_or_plus['ok'] else self.result.append(False),
            # 13: self.result.append(True) if self.good_numbers['ok'] else self.result.append(False),
            14: self.result.append(True) if self.proper_intersections['ok'] else self.result.append(False),
            15: self.result.append(True) if self.sequence_group['ok'] else self.result.append(False),
            16: self.result.append(True) if self.game_edges['ok'] else self.result.append(False),
            17: self.result.append(True) if self.game_center['ok'] else self.result.append(False),
            # 18: self.result.append(True) if self.game_horizontal_code['ok'] else self.result.append(False),
            # 19: self.result.append(True) if self.game_vertical_code['ok'] else self.result.append(False),
            20: self.result.append(True) if self.game_history_numbers['ok'] else self.result.append(False),
            21: self.result.append(True) if self.game_odd_even_countage['ok'] else self.result.append(False)
        }
        self.comparisons = []
        self.conditions_game_vs_last = {
            1: self.comparisons.append(True) if self.last_game_edge['array'] != self.game_edges['array']
            else self.comparisons.append(False),
            2: self.comparisons.append(True) if self.last_game_center['array'] != self.game_center['array']
            else self.comparisons.append(False),
            3: self.comparisons.append(True) if self.last_game_horizontal_code['report'] != self.game_horizontal_code[
                'report'] else self.comparisons.append(False),
            4: self.comparisons.append(True) if self.last_game_vertical_code['report'] != self.game_vertical_code[
                'report'] else self.comparisons.append(False),
            5: self.comparisons.append(True) if self.last_game_prime_numbers['array'] != self.game_prime_numbers[
                'array'] else self.comparisons.append(False)
        }

        if self.result.count(False) == 0 and self.comparisons.count(False) == 0:
            self.report = True
        else:
            self.report = False

    def create_game(self, length: int):
        from random import choice
        self.game = set({})
        while len(self.game) < length:
            self.game.add(choice(self.card))
        return list(self.game)

    def sequence_horizontal(self) -> dict:
        row_1, row_2, row_3, row_4, row_5 = 0, 0, 0, 0, 0

        # Cada linha do volante em ordem crescente
        row_1_numbers = [*range(1, 6)]
        row_2_numbers = [*range(6, 11)]
        row_3_numbers = [*range(11, 16)]
        row_4_numbers = [*range(16, 21)]
        row_5_numbers = [*range(21, 26)]

        # Estou ciente de que as ações deveriam estar nas linhas abaixo, mas é desejado economizar linhas
        for number in self.game:
            if number in row_1_numbers: row_1 += 1
            elif number in row_2_numbers: row_2 += 1
            elif number in row_3_numbers: row_3 += 1
            elif number in row_4_numbers: row_4 += 1
            elif number in row_5_numbers: row_5 += 1

        game_horizontal = [row_1, row_2, row_3, row_4, row_5]

        if 0 not in game_horizontal:
            return {'ok': True, 'report': game_horizontal}
        return {'ok': False, 'report': game_horizontal}

    def sequence_vertical(self) -> dict:
        column_1, column_2, column_3, column_4, column_5 = 0, 0, 0, 0, 0

        column_1_numbers = [1, 6, 11, 16, 21]
        column_2_numbers = [2, 7, 12, 17, 22]
        column_3_numbers = [3, 8, 13, 18, 23]
        column_4_numbers = [4, 9, 14, 19, 24]
        column_5_numbers = [5, 10, 15, 20, 25]

        # Estou ciente de que as ações deveriam estar nas linhas abaixo, mas é desejado economizar linhas
        for number in self.game:
            if number in column_1_numbers:
                column_1 += 1
            elif number in column_2_numbers:
                column_2 += 1
            elif number in column_3_numbers:
                column_3 += 1
            elif number in column_4_numbers:
                column_4 += 1
            elif number in column_5_numbers:
                column_5 += 1

        game_vertical = [column_1, column_2, column_3, column_4, column_5]

        if 0 not in game_vertical:
            return {'ok': True, 'report': game_vertical}
        return {'ok': False, 'report': game_vertical}

    def proper_gap(self, reference) -> dict:
        result = []

        calculus = []

        index_first = 0
        index_second = 1

        while index_second < len(self.game):
            calculus.append(self.game[index_second] - self.game[index_first])

            index_first += 1
            index_second += 1

        gap_of_3_amount = calculus.count(4)
        gap_of_4_amount = calculus.count(5)

        # Análise [1]: O jogo só pode ter 1 lacuna de 3
        if gap_of_3_amount > 1:
            result.append('overflow_gap_3')
        # Análise [2]: O jogo não pode ter qualquer lacuna de 4
        if gap_of_4_amount != 0:
            result.append('overflow_gap_4')

        # Jogo reprovado
        if 'overflow_gap_3' in result or 'overflow_gap_4' in result or self.game[0] not in reference:
            return {'ok': False, 'report': calculus, 'data': result}

        # Jogo aprovado
        if 'overflow_gap_3' not in result and 'overflow_gap_4' not in result and self.game[0] in reference:
            return {'ok': True, 'report': calculus, 'data': result}

    def avoid_large_odd_even_sequence(self, reference) -> dict:
        box = []

        odd, even = 'i', 'p'
        [box.append(even) if not number % 2 else box.append(odd) for number in self.game]
        game_string = "".join(box)

        must_have_false_only = []

        for code in reference: must_have_false_only.append(code in game_string)

        if True in must_have_false_only:
            return {'ok': False, 'report': game_string, 'proof': must_have_false_only}
        return {'ok': True, 'report': game_string, 'proof': must_have_false_only}

    def row_repetition(self) -> dict:
        array_of_ones = []
        arrays_of_zeros = []
        [array_of_ones.append(1) for n in range(15)]
        [arrays_of_zeros.append(0) for n in range(10)]

        all_numbers = set(range(1, 26))
        ones_to_receive_1 = set(self.game)
        ones_to_receive_zero = all_numbers.difference(ones_to_receive_1)

        ones_inside_game = list(zip(self.game, array_of_ones))
        ones_outside_game = list(zip(ones_to_receive_zero, arrays_of_zeros))

        # Junção: [(número de "self.game", 1), (número fora de "self.game", 0), ...]
        for outsider in ones_outside_game:
            ones_inside_game.append(outsider)

        tuples_ordered = sorted(ones_inside_game, key=lambda index_1st: index_1st[0])

        binary_result = [index[1] for index in tuples_ordered]

        binary_group_1 = "".join([str(index) for index in binary_result[0:5]])
        binary_group_2 = "".join([str(index) for index in binary_result[5:10]])
        binary_group_3 = "".join([str(index) for index in binary_result[10:15]])
        binary_group_4 = "".join([str(index) for index in binary_result[15:20]])
        binary_group_5 = "".join([str(index) for index in binary_result[20:25]])

        row_code = [binary_group_1, binary_group_2, binary_group_3, binary_group_4, binary_group_5]
        row_code_as_set = set(row_code)

        if len(row_code_as_set) == 5:
            return {'ok': True, 'set': row_code, 'report': len(row_code_as_set)}
        return {'ok': False, 'set': row_code, 'report': len(row_code_as_set)}

    def column_repetition(self) -> dict:
        array_of_ones = []

        arrays_of_zeros = []
        [array_of_ones.append(1) for n in range(15)]
        [arrays_of_zeros.append(0) for n in range(10)]

        all_numbers = set(range(1, 26))
        ones_to_receive_1 = set(self.game)
        ones_to_receive_zero = all_numbers.difference(ones_to_receive_1)

        ones_inside_game = list(zip(self.game, array_of_ones))
        ones_outside_game = list(zip(ones_to_receive_zero, arrays_of_zeros))

        for tuple_element in ones_outside_game:
            ones_inside_game.append(tuple_element)

        tuples_ordered = sorted(ones_inside_game, key=lambda index_1st: index_1st[0])

        # O nome da variável foi modificada apenas p/ caber na linha abaixo
        x = tuples_ordered

        binary_group_1 = tuple([x[0][1], x[5][1], x[10][1], x[15][1], x[20][1]])
        binary_group_2 = tuple([x[1][1], x[6][1], x[11][1], x[16][1], x[21][1]])
        binary_group_3 = tuple([x[2][1], x[7][1], x[12][1], x[17][1], x[22][1]])
        binary_group_4 = tuple([x[3][1], x[8][1], x[13][1], x[18][1], x[23][1]])
        binary_group_5 = tuple([x[4][1], x[9][1], x[14][1], x[19][1], x[24][1]])

        # Para não ficar código repetido
        del tuples_ordered

        # ANTES: binary_group_1...2... (o resto foi add apenas p/ reduzir dados no template)
        column_code = [
            "".join([str(number) for number in binary_group_1]),
            "".join([str(number) for number in binary_group_2]),
            "".join([str(number) for number in binary_group_3]),
            "".join([str(number) for number in binary_group_4]),
            "".join([str(number) for number in binary_group_5])
        ]
        column_code_as_set = set(column_code)

        if len(column_code_as_set) == 5:
            return {'ok': True, 'set': column_code, 'report': len(column_code_as_set)}
        return {'ok': False, 'set': column_code, 'report': len(column_code_as_set)}

    def avoid_long_sequences(self, reference: list, first_index=0, second_index=1) -> dict:
        integer_list = []

        answer = []

        while second_index < len(self.game):
            # O cálculo precisa ser 0. Vamos pegar o jogo [1, 2, 3, 5, 7, 8, 10, 11, 14, 16, 17, 19, 21, 24, 25]
            # A lógica é: (2 - 1) (3 - 2) (5 - 3) (7 - 5) e assim por diante até acabar os índices do array
            # Se os números são seguidos, o valor será 1, mas na anexação é subtraído por 1, ou seja, será 0
            # No array que anexa, que é "integer_list", só pode haver 0 até 5 vezes (significa 5 números seguidos)
            integer_list.append((self.game[second_index] - self.game[first_index]) - 1)
            first_index += 1
            second_index += 1

        [answer.append('y') if integer == 0 else answer.append('n') for integer in integer_list]

        answer_code = "".join(answer)

        report = []
        for code in reference:
            if code not in answer_code:
                report.append(True)
            else:
                report.append(False)

        if False in report:
            return {'ok': False, 'calculus': [integer + 1 for integer in integer_list], 'report': answer_code, 'proof': report}
        return {'ok': True, 'calculus': [integer + 1 for integer in integer_list], 'report': answer_code, 'proof': report}

    def game_type(self, reference) -> dict:
        upper, lower, upper_area, lower_area = 0, 0, tuple(range(1, 16)), tuple(range(16, 26))

        for number in self.game:
            if number in upper_area:
                upper += 1
            elif number in lower_area:
                lower += 1

        game_class = f"{upper}/{lower}"

        if game_class in reference:
            return {'ok': True, 'report': game_class}
        return {'ok': False, 'report': game_class}

    @staticmethod
    def prime_numbers_counter(target_game, references) -> dict:

        prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23]
        prime_numbers_box = []

        for number in target_game:
            if number in prime_numbers:
                prime_numbers_box.append(number)

        array_size = len(prime_numbers_box)

        if len(prime_numbers_box) in references[0]:
            return {'ok': True, 'report': f'{prime_numbers_box} {array_size} número(s)', 'array': prime_numbers_box}
        return {'ok': False, 'report': f'{prime_numbers_box} {array_size} número(s)', 'array': prime_numbers_box}

    def score_admin(self, single_score: bool,
                    score: int,
                    has_comparison=False,
                    operator='equals',
                    repeated=0
                    ) -> [int, str]:
        similarities = []

        for i in range(len(self.db)):
            game_main_as_set = set(self.game)
            game_comparared_as_set = set(self.db[i])
            similarity_target_game_vs_db_game = len(game_main_as_set.intersection(game_comparared_as_set))
            similarities.append(similarity_target_game_vs_db_game)

        precisions = [
            similarities.count(6), similarities.count(7), similarities.count(8), similarities.count(9),
            similarities.count(10), similarities.count(11), similarities.count(12), similarities.count(13),
            similarities.count(14), similarities.count(15)
        ]

        score_panel = f"""
                Jogo analisado: {self.game}
                ========== PONTUAÇÃO GLOBAL ==========
                6  pontos || {precisions[0]} vezes
                7  pontos || {precisions[1]} vezes
                8  pontos || {precisions[2]} vezes
                9  pontos || {precisions[3]} vezes
                10 pontos || {precisions[4]} vezes
                11 pontos || {precisions[5]} vezes
                12 pontos || {precisions[6]} vezes
                13 pontos || {precisions[7]} vezes
                14 pontos || {precisions[8]} vezes
                15 pontos || {precisions[9]} vezes"""

        if single_score:
            scores = {
                6: precisions[0], 7: precisions[1], 8: precisions[2], 9: precisions[3], 10: precisions[4],
                11: precisions[5], 12: precisions[6], 13: precisions[7], 14: precisions[8], 15: precisions[9],
            }

            box_with_score = []
            [box_with_score.append(scores[key]) for key in scores if score == key]

            score_found = box_with_score[0]
            correct = {'ok': True, 'banner': score_panel, 'report': score_found}
            incorrect = {'ok': False, 'banner': score_panel, 'report': score_found}

            if has_comparison and operator == 'equals':
                if box_with_score[0] == repeated:
                    return correct
                return incorrect
            if has_comparison and operator == 'greater':
                if box_with_score[0] > repeated:
                    return correct
                return incorrect
            if has_comparison and operator == 'lesser':
                if box_with_score[0] < repeated:
                    return correct
                return incorrect

            if not has_comparison:
                return box_with_score[0]

        else:
            return score_panel

    def numbers_frequency(self, references) -> dict:
        similarity = set(self.game).intersection(set(references[0]))

        similarity_amount = len(similarity)

        if references[1]['40%'] <= similarity_amount <= references[1]['70%']:
            return {'ok': True, 'report': similarity}
        return {'ok': False, 'report': similarity}

    def ten_last_comparison(self, reference) -> dict:
        bad_codes = ('888', '8888', '88888', '999', '9999', '99999', '101010', '10101010', '1010101010')

        exceeding_patterns = []

        bad_combinations = (
            '891011', '111098', '8910', '91011', '11109', '1098',
            '8989', '810810', '811811',
            '9898', '910910', '911911',
            '108108', '109109', '10111011',
            '118118', '119119', '11101110',
        )
        stupid_patterns = []

        too_similar = False

        result = []
        for index, game in enumerate(reference):
            result.append(len(set(game).intersection(set(self.game))))

        intersection_code = "".join([str(index) for index in result])

        # Análise [1]: Condição satisfeita: jogo invalidado
        if result.count(11) > 2: too_similar = True

        # Análise [2]: else satisfeito, jogo invalidado
        for code in bad_codes:
            if code not in intersection_code:
                exceeding_patterns.append(False)
            else:
                exceeding_patterns.append(True)

        # Análise [3]: else satisfeito, jogo invalidado
        for code in bad_combinations:
            if code not in intersection_code:
                stupid_patterns.append(False)
            else:
                stupid_patterns.append(True)

        # Todas as condições em "conditions" devem ser "True", ou seja, não deve haver "False" anexado a "box"
        box = []
        before_last_game = result[-2]
        last_game = result[-1]
        very_similar_range = range(11, 16)
        very_different_range = 7
        conditions = {
            1: box.append(True) if 5 not in result and 6 not in result and 7 not in result else box.append(False),
            2: box.append(
                True) if 12 not in result and 13 not in result and 14 not in result and 15 not in result else box.append(
                False),
            3: box.append(True) if 8 in result and 9 in result and 10 in result and 11 in result else box.append(False),
            4: box.append(
                True) if last_game not in very_similar_range and last_game != very_different_range else box.append(
                False),
            5: box.append(True) if last_game != before_last_game else box.append(False),
            6: box.append(True) if True not in exceeding_patterns else box.append(False),
            7: box.append(True) if True not in stupid_patterns else box.append(False),
            8: box.append(True) if not too_similar else box.append(False)
        }

        if False not in box:
            return {'ok': True, 'report': result}
        return {'ok': False, 'report': result}

    def three_in_a_row_counter(self, reference) -> dict:
        rows = []

        i, i2, i3 = 1, 2, 3
        for n in range(23):
            rows.append([i, i2, i3])
            i += 1
            i2 += 1
            i3 += 1

        game_cells = [
            self.game[0:3], self.game[1:4], self.game[2:5], self.game[3:6], self.game[4:7],
            self.game[5:8], self.game[6:9], self.game[7:10], self.game[8:11], self.game[9:12],
            self.game[10:13], self.game[11:14], self.game[12:15]
        ]

        three_in_a_row_sequence = 0
        for cell in game_cells:
            if cell in rows:
                three_in_a_row_sequence += 1

        if three_in_a_row_sequence in reference:
            return {'ok': True, 'report': three_in_a_row_sequence}
        return {'ok': False, 'report': three_in_a_row_sequence}

    @staticmethod
    def get_border_or_center_size(target_game, site, references):
        # Anexa os números de canto e centro encontrados em "self.game", respectivamente
        card_edges = []
        card_center = []

        # Todos os números de borda do volante (quadrado)
        for n in list(target_game):
            if n == 1 or n == 2 or n == 3 or n == 4 or n == 5 or \
                    n == 10 or n == 15 or n == 20 or n == 25 or \
                    n == 24 or n == 23 or n == 22 or n == 21 or \
                    n == 16 or n == 11 or n == 6:
                card_edges.append(n)

        # Todos os números de centro do volante (retângulo)
        for n in list(target_game):
            if n == 7 or n == 8 or n == 9 or n == 12 or n == 13 or n == 14 or n == 17 or n == 18 or n == 19:
                card_center.append(n)

        ""
        # Quando for desejado analisar os números de borda (16 números)
        # "references[0]" = qtd. de números de borda mais recorrentes (10%+)
        # "card_edges" define a qtd. de números de borda. Essa qtd. estando em "references[0]": jogo válido
        edge_amount = len(card_edges)
        if site == 'edges':
            if edge_amount in references[0]:
                return {'ok': True, 'report': edge_amount, 'array': card_edges}
            return {'ok': False, 'report': edge_amount, 'array': card_edges}

        ""
        # Quando for desejado analisar os números de centro (9 números)
        # "references[1]" = qtd. de números de centro mais recorrentes (10%+)
        # "card_center" define a qtd. de números de centro. Essa qtd. estando em "references[1]": jogo válido
        center_amount = len(card_center)
        if site == 'center':
            if center_amount in references[1]:
                return {'ok': True, 'report': center_amount, 'array': card_center}
            return {'ok': False, 'report': center_amount, 'array': card_center}

    @staticmethod
    def horizontal_code(reference, target_game):

        rows = {'1st': 0, '2nd': 0, '3rd': 0, '4th': 0, '5th': 0}

        for number in target_game:
            if number in range(1, 6): rows['1st'] += 1
            elif number in range(6, 11): rows['2nd'] += 1
            elif number in range(11, 16): rows['3rd'] += 1
            elif number in range(16, 21): rows['4th'] += 1
            elif number in range(21, 26): rows['5th'] += 1

        game_code_tuple = tuple(rows.values())

        game_code_str = "".join([str(int_index) for int_index in game_code_tuple])

        if game_code_str in reference:
            return {
                'ok': True,
                'report': game_code_str,
                'full_report': f'{game_code_str} [rank: {reference.index(game_code_str)}]'
            }
        return {'ok': False, 'report': game_code_str, 'full_report': f'{game_code_str} [fora do rank]'}

    @staticmethod
    def vertical_code(reference, target_game):

        columns = {
            '1st': {'sequence': [1, 6, 11, 16, 21], 'countage': 0},
            '2nd': {'sequence': [2, 7, 12, 17, 22], 'countage': 0},
            '3rd': {'sequence': [3, 8, 13, 18, 23], 'countage': 0},
            '4th': {'sequence': [4, 9, 14, 19, 24], 'countage': 0},
            '5th': {'sequence': [5, 10, 15, 20, 25], 'countage': 0}
        }

        for number in target_game:
            if number in columns['1st']['sequence']:
                columns['1st']['countage'] += 1
            elif number in columns['2nd']['sequence']:
                columns['2nd']['countage'] += 1
            elif number in columns['3rd']['sequence']:
                columns['3rd']['countage'] += 1
            elif number in columns['4th']['sequence']:
                columns['4th']['countage'] += 1
            elif number in columns['5th']['sequence']:
                columns['5th']['countage'] += 1

        game_code_tuple = (
            columns['1st']['countage'], columns['2nd']['countage'], columns['3rd']['countage'],
            columns['4th']['countage'], columns['5th']['countage']
        )

        game_code_str = "".join([str(int_index) for int_index in game_code_tuple])

        if game_code_str in reference:
            return {
                'ok': True,
                'report': game_code_str,
                'full_report': f'{game_code_str} [rank: {reference.index(game_code_str)}]'
            }
        return {'ok': False, 'report': game_code_str, 'full_report': f' {game_code_str} [fora do rank]'}

    def game_numbers_position(self, references: list) -> dict:
        """
        * Coletar os números mais comuns de cada posição de 1 até 15
        * Ele representa o histórico de cada índice de cada jogo na história da Lotofácil
        * '1st' = representa os números mais comuns ao primeiro número dentre todos os jogos
        * '2nd' = representa os números mais comuns ao segundo número dentre todos os jogos
        * Exemplo do que pode ser "references[0]" (conforme novos jogos são add, valores podem mudar)
        references[0] = {
            '1st': [1, 2, 3],
            '2nd': [2, 3, 4],
            '3rd': [3, 4, 5, 6],
            '4th': [4, 5, 6, 7, 8],
            '5th': [6, 7, 8, 9, 10],
            '6th': [8, 9, 10, 11, 12],
            '7th': [9, 10, 11, 12, 13],
            '8th': [11, 12, 13, 14, 15],
            '9th': [13, 14, 15, 16, 17],
            '10th': [14, 15, 16, 17, 18],
            '11th': [16, 17, 18, 19, 20],
            '12th': [18, 19, 20, 21, 22],
            '13th': [20, 21, 22, 23],
            '14th': [22, 23, 24],
            '15th': [24, 25]
        }

        ===== parte 1 ===== \n
        * É desejado saber se cada índice de "self.game" está dentro de cada um dos dados em "references[0]"
        * Para funcionar, "self.game" e "references[0]" possuem qtd. de índices equivalentes
        * Origem de "references[0]"? "estatistica/historico_numeros" via "proper_numbers_by_position"
        * Ex: (1, 3, 4, 6, 7, 9, 10, 12, 13, 14, 17, 18, 21, 23, 24)
        * No loop, [1] é procurado em references[0]['1st]...[3] é procurado em references[0]['2nd']...
        * Se for achado: result.append(True), se não for: result.append(False)

        ===== parte 2 ===== \n
        * A qtd. de "False" encontrados em "result" é contado p/ ser comparado com "reference[1]"
        * Origem de "references[1]"? "estatistica/historico_numeros" via "tolerable_mistakes"
        * Na época que foi criado "tolerable_mistakes = [0, 1, 2, 3]", foram as qtds. encontradas acima de 10%
        * As qtds. abaixo de 10% foram descartadas, pois é trabalhado com as maiores possibilidades
        * Interpretação: "self.game" deve ter [15, 14, 13, 12] dos números em "references[0]" com base em [0, 1, 2, 3]
        """

        # Recebe uma sequência de "True" e "False" (15 no total)
        result = []

        # "reference" têm todas essas chaves, que estão na mesma qtd. de "self.game" (15)
        positions = [
            '1st', '2nd', '3rd', '4th', '5th',
            '6th', '7th', '8th', '9th', '10th',
            '11th', '12th', '13th', '14th', '15th'
        ]

        # (parte 1) Leia a documentação da função
        for index in range(len(self.game)):
            if self.game[index] in references[0][positions[index]]: result.append(True)
            else: result.append(False)

        # (parte 2) Leia a documentação da função
        mistakes = result.count(False)
        if mistakes in references[1]:
            return {'ok': True, 'report': f'Erros cometidos: {mistakes}'}
        return {'ok': False, 'report': f'Erros cometidos: {mistakes}'}

    def odd_even_countage(self, reference):
        odd_ = 0
        even_ = 0
        for letter in self.game_odd_even_sequence['report']:
            if letter == 'i':
                odd_ += 1
            else:
                even_ += 1

        odd_even_seq = f'{odd_}/{even_}'
        if odd_even_seq in reference:
            return {'ok': True, 'report': odd_even_seq}
        return {'ok': False, 'report': odd_even_seq}

    def get_context_data(self, **kwargs):
        context = super(LotofacilView, self).get_context_data(**kwargs)
        context['db'] = self.db
        context['last_game'] = self.db[-1]
        context['game'] = self.game
        context['horizontal_code'] = self.game_horizontal_blank_free['report']
        context['vertical_code'] = self.game_vertical_blank_free['report']
        context['gap'] = self.game_gap['report']
        context['odd_even_seq'] = self.game_odd_even_sequence['report']
        context['len_row_pattern'] = len(self.game_row_pattern['set'])
        context['row_pattern'] = self.game_row_pattern['set']
        context['column_pattern'] = self.game_column_pattern['set']
        context['sequence_in_row'] = self.game_sequence_in_row['calculus']
        context['game_type'] = self.game_split['report']
        context['prime_numbers'] = self.game_prime_numbers['report']
        context['15_void'] = self.game_score_15_void['report']
        context['14_void'] = self.game_score_14_void['report']
        context['13_scored'] = f"{self.game_score_13_one_or_plus['report']} jogos"
        context['good_numbers_amount'] = self.good_numbers['report']
        context['proper_intersections'] = self.proper_intersections['report']
        context['3_in_row_amount'] = self.sequence_group['report']
        context['game_edge'] = self.game_edges['array']
        context['game_center'] = self.game_center['array']
        context['horizontal_string'] = self.game_horizontal_code['full_report']
        context['vertical_string'] = self.game_vertical_code['full_report']
        context['mistakes_found'] = self.game_history_numbers['report']
        context['odd_even_countage'] = self.game_odd_even_countage['report']

        context['game_approved'] = f'Condições satisfeitas do jogo: [{self.result.count(True)}/{len(self.result)}]'
        context['game_approved_vs_last_game'] = f'Condições satisfeitas do jogo em relação ao último: [{self.comparisons.count(True)}/{len(self.comparisons)}]'

        context['last_game_edge'] = self.last_game_edge['array']
        context['last_game_center'] = self.last_game_center['array']
        context['last_game_horizontal_string'] = self.last_game_horizontal_code['full_report']
        context['last_game_vertical_string'] = self.last_game_vertical_code['full_report']
        context['last_game_prime_numbers'] = self.last_game_prime_numbers['report']

        context['result'] = self.result
        context['report'] = self.report
        return context


class TestView(TemplateView):
    template_name = 'tests.html'
    birthday = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        context['array'] = [0, 1, 2, 3, 4, 5]
        context['age'] = self.request.GET.get('age')
        return context


class NewGameFormView(FormView):
    template_name = 'new_game.html'
    form_class = NewGameModelForm
    success_url = reverse_lazy('add')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = NewGame.objects.all()

        # ========== Verificação se os bancos (manual e django) estão em sincronia ==========

        # Lista de tuplas com todos os jogos add manualmente
        self.manual_db = dtb
        # Lista de strings da forma convertida dos jogos em tupla
        self.db_str = Game.objects.all()

        self.scan = []
        self.proof = []

        # Converter as strings de volta p/ jogos tupla
        for i, code_str in enumerate(self.db_str):
            obj_str_translated_to_tuple = tuple(GameInt(code_str.code).game)

            # Registrar evidências (não mandatório)
            analysis = f"O jogo {str(code_str.code).upper()} significa {obj_str_translated_to_tuple}. Ele é igual a {dtb[i]}? {['sim' if obj_str_translated_to_tuple == dtb[i] else 'não']}"
            self.proof.append(analysis)

            # Verificar se a conversão corresponde a algum jogo do banco de tuplas
            if obj_str_translated_to_tuple in self.manual_db:
                self.scan.append(True)

        # Como é descoberto se os bancos estão sincronizados
        self.equivalences = self.scan.count(True)

        # Confirmação se os bancos estão sincronizados (todas as conversões foram encontradas no banco de tuplas)
        if self.equivalences == len(self.manual_db):
            print(f"""
            ========== RELATÓRIO ==========
            Qtd. de índices do banco manual?     {len(self.manual_db)}
            Qtd. de índices do banco de strings? {len(self.db_str)}
            Equivalências encontradas?           {self.equivalences}
            Todos os jogos do banco de strings são equivalentes ao do banco manual\n""")

        else:
            print(f'Algo errado aconteceu: {self.equivalences}/{len(self.manual_db)}')

    def form_valid(self, form):
        # input_value = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15'
        # input_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
        # input_string = 'abcdefghijklmno'
        input_value = form.cleaned_data.get('game_text')
        input_tuple = tuple([int(integer) for integer in input_value.split(' ')])
        input_string = GameStr(game_tuple=input_tuple).game_str_code

        # Pelo modelo "NewGame", o modelo "Game" acessa o objeto final e o envia como objeto do modelo "Game"
        new_obj = Game(code=input_string)
        new_obj.save()

        # Mostrar que "form" é uma var "self.form" de "forms.py/NewGameModelForm"
        form.show_object_data()
        # print(dir(form))
        # form.save()
        return super(NewGameFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(NewGameFormView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(NewGameFormView, self).get_context_data(**kwargs)
        # context['condition'] = self.equivalences == len(self.manual_db)
        # context['manual_tuple_db_size'] = len(self.manual_db)
        context['string_db'] = len(self.db_str)
        # context['equivalences_amount'] = self.equivalences
        # context['result'] = 'Todos os jogos do banco de strings são equivalentes ao do banco manual'
        # context['proof'] = self.proof
        # context['reproved'] = f'Algo errado aconteceu: {self.equivalences}/{len(self.manual_db)}'
        return context
