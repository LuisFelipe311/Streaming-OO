from enum import Enum

from .conteudo import Conteudo


class PlanoAssinatura(Enum):
    FREE = "Free"
    STANDARD = "Standard"
    PREMIUM = "Premium"


class Assinatura:
  

    _PRECOS = {
        PlanoAssinatura.FREE: 0.0,
        PlanoAssinatura.STANDARD: 29.90,
        PlanoAssinatura.PREMIUM: 49.90,
    }

    def __init__(self, plano: PlanoAssinatura = PlanoAssinatura.FREE):
        self.plano = plano

    @property
    def preco_mensal(self) -> float:
        return self._PRECOS[self.plano]

    def __repr__(self) -> str:
        return f"<Assinatura {self.plano.value} (R$ {self.preco_mensal:.2f})>"


class ListaFavoritos:
    

    def __init__(self):
        self._itens: list[Conteudo] = []

    def adicionar(self, conteudo: Conteudo) -> None:
        if conteudo not in self._itens:
            self._itens.append(conteudo)

    def remover(self, conteudo: Conteudo) -> None:
        if conteudo in self._itens:
            self._itens.remove(conteudo)

    def listar(self) -> tuple:
        return tuple(self._itens)


class Usuario:
    def __init__(self, nome: str, email: str, genero_favorito: str):
        self.id: int | None = None  # preenchido pelo RepositorioStreaming ao salvar
        self.nome = nome
        self.email = email
        self.genero_favorito = genero_favorito
        self.favoritos = ListaFavoritos()  # composição
        self.assinatura = Assinatura()  # associação

    def assinar(self, plano: PlanoAssinatura) -> None:
        self.assinatura = Assinatura(plano)

    def __repr__(self) -> str:
        return f"<Usuario {self.nome}>"
