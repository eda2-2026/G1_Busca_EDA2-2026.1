import tkinter as tk
from tkinter import ttk

from constants import (
    WALL, OPEN, VISITED, PATH,
    COLORS, WP_COLORS, WP_FG,
    CELL_SIZE, ANIM_DELAY,
    GRID_SIZES,
)
from maze import GENERATORS
from algorithms import ALGOS


class MazeApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("maze pathfinder")
        self.root.resizable(False, False)
        self.root.configure(bg="#f8fafc")

        self.grid: list[list[int]] = []
        self.linhas = 21
        self.colunas = 21
        self.pontos: list[tuple[int, int]] = []
        self.retangulos: dict[tuple, int] = {}
        self.textos: dict[tuple, int] = {}

        self._job_animacao: str | None = None
        self._frames_animacao: list = []
        self._indice_animacao = 0

        self._construir_ui()
        self.novo_labirinto()

    # ── construcao da interface ────────────────────────────────────────────────

    def _construir_ui(self) -> None:
        topo = tk.Frame(self.root, bg="#f8fafc", pady=8, padx=12)
        topo.pack(side=tk.TOP, fill=tk.X)

        # linha 1
        linha1 = tk.Frame(topo, bg="#f8fafc")
        linha1.pack(fill=tk.X, pady=(0, 4))

        self._rotulo(linha1, "tamanho:")
        self.var_tamanho = tk.StringVar(value="21×21")
        tamanho_cb = ttk.Combobox(
            linha1, textvariable=self.var_tamanho,
            values=list(GRID_SIZES.keys()),
            width=10, state="readonly", font=("Courier", 11),
        )
        tamanho_cb.pack(side=tk.LEFT, padx=(0, 10))

        self._rotulo(linha1, "tipo de labirinto:")
        self.var_gerador = tk.StringVar(value="DFS recursivo")
        gerador_cb = ttk.Combobox(
            linha1, textvariable=self.var_gerador,
            values=list(GENERATORS.keys()),
            width=17, state="readonly", font=("Courier", 11),
        )
        gerador_cb.pack(side=tk.LEFT, padx=(0, 10))

        self._botao(linha1, "novo labirinto", self.novo_labirinto, "#3b82f6")

        # linha 2
        linha2 = tk.Frame(topo, bg="#f8fafc")
        linha2.pack(fill=tk.X)

        self._rotulo(linha2, "algoritmo:")
        self.var_algoritmo = tk.StringVar(value="A*")
        algoritmo_cb = ttk.Combobox(
            linha2, textvariable=self.var_algoritmo,
            values=list(ALGOS.keys()),
            width=17, state="readonly", font=("Courier", 11),
        )
        algoritmo_cb.pack(side=tk.LEFT, padx=(0, 10))

        self._botao(linha2, "encontrar caminho", self.resolver, "#10b981")
        self._botao(linha2, "limpar pontos", self.limpar_pontos, "#ef4444")
        self._botao(linha2, "limpar caminho", self.limpar_caminho, "#f59e0b")

        # canvas
        frame_canvas = tk.Frame(self.root, bg="#e2e8f0", padx=1, pady=1)
        frame_canvas.pack(padx=12, pady=(6, 8))

        self.canvas = tk.Canvas(frame_canvas, highlightthickness=0, bg=COLORS[WALL])
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.ao_clicar)

        # barra inferior
        base = tk.Frame(self.root, bg="#f1f5f9", pady=6, padx=12)
        base.pack(fill=tk.X)

        self.var_info = tk.StringVar(value="")
        self.var_estat = tk.StringVar(value="")

        tk.Label(base, textvariable=self.var_info, bg="#f1f5f9",
                 fg="#334155", font=("Courier", 11), anchor="w").pack(side=tk.LEFT)
        tk.Label(base, textvariable=self.var_estat, bg="#f1f5f9",
                 fg="#64748b", font=("Courier", 10), anchor="e").pack(side=tk.RIGHT)

    def _rotulo(self, parent, texto: str) -> None:
        tk.Label(parent, text=texto, bg="#f8fafc", fg="#475569",
                 font=("Courier", 11)).pack(side=tk.LEFT, padx=(0, 4))

    def _botao(self, parent, texto: str, comando, cor: str) -> tk.Button:
        b = tk.Button(
            parent, text=texto, command=comando,
            bg=cor, fg="white",
            font=("Courier", 11, "bold"),
            relief=tk.FLAT, padx=10, pady=4,
            cursor="hand2",
            activebackground=cor, activeforeground="white", bd=0,
        )
        b.pack(side=tk.LEFT, padx=4)
        return b

    # ── labirinto ─────────────────────────────────────────────────────────────

    def novo_labirinto(self) -> None:
        self._parar_animacao()
        self.linhas, self.colunas = GRID_SIZES[self.var_tamanho.get()]
        func_gerador = GENERATORS[self.var_gerador.get()]
        self.grid = func_gerador(self.linhas, self.colunas)
        self.pontos = []
        self._redimensionar_canvas()
        self._desenhar_tudo()
        self.var_info.set(
            f"{self.var_gerador.get()} {self.var_tamanho.get()} pronto. clique em celulas abertas para adicionar pontos."
        )
        self.var_estat.set("")

    def _redimensionar_canvas(self) -> None:
        self.canvas.config(
            width=self.colunas * CELL_SIZE,
            height=self.linhas * CELL_SIZE,
        )

    # ── desenho ───────────────────────────────────────────────────────────────

    def _desenhar_tudo(self) -> None:
        self.canvas.delete("all")
        self.retangulos = {}
        self.textos = {}
        for r in range(self.linhas):
            for c in range(self.colunas):
                self._desenhar_celula(r, c)
        self._desenhar_pontos()

    def _celula_xy(self, r: int, c: int) -> tuple[int, int, int, int]:
        x1 = c * CELL_SIZE
        y1 = r * CELL_SIZE
        return x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE

    def _desenhar_celula(self, r: int, c: int) -> None:
        x1, y1, x2, y2 = self._celula_xy(r, c)
        v = self.grid[r][c]
        idx = next(
            (i for i, (pr, pc) in enumerate(self.pontos) if pr == r and pc == c),
            None,
        )
        fill = (
            WP_COLORS[idx % len(WP_COLORS)]
            if idx is not None
            else COLORS.get(v, COLORS[OPEN])
        )
        chave = (r, c)
        if chave in self.retangulos:
            self.canvas.itemconfig(self.retangulos[chave], fill=fill, outline=fill)
        else:
            rid = self.canvas.create_rectangle(
                x1 + 1, y1 + 1, x2 - 1, y2 - 1,
                fill=fill, outline=fill,
            )
            self.retangulos[chave] = rid

    def _desenhar_pontos(self) -> None:
        for tid in self.textos.values():
            self.canvas.delete(tid)
        self.textos = {}
        for i, (r, c) in enumerate(self.pontos):
            self._desenhar_celula(r, c)
            x1, y1, x2, y2 = self._celula_xy(r, c)
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            tid = self.canvas.create_text(
                cx, cy, text=str(i + 1),
                fill=WP_FG, font=("Courier", 10, "bold"),
                tags="ponto",
            )
            self.textos[(r, c)] = tid
            self.canvas.tag_raise(tid)

    def _redesenhar_celula(self, r: int, c: int) -> None:
        self._desenhar_celula(r, c)
        chave = (r, c)
        if chave in self.textos:
            self.canvas.tag_raise(self.textos[chave])

    # ── interacao ─────────────────────────────────────────────────────────────

    def ao_clicar(self, event: tk.Event) -> None:
        if not self.grid:
            return
        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE
        if not (0 <= r < self.linhas and 0 <= c < self.colunas):
            return
        if self.grid[r][c] == WALL:
            return

        existente = next(
            (i for i, (pr, pc) in enumerate(self.pontos) if pr == r and pc == c),
            None,
        )
        if existente is not None:
            self.pontos.pop(existente)
        else:
            self.pontos.append((r, c))

        self._resetar_caminhos()
        self._desenhar_tudo()
        n = len(self.pontos)
        self.var_info.set(f"{n} ponto(s). adicione mais ou clique em encontrar caminho.")
        self.var_estat.set("")

    def limpar_pontos(self) -> None:
        self._parar_animacao()
        self.pontos = []
        self._resetar_caminhos()
        self._desenhar_tudo()
        self.var_info.set("pontos removidos.")
        self.var_estat.set("")

    def limpar_caminho(self) -> None:
        self._parar_animacao()
        self._resetar_caminhos()
        self._desenhar_tudo()
        self.var_info.set("caminho removido.")
        self.var_estat.set("")

    def _resetar_caminhos(self) -> None:
        for r in range(self.linhas):
            for c in range(self.colunas):
                if self.grid[r][c] in (VISITED, PATH):
                    self.grid[r][c] = OPEN

    # ── resolver caminho ──────────────────────────────────────────────────────

    def resolver(self) -> None:
        if len(self.pontos) < 2:
            self.var_info.set("adicione pelo menos 2 pontos primeiro.")
            return

        self._parar_animacao()
        self._resetar_caminhos()
        self._desenhar_tudo()

        func_algoritmo = ALGOS[self.var_algoritmo.get()]
        conjunto_pontos = set(self.pontos)
        todos_visitados: list = []
        caminho_completo: list = []
        custo_total = 0

        for i in range(len(self.pontos) - 1):
            caminho, ordem_visitada = func_algoritmo(
                self.grid, self.pontos[i], self.pontos[i + 1]
            )
            if caminho is None:
                self.var_info.set("nao foi encontrado caminho entre alguns pontos.")
                return
            todos_visitados.extend(ordem_visitada)
            seg = caminho if i == 0 else caminho[1:]
            caminho_completo.extend(seg)
            custo_total += len(caminho) - 1

        conjunto_caminho = set(caminho_completo)

        frames: list[tuple[str, tuple]] = []
        for cel in todos_visitados:
            if cel not in conjunto_pontos and cel not in conjunto_caminho:
                frames.append(("visita", cel))
        for cel in caminho_completo:
            if cel not in conjunto_pontos:
                frames.append(("caminho", cel))

        nome_algoritmo = self.var_algoritmo.get()
        self.var_info.set(
            f"{nome_algoritmo} encontrou caminho passando por {len(self.pontos)} pontos."
        )
        self.var_estat.set(
            f"comprimento: {custo_total} passos | explorado: {len(todos_visitados)} celulas"
        )

        self._frames_animacao = frames
        self._indice_animacao = 0
        self._animar()

    # ── animacao ──────────────────────────────────────────────────────────────

    def _animar(self) -> None:
        if self._indice_animacao >= len(self._frames_animacao):
            return
        lote = max(1, len(self._frames_animacao) // 120)
        for _ in range(lote):
            if self._indice_animacao >= len(self._frames_animacao):
                break
            tipo, (r, c) = self._frames_animacao[self._indice_animacao]
            self.grid[r][c] = VISITED if tipo == "visita" else PATH
            self._redesenhar_celula(r, c)
            self._indice_animacao += 1
        self._job_animacao = self.root.after(ANIM_DELAY, self._animar)

    def _parar_animacao(self) -> None:
        if self._job_animacao:
            self.root.after_cancel(self._job_animacao)
            self._job_animacao = None