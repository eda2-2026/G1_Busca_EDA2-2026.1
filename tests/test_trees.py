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
    # 20 should be black root, 10 and 30 black (due to LLRB color flip)
    assert rb.root is not None
    assert rb.root.value == 20
    assert rb.root.color == "BLACK"
    assert rb.root.left.value == 10
    assert rb.root.left.color == "BLACK"

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

