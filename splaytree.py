class Node:
    def __init__(self, key, value, left=None, right=None, parent=None, level=0):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self.level = level

    def set_parent_to(self, child):
        if child is not None:
            child.parent = self

    def keep_parent(self):
        self.set_parent_to(self.left)
        self.set_parent_to(self.right)


class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        elem = Node(key, value)
        if self.root is None:
            self.root = elem
            return
        current = self.root
        while True:
            if current.key == elem.key:
                return
            elif current.key < elem.key and current.right is not None:
                current = current.right
            elif current.key < elem.key:
                current.right = elem
                current.keep_parent()
                break
            elif current.key > elem.key and current.left is not None:
                current = current.left
            else:
                current.left = elem
                current.keep_parent()
                break
        self.splay(elem)

    def find(self, key):
        current = self.root
        while current is not None:
            if current.key == key:
                self.splay(current)
                return current
            if key > current.key:
                current = current.right
            else:
                current = current.left
        raise Exception('element was not found')

    def remove(self, key):
        self.find(key)
        if self.root.left is None and self.root.right is None:
            self.root = None
        elif self.root.left is None:
            self.root = self.root.right
            self.root.parent = None
        elif self.root.right is None:
            self.root = self.root.left
            self.root.parent = None
        else:
            left_tree = self.root.left
            self.root = self.root.right
            self.root.parent = None
            current = self.root
            while current.left is not None:
                current = current.left
            current.left = left_tree
            current.keep_parent()

    def rotate(self, node):
        parent = node.parent
        grandpa = parent.parent
        if parent.left == node:
            parent.left = node.right
            node.right = parent
        else:
            parent.right = node.left
            node.left = parent
        node.parent = grandpa
        parent.keep_parent()
        node.keep_parent()
        if grandpa is None:
            self.root = node
        else:
            if grandpa.left == parent:
                grandpa.left = node
            else:
                grandpa.right = node

    def splay(self, node):
        parent = node.parent
        if parent is None:
            return
        grandpa = parent.parent
        if grandpa is None:
            return self.rotate(node)
        if (grandpa.right == parent and parent.right == node) or (grandpa.left == parent and parent.left == node):
            self.rotate(parent)
            self.rotate(node)
        else:
            self.rotate(node)
            self.rotate(node)
        return self.splay(node)

    def _node_printing(self, node):
        self.root.level = 0
        if node != self.root and node is not None:
            node.level = node.parent.level + 1
        if node is not None:
            self._node_printing(node.right)
            print('     ' * node.level + str(node.key))
            self._node_printing(node.left)

    def show(self):
        if self.root is not None:
            self._node_printing(self.root)


if __name__ == '__main__':
    tree = SplayTree()
    tree.insert(5, 34)
    tree.insert(1, 'яблоко')
    tree.insert(2, 'банан')
    tree.insert(6, 456735)
    tree.insert(3, True)
    tree.show()
    print(tree.find(1).value)
    tree.show()
    tree.remove(6)
    tree.show()
