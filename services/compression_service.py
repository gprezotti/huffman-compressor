import struct
from core.huffman import Huffman
from storage.file_handler import FileHandler


class CompressionService:
    MAGIC = b'HUF1'
    HEADER = struct.Struct('>4sHQB')  # assinatura, símbolos distintos, bytes originais, preenchimento
    ENTRY = struct.Struct('>BI')       # valor do byte, frequência
    
    def __init__(self):
        self.tree_root = None

    @staticmethod
    def _pack_bits(bits):
        padding = (-len(bits)) % 8
        bits += '0' * padding
        payload = bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))
        return payload, padding

    @staticmethod
    def _unpack_bits(payload, padding):
        if not 0 <= padding <= 7:
            raise ValueError('Preenchimento inválido')
        if padding and (not payload or payload[-1] & ((1 << padding) - 1)):
            raise ValueError('Bits de preenchimento inválidos')
        bits = ''.join(f'{byte:08b}' for byte in payload)
        return bits[:-padding] if padding else bits

    def compress_file(self, input_path, output_path):
        raw = FileHandler.read_binary(input_path)
        # Codificamos bytes (0..255), preservando inclusive UTF-8 e quebras de linha.
        text = raw.decode('latin-1')
        frequencies = {}
        for byte in raw:
            frequencies[byte] = frequencies.get(byte, 0) + 1

        huffman = Huffman()
        bits = huffman.encode(text)
        self.tree_root = huffman.root
        payload, padding = self._pack_bits(bits)

        header = self.HEADER.pack(self.MAGIC, len(frequencies), len(raw), padding)
        table = b''.join(self.ENTRY.pack(byte, freq)
                         for byte, freq in sorted(frequencies.items()))
        FileHandler.write_binary(output_path, header + table + payload)
        compacted_size = len(header) + len(table) + len(payload)
        return {
            'original_bytes': len(raw),
            'compressed_bytes': compacted_size,
            'encoded_bits': len(bits),
            'padding_bits': padding,
            'reduction_percent': (1 - compacted_size / len(raw)) * 100 if raw else 0.0
        }

    def decompress_file(self, input_path, output_path):
        blob = FileHandler.read_binary(input_path)
        if len(blob) < self.HEADER.size:
            raise ValueError('Arquivo muito curto')
        magic, distinct, original_size, padding = self.HEADER.unpack_from(blob)
        if magic != self.MAGIC or distinct > 256:
            raise ValueError('Arquivo .huff inválido')
        table_end = self.HEADER.size + distinct * self.ENTRY.size
        if len(blob) < table_end:
            raise ValueError('Tabela de frequências incompleta')
        frequencies = {}
        offset = self.HEADER.size
        for _ in range(distinct):
            byte, freq = self.ENTRY.unpack_from(blob, offset)
            offset += self.ENTRY.size
            if byte in frequencies or freq == 0:
                raise ValueError('Tabela de frequências inválida')
            frequencies[byte] = freq
        if sum(frequencies.values()) != original_size:
            raise ValueError('Tamanho original incompatível com a tabela')
        bits = self._unpack_bits(blob[table_end:], padding)
        huffman = Huffman()
        huffman.root = huffman.generate_tree({chr(byte): freq for byte, freq in frequencies.items()})
        text = huffman.decode(bits)
        raw = text.encode('latin-1')
        if len(raw) != original_size:
            raise ValueError('Dados compactados incompletos ou inválidos')
        FileHandler.write_binary(output_path, raw)
        return {'restored_bytes': len(raw)}
