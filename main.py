from services.compression_service import CompressionService


def main():
    service = CompressionService()
    print('1 - Compactar TXT')
    print('1 - Descompactar HUFF')
    choice = input('Opção: ').strip()
    if choice == '1':
        source = input('Arquivo de entrada: ').strip().strip('"')
        destination = input('Arquivo de saída: ').strip().strip('"')
        result = service.compress_file(source, destination)
    elif choice == '2':
        source = input('Arquivo de entrada: ').strip().strip('"')
        destination = input('Arquivo de saída: ').strip().strip('"')
        result = service.decompress_file(source, destination)
    else:
        print('Opção inválida')
        return
    print('Concluído:', result)


if __name__ == '__main__':
    main()
