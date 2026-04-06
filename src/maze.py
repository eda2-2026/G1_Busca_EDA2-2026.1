
import random
import sys
from constants import WALL, OPEN


# auxiliares
def _vazio(rows: int, cols: int, fill: int = WALL) -> list[list[int]]:
    return [[fill] * cols for _ in range(rows)]



def generate_recursive_backtracker(rows: int, cols: int) -> list[list[int]]:
    grid = _vazio(rows, cols)
    visitado = [[False] * cols for _ in range(rows)]

    def carve(r: int, c: int) -> None:
        visitado[r][c] = True
        grid[r][c] = OPEN
        dirs = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visitado[nr][nc]:
                grid[r + dr // 2][c + dc // 2] = OPEN
                carve(nr, nc)

    limite_antigo = sys.getrecursionlimit()
    sys.setrecursionlimit(max(limite_antigo, rows * cols * 2))
    carve(1, 1)
    sys.setrecursionlimit(limite_antigo)
    return grid


def generate_recursive_backtracker_iterative(rows: int, cols: int) -> list[list[int]]:

    grid = _vazio(rows, cols)
    visitado = [[False] * cols for _ in range(rows)]

    pilha = [(1, 1)]
    visitado[1][1] = True
    grid[1][1] = OPEN

    while pilha:
        r, c = pilha[-1]
        dirs = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(dirs)
        moveu = False
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visitado[nr][nc]:
                visitado[nr][nc] = True
                grid[r + dr // 2][c + dc // 2] = OPEN
                grid[nr][nc] = OPEN
                pilha.append((nr, nc))
                moveu = True
                break
        if not moveu:
            pilha.pop()

    return grid


def generate_prims(rows: int, cols: int) -> list[list[int]]:
    grid = _vazio(rows, cols)

    def neighbours2(r: int, c: int):
        for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                yield nr, nc, r + dr // 2, c + dc // 2

    no_labirinto = set()
    fronteira: list[tuple] = []

    def add_frontiers(r: int, c: int):
        for nr, nc, wr, wc in neighbours2(r, c):
            if (nr, nc) not in no_labirinto:
                fronteira.append((nr, nc, wr, wc))

    inicio_r, inicio_c = 1, 1
    grid[inicio_r][inicio_c] = OPEN
    no_labirinto.add((inicio_r, inicio_c))
    add_frontiers(inicio_r, inicio_c)

    while fronteira:
        idx = random.randrange(len(fronteira))
        nr, nc, wr, wc = fronteira[idx]
        fronteira[idx] = fronteira[-1]
        fronteira.pop()
        if (nr, nc) in no_labirinto:
            continue
        grid[nr][nc] = OPEN
        grid[wr][wc] = OPEN
        no_labirinto.add((nr, nc))
        add_frontiers(nr, nc)

    return grid


def generate_kruskal(rows: int, cols: int) -> list[list[int]]:

    grid = _vazio(rows, cols)

    # marcar celulas impares como abertas
    celulas = [(r, c) for r in range(1, rows, 2) for c in range(1, cols, 2)]
    for r, c in celulas:
        grid[r][c] = OPEN

    # union-find
    parent = {cell: cell for cell in celulas}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[ra] = rb
        return True

    # paredes internas entre celulas
    paredes = []
    for r, c in celulas:
        if r + 2 < rows:
            paredes.append(((r, c), (r + 2, c), (r + 1, c)))
        if c + 2 < cols:
            paredes.append(((r, c), (r, c + 2), (r, c + 1)))

    random.shuffle(paredes)
    for a, b, parede in paredes:
        if union(a, b):
            grid[parede[0]][parede[1]] = OPEN

    return grid


def generate_open_room(rows: int, cols: int) -> list[list[int]]:

    grid = _vazio(rows, cols, OPEN)
    for r in range(rows):
        grid[r][0] = WALL
        grid[r][cols - 1] = WALL
    for c in range(cols):
        grid[0][c] = WALL
        grid[rows - 1][c] = WALL
    return grid


def generate_sparse_obstacles(rows: int, cols: int,
                              density: float = 0.20) -> list[list[int]]:
    grid = generate_open_room(rows, cols)
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if random.random() < density:
                grid[r][c] = WALL
    return grid


# ── registro ──────────────────────────────────────────────────────────────────
# nome exibido na interface → funcao geradora
GENERATORS: dict[str, callable] = {
    "DFS recursivo": generate_recursive_backtracker_iterative,
    "Prim's": generate_prims,
    "Kruskal's": generate_kruskal,
    "Aberto": generate_open_room,
    "Aberto com obstaculos": generate_sparse_obstacles,
}