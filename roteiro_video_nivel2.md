# Roteiro do vídeo — Nível 2 (Desk App II) — StreamFlix

Duração alvo: **6:00**. Diferente do nível 1, aqui o vídeo é uma
**demonstração ao vivo rodando na sua máquina** — grave a tela do terminal
navegando pelo menu de verdade (não precisa ler um script decorado, só
seguir os passos abaixo com calma).

---

## [0:00 – 0:25] Abertura

> "Oi de novo! Esse é o nível 2 do StreamFlix. No nível 1 mostrei a
> modelagem; agora vou mostrar o projeto funcionando de verdade, com um
> menu que dá acesso a todas as funcionalidades. Ainda não tem banco de
> dados — os dados vivem em memória enquanto o programa está rodando,
> como pede o enunciado desse nível."

Rode no terminal (na raiz do projeto):

```bash
python main.py
```

*(rode rapidinho o `main.py`/`demo.py` só pra lembrar o que já existia — 10 segundos, não precisa explicar de novo)*

## [0:25 – 0:45] Abrindo o menu

```bash
python menu.py
```

> "Esse programa já nasce com alguns dados de exemplo carregados —
> um usuário e três conteúdos — só pra não começar tudo vazio."

## [0:45 – 2:30] Catálogo — mostrando herança e polimorfismo na prática

Navegue: **1 (Gerenciar catálogo)**

> "Aqui dá pra cadastrar qualquer tipo de conteúdo."

- **1. Adicionar filme** → cadastre um filme rápido
- **2. Adicionar série (com episódios)** → cadastre uma série com 2 episódios
- **5. Listar catálogo** → mostre que filme, série e documentário aparecem
  juntos, cada um com sua própria informação (polimorfismo de
  `exibir_informacoes()`)
- **6. Reproduzir um conteúdo** → escolha a série cadastrada e reproduza
  duas vezes seguidas, mostrando que ela avança pro próximo episódio

> "Reparem que 'reproduzir' se comporta diferente pra cada tipo — filme
> toca do início ao fim, série avança episódio por episódio. É o
> polimorfismo que expliquei no vídeo do nível 1, só que agora
> funcionando interativamente."

Volte: **0**

## [2:30 – 4:15] Usuários, assinatura e favoritos

Navegue: **2 (Gerenciar usuários)**

- **1. Cadastrar usuário** → cadastre um segundo usuário
- **3. Assinar/alterar plano** → mude o plano dele pra Premium
- **4. Favoritar conteúdo** → favorite 1 ou 2 itens do catálogo
- **6. Listar favoritos** → mostre os favoritos salvos

> "Aqui dá pra ver a composição e a associação: a lista de favoritos
> pertence ao usuário, mas os conteúdos favoritados continuam sendo os
> mesmos objetos do catálogo — não são cópias."

Volte: **0**

## [4:15 – 5:15] Recomendações

Navegue: **3 (Recomendações)**

- **1. Gerar recomendações** → escolha um usuário e peça 2 ou 3
  recomendações

> "Essa é a dependência que mostrei na modelagem: o serviço usa um motor
> de recomendação por trás dos panos, só durante essa chamada."

Volte: **0**

## [5:15 – 6:00] Encerramento

> "Isso cobre o menu completo: catálogo, usuários, assinaturas,
> favoritos e recomendações, tudo funcionando em memória, sem banco de
> dados ainda — exatamente o que esse nível pede. O código atualizado
> está no mesmo repositório do nível 1, link na descrição. Até o
> próximo nível!"

---

## Checklist antes de gravar

- [ ] Rodar `python menu.py` uma vez sozinho, sem gravar, só pra treinar
      a sequência de opções (evita hesitação na hora de gravar)
- [ ] Terminal com fonte grande o suficiente pra leitura no vídeo
- [ ] Conferir que `git push` do nível 2 já foi feito antes de gravar
      (ou deixar claro na fala que o código gravado é o mesmo do link)
- [ ] Ficar de olho no tempo — 6 minutos passam rápido navegando por menu
