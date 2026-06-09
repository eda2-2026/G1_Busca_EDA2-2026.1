# RootQuest - Algoritmos de Arvores

**Número da Lista**: 1
**Conteúdo da Disciplina**: FGA0239 - ESTRUTURA DE DADOS 2 - T01


## Alunos

<div align = "center">
<table>
  <tr>
    <td align="center"><a href="https://github.com/victorcamaraa"><img style="border-radius: 50%;" src="https://github.com/victorcamaraa.png" width="190px;" alt=""/><br /><sub><b>Victor Camara</b></sub></a><br /><a href="Link git" title="Rocketseat"></a></td>
    <td align="center"><a href="https://github.com/yanzin00"><img style="border-radius: 50%;" src="https://github.com/yanzin00.png" width="190px;" alt=""/><br /><sub><b>Yan Guimarães </b></sub></a><br />
  </tr>
</table>

| Matrícula   | Aluno                             |
| ----------- | ---------------------------------- |
| 222006220  | Yan Lucas Souza Guimarães |
| 221031238  | Victor Augusto de Sousa Camara |
</div>

## Sobre

Este projeto é a continuação do desenvolvimento das aplicações interativas [MazePathfinder](https://github.com/eda2-2026/G1_Busca_EDA2-2026.1), introduzindo agora o **RootQuest (Tree Visualizer)**. O objetivo desta funcionalidade é fornecer uma ferramenta visual rica e interativa para auxiliar no estudo e compreensão de árvores de busca autobalanceadas.

Através de uma interface gráfica baseada em Tkinter, o usuário pode:
- **Selecionar Estruturas**: Escolher entre manipular uma **Árvore AVL** ou uma **Red-Black Tree**.
- **Inserção Interativa**: Adicionar novos valores numéricos (nós) à árvore em tempo real.
- **Visualização do Balanceamento**: Acompanhar visualmente como a estrutura da árvore se modifica e se adapta para manter as propriedades de balanceamento estrito (no caso da AVL) ou balanceamento de cor (no caso da Red-Black Tree) após cada inserção.
- **Renderização Dinâmica**: A árvore é redesenhada automaticamente calculando posições x e y de forma recursiva para evitar sobreposição visual, demonstrando a hierarquia exata e as rotações (Left-Leaning, etc) sob o capô.

Esta funcionalidade ajuda a desmistificar a complexidade estrutural das rotações duplas/simples e recolorações que frequentemente confundem os alunos ao estudarem estruturas avançadas.

## Screenshot

<!-- Adicione o link ou path local para a screenshot do RootQuest aqui -->
<img width="1752" height="1308" alt="Screenshot do RootQuest" src="[LINK_DA_SUA_SCREENSHOT_AQUI]" />

## Requisitos

- **Python 3.10+**
- **Tkinter** (geralmente incluído na instalação padrão do Python)

### Instalando o Python

### Opção 1: Site Oficial do Python (Recomendado)

1. **Visite o site do Python**: Acesse [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Baixe o Python**:
   - Escolha a versão 3.10 ou superior
   - Selecione o instalador apropriado para seu sistema operacional:
     - **Windows**: Baixe o instalador `.exe`
     - **macOS**: Use o instalador do site ou `brew install python3`
     - **Linux**: Use o gerenciador de pacotes da sua distribuição (ex: `sudo apt install python3 python3-tk`)

3. **Instale o Python**:
   - **Windows**: Execute o arquivo `.exe` e marque a opção "Add Python to PATH"
   - **macOS**: Siga as instruções do instalador
   - **Linux**: A instalação via gerenciador de pacotes já configura tudo automaticamente

4. **Instale o Tkinter (macOS com Homebrew)**:
   
   Se estiver usando Python do Homebrew, o Tkinter não é incluído por padrão. Instale separadamente:
   ```bash
   brew install python-tk
   ```
   
5. **Verifique a Instalação**:
   ```bash
   python3 --version
   ```
   Você deve ver uma saída como: `Python 3.1x.x`

6. **Verifique o Tkinter**:
   ```bash
   python3 -m tkinter
   ```
   Uma janela de demonstração do Tkinter deve abrir.

## Configurando o Projeto

### 1. Clone ou Baixe o Projeto
```bash
git clone https://github.com/yanzin00/G1_Busca_EDA2-2026.1.git

cd G1_Busca_EDA2-2026.1
```

### 2. Execute a Aplicação
```bash
# Navegue até o diretório src
cd src

# Rodar a aplicação
python main.py
```

## Como Usar

Ao iniciar a aplicação, você verá o menu principal **ESCOLHA SEU DESAFIO**.

1. Clique no botão verde **RootQuest (Tree Visualizer)**.
2. **Escolha a Estrutura**: No menu superior da nova tela, use o menu suspenso para escolher o tipo de árvore que deseja estudar (**AVL** ou **Red-Black**).
3. **Insira um Valor**: Digite um número inteiro na caixa de entrada rotulada como **Valor**.
4. **Acione a Inserção**: Pressione a tecla **Enter** ou clique no botão **Inserir**. A árvore será desenhada ou atualizada na tela central, demonstrando a nova estrutura balanceada.
5. **Continue Inserindo**: Repita o processo de inserção para ver a árvore crescer e realizar as rotações necessárias.
6. **Limpar a Tela**: Clique no botão vermelho **Limpar** a qualquer momento para resetar a tela e recomeçar a árvore do zero.

## Estrutura do Projeto

```
G1_Busca_EDA2-2026.1/
├── README.md
└── src/
    ├── main.py         # Arquivo de inicialização principal
    ├── home.py         # Interface do menu principal de seleção
    ├── app.py          # Interface legada (Maze Pathfinder)
    ├── tree_app.py     # Interface e lógica de UI do RootQuest Visualizer
    ├── maze.py         # Lógica legada
    ├── algorithms.py   # Lógica legada
    ├── trees.py        # Algoritmos principais e modelagem de dados das árvores AVL e Red-Black
    └── constants.py    # Constantes e configurações globais
```

## Apresentação

<!-- Adicione aqui o link para vídeo de demonstração quando disponível -->
[Vídeo de demonstração](https://drive.google.com/drive/folders/1iFZ5N3bZ-zTFKSO7wrfIlDC-y0j5MnkC?usp=sharing)
