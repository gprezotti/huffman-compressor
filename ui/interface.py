
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from services.compression_service import CompressionService
from ui.tree_visualizer import TreeVisualizer


class HuffmanInterface:
    def __init__(self):
        self.service = CompressionService()

        self.window = tk.Tk()
        self.window.title("Compactador Huffman")
        self.window.geometry("650x500")
        self.window.minsize(500, 350)
        self.window.resizable(False, False)

        self.mode = tk.StringVar(value="compress")
        self.source = tk.StringVar()
        self.destination = tk.StringVar()
        self.result = tk.StringVar(value="Aguardando operação...")

        self.create_widgets()

    def create_widgets(self):
        container = ttk.Frame(self.window)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            container,
            highlightthickness=0
        )
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        frame = ttk.Frame(canvas, padding=25)

        frame_id = canvas.create_window(
            (0, 0),
            window=frame,
            anchor="nw"
        )

        def update_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def resize_frame(event):
            canvas.itemconfigure(frame_id, width=event.width)

        frame.bind("<Configure>", update_scrollregion)
        canvas.bind("<Configure>", resize_frame)

        def scroll(event):
            canvas.yview_scroll(
                int(-event.delta / 120),
                "units"
            )

        canvas.bind_all("<MouseWheel>", scroll)

        ttk.Label(
            frame,
            text="Compactador Huffman",
            font=("Arial", 20, "bold")
        ).pack(pady=(0, 20))

        modes = ttk.Frame(frame)
        modes.pack(pady=10)

        ttk.Radiobutton(
            modes,
            text="Compactar",
            variable=self.mode,
            value="compress",
            command=self.change_mode
        ).pack(side="left", padx=15)

        ttk.Radiobutton(
            modes,
            text="Descompactar",
            variable=self.mode,
            value="decompress",
            command=self.change_mode
        ).pack(side="left", padx=15)

        ttk.Label(frame, text="Arquivo de entrada:").pack(anchor="w")

        input_frame = ttk.Frame(frame)
        input_frame.pack(fill="x", pady=(5, 15))

        ttk.Entry(
            input_frame,
            textvariable=self.source
        ).pack(side="left", fill="x", expand=True)

        ttk.Button(
            input_frame,
            text="Procurar",
            command=self.select_source
        ).pack(side="left", padx=(10, 0))

        ttk.Label(frame, text="Arquivo de saída:").pack(anchor="w")

        output_frame = ttk.Frame(frame)
        output_frame.pack(fill="x", pady=(5, 20))

        ttk.Entry(
            output_frame,
            textvariable=self.destination
        ).pack(side="left", fill="x", expand=True)

        ttk.Button(
            output_frame,
            text="Salvar em",
            command=self.select_destination
        ).pack(side="left", padx=(10, 0))

        ttk.Button(
            frame,
            text="Executar",
            command=self.execute
        ).pack(fill="x", pady=10)

        ttk.Label(
            frame,
            text="Resultado:",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(15, 5))

        ttk.Label(
            frame,
            textvariable=self.result,
            justify="left"
        ).pack(anchor="w")

        self.tree_button = ttk.Button(
            frame,
            text="Visualizar árvore",
            command=self.show_tree,
            state="disabled"
        )
        self.tree_button.pack(pady=20)

    def change_mode(self):
        self.source.set("")
        self.destination.set("")
        self.result.set("Aguardando operação...")
        self.tree_button.config(state="disabled")
        self.service.tree_root = None

    def select_source(self):
        if self.mode.get() == "compress":
            filetypes = [("Arquivos TXT", "*.txt")]
        else:
            filetypes = [("Arquivos Huffman", "*.huff")]

        path = filedialog.askopenfilename(filetypes=filetypes)

        if path:
            self.source.set(path)

            source_path = Path(path)

            if self.mode.get() == "compress":
                destination = source_path.with_suffix(".huff")
            else:
                destination = source_path.with_name(
                    source_path.stem + "_recuperado.txt"
                )

            self.destination.set(str(destination))

    def select_destination(self):
        extension = ".huff" if self.mode.get() == "compress" else ".txt"

        path = filedialog.asksaveasfilename(
            defaultextension=extension,
            filetypes=[(f"Arquivo {extension}", f"*{extension}")]
        )

        if path:
            self.destination.set(path)

    def execute(self):
        source = self.source.get().strip()
        destination = self.destination.get().strip()

        if not source or not destination:
            messagebox.showwarning(
                "Atenção",
                "Selecione os arquivos de entrada e saída."
            )
            return

        self.tree_button.config(state="disabled")
        self.service.tree_root = None

        try:
            if self.mode.get() == "compress":
                result = self.service.compress_file(
                    source, destination
                )

                reduction = result["reduction_percent"]

                reduction_text = (
                    f"{reduction:.2f}%"
                    if result["original_bytes"] > 0
                    else "Não aplicável"
                )

                self.result.set(
                    f"Tamanho original: {result['original_bytes']} bytes\n"
                    f"Tamanho compactado: {result['compressed_bytes']} bytes\n"
                    f"Bits codificados: {result['encoded_bits']}\n"
                    f"Redução: {reduction_text}"
                )

                if self.service.tree_root is not None:
                    self.tree_button.config(state="normal")

            else:
                result = self.service.decompress_file(
                    source, destination
                )

                self.result.set(
                    f"Arquivo recuperado com sucesso!\n"
                    f"Tamanho: {result['restored_bytes']} bytes"
                )

            messagebox.showinfo(
                "Sucesso",
                "Operação concluída com sucesso!"
            )

        except Exception as error:
            self.result.set("Erro durante a operação.")
            messagebox.showerror("Erro", str(error))

    def show_tree(self):
        if self.service.tree_root is not None:
            TreeVisualizer(self.service.tree_root).show()

    def run(self):
        self.window.mainloop()
