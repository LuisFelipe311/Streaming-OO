import random

from .conteudo import Conteudo, Episodio, Serie
from .repositorio import RepositorioStreaming
from .usuario import PlanoAssinatura, Usuario


class MotorDeRecomendacao:
   
    def recomendar(
        self, usuario: Usuario, catalogo: list[Conteudo], quantidade: int = 3
    ) -> list[Conteudo]:
        candidatos = [c for c in catalogo if c.genero == usuario.genero_favorito]
        if not candidatos:
            candidatos = list(catalogo)
        random.shuffle(candidatos)
        return candidatos[:quantidade]


class ServicoStreaming:
    def __init__(self, nome: str, caminho_banco: str = "streamflix.db"):
        self.nome = nome
        self._catalogo: list[Conteudo] = []  # composição
        self._usuarios: list[Usuario] = []
        self.repositorio = RepositorioStreaming(caminho_banco)  # composição

    # ---------- catálogo e usuários ----------

    def adicionar_conteudo(self, conteudo: Conteudo) -> None:
        self._catalogo.append(conteudo)
        self.repositorio.salvar_conteudo(conteudo)

    def cadastrar_usuario(self, usuario: Usuario) -> None:
        self._usuarios.append(usuario)
        self.repositorio.salvar_usuario(usuario)

    def adicionar_episodio(self, serie: Serie, episodio: Episodio) -> None:
        serie.adicionar_episodio(episodio)
        self.repositorio.salvar_episodio(serie.id, episodio)

    @property
    def catalogo(self) -> tuple:
        return tuple(self._catalogo)

    @property
    def usuarios(self) -> tuple:
        return tuple(self._usuarios)

    # ---------- assinatura e favoritos (persistidos) ----------

    def assinar_plano(self, usuario: Usuario, plano: PlanoAssinatura) -> None:
        usuario.assinar(plano)
        self.repositorio.atualizar_plano(usuario)

    def favoritar(self, usuario: Usuario, conteudo: Conteudo) -> None:
        usuario.favoritos.adicionar(conteudo)
        self.repositorio.adicionar_favorito(usuario.id, conteudo.id)

    def desfavoritar(self, usuario: Usuario, conteudo: Conteudo) -> None:
        usuario.favoritos.remover(conteudo)
        self.repositorio.remover_favorito(usuario.id, conteudo.id)

    # ---------- recomendação e reprodução ----------

    def recomendar_para(self, usuario: Usuario, quantidade: int = 3) -> list[Conteudo]:
        motor = MotorDeRecomendacao()  # dependência: criada e usada localmente
        return motor.recomendar(usuario, self._catalogo, quantidade)

    def reproduzir_para(self, usuario: Usuario, conteudo: Conteudo) -> str:
        resultado = conteudo.reproduzir()  # polimorfismo em ação
        if isinstance(conteudo, Serie):
            for episodio in conteudo.episodios:
                if episodio.assistido:
                    self.repositorio.atualizar_episodio(episodio)
        return resultado

    # ---------- persistência ----------

    def carregar_dados_persistidos(self) -> None:
    
        self._catalogo = self.repositorio.carregar_catalogo()
        self._usuarios = self.repositorio.carregar_usuarios()
        conteudo_por_id = {conteudo.id: conteudo for conteudo in self._catalogo}
        for usuario in self._usuarios:
            for conteudo_id in self.repositorio.carregar_favoritos_ids(usuario.id):
                conteudo = conteudo_por_id.get(conteudo_id)
                if conteudo is not None:
                    usuario.favoritos.adicionar(conteudo)
