import unittest

from streaming.Models import (
    Documentario,
    Episodio,
    Filme,
    PlanoAssinatura,
    RepositorioStreaming,
    Serie,
    ServicoStreaming,
    Usuario,
)


class TestRepositorioStreamingRoundTrip(unittest.TestCase):
    """Cada teste usa um banco SQLite em memória isolado (":memory:")."""

    def setUp(self):
        self.repo = RepositorioStreaming(":memory:")

    def test_salvar_e_carregar_filme(self):
        filme = Filme("Interestelar", 2014, "Ficção", 9.1, 169)
        self.repo.salvar_conteudo(filme)
        self.assertIsNotNone(filme.id)

        catalogo = self.repo.carregar_catalogo()
        self.assertEqual(len(catalogo), 1)
        recarregado = catalogo[0]
        self.assertIsInstance(recarregado, Filme)
        self.assertEqual(recarregado.titulo, "Interestelar")
        self.assertEqual(recarregado.duracao_minutos, 169)

    def test_salvar_e_carregar_documentario(self):
        doc = Documentario("Cosmos", 2019, "Ficção", 8.7, "Ann Druyan")
        self.repo.salvar_conteudo(doc)

        catalogo = self.repo.carregar_catalogo()
        recarregado = catalogo[0]
        self.assertIsInstance(recarregado, Documentario)
        self.assertEqual(recarregado.diretor, "Ann Druyan")

    def test_salvar_serie_persiste_episodios_e_assistido(self):
        serie = Serie("Dark", 2017, "Ficção", 9.0)
        serie.adicionar_episodio(Episodio(1, "Secretos", 55))
        serie.adicionar_episodio(Episodio(2, "Mentiras", 51))
        self.repo.salvar_conteudo(serie)

        serie.episodios[0].assistido = True
        self.repo.atualizar_episodio(serie.episodios[0])

        catalogo = self.repo.carregar_catalogo()
        recarregada = catalogo[0]
        self.assertIsInstance(recarregada, Serie)
        self.assertEqual(len(recarregada.episodios), 2)
        self.assertTrue(recarregada.episodios[0].assistido)
        self.assertFalse(recarregada.episodios[1].assistido)

    def test_salvar_e_carregar_usuario_com_plano(self):
        usuario = Usuario("Luis", "luis@example.com", "Ficção")
        usuario.assinar(PlanoAssinatura.PREMIUM)
        self.repo.salvar_usuario(usuario)

        usuarios = self.repo.carregar_usuarios()
        self.assertEqual(len(usuarios), 1)
        recarregado = usuarios[0]
        self.assertEqual(recarregado.nome, "Luis")
        self.assertEqual(recarregado.assinatura.plano, PlanoAssinatura.PREMIUM)

    def test_favoritos_persistem_e_podem_ser_removidos(self):
        filme = Filme("Interestelar", 2014, "Ficção", 9.1, 169)
        self.repo.salvar_conteudo(filme)
        usuario = Usuario("Luis", "luis@example.com", "Ficção")
        self.repo.salvar_usuario(usuario)

        self.repo.adicionar_favorito(usuario.id, filme.id)
        self.assertEqual(self.repo.carregar_favoritos_ids(usuario.id), [filme.id])

        self.repo.remover_favorito(usuario.id, filme.id)
        self.assertEqual(self.repo.carregar_favoritos_ids(usuario.id), [])

    def test_email_duplicado_gera_erro_de_integridade(self):
        import sqlite3

        self.repo.salvar_usuario(Usuario("Luis", "luis@example.com", "Ficção"))
        with self.assertRaises(sqlite3.IntegrityError):
            self.repo.salvar_usuario(Usuario("Outro Luis", "luis@example.com", "Drama"))


class TestServicoStreamingPersisteEmSqlite(unittest.TestCase):
    """Testa que ServicoStreaming persiste de verdade: fecha e reabre o
    'banco' (usando um arquivo temporário) e os dados continuam lá."""

    def setUp(self):
        import os
        import tempfile

        self._arquivo_temp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self._arquivo_temp.close()
        self.caminho_banco = self._arquivo_temp.name

    def tearDown(self):
        import os

        os.unlink(self.caminho_banco)

    def test_dados_sobrevivem_a_um_novo_servico_no_mesmo_arquivo(self):
        servico1 = ServicoStreaming("StreamFlix", caminho_banco=self.caminho_banco)
        filme = Filme("Interestelar", 2014, "Ficção", 9.1, 169)
        servico1.adicionar_conteudo(filme)
        usuario = Usuario("Luis", "luis@example.com", "Ficção")
        servico1.cadastrar_usuario(usuario)
        servico1.favoritar(usuario, filme)
        servico1.repositorio.fechar()

        servico2 = ServicoStreaming("StreamFlix", caminho_banco=self.caminho_banco)
        servico2.carregar_dados_persistidos()

        self.assertEqual(len(servico2.catalogo), 1)
        self.assertEqual(servico2.catalogo[0].titulo, "Interestelar")
        self.assertEqual(len(servico2.usuarios), 1)
        usuario_recarregado = servico2.usuarios[0]
        self.assertEqual(len(usuario_recarregado.favoritos.listar()), 1)
        self.assertEqual(usuario_recarregado.favoritos.listar()[0].titulo, "Interestelar")

        servico2.repositorio.fechar()


if __name__ == "__main__":
    unittest.main()
