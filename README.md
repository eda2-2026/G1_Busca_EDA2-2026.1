# Maze Pathfinder - Algoritmos de Busca

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

Este projeto é uma aplicação gráfica interativa que demonstra algoritmos de busca em labirintos gerados proceduralmente. Através de uma interface Tk2, o usuário pode:

- **Gerar Labirintos**: Criar labirintos usando diferentes algoritmos (DFS recursivo, Prim's, Kruskal's).
- **Definir Pontos de Passagem**: Clicar em células do labirinto para adicionar pontos que o caminho deve visitar.
- **Visualizar Algoritmos de Busca**: Executar algoritmos clássicos de busca em grafos para encontrar caminhos entre pontos:
  - **BFS (Busca em Largura)**: Encontra o caminho mais curto em grafos não ponderados
  - **DFS (Busca em Profundidade)**: Explora o máximo possível antes de retroceder
  - **Dijkstra**: Algoritmo de busca de caminho mais curto com pesos uniformes
  - **A***: Busca heurística que combina custo e estimativa para eficiência
- **Animação em Tempo Real**: Visualizar a exploração das células e a construção do caminho passo a passo com animação fluida.
- **Estatísticas**: Ver métricas como comprimento do caminho e número de células exploradas.

O projeto facilita o entendimento visual de como diferentes algoritmos de busca exploram espaços e encontram caminhos, permitindo comparar seu comportamento em tempo real.

## Algoritmos de Geração de Labirintos

### DFS Recursivo (Recursive Backtracker)
Gera labirintos perfeitos usando busca em profundidade com backtracking, criando corredores longos e sinuosos.

### Prim's
Algoritmo baseado em árvore geradora mínima, produz labirintos com ramificações mais distribuídas.

### Kruskal's
Outro algoritmo de árvore geradora mínima usando Union-Find, cria labirintos com estrutura aleatória balanceada.

### Aberto com Obstáculos
Ambiente aberto com densidade configurável de obstáculos aleatórios, útil para testar algoritmos em cenários menos estruturados.

## Algoritmos de Busca Implementados

| Algoritmo | Tipo | Garantia | Uso de Memória |
|-----------|------|----------|----------------|
| BFS | Cega | Caminho mais curto | Moderado |
| DFS | Cega | Não garante optimalidade | Baixo |
| Dijkstra | Informada | Caminho mais curto | Moderado |
| A* | Heurística | Caminho mais curto (com heurística admissível) | Moderado |

## Screenshot

<img width="1752" height="1308" alt="image" src="https://github.com/user-attachments/assets/1414d2c5-2ac1-4c13-88dc-2ef89df867fc" />

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

1. **Escolha o Tamanho**: Selecione o tamanho do labirinto no dropdown (11×11 até 41×41).
2. **Escolha o Tipo**: Selecione o algoritmo de geração do labirinto.
3. **Gerar Labirinto**: Clique em "novo labirinto" para gerar.
4. **Adicionar Pontos**: Clique nas células abertas (brancas) para adicionar pontos de passagem numerados.
5. **Escolha o Algoritmo**: Selecione BFS, DFS, Dijkstra ou A*.
6. **Encontrar Caminho**: Clique em "encontrar caminho" para visualizar o algoritmo em ação.
7. **Limpar**: Use "limpar pontos" ou "limpar caminho" para resetar elementos específicos.

## Estrutura do Projeto

```
G1_Busca_EDA2-2026.1/
├── README.md
└── src/
    ├── main.py         # Ponto de entrada da aplicação
    ├── app.py          # Classe principal da interface Tk2
    ├── maze.py         # Algoritmos de geração de labirintos
    ├── algorithms.py   # Algoritmos de busca (BFS, DFS, Dijkstra, A*)
    └── constants.py    # Constantes e configurações globais
```

## Apresentação

<!-- Adicione aqui o link para vídeo de demonstração quando disponível -->
[Vídeo de demonstração](https://drive.google.com/drive/folders/1iFZ5N3bZ-zTFKSO7wrfIlDC-y0j5MnkC?usp=sharing)

