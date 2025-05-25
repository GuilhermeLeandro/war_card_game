# Jogo de Guerra (War Card Game)

Bem-vindo à documentação do Jogo de Guerra, uma implementação do clássico jogo de cartas utilizando Python e a biblioteca Pygame. Este projeto foi desenvolvido com foco na aplicação de estruturas de dados fundamentais como Pilha (Stack), Fila (Queue) e Lista Duplamente Encadeada (Doubly Linked List).

## Sumário

1.  [Visão Geral](#visão-geral)
2.  [Recursos](#recursos)
3.  [Regras do Jogo](#regras-do-jogo)
    *   [Objetivo](#objetivo-do-jogo)
    *   [Preparação](#preparação)
    *   [Hierarquia das Cartas](#hierarquia-das-cartas)
    *   [Como Jogar uma Rodada](#como-jogar-uma-rodada)
    *   [Guerra (Empate)](#guerra-quando-há-um-empate)
    *   [Fim do Jogo](#fim-do-jogo)
4.  [Tecnologias Utilizadas](#tecnologias-utilizadas)
5.  [Estrutura do Projeto](#estrutura-do-projeto)
6.  [Descrição dos Módulos](#descrição-dos-módulos)
    *   [`main.py` (ou `run_game.py`)](#mainpy-ou-run_gamepy)
    *   [`estruturas_dados/`](#estruturas_dados)
    *   [`jogo/`](#jogo)
    *   [`interface/`](#interface)
    *   [`assets/`](#assets)
7.  [Uso das Estruturas de Dados](#uso-das-estruturas-de-dados)
    *   [Pilha (Stack)](#pilha-stack---estruturas_dadospilhapy)
    *   [Fila (Queue)](#fila-queue---estruturas_dadosfilapy)
    *   [Lista Duplamente Encadeada](#lista-duplamente-encadeada---estruturas_dadoslista_duplamente_encadeadapy)
8.  [Como Executar](#como-executar)

## Visão Geral

Este projeto simula o jogo de cartas "Guerra" entre um jogador humano e a máquina. Ele possui uma interface gráfica construída com Pygame, permitindo uma experiência visual interativa. O núcleo do jogo demonstra a aplicação prática de estruturas de dados personalizadas para gerenciar o baralho, as mãos dos jogadores e o histórico de jogadas.

## Recursos

*   Interface gráfica completa com Pygame.
*   Telas de Menu Principal, Jogo e Regras.
*   Animações visuais para jogadas de cartas, viradas e coleta.
*   Lógica completa do jogo de Guerra, incluindo o mecanismo de "guerra" em caso de empates.
*   Uso de Pilha para o baralho principal.
*   Uso de Fila para a mão de cada jogador e para a sequência de eventos de animação.
*   Uso de Lista Duplamente Encadeada para o histórico de rodadas do jogo.
*   Exibição do histórico de jogadas detalhado.
*   Assets gráficos para cartas (com placeholders caso as imagens não sejam encontradas).

## Regras do Jogo

Estas são as regras conforme implementadas no jogo e exibidas na tela de regras:

### Objetivo do Jogo
Ser o primeiro jogador a conquistar todas as cartas do baralho!

### Preparação
1.  Utiliza-se um baralho padrão de 52 cartas.
2.  O baralho é embaralhado e dividido igualmente entre os dois jogadores (Você e a Máquina).
3.  Cada jogador mantém sua pilha de cartas virada para baixo à sua frente.

### Hierarquia das Cartas
A ordem das cartas, da menor para a maior, é:
**2, 3, 4, 5, 6, 7, 8, 9, 10, Valete (J), Dama (Q), Rei (K), Ás (A)**.
Os naipes (Copas, Ouros, Paus, Espadas) não influenciam o valor da carta no jogo padrão de Guerra.

### Como Jogar uma Rodada
1.  A cada rodada, ambos os jogadores viram simultaneamente a carta do topo de suas pilhas.
2.  As cartas reveladas são comparadas com base na hierarquia acima.
3.  A carta de maior valor vence a rodada.
4.  O vencedor coleta ambas as cartas jogadas e as adiciona ao fundo de sua própria pilha.

### Guerra (Quando há um Empate!)
1.  Se as cartas jogadas na rodada tiverem o mesmo valor, uma **GUERRA** é declarada!
2.  Para a Guerra, cada jogador coloca **três cartas** da sua pilha viradas para baixo sobre a mesa (esta é a "aposta de guerra").
3.  Em seguida, cada jogador vira uma **quarta carta** para cima.
4.  A carta virada para cima de maior valor vence a Guerra. O vencedor coleta **TODAS** as cartas da mesa (as duas originais do empate, as seis da aposta e as duas de revelação).
5.  Se as cartas de revelação da Guerra também forem iguais, o processo de Guerra se repete com as cartas já acumuladas na mesa.
6.  Se um jogador não tiver cartas suficientes para completar a aposta de guerra ou a carta de revelação, ele perde automaticamente a Guerra (e, potencialmente, o jogo).

### Fim do Jogo
O jogo continua até que um jogador conquiste todas as 52 cartas. Alternativamente, se um limite de (por exemplo) **1000 rodadas** for atingido (conforme definido em `war_game_logic.py`), o jogador com mais cartas nesse momento é declarado o vencedor. Um jogador também perde se não tiver cartas para jogar uma rodada ou participar de uma guerra.

## Tecnologias Utilizadas

*   **Python 3.x**
*   **Pygame** (para a interface gráfica, manipulação de eventos e assets)

## Estrutura do Projeto

A organização dos arquivos e pastas do projeto é a seguinte (baseada na sua estrutura ajustada):

```bash
jogo_guerra/
├── run_game.py # Ponto de entrada da aplicação
├── src/
│ ├── init.py # Torna 'src' um pacote Python
│ ├── game/
│ │ ├── init.py # Torna 'game' um pacote Python
│ │ └── war_game_logic.py # Lógica principal do jogo de Guerra
│ ├── models/
│ │ ├── init.py # Torna 'models' um pacote Python
│ │ ├── card.py # Definição da classe Card
│ │ ├── deck.py # Definição da classe Deck
│ │ └── player.py # Definição da classe Player
│ ├── structures/
│ │ ├── init.py # Torna 'structures' um pacote Python
│ │ ├── doubly_linked_list.py # Implementação da Lista Duplamente Encadeada
│ │ ├── queue.py # Implementação da Fila
│ │ └── stack.py # Implementação da Pilha
│ └── ui/
│ ├── init.py # Torna 'ui' um pacote Python
│ ├── assets/ # Contém subpastas para fontes, imagens de cartas, fundos
│ │ ├── fonts/ # Arquivos de fonte (.ttf, .otf)
│ │ ├── cards/ # Imagens das cartas (ex: card_hearts_A.png)
│ │ └── backgrounds/ # Imagens de fundo para telas
│ ├── base_screen.py # Classe base para todas as telas da UI
│ ├── card_graphics.py # Módulo para carregar e gerenciar superfícies de cartas
│ ├── constants.py # Constantes globais de UI (cores, tamanhos, etc.)
│ ├── elements.py # Elementos de UI reutilizáveis (ex: Button, VisualCard)
│ ├── game_screen.py # Tela principal do jogo
│ ├── gui_manager.py # Gerenciador principal da GUI e transição entre telas
│ ├── log_display.py # Componente para exibir o histórico do jogo
│ ├── menu_screen.py # Tela do menu principal
│ ├── rules_screen.py # Tela de exibição das regras
│ └── ui_utils.py # Utilitários para UI (ex: desenhar gradientes)
└── README.md # Este arquivo de documentação
```

*(Nota: A presença de arquivos `__init__.py` em `src/` e em cada um de seus subdiretórios (`structures`, `models`, `game`, `ui`) é essencial para que o Python os reconheça como pacotes, permitindo que `run_game.py` importe módulos de dentro de `src/` após a configuração do `sys.path`.)*

## Arquitetura e Módulos Principais

O projeto é modularizado para separar responsabilidades, facilitando o desenvolvimento e a manutenção.

### Ponto de Entrada (`run_game.py`)
O arquivo `run_game.py`, localizado na raiz do projeto, é o script que inicia toda a aplicação. Suas funções primárias são:
1.  **Configurar o Ambiente de Importação:** Modifica o `sys.path` para incluir o diretório `src/`. Isso permite que os módulos dentro de `src/` (como `ui.gui_manager`) sejam importados de forma limpa e direta em `run_game.py` e entre si, sem a necessidade de prefixar cada importação com `src.`.
2.  **Inicializar o Gerenciador da Interface:** Importa e instancia `GUIManager` de `src/ui/gui_manager.py`.
3.  **Executar o Jogo:** Chama o método `executar()` do `GUIManager`, que contém o loop principal do Pygame e gerencia o ciclo de vida da aplicação.
4.  **Tratamento de Erros:** Inclui blocos `try-except` para capturar exceções gerais e garantir que o Pygame seja finalizado corretamente.

### Pacote `src/`
Este diretório funciona como o contêiner principal para todo o código-fonte da lógica e interface do jogo.

#### Pacote de Estruturas de Dados (`src/structures/`)
Este pacote centraliza as implementações personalizadas das estruturas de dados:
*   `stack.py`: Fornece a classe `Stack` (Pilha).
*   `queue.py`: Contém a classe `Queue` (Fila).
*   `doubly_linked_list.py`: Apresenta a `DoublyLinkedList`.

#### Pacote de Modelos do Jogo (`src/models/`)
Define as entidades fundamentais do jogo:
*   `card.py`: A classe `Card` representa uma carta individual.
*   `deck.py`: A classe `Deck` gerencia o baralho, utilizando a `Stack` para suas operações.
*   `player.py`: A classe `Player` representa um jogador e sua mão de cartas, gerenciada por uma `Queue`.

#### Pacote de Lógica do Jogo (`src/game/`)
Contém a inteligência e as regras do jogo:
*   `war_game_logic.py`: A classe `WarGameLogic` é o motor do jogo. Ela coordena as rodadas, aplica as regras de comparação e "guerra", e registra o histórico usando uma `DoublyLinkedList`.

#### Pacote da Interface Gráfica (`src/ui/`)
Responsável por toda a apresentação visual e interação com o usuário:
*   `gui_manager.py`: O `GUIManager` orquestra a UI, gerenciando as telas e o fluxo da aplicação.
*   `base_screen.py`: Classe base abstrata para as telas (`MenuScreen`, `GameScreen`, `RulesScreen`).
*   `menu_screen.py`, `game_screen.py`, `rules_screen.py`: Implementações das telas.
*   `elements.py`: Componentes de UI como `Button`, `VisualCard`.
*   `card_graphics.py`: Lida com o carregamento e o cache das imagens das cartas.
*   `log_display.py`: Componente para exibir o histórico do jogo.
*   `constants.py`: Define constantes visuais (cores, fontes, tamanhos).
*   `ui_utils.py`: Funções utilitárias para a UI.

### Recursos Visuais (`src/ui/assets/`)
Este diretório, dentro de `src/ui/`, armazena todos os recursos visuais necessários:
*   `fonts/`: Arquivos de fonte.
*   `cards/`: Imagens para cada carta do baralho.
*   `backgrounds/`: Imagens de fundo para as telas.

## Aplicação das Estruturas de Dados

O projeto demonstra a aplicação prática de estruturas de dados para resolver problemas específicos do domínio do jogo.

### Pilha (`Stack`): Gerenciamento do Baralho
A `Pilha` (de `src/structures/stack.py`) é fundamental para a classe `Deck` (em `src/models/deck.py`).
*   **Representação Natural:** Um baralho de onde se compra cartas do topo se alinha perfeitamente com o comportamento LIFO de uma pilha.
*   **Operações:**
    *   `push()`: Usado para adicionar cartas ao baralho durante sua criação e após o embaralhamento.
    *   `pop()`: Usado para "comprar" ou distribuir a carta do topo do baralho.
    *   `is_empty()`, `size()`: Para verificar o estado do baralho.

*(Placeholder para trecho de código de `src/models/deck.py` ilustrando `self._pilha_cartas = Stack()` e seus métodos)*

### Fila (`Queue`): Mãos dos Jogadores e Eventos de UI
A `Fila` (de `src/structures/queue.py`) tem duas aplicações importantes, devido à sua natureza FIFO:
1.  **Mão do Jogador (`src/models/player.py`):**
    *   As cartas que um jogador coleta são adicionadas ao "final" de sua mão (`enqueue()`).
    *   A carta a ser jogada é sempre a que está no "início" da mão por mais tempo (`dequeue()`).
2.  **Sequenciamento de Animações (`src/ui/game_screen.py`):**
    *   A `GameScreen` utiliza uma fila para gerenciar a ordem dos eventos visuais.
    *   Eventos são adicionados à fila (`append()` ou `enqueue()`) pela lógica do jogo.
    *   A tela processa um evento da frente da fila (`popleft()` ou `dequeue()`) por vez.

*(Placeholder para trechos de código de `src/models/player.py` para `self.hand = Queue()` e de `src/ui/game_screen.py` para `self.event_animation_queue = Queue()`)*

### Lista Duplamente Encadeada (`DoublyLinkedList`): Histórico do Jogo
A `Lista Duplamente Encadeada` (de `src/structures/doubly_linked_list.py`) é usada pela `WarGameLogic` (em `src/game/war_game_logic.py`) para manter um registro cronológico detalhado de todas as rodadas.
*   **Registro Cronológico:** Novas entradas de log são adicionadas ao final da lista (`append()`).
*   **Acesso aos Dados:** O `LogDisplay` (`src/ui/log_display.py`) recupera todas as entradas (`get_all_entries()`) para exibir o histórico.
*   **Flexibilidade:** Ideal para um log onde novas informações são constantemente adicionadas.

*(Placeholder para trecho de código de `src/game/war_game_logic.py` ilustrando `self.game_log = DoublyLinkedList()` e o método `_add_log_entry`)*

## Como Executar

1.  **Pré-requisitos:**
    *   Python 3.7 ou superior.
    *   Pygame instalado. Se não tiver, instale com:
        ```bash
        pip install pygame
        ```

2.  **Estrutura de Arquivos:**
    Certifique-se de que os arquivos do projeto estão organizados conforme a estrutura detalhada na seção [Estrutura do Projeto](#estrutura-do-projeto). Isso inclui:
    *   O arquivo `run_game.py` na pasta raiz do projeto.
    *   A pasta `src/` contendo os subdiretórios `structures/`, `models/`, `game/`, e `ui/`, cada um com seus respectivos arquivos `.py`.
    *   A subpasta `src/ui/assets/` com os recursos visuais.
    *   **Crucial:** A presença de arquivos `__init__.py` (podem estar vazios) em `src/` e em cada um de seus subdiretórios que funcionam como pacotes (`structures`, `models`, `game`, `ui`).

3.  **Executando o Jogo:**
    Após configurar a estrutura de arquivos e instalar o Pygame:
    1.  Abra seu terminal ou prompt de comando.
    2.  Use o comando `cd` para navegar até o diretório raiz do seu projeto (a pasta `jogo_guerra/`, que contém `run_game.py` e a pasta `src/`).
    3.  Execute o script `run_game.py` com o comando:
        ```bash
        python3 run_game.py
        ```

Aproveite o Jogo de Guerra!
