# Definindo a classe Arredondador
class Arredondador:
    # Método estático que recebe o número e o tipo de arredondamento a
    # ser realizado
    @staticmethod
    def arredondar(numero_str, tipo):
        # Convertendo o número de string para float
        numero = float(numero_str)
        # Verificando qual tipo de arredondamento deve ser realizado
        if tipo == "Para mais":
            # Arredonda para mais e retorna a string formatada com 2
            # casas decimais
            return "{:.2f}".format(round(numero, 2))
        elif tipo == "Para menos":
            # Arredonda para menos e retorna a string formatada com 2
            # casas decimais
            return "{:.2f}".format(round(numero - 0.005, 2))
        elif tipo == "Automatico":
            # Arredonda automaticamente e retorna a string formatada com
            # 2 casas decimais
            return "{:.2f}".format(round(numero, 2))
        else:
            # Se o tipo de arredondamento não for válido, retorna um erro
            raise ValueError(
                "Tipo de arredondamento inválido. Escolha entre 'Para mais',"
                " 'Para menos' ou 'Automatico'")
