"""Janela de favoritos do usuário atual: listar e remover."""

import customtkinter as ctk

from . import tema


class JanelaFavoritos(ctk.CTkToplevel):
    def __init__(self, principal):
        super().__init__(principal)
        self.principal = principal
        self.servico = principal.servico

        self.title("StreamFlix — Favoritos")
        self.geometry("420x480")
        self.configure(fg_color=tema.BG_JANELA)
        self.transient(principal)

        self._montar_widgets()
        self._atualizar_lista()

    def _montar_widgets(self) -> None:
        usuario = self.principal.usuario_atual
        ctk.CTkLabel(
            self,
            text=f"Favoritos de {usuario.nome}",
            font=tema.FONTE_TITULO,
            text_color=tema.TEXTO_PRINCIPAL,
            wraplength=380,
        ).pack(pady=(20, 10), padx=20)

        self.lista = ctk.CTkScrollableFrame(self, fg_color=tema.BG_CAMPO, corner_radius=10)
        self.lista.pack(padx=20, pady=(0, 20), fill="both", expand=True)

    def _atualizar_lista(self) -> None:
        for widget in self.lista.winfo_children():
            widget.destroy()

        usuario = self.principal.usuario_atual
        favoritos = usuario.favoritos.listar()

        if not favoritos:
            ctk.CTkLabel(
                self.lista,
                text="Nenhum favorito ainda.",
                text_color=tema.TEXTO_SECUNDARIO,
                font=tema.FONTE_LABEL,
            ).pack(pady=20)
            return

        for conteudo in favoritos:
            self._criar_linha(conteudo)

    def _criar_linha(self, conteudo) -> None:
        linha = ctk.CTkFrame(self.lista, fg_color=tema.BG_JANELA, corner_radius=8)
        linha.pack(fill="x", pady=6, padx=6)

        info = ctk.CTkFrame(linha, fg_color="transparent")
        info.pack(side="left", padx=12, pady=10, fill="x", expand=True)
        ctk.CTkLabel(
            info, text=conteudo.titulo, font=tema.FONTE_LABEL_NEGRITO, text_color=tema.TEXTO_PRINCIPAL, anchor="w"
        ).pack(fill="x")
        ctk.CTkLabel(
            info,
            text=f"{type(conteudo).__name__} · {conteudo.ano}",
            font=tema.FONTE_PEQUENA,
            text_color=tema.TEXTO_SECUNDARIO,
            anchor="w",
        ).pack(fill="x")

        tema.botao_secundario(
            linha, "Remover", lambda c=conteudo: self._remover(c), width=90
        ).pack(side="right", padx=12)

    def _remover(self, conteudo) -> None:
        usuario = self.principal.usuario_atual
        self.servico.desfavoritar(usuario, conteudo)
        self._atualizar_lista()
