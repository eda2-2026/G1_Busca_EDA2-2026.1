import heapq
from collections import deque
from constants import WALL

# auxiliares compartilhadas

def _vizinhos(grid: list[list[int]], r: int, c: int):
    linhas, colunas = len(grid), len(grid[0])
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < linhas and 0 <= nc < colunas and grid[nr][nc] != WALL:
            yield nr, nc


def _reconstruir(anterior: dict, fim: tuple) -> list[tuple]:
    caminho, atual = [], fim
    while atual is not None:
        caminho.append(atual)
        atual = anterior.get(atual)
    return list(reversed(caminho))


# algoritmos

def bfs(grid, inicio, fim):
    fila = deque([inicio])
    anterior = {inicio: None}
    ordem = []

    while fila:
        atual = fila.popleft()
        ordem.append(atual)
        if atual == fim:
            return _reconstruir(anterior, fim), ordem
        for vizinho in _vizinhos(grid, *atual):
            if vizinho not in anterior:
                anterior[vizinho] = atual
                fila.append(vizinho)

    return None, ordem

def dfs(grid, inicio, fim):
    pilha = [inicio]
    anterior = {inicio: None}
    ordem= []

    while pilha:
        atual = pilha.pop()
        if atual in ordem:
            continue
        ordem.append(atual)
        if atual == fim:
            return _reconstruir(anterior, fim), ordem
        for vizinho in _vizinhos(grid, *atual):
            if vizinho not in anterior:
                anterior[vizinho] = atual
                pilha.append(vizinho)

    return None, ordem


def dijkstra(grid, inicio, fim):

    dist = {inicio: 0}
    anterior = {inicio: None}
    fila_prioridade = [(0, inicio)]
    ordem = []

    while fila_prioridade:
        d, atual = heapq.heappop(fila_prioridade)
        if d > dist.get(atual, float("inf")):
            continue
        ordem.append(atual)
        if atual == fim:
            return _reconstruir(anterior, fim), ordem
        for vizinho in _vizinhos(grid, *atual):
            novo_d = dist[atual] + 1
            if novo_d < dist.get(vizinho, float("inf")):
                dist[vizinho] = novo_d
                anterior[vizinho] = atual
                heapq.heappush(fila_prioridade, (novo_d, vizinho))

    return None, ordem


def astar(grid, inicio, fim):

    def h(r, c):
        return abs(r - fim[0]) + abs(c - fim[1])

    g = {inicio: 0}
    anterior = {inicio: None}
    fila_prioridade = [(h(*inicio), inicio)]
    fechados: set = set()
    ordem = []

    while fila_prioridade:
        _, atual = heapq.heappop(fila_prioridade)
        if atual in fechados:
            continue
        fechados.add(atual)
        ordem.append(atual)
        if atual == fim:
            return _reconstruir(anterior, fim), ordem
        for vizinho in _vizinhos(grid, *atual):
            novo_g = g[atual] + 1
            if novo_g < g.get(vizinho, float("inf")):
                g[vizinho] = novo_g
                anterior[vizinho] = atual
                heapq.heappush(fila_prioridade, (novo_g + h(*vizinho), vizinho))

    return None, ordem


# ── registro ──────────────────────────────────────────────────────────────────
# nome exibido na interface → funcao do algoritmo
ALGOS: dict[str, callable] = {
    "BFS": bfs,
    "DFS": dfs,
    "Dijkstra": dijkstra,
    "A*": astar,
}