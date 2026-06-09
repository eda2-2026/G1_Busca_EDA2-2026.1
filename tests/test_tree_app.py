import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tree_app import TreeApp

def test_tree_app_import():
    assert TreeApp is not None
