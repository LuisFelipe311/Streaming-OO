"""Janela de catálogo: listar conteúdo, favoritar/desfavoritar, reproduzir,
e cadastrar filmes, séries (com episódios) e documentários."""

import customtkinter as ctk

from streaming.Models import Documentario, Episodio, Filme, Serie

from . import tema


class JanelaCatalogo(ctk.CTkToplevel):
    def __init__(self, principal):
        super().__init__(principal)
        self.principal = principal
        self.servico = principal.servico

        self.title("StreamFlix — Catálogo")
        self.geometry("460x580")
        self.configure(fg_color=tema.BG_JANELA)
        self.transient(principal)

        self._montar_widgets()
        self._atualizar_lista()

    def _montar_widgets(self) -> None:
        ctk.CTkLabel(
            self, text="Catálogo", font=tema.FONTE_TITULO, text_color=tema.TEXTO_PRINCIPAL
        ).pack(pady=(20, 10))

        self.lista = ctk.CTkScrollableFrame(self, fg_color=tema.BG_CAMPO, corner_radius=10)
        self.lista.pack(padx=20, fill="both", expand=True)

        linha1 = ctk.CTkFrame(self, fg_color="transparent")
        linha1.pack(padx=20, pady=(16, 6), fill="x")
        linha1.grid_columnconfigure((0, 1, 2), weight=1)
        tema.botao_primario(linha1, "+ Filme", self._abrir_formulario_filme).grid(
            row=0, column=0, padx=4, sticky="ew"
        )
        tema.botao_primario(linha1, "+ Série", self._abrir_formulario_serie).grid(
            row=0, column=1, padx=4, sticky="ew"
        )
        tema.botao_primario(linha1, "+ Documentário", self._abrir_formulario_documentario).grid(
            row=0, column=2, padx=4, sticky="ew"
        )

        linha2 = ctk.CTkFrame(self, fg_color="transparent")
        linha2.pack(padx=20, pady=(0, 16), fill="x")
        tema.botao_secundario(linha2, "+ Episódio em série existente", self._abrir_formulario_episodio).pack(
            fill="x"
        )

    def _atualizar_lista(self) -> None:
        for widget in self.lista.winfo_children():
            widget.destroy()

        if not self.servico.catalogo:
            ctk.CTkLabel(
                self.lista, text="Catálogo vazio.", text_color=tema.TEXTO_SECUNDARIO, font=tema.FONTE_LABEL
            ).pack(pady=20)
            return

        for conteudo in self.servico.catalogo:
            self._criar_linha(conteudo)

    def _criar_linha(self, conteudo) -> None:
        usuario = self.principal.usuario_atual
        e_favorito = usuario is not None and conteudo in usuario.favoritos.listar()

        linha = ctk.CTkFrame(self.lista, fg_color=tema.BG_JANELA, corner_radius=8)
        linha.pack(fill="x", pady=6, padx=6)

        info = ctk.CTkFrame(linha, fg_color="transparent")
        info.pack(side="left", padx=12, pady=10, fill="x", expand=True)
        tipo = type(conteudo).__name__
        ctk.CTkLabel(
            info, text=conteudo.titulo, font=tema.FONTE_LABEL_NEGRITO, text_color=tema.TEXTO_PRINCIPAL, anchor="w"
        ).pack(fill="x")
        ctk.CTkLabel(
            info,
            text=f"{tipo} · {conteudo.ano} · {conteudo.genero}",
            font=tema.FONTE_PEQUENA,
            text_color=tema.TEXTO_SECUNDARIO,
            anchor="w",
        ).pack(fill="x")

        botoes = ctk.CTkFrame(linha, fg_color="transparent")
        botoes.pack(side="right", padx=12)

        cor_coracao = tema.DESTAQUE if e_favorito else tema.BG_CAMPO
        cor_texto_coracao = tema.TEXTO_SOBRE_DESTAQUE if e_favorito else tema.DESTAQUE
        ctk.CTkButton(
            botoes,
            text="♥",
            width=36,
            height=28,
            corner_radius=7,
            fg_color=cor_coracao,
            hover_color=tema.DESTAQUE_HOVER,
            text_color=cor_texto_coracao,
            font=("Segoe UI", 13),
            command=lambda c=conteudo: self._alternar_favorito(c),
        ).pack(side="left", padx=(0, 6))

        tema.botao_secundario(
            botoes, "Reproduzir", lambda c=conteudo: self._reproduzir(c), width=90
        ).pack(side="left")

    def _alternar_favorito(self, conteudo) -> None:
        usuario = self.principal.usuario_atual
        if usuario is None:
            tema.mostrar_aviso(self, "Selecione um usuário primeiro, na janela Usuários.")
            return
        if conteudo in usuario.favoritos.listar():
            self.servico.desfavoritar(usuario, conteudo)
        else:
            self.servico.favoritar(usuario, conteudo)
        self._atualizar_lista()

    def _reproduzir(self, conteudo) -> None:
        usuario = self.principal.usuario_atual
        if usuario is None:
            tema.mostrar_aviso(self, "Selecione um usuário primeiro, na janela Usuários.")
            return
        resultado = self.servico.reproduzir_para(usuario, conteudo)
        tema.mostrar_aviso(self, resultado, titulo="Reproduzindo")

    def _campos_basicos(self, formulario):
        tema.rotulo_campo(formulario, "Título").pack(fill="x", padx=24, pady=(24, 4))
        campo_titulo = tema.campo_entrada(formulario, "Título")
        campo_titulo.pack(fill="x", padx=24)

        tema.rotulo_campo(formulario, "Ano").pack(fill="x", padx=24, pady=(16, 4))
        campo_ano = tema.campo_entrada(formulario, "Ex: 2024")
        campo_ano.pack(fill="x", padx=24)

        tema.rotulo_campo(formulario, "Gênero").pack(fill="x", padx=24, pady=(16, 4))
        campo_genero = tema.campo_entrada(formulario, "Ex: Ficção")
        campo_genero.pack(fill="x", padx=24)

        tema.rotulo_campo(formulario, "Avaliação (0 a 10)").pack(fill="x", padx=24, pady=(16, 4))
        campo_avaliacao = tema.campo_entrada(formulario, "Ex: 8.5")
        campo_avaliacao.pack(fill="x", padx=24)

        return campo_titulo, campo_ano, campo_genero, campo_avaliacao

    def _ler_campos_basicos(self, campos, label_erro):
        campo_titulo, campo_ano, campo_genero, campo_avaliacao = campos
        titulo = campo_titulo.get().strip()
        genero = campo_genero.get().strip()
        if not titulo or not genero:
            label_erro.configure(text="Título e gênero são obrigatórios.")
            return None
        try:
            ano = int(campo_ano.get().strip())
            avaliacao = float(campo_avaliacao.get().strip())
        except ValueError:
            label_erro.configure(text="Ano precisa ser inteiro e avaliação precisa ser um número.")
            return None
        return titulo, ano, genero, avaliacao

    def _abrir_formulario_filme(self) -> None:
        formulario = tema.nova_janela(self, "Novo filme", 340, 480)
        campos = self._campos_basicos(formulario)

        tema.rotulo_campo(formulario, "Duração (minutos)").pack(fill="x", padx=24, pady=(16, 4))
        campo_duracao = tema.campo_entrada(formulario, "Ex: 120")
        campo_duracao.pack(fill="x", padx=24)

        label_erro = tema.rotulo_erro(formulario)

        def salvar() -> None:
            dados = self._ler_campos_basicos(campos, label_erro)
            if dados is None:
                return
            titulo, ano, genero, avaliacao = dados
            try:
                duracao = int(campo_duracao.get().strip())
            except ValueError:
                label_erro.configure(text="Duração precisa ser um número inteiro de minutos.")
                return
            filme = Filme(titulo, ano, genero, avaliacao, duracao)
            self.servico.adicionar_conteudo(filme)
            formulario.destroy()
            self._atualizar_lista()

        tema.botao_primario(formulario, "Adicionar", salvar).pack(fill="x", padx=24, pady=24)

    def _abrir_formulario_documentario(self) -> None:
        formulario = tema.nova_janela(self, "Novo documentário", 340, 480)
        campos = self._campos_basicos(formulario)

        tema.rotulo_campo(formulario, "Diretor").pack(fill="x", padx=24, pady=(16, 4))
        campo_diretor = tema.campo_entrada(formulario, "Ex: Ann Druyan")
        campo_diretor.pack(fill="x", padx=24)

        label_erro = tema.rotulo_erro(formulario)

        def salvar() -> None:
            dados = self._ler_campos_basicos(campos, label_erro)
            if dados is None:
                return
            titulo, ano, genero, avaliacao = dados
            diretor = campo_diretor.get().strip()
            if not diretor:
                label_erro.configure(text="Informe o diretor.")
                return
            doc = Documentario(titulo, ano, genero, avaliacao, diretor)
            self.servico.adicionar_conteudo(doc)
            formulario.destroy()
            self._atualizar_lista()

        tema.botao_primario(formulario, "Adicionar", salvar).pack(fill="x", padx=24, pady=24)

    def _abrir_formulario_serie(self) -> None:
        formulario = tema.nova_janela(self, "Nova série", 340, 440)
        campos = self._campos_basicos(formulario)

        ctk.CTkLabel(
            formulario,
            text="Você poderá adicionar episódios depois de criar a série.",
            font=tema.FONTE_PEQUENA,
            text_color=tema.TEXTO_SECUNDARIO,
            wraplength=280,
            justify="left",
        ).pack(fill="x", padx=24, pady=(6, 0))

        label_erro = tema.rotulo_erro(formulario)

        def salvar() -> None:
            dados = self._ler_campos_basicos(campos, label_erro)
            if dados is None:
                return
            titulo, ano, genero, avaliacao = dados
            serie = Serie(titulo, ano, genero, avaliacao)
            self.servico.adicionar_conteudo(serie)
            formulario.destroy()
            self._atualizar_lista()

        tema.botao_primario(formulario, "Adicionar", salvar).pack(fill="x", padx=24, pady=24)

    def _abrir_formulario_episodio(self) -> None:
        series = [c for c in self.servico.catalogo if isinstance(c, Serie)]
        if not series:
            tema.mostrar_aviso(self, "Cadastre uma série antes de adicionar episódios.")
            return

        formulario = tema.nova_janela(self, "Novo episódio", 340, 440)

        tema.rotulo_campo(formulario, "Série").pack(fill="x", padx=24, pady=(24, 4))
        nomes = [serie.titulo for serie in series]
        menu_serie = tema.menu_opcoes(formulario, nomes)
        menu_serie.set(nomes[0])
        menu_serie.pack(fill="x", padx=24)

        tema.rotulo_campo(formulario, "Número do episódio").pack(fill="x", padx=24, pady=(16, 4))
        campo_numero = tema.campo_entrada(formulario, "Ex: 1")
        campo_numero.pack(fill="x", padx=24)

        tema.rotulo_campo(formulario, "Título do episódio").pack(fill="x", padx=24, pady=(16, 4))
        campo_titulo = tema.campo_entrada(formulario, "Título")
        campo_titulo.pack(fill="x", padx=24)

        tema.rotulo_campo(formulario, "Duração (minutos)").pack(fill="x", padx=24, pady=(16, 4))
        campo_duracao = tema.campo_entrada(formulario, "Ex: 45")
        campo_duracao.pack(fill="x", padx=24)

        label_erro = tema.rotulo_erro(formulario)

        def salvar() -> None:
            titulo = campo_titulo.get().strip()
            if not titulo:
                label_erro.configure(text="Informe o título do episódio.")
                return
            try:
                numero = int(campo_numero.get().strip())
                duracao = int(campo_duracao.get().strip())
            except ValueError:
                label_erro.configure(text="Número e duração precisam ser inteiros.")
                return
            serie = next(s for s in series if s.titulo == menu_serie.get())
            episodio = Episodio(numero, titulo, duracao)
            self.servico.adicionar_episodio(serie, episodio)
            formulario.destroy()

        tema.botao_primario(formulario, "Adicionar", salvar).pack(fill="x", padx=24, pady=24)
