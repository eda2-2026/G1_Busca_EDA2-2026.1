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
