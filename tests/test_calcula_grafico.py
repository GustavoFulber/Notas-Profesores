from decimal import Decimal

from utils.calcula_grafico import Calcula_grafico


def test_process_grades():
    grades = [8.5, 9.5, 5.6, 3.8]
    expected_bins = [1, 1, 1, 1]

    assert Calcula_grafico.process_grades(grades) == expected_bins

    grades = [10.0, 9.0, 8.0, 7.0]
    expected_bins = [2, 2, 0, 0]

    assert Calcula_grafico.process_grades(grades) == expected_bins


def test_calcula360():
    notas = [0, 9, 8, 7, 6, 5, 4]  # O índice 0 é ignorado na função calcula360
    expected_score = Decimal(
                             (9*10 + 8*10 + 7*2.5 + 6*2.5 + 5*2.5 + 4*2.5) / 30
                            )

    assert Calcula_grafico.calcula360(notas) == expected_score

    notas = [0, 10, 10, 10, 10, 10, 10]  # Caso com todas as notas no máximo
    expected_score = Decimal(10)  # A média ponderada neste caso é 10

    assert Calcula_grafico.calcula360(notas) == expected_score
