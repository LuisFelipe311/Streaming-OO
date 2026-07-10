"""Usuario, sua lista de favoritos e sua assinatura.

Relações demonstradas neste arquivo:
- COMPOSIÇÃO: Usuario "possui" ListaFavoritos — a lista não existe sem o usuário.
- ASSOCIAÇÃO: Usuario está associado a uma Assinatura (a assinatura tem sentido
  próprio, pode ser trocada/consultada, não é "parte" do usuário).
- ASSOCIAÇÃO: ListaFavoritos referencia objetos Conteudo que pertencem ao
  catálogo (ela não é dona deles, só aponta para eles).
"""

from enum import Enum

from .conteudo import Conteudo


class PlanoAssinatura(Enum):
    FREE = "Free"
    STANDARD = "Standard"
    PREMIUM = "Premium"


class Assinatura:
    """Existe de forma independente do Usuario -> relação de ASSOCIAÇÃO."""

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
    """Pertence a um único Usuario (COMPOSIÇÃO), mas apenas referencia os
    Conteudo favoritados, que existem de forma independente no catálogo
    (ASSOCIAÇÃO)."""

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
        self.id: int | None = None
        self.nome = nome
        self.email = email
        self.genero_favorito = genero_favorito
        self.favoritos = ListaFavoritos()
        self.assinatura = Assinatura()

    def assinar(self, plano: PlanoAssinatura) -> None:
        self.assinatura = Assinatura(plano)

    def __repr__(self) -> str:
        return f"<Usuario {self.nome}>"
