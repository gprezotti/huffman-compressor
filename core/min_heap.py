class MinHeap:
    def __init__(self):
        self.heap = []

    def __len__(self):
        return len(self.heap)

    def insert(self, node):
        self.heap.append(node)
        index = len(self.heap) - 1
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[parent].freq <= self.heap[index].freq:
                break
            self.heap[parent], self.heap[index] = self.heap[index], self.heap[parent]
            index = parent

    def remove_min(self):
        if not self.heap:
            raise IndexError('Min-heap vazia')
        minimum = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            index = 0
            while True:
                smallest = index
                left = 2 * index + 1
                right = 2 * index + 2
                if left < len(self.heap) and self.heap[left].freq < self.heap[smallest].freq:
                    smallest = left
                if right < len(self.heap) and self.heap[right].freq < self.heap[smallest].freq:
                    smallest = right
                if smallest == index:
                    break
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
        return minimum
