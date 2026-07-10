"""Janela principal (hub) da interface gráfica do StreamFlix — nível 4."""

import customtkinter as ctk

from . import tema
from .janela_catalogo import JanelaCatalogo
from .janela_favoritos import JanelaFavoritos
from .janela_recomendacoes import JanelaRecomendacoes
from .janela_usuarios import JanelaUsuarios


class JanelaPrincipal(ctk.CTk):
    """Janela raiz: mostra o usuário atual e dá acesso às demais janelas."""

    def __init__(self, servico):
        super().__init__()
        self.servico = servico
        self.usuario_atual = None

        self.title("StreamFlix")
        self.geometry("420x480")
        self.configure(fg_color=tema.BG_JANELA)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self._ao_fechar)

        self._montar_widgets()

    def _montar_widgets(self) -> None:
        ctk.CTkLabel(
            self, text="StreamFlix", font=tema.FONTE_TITULO, text_color=tema.TEXTO_PRINCIPAL
        ).pack(pady=(30, 4))

        self.label_usuario = ctk.CTkLabel(
            self,
            text="Nenhum usuário selecionado",
            font=tema.FONTE_SUBTITULO,
            text_color=tema.TEXTO_SECUNDARIO,
        )
        self.label_usuario.pack(pady=(0, 24))

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(padx=40, fill="x")

        acoes = (
            ("Usuários", self.abrir_usuarios),
            ("Catálogo", self.abrir_catalogo),
            ("Favoritos", self.abrir_favoritos),
            ("Recomendações", self.abrir_recomendacoes),
        )
        for texto, comando in acoes:
            tema.botao_primario(container, texto, comando).pack(fill="x", pady=6)

        tema.botao_secundario(self, "Sair", self._ao_fechar).pack(
            side="bottom", pady=24, padx=40, fill="x"
        )

    def definir_usuario_atual(self, usuario) -> None:
        self.usuario_atual = usuario
        self.label_usuario.configure(text=f"Usuário atual: {usuario.nome}")

    def abrir_usuarios(self) -> None:
        JanelaUsuarios(self)

    def abrir_catalogo(self) -> None:
        if self._exigir_usuario():
            JanelaCatalogo(self)

    def abrir_favoritos(self) -> None:
        if self._exigir_usuario():
            JanelaFavoritos(self)

    def abrir_recomendacoes(self) -> None:
        if self._exigir_usuario():
            JanelaRecomendacoes(self)

    def _exigir_usuario(self) -> bool:
        if self.usuario_atual is None:
            tema.mostrar_aviso(self, "Selecione um usuário primeiro, na janela Usuários.")
            return False
        return True

    def _ao_fechar(self) -> None:
        self.servico.repositorio.fechar()
        self.destroy()
