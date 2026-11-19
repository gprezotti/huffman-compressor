# Compactador Huffman

Aplicação em **Python** para compactar e descompactar arquivos de texto utilizando o **algoritmo de Huffman**, com interface gráfica desenvolvida em **Tkinter**.

O algoritmo de Huffman foi implementado manualmente, incluindo a construção da árvore binária e o uso de uma *min-heap*. O Tkinter é utilizado apenas na interface e na visualização da árvore.

## Funcionalidades

- Compactação de arquivos `.txt` em arquivos `.huff`.
- Descompactação de arquivos `.huff`, recuperando o conteúdo original.
- Interface gráfica para selecionar arquivos de entrada e saída.
- Visualização da árvore de Huffman, com frequências e arestas identificadas por `0` e `1`.
- Exibição do tamanho original, tamanho compactado, quantidade de bits codificados e redução percentual.
- Preservação dos bytes originais, incluindo textos em UTF-8 e quebras de linha.

## Requisitos

- Python 3 com suporte a Tkinter.
- Nenhuma biblioteca externa de Huffman.

> **Observação:** em algumas instalações do Python, o Tkinter pode precisar ser instalado ou habilitado separadamente.

## Como executar

1. Clone o repositório e acesse a pasta do projeto:

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd huffman_project
   ```

2. Inicie a aplicação:

   ```bash
   python main.py
   ```


3. Na interface, escolha **Compactar** ou **Descompactar**, selecione o arquivo de entrada e defina o destino.
4. Clique em **Executar**. Após uma compactação de arquivo não vazio, use **Visualizar árvore** para abrir a representação gráfica.

## Estrutura do projeto

```text
huffman_project/
├── main.py                       # Ponto de entrada da aplicação
├── core/
│   ├── huffman.py               # Codificação, decodificação e árvore
│   ├── huffman_node.py          # Estrutura dos nós
│   └── min_heap.py              # Fila de prioridade implementada manualmente
├── services/
│   └── compression_service.py   # Fluxo de compactação e descompactação
├── storage/
│   └── file_handler.py         # Leitura e gravação de arquivos
├── ui/
│   ├── interface.py             # Interface principal em Tkinter
│   └── tree_visualizer.py      # Visualização gráfica da árvore
├── tests/
│   └── test_huffman.py          # Testes do algoritmo
└── test_files/              # Arquivos usados nos experimentos
```

## Como funciona

**Compactação:** o programa lê os bytes do arquivo, conta suas frequências, constrói a árvore de Huffman e atribui códigos binários de comprimento variável aos símbolos. Os bits são agrupados em bytes e gravados em um arquivo `.huff`, junto com as informações necessárias à descompactação.

**Descompactação:** o programa lê o cabeçalho e a tabela de frequências do `.huff`, reconstrói a árvore, interpreta os bits codificados e recupera os bytes originais.

O formato `.huff` é **próprio deste projeto** e não garante compatibilidade com outros compactadores.

## Taxa de redução

Para arquivos não vazios, a redução percentual é calculada por:

$
R = \left(1 - \frac{T_c}{T_o}\right) \times 100
$

Em que:

- $T_o$: tamanho original, em bytes;
- $T_c$: tamanho final do arquivo `.huff`, incluindo cabeçalho e metadados.

Um valor **positivo** indica economia de espaço; um valor **negativo** indica que o arquivo compactado ficou maior. Para arquivos vazios, a redução percentual não é aplicável.

## Testes

Os testes podem ser executados a partir da raiz do projeto com:

```bash
python -m unittest discover -s tests
```

Os arquivos em `test_files/` permitem avaliar a compactação com diferentes tamanhos e distribuições de caracteres. Arquivos pequenos podem aumentar de tamanho devido ao espaço ocupado pelos metadados.

## Contexto acadêmico

Projeto desenvolvido para a disciplina de **Teoria dos Grafos**, com foco na aplicação de árvores binárias, filas de prioridade e codificação de Huffman.
