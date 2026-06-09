import tkinter as tk
from tkinter import ttk
from trees import AVLTree, RedBlackTree

class TreeApp:
    def __init__(self, parent_frame: tk.Frame) -> None:
        self.frame = parent_frame
        self.frame.configure(bg="#f8fafc")
        
        self.tree = AVLTree()
        self.tree_type = "AVL"
        
        self._construir_ui()

    def _construir_ui(self):
        topo = tk.Frame(self.frame, bg="#f8fafc", pady=8, padx=12)
        topo.pack(side=tk.TOP, fill=tk.X)

        tk.Label(topo, text="Tipo de Arvore:", bg="#1e293b", fg="#cbd5e1", font=("Courier", 11)).pack(side=tk.LEFT, padx=(0, 4))
        self.var_tipo = tk.StringVar(value="AVL")
        tipo_cb = ttk.Combobox(topo, textvariable=self.var_tipo, values=["AVL", "Red-Black"], width=10, state="readonly", font=("Courier", 11))
        tipo_cb.pack(side=tk.LEFT, padx=(0, 10))
        tipo_cb.bind("<<ComboboxSelected>>", self._mudar_arvore)

        tk.Label(topo, text="Valor:", bg="#1e293b", fg="#cbd5e1", font=("Courier", 11)).pack(side=tk.LEFT, padx=(0, 4))
        self.entry_valor = tk.Entry(topo, width=8, font=("Courier", 11), bg="#334155", fg="white", insertbackground="white")
        self.entry_valor.pack(side=tk.LEFT, padx=(0, 10))
        self.entry_valor.bind("<Return>", lambda e: self._inserir())

        btn = tk.Button(topo, text="Inserir", command=self._inserir, bg="#10b981", fg="white", font=("Courier", 11, "bold"), relief=tk.FLAT, padx=10, pady=4)
        btn.pack(side=tk.LEFT, padx=4)

        btn_limpar = tk.Button(topo, text="Limpar", command=self._limpar, bg="#ef4444", fg="white", font=("Courier", 11, "bold"), relief=tk.FLAT, padx=10, pady=4)
        btn_limpar.pack(side=tk.LEFT, padx=4)

        frame_canvas = tk.Frame(self.frame, bg="#e2e8f0", padx=1, pady=1)
        frame_canvas.pack(padx=12, pady=(6, 8), fill=tk.BOTH, expand=True)

        self.canvas_width = 800
        self.canvas_height = 500
        self.canvas = tk.Canvas(frame_canvas, width=self.canvas_width, height=self.canvas_height, highlightthickness=0, bg="#ffffff")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def _mudar_arvore(self, event=None):
        self.tree_type = self.var_tipo.get()
        self._limpar()

    def _inserir(self):
        val = self.entry_valor.get()
        if val.isdigit() or (val.startswith('-') and val[1:].isdigit()):
            self.tree.insert(int(val))
            self.entry_valor.delete(0, tk.END)
            self._desenhar_arvore()

    def _limpar(self):
        if self.tree_type == "AVL":
            self.tree = AVLTree()
        else:
            self.tree = RedBlackTree()
        self.canvas.delete("all")

    def _desenhar_arvore(self):
        self.canvas.delete("all")
        if not self.tree.root:
            return
            
        positions = self.tree.get_layout(self.canvas_width)
        r = 15 # radius

        # Draw lines
        for val, pos in positions.items():
            node = pos['node']
            if node.left:
                lpos = positions[node.left.value]
                self.canvas.create_line(pos['x'], pos['y'], lpos['x'], lpos['y'], fill="#94a3b8", width=2)
            if node.right:
                rpos = positions[node.right.value]
                self.canvas.create_line(pos['x'], pos['y'], rpos['x'], rpos['y'], fill="#94a3b8", width=2)

        # Draw nodes
        for val, pos in positions.items():
            x, y, color = pos['x'], pos['y'], pos['color']
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="#ffffff", width=2)
            self.canvas.create_text(x, y, text=str(val), fill="#ffffff", font=("Courier", 10, "bold"))
