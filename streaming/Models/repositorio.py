"""Persistência do StreamFlix em SQLite — Nível 3 (Desk App III).

Relação demonstrada neste arquivo:
- COMPOSIÇÃO: ServicoStreaming "possui" um RepositorioStreaming — o
  repositório é criado pelo próprio serviço, no construtor, e não existe
  com propósito próprio fora dele.

Usa só a biblioteca padrão do Python (sqlite3), sem dependências externas.
"""

import sqlite3

from .conteudo import Conteudo, Documentario, Episodio, Filme, Serie
from .usuario import PlanoAssinatura, Usuario

_SCHEMA = """
CREATE TABLE IF NOT EXISTS conteudo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    titulo TEXT NOT NULL,
    ano INTEGER NOT NULL,
    genero TEXT NOT NULL,
    avaliacao REAL NOT NULL,
    duracao_minutos INTEGER,
    diretor TEXT
);

CREATE TABLE IF NOT EXISTS episodio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conteudo_id INTEGER NOT NULL REFERENCES conteudo(id),
    numero INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    duracao_minutos INTEGER NOT NULL,
    assistido INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    genero_favorito TEXT NOT NULL,
    plano TEXT NOT NULL DEFAULT 'Free'
);

CREATE TABLE IF NOT EXISTS favorito (
    usuario_id INTEGER NOT NULL REFERENCES usuario(id),
    conteudo_id INTEGER NOT NULL REFERENCES conteudo(id),
    PRIMARY KEY (usuario_id, conteudo_id)
);
"""


class RepositorioStreaming:
    """Camada de persistência: converte objetos do domínio em linhas de
    banco de dados e vice-versa. Quem usa o serviço não precisa saber SQL."""

    def __init__(self, caminho_banco: str = "streamflix.db"):
        self.conexao = sqlite3.connect(caminho_banco)
        self.conexao.row_factory = sqlite3.Row
        self.conexao.execute("PRAGMA foreign_keys = ON")
        self.conexao.executescript(_SCHEMA)
        self.conexao.commit()

    def salvar_conteudo(self, conteudo: Conteudo) -> int:
        tipo = type(conteudo).__name__
        duracao = getattr(conteudo, "duracao_minutos", None)
        diretor = getattr(conteudo, "diretor", None)
        cursor = self.conexao.execute(
            "INSERT INTO conteudo (tipo, titulo, ano, genero, avaliacao, duracao_minutos, diretor) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (tipo, conteudo.titulo, conteudo.ano, conteudo.genero, conteudo.avaliacao, duracao, diretor),
        )
        self.conexao.commit()
        conteudo.id = cursor.lastrowid
        if isinstance(conteudo, Serie):
            for episodio in conteudo.episodios:
                self.salvar_episodio(conteudo.id, episodio)
        return conteudo.id

    def salvar_episodio(self, conteudo_id: int, episodio: Episodio) -> int:
        cursor = self.conexao.execute(
            "INSERT INTO episodio (conteudo_id, numero, titulo, duracao_minutos, assistido) "
            "VALUES (?, ?, ?, ?, ?)",
            (conteudo_id, episodio.numero, episodio.titulo, episodio.duracao_minutos, int(episodio.assistido)),
        )
        self.conexao.commit()
        episodio.id = cursor.lastrowid
        return episodio.id

    def atualizar_episodio(self, episodio: Episodio) -> None:
        self.conexao.execute(
            "UPDATE episodio SET assistido = ? WHERE id = ?",
            (int(episodio.assistido), episodio.id),
        )
        self.conexao.commit()

    def carregar_catalogo(self) -> list[Conteudo]:
        catalogo: list[Conteudo] = []
        linhas = self.conexao.execute("SELECT * FROM conteudo ORDER BY id").fetchall()
        for linha in linhas:
            if linha["tipo"] == "Filme":
                conteudo = Filme(
                    linha["titulo"], linha["ano"], linha["genero"], linha["avaliacao"], linha["duracao_minutos"]
                )
            elif linha["tipo"] == "Documentario":
                conteudo = Documentario(
                    linha["titulo"], linha["ano"], linha["genero"], linha["avaliacao"], linha["diretor"]
                )
            elif linha["tipo"] == "Serie":
                conteudo = Serie(linha["titulo"], linha["ano"], linha["genero"], linha["avaliacao"])
                episodios = self.conexao.execute(
                    "SELECT * FROM episodio WHERE conteudo_id = ? ORDER BY numero", (linha["id"],)
                ).fetchall()
                for ep in episodios:
                    episodio = Episodio(ep["numero"], ep["titulo"], ep["duracao_minutos"])
                    episodio.assistido = bool(ep["assistido"])
                    episodio.id = ep["id"]
                    conteudo.adicionar_episodio(episodio)
            else:
                continue
            conteudo.id = linha["id"]
            catalogo.append(conteudo)
        return catalogo

    def salvar_usuario(self, usuario: Usuario) -> int:
        cursor = self.conexao.execute(
            "INSERT INTO usuario (nome, email, genero_favorito, plano) VALUES (?, ?, ?, ?)",
            (usuario.nome, usuario.email, usuario.genero_favorito, usuario.assinatura.plano.value),
        )
        self.conexao.commit()
        usuario.id = cursor.lastrowid
        return usuario.id

    def atualizar_plano(self, usuario: Usuario) -> None:
        self.conexao.execute(
            "UPDATE usuario SET plano = ? WHERE id = ?",
            (usuario.assinatura.plano.value, usuario.id),
        )
        self.conexao.commit()

    def carregar_usuarios(self) -> list[Usuario]:
        usuarios: list[Usuario] = []
        linhas = self.conexao.execute("SELECT * FROM usuario ORDER BY id").fetchall()
        for linha in linhas:
            usuario = Usuario(linha["nome"], linha["email"], linha["genero_favorito"])
            usuario.assinar(PlanoAssinatura(linha["plano"]))
            usuario.id = linha["id"]
            usuarios.append(usuario)
        return usuarios

    def adicionar_favorito(self, usuario_id: int, conteudo_id: int) -> None:
        self.conexao.execute(
            "INSERT OR IGNORE INTO favorito (usuario_id, conteudo_id) VALUES (?, ?)",
            (usuario_id, conteudo_id),
        )
        self.conexao.commit()

    def remover_favorito(self, usuario_id: int, conteudo_id: int) -> None:
        self.conexao.execute(
            "DELETE FROM favorito WHERE usuario_id = ? AND conteudo_id = ?",
            (usuario_id, conteudo_id),
        )
        self.conexao.commit()

    def carregar_favoritos_ids(self, usuario_id: int) -> list[int]:
        linhas = self.conexao.execute(
            "SELECT conteudo_id FROM favorito WHERE usuario_id = ?", (usuario_id,)
        ).fetchall()
        return [linha["conteudo_id"] for linha in linhas]

    def fechar(self) -> None:
        self.conexao.close()
