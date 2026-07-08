"""Menu interativo do StreamFlix — Nível 2 (Desk App II).

Dá acesso, em tempo de execução, a todos os modelos e funcionalidades:
catálogo (filmes, séries, episódios, documentários), usuários, assinaturas,
favoritos e recomendações. Os dados vivem em memória durante a execução —
ainda não há persistência em banco de dados, conforme pede o nível 2.
"""

from streaming.Models import (
    Documentario,
    Episodio,
    Filme,
    PlanoAssinatura,
    Serie,
    ServicoStreaming,
    Usuario,
)

servico = ServicoStreaming("StreamFlix")


# ---------- utilitários de entrada ----------

def pausar() -> None:
    input("\nPressione ENTER para continuar...")


def ler_int(mensagem: str, minimo: int | None = None, maximo: int | None = None) -> int:
    while True:
        valor = input(mensagem).strip()
        try:
            numero = int(valor)
        except ValueError:
            print("Digite um número inteiro válido.")
            continue
        if minimo is not None and numero < minimo:
            print(f"O valor mínimo é {minimo}.")
            continue
        if maximo is not None and numero > maximo:
            print(f"O valor máximo é {maximo}.")
            continue
        return numero


def ler_float(mensagem: str) -> float:
    while True:
        valor = input(mensagem).strip().replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            print("Digite um número válido (ex: 8.5).")


def escolher_da_lista(itens: list, titulo: str = "Escolha uma opção"):
    if not itens:
        print("Não há itens cadastrados ainda.")
        return None
    print(f"\n{titulo}:")
    for i, item in enumerate(itens, start=1):
        print(f"  {i}. {item}")
    indice = ler_int("Digite o número (0 para cancelar): ", minimo=0, maximo=len(itens))
    if indice == 0:
        return None
    return itens[indice - 1]


# ---------- catálogo ----------

def adicionar_filme() -> None:
    print("\n-- Novo filme --")
    titulo = input("Título: ").strip()
    ano = ler_int("Ano: ")
    genero = input("Gênero: ").strip()
    avaliacao = ler_float("Avaliação (0-10): ")
    duracao = ler_int("Duração (minutos): ")
    filme = Filme(titulo, ano, genero, avaliacao, duracao)
    servico.adicionar_conteudo(filme)
    print(f"Filme '{titulo}' adicionado ao catálogo.")


def adicionar_serie() -> None:
    print("\n-- Nova série --")
    titulo = input("Título: ").strip()
    ano = ler_int("Ano: ")
    genero = input("Gênero: ").strip()
    avaliacao = ler_float("Avaliação (0-10): ")
    serie = Serie(titulo, ano, genero, avaliacao)

    quantidade = ler_int("Quantos episódios deseja cadastrar agora? ", minimo=0)
    for numero in range(1, quantidade + 1):
        print(f"\nEpisódio {numero}:")
        titulo_ep = input("  Título do episódio: ").strip()
        duracao_ep = ler_int("  Duração (minutos): ")
        serie.adicionar_episodio(Episodio(numero, titulo_ep, duracao_ep))

    servico.adicionar_conteudo(serie)
    print(f"Série '{titulo}' adicionada ao catálogo com {quantidade} episódio(s).")


def adicionar_episodio_existente() -> None:
    series = [c for c in servico.catalogo if isinstance(c, Serie)]
    serie = escolher_da_lista(series, "Séries disponíveis")
    if serie is None:
        return
    proximo_numero = len(serie.episodios) + 1
    titulo_ep = input("Título do novo episódio: ").strip()
    duracao_ep = ler_int("Duração (minutos): ")
    serie.adicionar_episodio(Episodio(proximo_numero, titulo_ep, duracao_ep))
    print(f"Episódio {proximo_numero} adicionado a '{serie.titulo}'.")


def adicionar_documentario() -> None:
    print("\n-- Novo documentário --")
    titulo = input("Título: ").strip()
    ano = ler_int("Ano: ")
    genero = input("Gênero: ").strip()
    avaliacao = ler_float("Avaliação (0-10): ")
    diretor = input("Diretor: ").strip()
    documentario = Documentario(titulo, ano, genero, avaliacao, diretor)
    servico.adicionar_conteudo(documentario)
    print(f"Documentário '{titulo}' adicionado ao catálogo.")


def listar_catalogo() -> None:
    if not servico.catalogo:
        print("\nO catálogo está vazio.")
        return
    print("\n-- Catálogo --")
    for conteudo in servico.catalogo:
        print(" -", conteudo.exibir_informacoes(), f"[{type(conteudo).__name__}]")


def reproduzir_conteudo() -> None:
    conteudo = escolher_da_lista(list(servico.catalogo), "Conteúdo disponível")
    if conteudo is None:
        return
    usuario = escolher_da_lista(list(servico.usuarios), "Quem está assistindo?")
    if usuario is None:
        return
    print(servico.reproduzir_para(usuario, conteudo))


def menu_catalogo() -> None:
    opcoes = {
        "1": adicionar_filme,
        "2": adicionar_serie,
        "3": adicionar_episodio_existente,
        "4": adicionar_documentario,
        "5": listar_catalogo,
        "6": reproduzir_conteudo,
    }
    while True:
        print("\n=== Catálogo ===")
        print("1. Adicionar filme")
        print("2. Adicionar série (com episódios)")
        print("3. Adicionar episódio a uma série existente")
        print("4. Adicionar documentário")
        print("5. Listar catálogo")
        print("6. Reproduzir um conteúdo")
        print("0. Voltar")
        escolha = input("Escolha: ").strip()
        if escolha == "0":
            return
        acao = opcoes.get(escolha)
        if acao is None:
            print("Opção inválida.")
            continue
        acao()
        pausar()


# ---------- usuários ----------

PLANOS = {
    "1": PlanoAssinatura.FREE,
    "2": PlanoAssinatura.STANDARD,
    "3": PlanoAssinatura.PREMIUM,
}


def cadastrar_usuario() -> None:
    print("\n-- Novo usuário --")
    nome = input("Nome: ").strip()
    email = input("E-mail: ").strip()
    genero_favorito = input("Gênero favorito: ").strip()
    usuario = Usuario(nome, email, genero_favorito)
    servico.cadastrar_usuario(usuario)
    print(f"Usuário '{nome}' cadastrado.")


def listar_usuarios() -> None:
    if not servico.usuarios:
        print("\nNenhum usuário cadastrado ainda.")
        return
    print("\n-- Usuários --")
    for usuario in servico.usuarios:
        print(" -", usuario.nome, "|", usuario.email, "|", usuario.assinatura)


def assinar_plano() -> None:
    usuario = escolher_da_lista(list(servico.usuarios), "Escolha o usuário")
    if usuario is None:
        return
    print("\nPlanos disponíveis:")
    print("1. Free")
    print("2. Standard")
    print("3. Premium")
    escolha = input("Escolha o plano: ").strip()
    plano = PLANOS.get(escolha)
    if plano is None:
        print("Opção inválida.")
        return
    usuario.assinar(plano)
    print(f"{usuario.nome} agora está no plano {usuario.assinatura}.")


def favoritar_conteudo() -> None:
    usuario = escolher_da_lista(list(servico.usuarios), "Escolha o usuário")
    if usuario is None:
        return
    conteudo = escolher_da_lista(list(servico.catalogo), "Escolha o conteúdo")
    if conteudo is None:
        return
    usuario.favoritos.adicionar(conteudo)
    print(f"'{conteudo.titulo}' adicionado aos favoritos de {usuario.nome}.")


def remover_favorito() -> None:
    usuario = escolher_da_lista(list(servico.usuarios), "Escolha o usuário")
    if usuario is None:
        return
    conteudo = escolher_da_lista(list(usuario.favoritos.listar()), f"Favoritos de {usuario.nome}")
    if conteudo is None:
        return
    usuario.favoritos.remover(conteudo)
    print(f"'{conteudo.titulo}' removido dos favoritos de {usuario.nome}.")


def listar_favoritos() -> None:
    usuario = escolher_da_lista(list(servico.usuarios), "Escolha o usuário")
    if usuario is None:
        return
    favoritos = usuario.favoritos.listar()
    if not favoritos:
        print(f"\n{usuario.nome} ainda não tem favoritos.")
        return
    print(f"\n-- Favoritos de {usuario.nome} --")
    for conteudo in favoritos:
        print(" -", conteudo.titulo)


def menu_usuarios() -> None:
    opcoes = {
        "1": cadastrar_usuario,
        "2": listar_usuarios,
        "3": assinar_plano,
        "4": favoritar_conteudo,
        "5": remover_favorito,
        "6": listar_favoritos,
    }
    while True:
        print("\n=== Usuários ===")
        print("1. Cadastrar usuário")
        print("2. Listar usuários")
        print("3. Assinar/alterar plano")
        print("4. Favoritar conteúdo")
        print("5. Remover favorito")
        print("6. Listar favoritos de um usuário")
        print("0. Voltar")
        escolha = input("Escolha: ").strip()
        if escolha == "0":
            return
        acao = opcoes.get(escolha)
        if acao is None:
            print("Opção inválida.")
            continue
        acao()
        pausar()


# ---------- recomendações ----------

def gerar_recomendacoes() -> None:
    usuario = escolher_da_lista(list(servico.usuarios), "Escolha o usuário")
    if usuario is None:
        return
    quantidade = ler_int("Quantas recomendações deseja? ", minimo=1)
    recomendados = servico.recomendar_para(usuario, quantidade=quantidade)
    if not recomendados:
        print("Não há conteúdo suficiente no catálogo para recomendar.")
        return
    print(f"\nRecomendado para {usuario.nome}:")
    for conteudo in recomendados:
        print(" -", conteudo.exibir_informacoes())


def menu_recomendacoes() -> None:
    while True:
        print("\n=== Recomendações ===")
        print("1. Gerar recomendações para um usuário")
        print("0. Voltar")
        escolha = input("Escolha: ").strip()
        if escolha == "0":
            return
        if escolha == "1":
            gerar_recomendacoes()
            pausar()
        else:
            print("Opção inválida.")


# ---------- menu principal ----------

def popular_dados_exemplo() -> None:
    """Alguns dados iniciais, só pra não começar com tudo vazio."""
    filme = Filme("Interestelar", 2014, "Ficção", 9.1, 169)
    documentario = Documentario("Cosmos", 2019, "Ficção", 8.7, "Ann Druyan")
    serie = Serie("Dark", 2017, "Ficção", 9.0)
    serie.adicionar_episodio(Episodio(1, "Secretos", 55))
    serie.adicionar_episodio(Episodio(2, "Mentiras", 51))
    for conteudo in (filme, documentario, serie):
        servico.adicionar_conteudo(conteudo)

    usuario = Usuario("Luis", "luis@example.com", genero_favorito="Ficção")
    usuario.assinar(PlanoAssinatura.PREMIUM)
    servico.cadastrar_usuario(usuario)


def menu_principal() -> None:
    while True:
        print(f"\n===== {servico.nome} =====")
        print("1. Gerenciar catálogo")
        print("2. Gerenciar usuários")
        print("3. Recomendações")
        print("0. Sair")
        escolha = input("Escolha: ").strip()
        if escolha == "1":
            menu_catalogo()
        elif escolha == "2":
            menu_usuarios()
        elif escolha == "3":
            menu_recomendacoes()
        elif escolha == "0":
            print("Até mais!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    popular_dados_exemplo()
    menu_principal()
