from services.compression_service import CompressionService


def main():
    service = CompressionService()
    choice = input('1 - Compactar TXT\n2 - Descompactar HUFF\nOpção: ').strip()
    source = input('Arquivo de entrada: ').strip().strip('"')
    destination = input('Arquivo de saída: ').strip().strip('"')
    if choice == '1':
        result = service.compress_file(source, destination)
    elif choice == '2':
        result = service.decompress_file(source, destination)
    else:
        print('Opção inválida')
        return
    print('Concluído:', result)


if __name__ == '__main__':
    main()
