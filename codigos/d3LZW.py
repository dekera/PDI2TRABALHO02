import cv2
import time
import pandas as pd
import numpy as np

# LZW (compressão) para sequência de inteiros 0..255
# Retorna: bits_total_comprimidos, quantidade_de_codigo
def lzw_compress_bits(data):
    # inicializa dicionário com todos os símbolos possíveis (0..255)
    dictionary = { (i,): i for i in range(256) }

    next_code = 256  # próximo código disponível (após 0..255)
    max_code = 255   # maior código já usado no dicionário

    w = ()  # sequência atual (tupla)
    codes = []  # lista de códigos gerados

    for k in data:  # percorre cada símbolo da entrada
        wk = w + (k,)  # tenta estender a sequência atual com o símbolo k
        if wk in dictionary:  # se já existe no dicionário
            w = wk  # mantém a sequência maior
        else:
            # emite o código da sequência atual w
            if w != ():
                codes.append(dictionary[w])
            else:
                # caso raro no começo (w vazio), emite o próprio símbolo
                codes.append(dictionary[(k,)])

            # adiciona a nova sequência wk no dicionário
            dictionary[wk] = next_code
            max_code = next_code  # atualiza o maior código
            next_code += 1  # incrementa para o próximo código

            # reinicia w com o símbolo atual
            w = (k,)

    # emite o último w se existir
    if w != ():
        codes.append(dictionary[w])

    # Cálculo de bits comprimidos
    # bits por código cresce conforme o dicionário cresce
    bits_total = 0
    # maior código começa em 255 (8 bits); com 256 precisa de 9 bits, etc.
    for c in codes:
        bits_por_codigo = max(8, int(np.ceil(np.log2(c + 1))))  # bits mínimos para representar c
        bits_total += bits_por_codigo  # soma no total

    return bits_total, len(codes)

# Lista das imagens
imagens = [
    r"D:\carto\PDI2\TRABALHO02\imagens_originais\lena-Color.png",
    r"D:\carto\PDI2\TRABALHO02\imagens_geradas\lena_binaria.jpg",
    r"D:\carto\PDI2\TRABALHO02\imagens_geradas\lena_cinza.jpg"
]

resultados = []
nomes = ["RGB", "Binária", "Pancromática"]
i = 0

for nome in imagens:

    # leitura da imagem em escala de cinza (mantive como você fez)
    img = cv2.imread(nome, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"Erro ao carregar {nome}")
        continue

    pixels = img.flatten().tolist()

    bits_original = img.size * 8  # 8 bits por pixel (grayscale)

    # inicia contagem de tempo
    inicio = time.perf_counter()

    compressed_bits, num_codes = lzw_compress_bits(pixels)

    fim = time.perf_counter()

    tempo = fim - inicio

    taxa_compressao = bits_original / compressed_bits if compressed_bits > 0 else np.nan
    bpp = compressed_bits / img.size

    resultados.append({
        "Imagem": nomes[i],
        "Tempo (s)": tempo,
        "Bits da Original": bits_original,
        "Bits da Comprimida": compressed_bits,
        "Taxa de Compressão": taxa_compressao,
        "Qtd. Códigos LZW": num_codes
    })

    i += 1

# Criar tabela final
df = pd.DataFrame(resultados)

print("\nTabela Final (LZW):\n")
print(df)

# salvar CSV
df.to_csv(r"D:\carto\PDI2\TRABALHO02\tabelas\lzw_lena.csv", index=False)