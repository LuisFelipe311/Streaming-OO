import unittest

from streaming.Models import Documentario, Filme, ServicoStreaming, Usuario


class TestServicoStreaming(unittest.TestCase):
    def setUp(self):
        self.servico = ServicoStreaming("StreamFlix")
        self.filme = Filme("Interestelar", 2014, "Ficção", 9.1, 169)
        self.doc = Documentario("Cosmos", 2019, "Ficção", 8.7, "Ann Druyan")
        self.servico.adicionar_conteudo(self.filme)
        self.servico.adicionar_conteudo(self.doc)
        self.usuario = Usuario("Luis", "luis@example.com", genero_favorito="Ficção")
        self.servico.cadastrar_usuario(self.usuario)

    def test_catalogo_guarda_conteudo_adicionado(self):
        self.assertEqual(len(self.servico.catalogo), 2)

    def test_reproduzir_para_delega_polimorficamente(self):
        resultado = self.servico.reproduzir_para(self.usuario, self.filme)
        self.assertIn("Interestelar", resultado)

    def test_recomendar_para_usa_motor_de_recomendacao(self):
        recomendados = self.servico.recomendar_para(self.usuario, quantidade=1)
        self.assertEqual(len(recomendados), 1)
        self.assertIn(recomendados[0].genero, ("Ficção",))

    def test_recomendar_sem_genero_compativel_retorna_algo_do_catalogo(self):
        usuario_comedia = Usuario("Ana", "ana@example.com", genero_favorito="Comédia")
        recomendados = self.servico.recomendar_para(usuario_comedia, quantidade=2)
        self.assertEqual(len(recomendados), 2)


if __name__ == "__main__":
    unittest.main()