from decimal import Decimal


class Calcula_grafico:

    @staticmethod
    def process_grades(grades):
        bins = [0, 0, 0, 0]

        for grade in grades:
            if grade >= 9.0:
                bins[0] += 1
            elif 7.0 <= grade < 9.0:
                bins[1] += 1
            elif 4.0 <= grade < 7.0:
                bins[2] += 1
            else:
                bins[3] += 1

        return bins

    @staticmethod
    def calcula360(notas):
        media = notas[1] * Decimal(10)
        media += notas[2] * Decimal(10)
        media += notas[3] * Decimal(2.5)
        media += notas[4] * Decimal(2.5)
        media += notas[5] * Decimal(2.5)
        media += notas[6] * Decimal(2.5)
        weighted_score = media / 30

        return weighted_score
