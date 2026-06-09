# RootQuest (Tree Visualizer) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement an interactive Red-Black and AVL Tree visualizer named "RootQuest" with a Home Screen to navigate between Maze Pathfinder and RootQuest.

**Architecture:** We will introduce a new `home.py` to act as the main entry point menu. The tree logic and rendering positions will be handled in `trees.py`, and the tree interactive UI in `tree_app.py`. The tree rendering will use Tkinter `Canvas` to draw nodes and edges, assigning coordinates based on depth and position to create a standard binary tree visual layout.

**Tech Stack:** Python 3, Tkinter.

---

### Task 1: Create the Tree Data Structures (AVL & Red-Black)

**Files:**
- Create: `src/trees.py`
- Test: `tests/test_trees.py`

- [ ] **Step 1: Write the failing test for AVL and RB Tree insertion**

```python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from trees import AVLTree, RedBlackTree

def test_avl_tree():
    avl = AVLTree()
    avl.insert(10)
    avl.insert(20)
    avl.insert(30)
    # 20 should be root due to rotation
    assert avl.root is not None
    assert avl.root.value == 20
    assert avl.root.left.value == 10
    assert avl.root.right.value == 30

def test_rb_tree():
    rb = RedBlackTree()
    rb.insert(10)
    rb.insert(20)
    rb.insert(30)
    # 20 should be black root, 10 and 30 red
    assert rb.root is not None
    assert rb.root.value == 20
    assert rb.root.color == "BLACK"
    assert rb.root.left.value == 10
    assert rb.root.left.color == "RED"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_trees.py -v`
Expected: FAIL with "ModuleNotFoundError" or "ImportError"

- [ ] **Step 3: Write minimal implementation**

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1
        self.color = "RED" # For RB Tree

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert_node(self.root, value)

    def _insert_node(self, root, value):
        if not root:
            return Node(value)
        elif value < root.value:
            root.left = self._insert_node(root.left, value)
        else:
            root.right = self._insert_node(root.right, value)

        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        balance = self._get_balance(root)

        # Rotations
        if balance > 1 and value < root.left.value:
            return self._right_rotate(root)
        if balance < -1 and value >= root.right.value: # Assuming >= for duplicates or simple > 
            return self._left_rotate(root)
        if balance > 1 and value >= root.left.value:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)
        if balance < -1 and value < root.right.value:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)
        return root

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _get_height(self, root):
        if not root: return 0
        return root.height

    def _get_balance(self, root):
        if not root: return 0
        return self._get_height(root.left) - self._get_height(root.right)

class RedBlackTree:
    # A simplified implementation for the visualizer.
    # Full RB Tree is complex, let's stick to standard RB rules or Left-Leaning Red-Black (LLRB) for brevity.
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert_node(self.root, value)
        self.root.color = "BLACK"

    def _is_red(self, node):
        if not node: return False
        return node.color == "RED"

    def _insert_node(self, h, value):
        if not h:
            return Node(value)

        if value < h.value:
            h.left = self._insert_node(h.left, value)
        elif value > h.value:
            h.right = self._insert_node(h.right, value)
        else:
            pass # No duplicates

        # LLRB logic
        if self._is_red(h.right) and not self._is_red(h.left):
            h = self._rotate_left(h)
        if self._is_red(h.left) and self._is_red(h.left.left):
            h = self._rotate_right(h)
        if self._is_red(h.left) and self._is_red(h.right):
            self._flip_colors(h)

        return h

    def _rotate_left(self, h):
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = "RED"
        return x

    def _rotate_right(self, h):
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = "RED"
        return x

    def _flip_colors(self, h):
        h.color = "RED"
        h.left.color = "BLACK"
        h.right.color = "BLACK"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_trees.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_trees.py src/trees.py
git commit -m "feat: add AVL and Red-Black tree structures"
```

---

### Task 2: Implement Layout Engine for the Trees

**Files:**
- Modify: `src/trees.py`
- Test: `tests/test_trees.py`

- [ ] **Step 1: Write the failing test**

```python
def test_tree_layout():
    avl = AVLTree()
    avl.insert(10)
    avl.insert(5)
    avl.insert(15)
    
    positions = avl.get_layout(width=800, y_start=50, y_step=60)
    assert len(positions) == 3
    # root at center
    assert positions[10]['x'] == 400
    assert positions[10]['y'] == 50
    # left child
    assert positions[5]['x'] < 400
    assert positions[5]['y'] == 110
    # right child
    assert positions[15]['x'] > 400
    assert positions[15]['y'] == 110
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_trees.py::test_tree_layout -v`
Expected: FAIL with "AttributeError: 'AVLTree' object has no attribute 'get_layout'"

- [ ] **Step 3: Write minimal implementation**

```python
# Add this method to both AVLTree and RedBlackTree (or a common base class)
def get_layout(self, width, y_start=50, y_step=60):
    positions = {}
    if not self.root:
        return positions
    
    def traverse(node, x, y, dx):
        if node.left:
            traverse(node.left, x - dx, y + y_step, dx / 2)
        if node.right:
            traverse(node.right, x + dx, y + y_step, dx / 2)
        color = getattr(node, 'color', '#3b82f6') # Blue for AVL, RB uses its color
        if color == "RED": color = "#ef4444"
        if color == "BLACK": color = "#1e293b"
        positions[node.value] = {'x': x, 'y': y, 'color': color, 'node': node}

    traverse(self.root, width / 2, y_start, width / 4)
    return positions

# Monkey patch or add directly to the classes in src/trees.py
AVLTree.get_layout = get_layout
RedBlackTree.get_layout = get_layout
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_trees.py::test_tree_layout -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/trees.py tests/test_trees.py
git commit -m "feat: add tree layout engine for canvas positioning"
```

---

### Task 3: Build the RootQuest UI (TreeApp)

**Files:**
- Create: `src/tree_app.py`

- [ ] **Step 1: Create a basic Tkinter window test (visual check/smoke test)**

```python
# Create tests/test_tree_app.py just to check import syntax
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tree_app import TreeApp

def test_tree_app_import():
    assert TreeApp is not None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_tree_app.py -v`

- [ ] **Step 3: Write minimal implementation**

```python
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

        tk.Label(topo, text="Tipo de Arvore:", bg="#f8fafc", fg="#475569", font=("Courier", 11)).pack(side=tk.LEFT, padx=(0, 4))
        self.var_tipo = tk.StringVar(value="AVL")
        tipo_cb = ttk.Combobox(topo, textvariable=self.var_tipo, values=["AVL", "Red-Black"], width=10, state="readonly", font=("Courier", 11))
        tipo_cb.pack(side=tk.LEFT, padx=(0, 10))
        tipo_cb.bind("<<ComboboxSelected>>", self._mudar_arvore)

        tk.Label(topo, text="Valor:", bg="#f8fafc", fg="#475569", font=("Courier", 11)).pack(side=tk.LEFT, padx=(0, 4))
        self.entry_valor = tk.Entry(topo, width=8, font=("Courier", 11))
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

```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_tree_app.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/tree_app.py tests/test_tree_app.py
git commit -m "feat: implement RootQuest interactive tree visualization UI"
```

---

### Task 4: Create the Main Menu (Home Screen) and Integrate Both Apps

**Files:**
- Create: `src/home.py`
- Modify: `src/main.py`
- Modify: `src/app.py` (Modify `MazeApp` init to accept a `parent_frame`)

- [ ] **Step 1: Write the Home screen test**

```python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from home import HomeApp
import tkinter as tk

def test_home_app():
    root = tk.Tk()
    app = HomeApp(root)
    assert app.current_frame is not None
```

- [ ] **Step 2: Adapt `MazeApp` to use a Frame instead of `root` directly**

```python
# In src/app.py, modify MazeApp.__init__:
def __init__(self, parent: tk.Tk | tk.Frame) -> None:
    # Instead of self.root = root, do:
    if isinstance(parent, tk.Tk):
        self.root = parent
        self.frame = self.root
        self.root.title("maze pathfinder")
        self.root.resizable(False, False)
        self.root.configure(bg="#f8fafc")
    else:
        self.frame = parent
        self.root = parent.winfo_toplevel()
        
    self.grid: list[list[int]] = []
    # Replace all self.root inside __init__ with self.frame for widgets:
    # e.g., topo = tk.Frame(self.frame, bg="#f8fafc", ...)
```

- [ ] **Step 3: Write `src/home.py` minimal implementation**

```python
import tkinter as tk
from app import MazeApp
from tree_app import TreeApp

class HomeApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Algoritmos EDA2 - 2026.1")
        self.root.geometry("850x650")
        self.root.configure(bg="#1e293b")
        
        self.main_container = tk.Frame(self.root, bg="#1e293b")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.current_frame = None
        self._show_menu()

    def _show_menu(self):
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = tk.Frame(self.main_container, bg="#1e293b")
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        title = tk.Label(self.current_frame, text="ESCOLHA SEU DESAFIO", bg="#1e293b", fg="#fbbf24", font=("Courier", 24, "bold"))
        title.pack(pady=(150, 50))
        
        btn_maze = tk.Button(self.current_frame, text="Maze Pathfinder", command=self._launch_maze, bg="#3b82f6", fg="white", font=("Courier", 16, "bold"), relief=tk.FLAT, padx=20, pady=10, cursor="hand2")
        btn_maze.pack(pady=10)
        
        btn_tree = tk.Button(self.current_frame, text="RootQuest (Tree Visualizer)", command=self._launch_tree, bg="#10b981", fg="white", font=("Courier", 16, "bold"), relief=tk.FLAT, padx=20, pady=10, cursor="hand2")
        btn_tree.pack(pady=10)

    def _launch_maze(self):
        if self.current_frame: self.current_frame.destroy()
        self.current_frame = tk.Frame(self.main_container, bg="#f8fafc")
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        self._add_back_button()
        MazeApp(self.current_frame)

    def _launch_tree(self):
        if self.current_frame: self.current_frame.destroy()
        self.current_frame = tk.Frame(self.main_container, bg="#f8fafc")
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        self._add_back_button()
        TreeApp(self.current_frame)

    def _add_back_button(self):
        nav = tk.Frame(self.current_frame, bg="#cbd5e1", pady=4, padx=8)
        nav.pack(fill=tk.X, side=tk.TOP)
        btn = tk.Button(nav, text="← Voltar ao Menu", command=self._show_menu, bg="#64748b", fg="white", font=("Courier", 10, "bold"), relief=tk.FLAT)
        btn.pack(side=tk.LEFT)
```

- [ ] **Step 4: Update `src/main.py`**

```python
import tkinter as tk
from home import HomeApp

if __name__ == "__main__":
    root = tk.Tk()
    app = HomeApp(root)
    root.mainloop()
```

- [ ] **Step 5: Run tests and test the UI**

Run: `pytest tests/test_home_app.py -v`
Run: `python src/main.py` to ensure visual layout works.

- [ ] **Step 6: Commit**

```bash
git add src/home.py src/main.py src/app.py tests/test_home_app.py
git commit -m "feat: add main menu and integrate RootQuest and MazePathfinder"
```
