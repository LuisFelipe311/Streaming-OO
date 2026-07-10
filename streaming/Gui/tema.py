"""Paleta de cores e helpers de estilo compartilhados por todas as janelas
da interface gráfica (nível 4).

Estilo escolhido: "Escuro Tech" (azul/teal), decidido pelo usuário a partir
de um mockup visual comparando 3 opções.
"""

import customtkinter as ctk

# ---------- paleta ----------
BG_JANELA = "#101d29"
BG_CAMPO = "#17293a"
TEXTO_PRINCIPAL = "#eaf6f6"
TEXTO_SECUNDARIO = "#9fb6c4"
DESTAQUE = "#1fd1b8"
DESTAQUE_HOVER = "#17b39d"
TEXTO_SOBRE_DESTAQUE = "#06222a"
BORDA_SUTIL = "#2a4457"
ERRO = "#ff6b6b"

# ---------- fontes ----------
FONTE_TITULO = ("Segoe UI", 20, "bold")
FONTE_SUBTITULO = ("Segoe UI", 13)
FONTE_LABEL = ("Segoe UI", 12)
FONTE_LABEL_NEGRITO = ("Segoe UI", 13, "bold")
FONTE_BOTAO = ("Segoe UI", 13, "bold")
FONTE_BOTAO_SECUNDARIO = ("Segoe UI", 12)
FONTE_PEQUENA = ("Segoe UI", 11)


def configurar_aparencia() -> None:
    """Chamar uma única vez, antes de criar a primeira janela."""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")


def botao_primario(master, texto, comando, **extra) -> ctk.CTkButton:
    return ctk.CTkButton(
        master,
        text=texto,
        command=comando,
        fg_color=DESTAQUE,
        hover_color=DESTAQUE_HOVER,
        text_color=TEXTO_SOBRE_DESTAQUE,
        corner_radius=8,
        font=FONTE_BOTAO,
        **extra,
    )


def botao_secundario(master, texto, comando, **extra) -> ctk.CTkButton:
    return ctk.CTkButton(
        master,
        text=texto,
        command=comando,
        fg_color="transparent",
        hover_color=BG_CAMPO,
        text_color=TEXTO_SECUNDARIO,
        border_width=1,
        border_color=BORDA_SUTIL,
        corner_radius=8,
        font=FONTE_BOTAO_SECUNDARIO,
        **extra,
    )


def campo_entrada(master, placeholder="", **extra) -> ctk.CTkEntry:
    return ctk.CTkEntry(
        master,
        placeholder_text=placeholder,
        fg_color=BG_CAMPO,
        text_color=TEXTO_PRINCIPAL,
        border_width=0,
        corner_radius=8,
        **extra,
    )


def menu_opcoes(master, valores, **extra) -> ctk.CTkOptionMenu:
    return ctk.CTkOptionMenu(
        master,
        values=valores,
        fg_color=BG_CAMPO,
        button_color=DESTAQUE,
        button_hover_color=DESTAQUE_HOVER,
        text_color=TEXTO_PRINCIPAL,
        **extra,
    )


def rotulo_campo(master, texto) -> ctk.CTkLabel:
    return ctk.CTkLabel(master, text=texto, font=FONTE_LABEL, text_color=TEXTO_SECUNDARIO, anchor="w")


def rotulo_erro(master) -> ctk.CTkLabel:
    label = ctk.CTkLabel(master, text="", font=FONTE_PEQUENA, text_color=ERRO, wraplength=280, justify="left")
    label.pack(fill="x", padx=24, pady=(10, 0))
    return label


def nova_janela(master, titulo, largura, altura) -> ctk.CTkToplevel:
    janela = ctk.CTkToplevel(master)
    janela.title(titulo)
    janela.geometry(f"{largura}x{altura}")
    janela.configure(fg_color=BG_JANELA)
    janela.transient(master)
    return janela


def mostrar_aviso(master, texto: str, titulo: str = "Aviso") -> None:
    aviso = nova_janela(master, titulo, 320, 170)
    ctk.CTkLabel(
        aviso,
        text=texto,
        font=FONTE_LABEL,
        text_color=TEXTO_PRINCIPAL,
        wraplength=270,
        justify="left",
    ).pack(expand=True, padx=20, pady=(20, 0))
    botao_primario(aviso, "OK", aviso.destroy).pack(pady=20, padx=20, fill="x")
