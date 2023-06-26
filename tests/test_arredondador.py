import pytest

from utils.arredondador import Arredondador


def test_arredondar_para_mais():
    assert Arredondador.arredondar("3.14989", "Para mais") == "3.15"


def test_arredondar_para_mais_especifico():
    assert Arredondador.arredondar("3.145", "Para mais") == "3.15"


def test_arredondar_para_menos():
    assert Arredondador.arredondar("3.14159", "Para menos") == "3.14"


def test_arredondar_para_menos_especifico():
    assert Arredondador.arredondar("3.145", "Para menos") == "3.14"


def test_arredondar_automatico():
    assert Arredondador.arredondar("3.14159", "Automatico") == "3.14"


def test_arredondar_automatico_especifico():
    assert Arredondador.arredondar("3.145", "Automatico") == "3.15"


def test_arredondar_invalido():
    with pytest.raises(ValueError):
        Arredondador.arredondar("3.14159", "Invalido")
