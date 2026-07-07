import random

from .conteudo import Conteudo
from .usuario import Usuario


class MotorDeRecomendacao:
    """Só é usada dentro de um método de ServicoStreaming -> DEPENDÊNCIA."""

    def recomendar(
        self, usuario: Usuario, catalogo: list[Conteudo], quantidade: int = 3
    ) -> list[Conteudo]:
        candidatos = [c for c in catalogo if c.genero == usuario.genero_favorito]
        if not candidatos:
            candidatos = list(catalogo)
        random.shuffle(candidatos)
        return candidatos[:quantidade]


class ServicoStreaming:
    def __init__(self, nome: str):
        self.nome = nome
        self._catalogo: list[Conteudo] = []  # composição
        self._usuarios: list[Usuario] = []

    def adicionar_conteudo(self, conteudo: Conteudo) -> None:
        self._catalogo.append(conteudo)

    def cadastrar_usuario(self, usuario: Usuario) -> None:
        self._usuarios.append(usuario)

    @property
    def catalogo(self) -> tuple:
        return tuple(self._catalogo)

    def recomendar_para(self, usuario: Usuario, quantidade: int = 3) -> list[Conteudo]:
        motor = MotorDeRecomendacao()  # dependência: criada e usada localmente
        return motor.recomendar(usuario, self._catalogo, quantidade)

    def reproduzir_para(self, usuario: Usuario, conteudo: Conteudo) -> str:
        return conteudo.reproduzir()  # polimorfismo em ação