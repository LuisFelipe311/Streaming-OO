from streaming.Models import (
    Documentario,
    Episodio,
    Filme,
    PlanoAssinatura,
    Serie,
    ServicoStreaming,
    Usuario,
)


def montar_catalogo(servico: ServicoStreaming) -> None:
    filme = Filme("Interestelar", 2014, "Ficção", 9.1, 169)
    documentario = Documentario("Cosmos", 2019, "Ficção", 8.7, "Ann Druyan")

    serie = Serie("Dark", 2017, "Ficção", 9.0)
    serie.adicionar_episodio(Episodio(1, "Secretos", 55))
    serie.adicionar_episodio(Episodio(2, "Mentiras", 51))

    for conteudo in (filme, documentario, serie):
        servico.adicionar_conteudo(conteudo)


def main() -> None:
    # Este script é a demonstração isolada do nível 1 e não precisa persistir
    # nada — por isso usa um banco SQLite só em memória (":memory:"), que
    # some quando o programa termina. O banco "de verdade" (streamflix.db)
    # é usado pelo menu.py, a partir do nível 3.
    servico = ServicoStreaming("StreamFlix", caminho_banco=":memory:")
    montar_catalogo(servico)

    usuario = Usuario("Luis", "luis@example.com", genero_favorito="Ficção")
    servico.cadastrar_usuario(usuario)
    usuario.assinar(PlanoAssinatura.PREMIUM)

    print(f"== {servico.nome} ==")
    print(f"Usuário: {usuario.nome} | {usuario.assinatura}\n")

    print("-- Catálogo completo --")
    for conteudo in servico.catalogo:
        print(" -", conteudo.exibir_informacoes())

    print("\n-- Reproduzindo cada item do catálogo (POLIMORFISMO) --")
    for conteudo in servico.catalogo:
        print(" -", servico.reproduzir_para(usuario, conteudo))

    print("\n-- Favoritando conteúdo (COMPOSIÇÃO + ASSOCIAÇÃO) --")
    for conteudo in servico.catalogo:
        usuario.favoritos.adicionar(conteudo)
    print("Favoritos de", usuario.nome, ":", [c.titulo for c in usuario.favoritos.listar()])

    print("\n-- Recomendações (DEPENDÊNCIA de MotorDeRecomendacao) --")
    recomendados = servico.recomendar_para(usuario, quantidade=2)
    print("Recomendado para", usuario.nome, ":", [c.titulo for c in recomendados])


if __name__ == "__main__":
    main()
