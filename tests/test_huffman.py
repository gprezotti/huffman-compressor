import tempfile
import unittest
from pathlib import Path
from core.huffman import Huffman
from services.compression_service import CompressionService


class TestHuffman(unittest.TestCase):
    def test_roundtrip_text(self):
        h = Huffman()
        for text in ['', 'BANANA COM CANELA', 'AAAA', 'Olá, mundo!']:
            self.assertEqual(h.decode(h.encode(text)), text)

    def test_roundtrip_file(self):
        samples = [b'', b'A' * 1000, b'BANANA COM CANELA' * 100,
                   'Olá, mundo!\n'.encode('utf-8') * 100, bytes(range(256)) * 4]
        with tempfile.TemporaryDirectory() as directory:
            for i, original in enumerate(samples):
                source = Path(directory) / f'{i}.txt'
                packed = Path(directory) / f'{i}.huff'
                restored = Path(directory) / f'{i}_restored.txt'
                source.write_bytes(original)
                CompressionService().compress_file(source, packed)
                # Outra instância: comprova independência da árvore em memória.
                CompressionService().decompress_file(packed, restored)
                self.assertEqual(restored.read_bytes(), original)

    def test_invalid_file(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'bad.huff'
            source.write_bytes(b'NOT A HUFFMAN FILE')
            with self.assertRaises(ValueError):
                CompressionService().decompress_file(source, Path(directory) / 'out.txt')


if __name__ == '__main__':
    unittest.main()
