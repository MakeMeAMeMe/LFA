from typing import Dict, List
from collections import namedtuple
from pathlib import Path
from json import load

pilha = list()

Operacao = namedtuple(
    "Operacao", ["simbolo_fita", "simbolo_pilha", "simbolo_empilhar", "next_state"])


class Estado:
    def __init__(self, nome: str, operacoes: List[Operacao]):
        self.nome = nome
        self.operacoes = operacoes


class AP:
    def __init__(self, fita: str, estados: List[Estado], estado_inicial: str, estados_finais: List[str], movimento_vazio: str = '#', coringa: str = "?"):
        self.__pilha = list()
        self.__estado_atual = estado_inicial
        self.estado_incial = estado_inicial
        self.estados_finais = estados_finais
        self.estados = estados
        self.fita = fita
        self.fita_inicial = fita
        self.movimento_vazio = movimento_vazio
        self.coringa = coringa

    @property
    def pilha(self):
        return self.__pilha

    @property
    def estado_atual(self):
        return self.__estado_atual

    def executar_operacao(self):
        letra_fita = None
        if len(self.fita) >= 1:
            letra_fita = self.fita[0]  # fita = aasdfasdgasd
            self.fita = self.fita[1:]  # fita[1:] = asdfasdgasd

        estado_atual = [
            estado for estado in self.estados if estado.nome == self.__estado_atual][0]  # :)
        if not letra_fita:
            for operacao in estado_atual.operacoes:
                if operacao.simbolo_fita == self.coringa:
                    if operacao.simbolo_pilha == self.coringa:
                        if len(self.__pilha) == 0:
                            if operacao.next_state in self.estados_finais:
                                print(str(operacao))
                                self.__estado_atual = operacao.next_state
                                return True
                    elif self.__pilha[-1] == operacao.simbolo_pilha:
                        self.__pilha.pop()
                        if operacao.simbolo_empilhar != self.movimento_vazio:
                            self.__pilha.extend(
                                [simbolo for simbolo in operacao.simbolo_empilhar])
                        print(str(operacao))
                        self.__estado_atual = operacao.next_state
                        return True
            return False

        for operacao in estado_atual.operacoes:
            if operacao.simbolo_fita == letra_fita:
                if self.movimento_vazio == operacao.simbolo_pilha:
                    if operacao.simbolo_empilhar != self.movimento_vazio:
                        self.__pilha.extend(
                            [simbolo for simbolo in operacao.simbolo_empilhar])
                    print(str(operacao))
                    self.__estado_atual = operacao.next_state
                    return True
                elif len(self.__pilha) > 0 and self.__pilha[-1] == operacao.simbolo_pilha:
                    self.__pilha.pop()
                    if operacao.simbolo_empilhar != self.movimento_vazio:
                        self.__pilha.extend(
                            [simbolo for simbolo in operacao.simbolo_empilhar])
                    print(str(operacao))
                    self.__estado_atual = operacao.next_state
                    return True
                elif operacao.simbolo_pilha == self.coringa and len(self.__pilha) == 0:
                    if operacao.simbolo_empilhar != self.movimento_vazio:
                        self.__pilha.extend(
                            [simbolo for simbolo in operacao.simbolo_empilhar])
                    print(str(operacao))
                    self.__estado_atual = operacao.next_state
                    return True
        return False

    def __str__(self):
        return f"Fita: {self.fita_inicial} -> {self.fita} & Estado Atual: {self.__estado_atual}"

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    with Path("./data.json").open("r") as data_file:
        data = load(data_file)
    estados = list()
    for estado_data in data["states"]:
        operacoes = list()
        for operacao_data in estado_data.get("operacoes"):
            operacao = Operacao(operacao_data.get("simbolo_fita"), operacao_data.get(
                "simbolo_pilha"), operacao_data.get("simbolo_empilhar"), operacao_data.get("next_state"))
            operacoes.append(operacao)
        estado = Estado(estado_data.get("nome"), operacoes)
        estados.append(estado)

    coringa = data.get("coringa")
    movimento_vazio = data.get("movimento_vazio")
    fitas_aprovar = data.get("fitas_aprovar")
    estado_inicial = data.get("estado_inicial")
    fitas_reprovar = data.get("fitas_reprovar")
    estados_finais = data.get("estados_finais")

    print("\nPalavras a aprovar\n")
    for fita in fitas_aprovar:
        ap = AP(fita, estados, estado_inicial,
                estados_finais, movimento_vazio, coringa)
        print("\nFita a ser testada: " + fita + "\n")
        while ap.executar_operacao():
            print("Pilha: " + str(ap.pilha) + "\nFita atual: " + ap.fita + "\nEstado atual: " + ap.estado_atual + "\n")
            # print(ap)
        if len(ap.fita) == 0 and len(ap.pilha) == 0 and ap.estado_atual in ap.estados_finais:
            print(f"Fita aprovada: {fita}")
        else:
            print(f"Erro fita: {fita}")

    print("\nPalavras a reprovar\n")
    for fita in fitas_reprovar:
        ap = AP(fita, estados, estado_inicial,
                estados_finais, movimento_vazio, coringa)
        print("\nFita a ser testada: " + fita + "\n")
        while ap.executar_operacao():
            print("Pilha: " + str(ap.pilha) + "\nFita atual: " + ap.fita + "\nEstado atual: " + ap.estado_atual + "\n")
            # print(ap)
        if len(ap.fita) != 0 or len(ap.pilha) != 0 or not ap.estado_atual in ap.estados_finais:
            print(f"Fita reprovada: {fita}")
        else:
            print(f"Erro fita: {fita}")
