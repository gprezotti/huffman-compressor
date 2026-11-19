from services.compression_service import CompressionService
from ui.tree_visualizer import TreeVisualizer


def main():
    service = CompressionService()

    print('1 - Compactar TXT')
    print('2 - Descompactar HUFF')

    choice = input('Opção: ').strip()

    if choice == '1':
        source = input('Arquivo de entrada: ').strip().strip('"')
        destination = input('Arquivo de saída: ').strip().strip('"')

        result = service.compress_file(source, destination)
        print('Concluído:', result)

        if service.tree_root is not None:
            TreeVisualizer(service.tree_root).show()

    elif choice == '2':
        source = input('Arquivo de entrada: ').strip().strip('"')
        destination = input('Arquivo de saída: ').strip().strip('"')

        result = service.decompress_file(source, destination)
        print('Concluído:', result)

    else:
        print('Opção inválida')


if __name__ == '__main__':
    main()