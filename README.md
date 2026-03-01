---

# Análise Comparativa de Compressão de Imagens

## Implementação dos Métodos de Huffman e LZW

---

## Descrição

Este projeto apresenta a implementação e avaliação comparativa dos algoritmos de compressão sem perdas:

* **Codificação de Huffman**
* **Codificação LZW (Lempel-Ziv-Welch)**

Os métodos foram aplicados a diferentes tipos de imagens digitais, com análise quantitativa baseada em:

* Tempo de execução
* Tamanho original (em bits)
* Tamanho comprimido (em bits)
* Taxa de compressão

---

## Objetivo

Avaliar o desempenho estatístico e computacional dos algoritmos de compressão em:

1. Imagem RGB
2. Imagem em escala de cinza
3. Imagem binária
4. Ortoimagem de alta resolução (`top_mosaic_09cm_area17.tif`)

A comparação considera eficiência de compressão e custo computacional.

---

## Estrutura do Projeto

```
TRABALHO02/
│
├── pixi.toml
├── pixi.lock
├── .pixi/
│
├── codigos_area17/
│   ├── d4huffman.py
│   └── d4LZW.py
│
├── codigos_lena/
│   ├── d3huffman.py
│   ├── d3LZW.py
│   └── d1_d2.py
│
├── imagens_originais/
│   ├── lena-Color.png
│   └── top_mosaic_09cm_area17.tif
│
├── imagens_geradas/
│   ├── lena_binaria.jpg
│   └── lena_cinza.jpg
│
└── tabelas/
    ├── huffman_lena.csv
    ├── lzw_lena.csv
    ├── huffman_area17.csv
    └── lzw_area17.csv
```

---

## Ambiente

O projeto utiliza ambiente isolado via **Pixi**.

### Ativação do ambiente

```bash
pixi shell
```

### Execução dos scripts

```bash
pixi run python codigos_area17/d4huffman.py
pixi run python codigos_area17/d4LZW.py
```

Para os experimentos com a imagem Lena:

```bash
pixi run python codigos_lena/d3huffman.py
pixi run python codigos_lena/d3LZW.py
```

---

## Metodologia

### Tratamento das Imagens RGB

Para imagens RGB, a compressão é realizada **separadamente por canal (R, G, B)**.

A taxa final é obtida pela soma dos bits comprimidos de cada canal.

* RGB → 24 bits por pixel
* Grayscale/Binária → 8 bits por pixel

Essa abordagem preserva a coerência estatística, uma vez que cada canal possui distribuição própria.

---

## Métricas Avaliadas

### 1️ Bits da Imagem Original

[
Bits_{orig} = largura \times altura \times bpp
]

---

### 2️ Bits da Imagem Comprimida

Total de bits produzidos pelo algoritmo.

---

### 3️ Taxa de Compressão

[
Taxa = Bits_original/Bits_{comprimida
]

Interpretação:

* Taxa > 1 → compressão efetiva
* Taxa ≈ 1 → baixa eficiência
* Taxa < 1 → expansão

---

### 4️ Tempo de Execução

Medido com:

```python
time.perf_counter()
```

---

##  Implementação dos Algoritmos

###  Codificação de Huffman

* Implementação baseada na biblioteca `dahuffman`.
* Construção de árvore de prefixos a partir da frequência dos símbolos.
* Compressão estatística ótima para códigos prefixados.

---

### Codificação LZW

* Implementação própria.
* Dicionário inicial com 256 símbolos.
* Crescimento dinâmico do dicionário.
* Cálculo do número mínimo de bits necessários por código.

---

## Saídas

Os resultados são exportados em formato CSV na pasta:

```
/tabelas
```

Formato das tabelas:

| Imagem | Tempo (s) | Bits da Original | Bits da Comprimida | Taxa de Compressão |
| ------ | --------- | ---------------- | ------------------ | ------------------ |

---

## Fundamentação Teórica

* Shannon, C. E. (1948). *A Mathematical Theory of Communication*.
* Gonzalez, R. C., & Woods, R. E. — *Digital Image Processing*.
* Welch, T. A. (1984). *A Technique for High-Performance Data Compression*.

---

## Observações

* Não está sendo considerado o custo de armazenamento do dicionário/cabeçalho.
* A implementação LZW não impõe limite fixo de bits (ex.: 12 bits).
* Resultados podem variar conforme o conteúdo estatístico da imagem.

---

Projeto desenvolvido para disciplina de Processamento Digital de Imagens 2.

---
