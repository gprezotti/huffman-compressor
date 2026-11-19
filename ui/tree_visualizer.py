
import tkinter as tk


class TreeVisualizer:
    def __init__(self, root):
        self.root = root
        self.window = None

    def show(self):
        if self.root is None:
            print("Não existe árvore para visualizar.")
            return

        self.window = tk.Toplevel()
        self.window.title("Árvore de Huffman")
        self.window.geometry("1200x700")

        self.canvas = tk.Canvas(
            self.window,
            bg="white",
            scrollregion=(0, 0, 2400, 1400)
        )

        scrollbar_x = tk.Scrollbar(
            self.window,
            orient="horizontal",
            command=self.canvas.xview
        )

        scrollbar_y = tk.Scrollbar(
            self.window,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            xscrollcommand=scrollbar_x.set,
            yscrollcommand=scrollbar_y.set
        )

        scrollbar_x.pack(side="bottom", fill="x")
        scrollbar_y.pack(side="right", fill="y")
        self.canvas.pack(fill="both", expand=True)

        self.draw_node(self.root, 1200, 60, 600)

    def draw_node(self, node, x, y, distance):
        if node is None:
            return

        next_y = y + 100
        next_distance = distance / 2

        if node.left is not None:
            left_x = x - distance

            self.canvas.create_line(
                x, y, left_x, next_y,
                width=2
            )

            self.canvas.create_text(
                (x + left_x) / 2,
                (y + next_y) / 2 - 12,
                text="0",
                fill="blue"
            )

            self.draw_node(
                node.left,
                left_x,
                next_y,
                next_distance
            )

        if node.right is not None:
            right_x = x + distance

            self.canvas.create_line(
                x, y, right_x, next_y,
                width=2
            )

            self.canvas.create_text(
                (x + right_x) / 2,
                (y + next_y) / 2 - 12,
                text="1",
                fill="red"
            )

            self.draw_node(
                node.right,
                right_x,
                next_y,
                next_distance
            )

        radius = 24

        self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill="lightblue",
            outline="black"
        )

        if node.left is None and node.right is None:
            label = f"{repr(node.data)}\n{node.freq}"
        else:
            label = str(node.freq)

        self.canvas.create_text(
            x,
            y,
            text=label,
            font=("Arial", 10)
        )
