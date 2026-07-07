import unittest

from streamflix.models import Documentario, Episodio, Filme, Serie


class TestHerancaEPolimorfismo(unittest.TestCase):
    def test_filme_reproduzir(self):
        filme = Filme("Interestelar", 2014, "Ficção", 9.1, 169)
        self.assertIn("Interestelar", filme.reproduzir())
        self.assertIn("169 min", filme.reproduzir())

    def test_documentario_reproduzir_e_informacoes(self):
        doc = Documentario("Cosmos", 2019, "Ficção", 8.7, "Ann Druyan")
        self.assertIn("Cosmos", doc.reproduzir())
        self.assertIn("Ann Druyan", doc.exibir_informacoes())

    def test_polimorfismo_reproduzir_varia_por_subclasse(self):
        filme = Filme("A", 2020, "Drama", 8.0, 100)
        doc = Documentario("B", 2020, "Drama", 8.0, "Diretor X")
        # mesmo método .reproduzir(), comportamento diferente por classe
        self.assertNotEqual(type(filme.reproduzir()), None)
        self.assertNotIn("dirigido por", filme.reproduzir())
        self.assertIn("documentário", doc.reproduzir())


class TestComposicaoSerieEpisodio(unittest.TestCase):
    def setUp(self):
        self.serie = Serie("Dark", 2017, "Ficção", 9.0)
        self.serie.adicionar_episodio(Episodio(1, "Secretos", 55))
        self.serie.adicionar_episodio(Episodio(2, "Mentiras", 51))

    def test_episodios_pertencem_a_serie(self):
        self.assertEqual(len(self.serie.episodios), 2)

    def test_reproduzir_avanca_episodio_nao_assistido(self):
        primeira = self.serie.reproduzir()
        self.assertIn("Secretos", primeira)
        self.assertTrue(self.serie.episodios[0].assistido)

        segunda = self.serie.reproduzir()
        self.assertIn("Mentiras", segunda)

    def test_reproduzir_quando_todos_assistidos(self):
        self.serie.reproduzir()
        self.serie.reproduzir()
        resultado = self.serie.reproduzir()
        self.assertIn("Não há episódios pendentes", resultado)


if __name__ == "__main__":
    unittest.main()