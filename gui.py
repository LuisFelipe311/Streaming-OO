
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
