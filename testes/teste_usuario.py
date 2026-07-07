import unittest

from streamflix.models import Filme, PlanoAssinatura, Usuario


class TestUsuarioAssinaturaEFavoritos(unittest.TestCase):
    def setUp(self):
        self.usuario = Usuario("Luis", "luis@example.com", genero_favorito="Ficção")
        self.filme = Filme("Interestelar", 2014, "Ficção", 9.1, 169)

    def test_usuario_comeca_no_plano_free(self):
        self.assertEqual(self.usuario.assinatura.plano, PlanoAssinatura.FREE)
        self.assertEqual(self.usuario.assinatura.preco_mensal, 0.0)

    def test_assinar_troca_o_plano(self):
        self.usuario.assinar(PlanoAssinatura.PREMIUM)
        self.assertEqual(self.usuario.assinatura.plano, PlanoAssinatura.PREMIUM)
        self.assertAlmostEqual(self.usuario.assinatura.preco_mensal, 49.90)

    def test_favoritos_pertencem_ao_usuario_mas_referenciam_conteudo_externo(self):
        self.usuario.favoritos.adicionar(self.filme)
        self.assertIn(self.filme, self.usuario.favoritos.listar())

        # remover do favoritos não afeta o objeto Conteudo em si (associação, não posse)
        self.usuario.favoritos.remover(self.filme)
        self.assertNotIn(self.filme, self.usuario.favoritos.listar())
        self.assertEqual(self.filme.titulo, "Interestelar")

    def test_adicionar_duplicado_nao_repete(self):
        self.usuario.favoritos.adicionar(self.filme)
        self.usuario.favoritos.adicionar(self.filme)
        self.assertEqual(len(self.usuario.favoritos.listar()), 1)


if __name__ == "__main__":
    unittest.main()