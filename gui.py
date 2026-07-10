"""Ponto de entrada da interface gráfica do StreamFlix — nível 4 (Desk App IV).

O terminal (menu.py) continua funcionando normalmente; este é só um jeito
alternativo de rodar o projeto, agora com janelas de verdade (customtkinter)
em vez de texto no console. Os dois usam o mesmo banco (streamflix.db) e o
mesmo ServicoStreaming por baixo dos panos.
"""

from streaming.Gui import tema
from streaming.Gui.janela_principal import JanelaPrincipal
from streaming.Models import ServicoStreaming


def main() -> None:
    servico = ServicoStreaming("StreamFlix")
    servico.carregar_dados_persistidos()

    tema.configurar_aparencia()
    app = JanelaPrincipal(servico)
    app.mainloop()


if __name__ == "__main__":
    main()
