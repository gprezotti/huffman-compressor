from core.huffman_node import HuffmanNode
from core.min_heap import MinHeap


class Huffman:
    def __init__(self):
        self.root = None
        self.char_binary_mapping = {}

    def generate_tree(self, mapping):
        queue = MinHeap()
        for char, freq in sorted(mapping.items()):
            if not isinstance(freq, int) or freq <= 0:
                raise ValueError('Frequência inválida')
            queue.insert(HuffmanNode(freq, char))
        if not queue:
            return None
        while len(queue) > 1:
            first = queue.remove_min()
            second = queue.remove_min()
            queue.insert(HuffmanNode(first.freq + second.freq, None, first, second))
        return queue.remove_min()

    def set_binary_code(self, node, code=''):
        if node is None:
            return
        if node.left is None and node.right is None:
            self.char_binary_mapping[node.data] = code or '0'
            return
        self.set_binary_code(node.left, code + '0')
        self.set_binary_code(node.right, code + '1')

    def encode(self, text):
        self.root = None
        self.char_binary_mapping.clear()
        if not text:
            return ''
        mapping = {}
        for char in text:
            mapping[char] = mapping.get(char, 0) + 1
        self.root = self.generate_tree(mapping)
        self.set_binary_code(self.root)
        return ''.join(self.char_binary_mapping[char] for char in text)

    def decode(self, encoded):
        if self.root is None:
            if encoded:
                raise ValueError('Árvore ausente')
            return ''
        if self.root.left is None and self.root.right is None:
            if any(bit != '0' for bit in encoded):
                raise ValueError('Código inválido')
            return self.root.data * len(encoded)
        actual = self.root
        result = []
        for bit in encoded:
            if bit == '0':
                actual = actual.left
            elif bit == '1':
                actual = actual.right
            else:
                raise ValueError('Bit inválido')
            if actual is None:
                raise ValueError('Caminho inválido')
            if actual.left is None and actual.right is None:
                result.append(actual.data)
                actual = self.root
        if actual is not self.root:
            raise ValueError('Sequência binária incompleta')
        return ''.join(result)
