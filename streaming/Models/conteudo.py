"""Hierarquia de conteúdo do catálogo: Conteudo (superclasse) -> Filme, Serie, Documentario.

Relações demonstradas neste arquivo:
- HERANÇA: Filme, Serie e Documentario herdam de Conteudo.
- POLIMORFISMO: cada subclasse implementa reproduzir() de um jeito diferente.
- COMPOSIÇÃO: Serie "possui" Episodio — um Episodio não existe fora de uma Serie.
"""

from abc import ABC, abstractmethod


class Conteudo(ABC):
    """Classe base abstrata para qualquer item do catálogo."""

    def __init__(self, titulo: str, ano: int, genero: str, avaliacao: float):
        self.id: int | None = None
        self.titulo = titulo
        self.ano = ano
        self.genero = genero
        self.avaliacao = avaliacao

    @abstractmethod
    def reproduzir(self) -> str:
        """Método polimórfico: cada subclasse decide o que significa 'reproduzir'."""
        raise NotImplementedError

    def exibir_informacoes(self) -> str:
        return f"{self.titulo} ({self.ano}) - {self.genero} - nota {self.avaliacao}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self.titulo}'>"


class Filme(Conteudo):
    def __init__(self, titulo, ano, genero, avaliacao, duracao_minutos):
        super().__init__(titulo, ano, genero, avaliacao)
        self.duracao_minutos = duracao_minutos

    def reproduzir(self) -> str:
        return f"Reproduzindo o filme '{self.titulo}' ({self.duracao_minutos} min)"


class Episodio:
    """Um Episodio só faz sentido dentro de uma Serie: relação de COMPOSIÇÃO."""

    def __init__(self, numero: int, titulo: str, duracao_minutos: int):
        self.id: int | None = None
        self.numero = numero
        self.titulo = titulo
        self.duracao_minutos = duracao_minutos
        self.assistido = False

    def __repr__(self) -> str:
        return f"<Episodio {self.numero}: {self.titulo}>"


class Serie(Conteudo):
    """Serie é composta por Episodios: eles nascem e morrem junto com a série."""

    def __init__(self, titulo, ano, genero, avaliacao):
        super().__init__(titulo, ano, genero, avaliacao)
        self._episodios: list[Episodio] = []

    def adicionar_episodio(self, episodio: Episodio) -> None:
        self._episodios.append(episodio)

    @property
    def episodios(self) -> tuple:
        return tuple(self._episodios)

    def reproduzir(self) -> str:
        proximo = next((ep for ep in self._episodios if not ep.assistido), None)
        if proximo is None:
            return f"Não há episódios pendentes em '{self.titulo}'"
        proximo.assistido = True
        return f"Reproduzindo {self.titulo} - {proximo}"


class Documentario(Conteudo):
    def __init__(self, titulo, ano, genero, avaliacao, diretor):
        super().__init__(titulo, ano, genero, avaliacao)
        self.diretor = diretor

    def reproduzir(self) -> str:
        return f"Reproduzindo o documentário '{self.titulo}', de {self.diretor}"

    def exibir_informacoes(self) -> str:
        base = super().exibir_informacoes()
        return f"{base} - dirigido por {self.diretor}"
