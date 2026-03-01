# Análise de Compressão de Imagens: Huffman e LZW

## Visão Geral

Este projeto implementa e avalia dois algoritmos clássicos de compressão sem perdas:

* Codificação de Huffman
* Codificação LZW (Lempel–Ziv–Welch)

Além da comparação direta entre os métodos, foi realizado um estudo experimental sobre o impacto do tamanho máximo do dicionário no algoritmo LZW, variando de 9 a 30 bits.

A análise considera:

* Taxa de compressão
* Tempo de execução
* Número de reinicializações do dicionário
* Região de estabilização do algoritmo

---

## Objetivos

* Implementar os algoritmos Huffman e LZW para diferentes tipos de imagens.
* Comparar desempenho estatístico e computacional.
* Avaliar a influência do tamanho máximo do dicionário no LZW.
* Identificar o ponto de estabilização do algoritmo.

---

## Estrutura do Projeto

```
TRABALHO02/
│
├── .pixi/
│   ├── envs/
│   ├── pixi.toml
│   └── pixi.lock
│
├── codigos_area17/
│   ├── d4huffman.py
│   └── d4LZW.py
│
├── codigos_lena/
│   ├── d1_d2.py
│   ├── d3huffman.py
│   └── d3LZW.py
│
├── imagens_originais/
│   ├── lena-Color.png
│   └── top_mosaic_09cm_area17.tif
│
├── imagens_geradas/
│   ├── lena_binaria.jpg
│   ├── lena_cinza.jpg
│   └── grafico_maxbits.png
│
├── tabelas/
│   ├── huffman_area17.csv
│   ├── huffman_lena.csv
│   ├── lzw_area17.csv
│   ├── lzw_lena.csv
│   └── lzw_limite_9a30_area17.csv
│
└── testes/
    ├── grafico.py
    └── max_bits.py
```

---

## Ambiente

O projeto utiliza ambiente isolado gerenciado pelo Pixi.

### Ativação do ambiente

```bash
pixi shell
```

### Execução dos códigos

Huffman (Area17):

```bash
pixi run python codigos_area17/d4huffman.py
```

LZW (Area17):

```bash
pixi run python codigos_area17/d4LZW.py
```

Experimento do limite do dicionário (9–30 bits):

```bash
pixi run python testes/max_bits.py
```

Geração do gráfico:

```bash
pixi run python testes/grafico.py
```

---

## Metodologia

### Tratamento de Imagens RGB

Para imagens RGB:

* A compressão é aplicada separadamente em cada canal (R, G e B).
* Os bits comprimidos são somados.
* Considera-se 24 bits por pixel na imagem original.

Para imagens em escala de cinza ou binárias:

* Considera-se 8 bits por pixel.

---

## Métricas Avaliadas

### Bits da Imagem Original

```
Bits_original = largura × altura × bits_por_pixel
```

### Bits da Imagem Comprimida

Total de bits produzidos pelo algoritmo.

### Taxa de Compressão

```
Taxa = Bits_original / Bits_comprimida
```

### Tempo de Execução

Medido utilizando:

```
time.perf_counter()
```

### Quantidade de Reinicializações (LZW)

Número de vezes que o dicionário foi reiniciado ao atingir o tamanho máximo permitido.

---

## Estudo Experimental — Limite do Dicionário no LZW

Foi realizado experimento variando:

```
max_bits ∈ [9, 30]
```

Principais observações:

* 9–11 bits: expansão da imagem devido a alto número de reinicializações.
* 12–20 bits: compressão crescente e redução significativa de resets.
* 21 bits: primeiro ponto sem reinicialização.
* 25 bits: menor tempo observado.
* ≥21 bits: regime estacionário de compressão.

Conclusão experimental:

A partir de 21 bits o algoritmo deixa de reinicializar, entrando em regime estável. Acima desse ponto, o ganho marginal é reduzido.

---

## Resultados

Os resultados são exportados em formato CSV na pasta:

```
/tabelas
```

O gráfico do experimento encontra-se em:

```
/imagens_geradas/grafico_maxbits.png
```

---

## Fundamentação Teórica

* Gonzalez, R. C.; Woods, R. E. Digital Image Processing.

---

## Conclusões Técnicas

* O algoritmo Huffman apresenta comportamento estável para imagens naturais com alta variabilidade.
* O desempenho do LZW depende fortemente do tamanho máximo do dicionário.
* Ortoimagens de alta resolução exigem dicionários maiores para compressão eficiente.
* O custo computacional é significativamente influenciado pelo número de reinicializações.

---
