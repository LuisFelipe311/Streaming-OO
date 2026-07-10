import customtkinter as ctk

from . import tema


class JanelaRecomendacoes(ctk.CTkToplevel):
    def __init__(self, principal):
        super().__init__(principal)
        self.principal = principal
        self.servico = principal.servico

        self.title("StreamFlix — Recomendações")
        self.geometry("420x480")
        self.configure(fg_color=tema.BG_JANELA)
        self.transient(principal)

        self._montar_widgets()

    def _montar_widgets(self) -> None:
        usuario = self.principal.usuario_atual
        ctk.CTkLabel(
            self,
            text=f"Recomendações para {usuario.nome}",
            font=tema.FONTE_TITULO,
            text_color=tema.TEXTO_PRINCIPAL,
            wraplength=380,
        ).pack(pady=(20, 10), padx=20)

        self.lista = ctk.CTkScrollableFrame(self, fg_color=tema.BG_CAMPO, corner_radius=10)
        self.lista.pack(padx=20, fill="both", expand=True)

        rodape = ctk.CTkFrame(self, fg_color="transparent")
        rodape.pack(padx=20, pady=16, fill="x")
        tema.botao_primario(rodape, "Gerar recomendações", self._gerar).pack(fill="x")

    def _gerar(self) -> None:
        for widget in self.lista.winfo_children():
            widget.destroy()

        usuario = self.principal.usuario_atual
        recomendados = self.servico.recomendar_para(usuario, quantidade=3)

        if not recomendados:
            ctk.CTkLabel(
                self.lista,
                text="Catálogo vazio — nada para recomendar ainda.",
                text_color=tema.TEXTO_SECUNDARIO,
                font=tema.FONTE_LABEL,
            ).pack(pady=20)
            return

        for conteudo in recomendados:
            linha = ctk.CTkFrame(self.lista, fg_color=tema.BG_JANELA, corner_radius=8)
            linha.pack(fill="x", pady=6, padx=6)
            info = ctk.CTkFrame(linha, fg_color="transparent")
            info.pack(padx=12, pady=10, fill="x", expand=True)
            ctk.CTkLabel(
                info,
                text=conteudo.titulo,
                font=tema.FONTE_LABEL_NEGRITO,
                text_color=tema.TEXTO_PRINCIPAL,
                anchor="w",
            ).pack(fill="x")
            ctk.CTkLabel(
                info,
                text=f"{type(conteudo).__name__} · {conteudo.ano} · {conteudo.genero}",
                font=tema.FONTE_PEQUENA,
                text_color=tema.TEXTO_SECUNDARIO,
                anchor="w",
            ).pack(fill="x")
