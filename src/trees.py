class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1
        self.color = "RED" # For RB Tree

class BaseTree:
    def get_layout(self, width, y_start=50, y_step=60):
        positions = {}
        if not hasattr(self, 'root') or not self.root:
            return positions
        
        def traverse(node, x, y, dx):
            if node.left:
                traverse(node.left, x - dx, y + y_step, dx / 2)
            if node.right:
                traverse(node.right, x + dx, y + y_step, dx / 2)
            color = getattr(node, 'color', '#3b82f6') # Blue for AVL, RB uses its color
            if isinstance(self, AVLTree): color = '#3b82f6' # Force blue for AVL since Node defaults to RED
            elif color == "RED": color = "#ef4444"
            elif color == "BLACK": color = "#1e293b"
            positions[node.value] = {'x': x, 'y': y, 'color': color, 'node': node}

        traverse(self.root, width / 2, y_start, width / 4)
        return positions

class AVLTree(BaseTree):
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

class RedBlackTree(BaseTree):
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
