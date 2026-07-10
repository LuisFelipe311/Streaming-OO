import customtkinter as ctk

from streaming.Models import PlanoAssinatura, Usuario

from . import tema


class JanelaUsuarios(ctk.CTkToplevel):
    def __init__(self, principal):
        super().__init__(principal)
        self.principal = principal
        self.servico = principal.servico

        self.title("StreamFlix — Usuários")
        self.geometry("420x520")
        self.configure(fg_color=tema.BG_JANELA)
        self.transient(principal)

        self._montar_widgets()
        self._atualizar_lista()

    def _montar_widgets(self) -> None:
        ctk.CTkLabel(
            self, text="Usuários", font=tema.FONTE_TITULO, text_color=tema.TEXTO_PRINCIPAL
        ).pack(pady=(20, 10))

        self.lista = ctk.CTkScrollableFrame(self, fg_color=tema.BG_CAMPO, corner_radius=10)
        self.lista.pack(padx=20, fill="both", expand=True)

        rodape = ctk.CTkFrame(self, fg_color="transparent")
        rodape.pack(padx=20, pady=16, fill="x")
        tema.botao_primario(rodape, "Novo usuário", self._abrir_formulario_novo).pack(fill="x")

    def _atualizar_lista(self) -> None:
        for widget in self.lista.winfo_children():
            widget.destroy()

        if not self.servico.usuarios:
            ctk.CTkLabel(
                self.lista,
                text="Nenhum usuário cadastrado ainda.",
                text_color=tema.TEXTO_SECUNDARIO,
                font=tema.FONTE_LABEL,
            ).pack(pady=20)
            return

        for usuario in self.servico.usuarios:
            self._criar_linha(usuario)

    def _criar_linha(self, usuario: Usuario) -> None:
        linha = ctk.CTkFrame(self.lista, fg_color=tema.BG_JANELA, corner_radius=8)
        linha.pack(fill="x", pady=6, padx=6)

        info = ctk.CTkFrame(linha, fg_color="transparent")
        info.pack(side="left", padx=12, pady=10, fill="x", expand=True)

        destaque = " (atual)" if usuario is self.principal.usuario_atual else ""
        ctk.CTkLabel(
            info,
            text=f"{usuario.nome}{destaque}",
            font=tema.FONTE_LABEL_NEGRITO,
            text_color=tema.TEXTO_PRINCIPAL,
            anchor="w",
        ).pack(fill="x")
        ctk.CTkLabel(
            info,
            text=f"{usuario.email} · {usuario.assinatura.plano.value}",
            font=tema.FONTE_PEQUENA,
            text_color=tema.TEXTO_SECUNDARIO,
            anchor="w",
        ).pack(fill="x")

        botoes = ctk.CTkFrame(linha, fg_color="transparent")
        botoes.pack(side="right", padx=12)
        tema.botao_primario(
            botoes, "Selecionar", lambda u=usuario: self._selecionar(u), width=100
        ).pack(pady=2)
        tema.botao_secundario(
            botoes, "Alterar plano", lambda u=usuario: self._abrir_alterar_plano(u), width=100
        ).pack(pady=2)

    def _selecionar(self, usuario: Usuario) -> None:
        self.principal.definir_usuario_atual(usuario)
        self._atualizar_lista()

    def _abrir_formulario_novo(self) -> None:
        formulario = tema.nova_janela(self, "Novo usuário", 340, 380)

        tema.rotulo_campo(formulario, "Nome").pack(fill="x", padx=24, pady=(24, 4))
        campo_nome = tema.campo_entrada(formulario, "Nome completo")
        campo_nome.pack(fill="x", padx=24)

        tema.rotulo_campo(formulario, "E-mail").pack(fill="x", padx=24, pady=(16, 4))
        campo_email = tema.campo_entrada(formulario, "voce@email.com")
        campo_email.pack(fill="x", padx=24)

        tema.rotulo_campo(formulario, "Gênero favorito").pack(fill="x", padx=24, pady=(16, 4))
        campo_genero = tema.campo_entrada(formulario, "Ex: Ficção")
        campo_genero.pack(fill="x", padx=24)

        label_erro = tema.rotulo_erro(formulario)

        def salvar() -> None:
            nome = campo_nome.get().strip()
            email = campo_email.get().strip()
            genero = campo_genero.get().strip()
            if not nome or not email:
                label_erro.configure(text="Nome e e-mail são obrigatórios.")
                return
            try:
                usuario = Usuario(nome, email, genero)
                self.servico.cadastrar_usuario(usuario)
            except Exception as erro:
                label_erro.configure(text=f"Não foi possível cadastrar: {erro}")
                return
            formulario.destroy()
            self._atualizar_lista()

        tema.botao_primario(formulario, "Cadastrar", salvar).pack(fill="x", padx=24, pady=24)

    def _abrir_alterar_plano(self, usuario: Usuario) -> None:
        janela = tema.nova_janela(self, f"Plano de {usuario.nome}", 300, 220)

        ctk.CTkLabel(
            janela,
            text=f"Plano de {usuario.nome}",
            font=tema.FONTE_LABEL_NEGRITO,
            text_color=tema.TEXTO_PRINCIPAL,
        ).pack(pady=(24, 12))

        opcoes = [plano.name for plano in PlanoAssinatura]
        menu = tema.menu_opcoes(janela, opcoes)
        menu.set(usuario.assinatura.plano.name)
        menu.pack(padx=24, fill="x")

        def confirmar() -> None:
            self.servico.assinar_plano(usuario, PlanoAssinatura[menu.get()])
            janela.destroy()
            self._atualizar_lista()

        tema.botao_primario(janela, "Confirmar", confirmar).pack(padx=24, pady=24, fill="x")
