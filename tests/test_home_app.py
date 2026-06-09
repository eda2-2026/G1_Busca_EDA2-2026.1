import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from home import HomeApp
import tkinter as tk

def test_home_app():
    root = tk.Tk()
    app = HomeApp(root)
    assert app.current_frame is not None
