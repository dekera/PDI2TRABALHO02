import cv2
import time
import pandas as pd
import numpy as np

# LZW (compressão) para sequência de inteiros 0..255
# Retorna: bits_total_comprimidos, quantidade_de_codigos
def lzw_compress_bits(data):
    dictionary = {(i,): i for i in range(256)}
    next_code = 256
    w = ()
    codes = []

    for k in data:
        wk = w + (k,)
        if wk in dictionary:
            w = wk
        else:
            if w != ():
                codes.append(dictionary[w])
            else:
                codes.append(dictionary[(k,)])

            dictionary[wk] = next_code
            next_code += 1
            w = (k,)

    if w != ():
        codes.append(dictionary[w])

    bits_total = 0
    for c in codes:
        bits_por_codigo = max(8, int(np.ceil(np.log2(c + 1))))
        bits_total += bits_por_codigo

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

for caminho in imagens:

    # lê a imagem mantendo os canais
    img = cv2.imread(caminho, cv2.IMREAD_UNCHANGED)

    if img is None:
        print(f"Erro ao carregar {caminho}")
        continue

    # bits originais
    if img.ndim == 3 and img.shape[2] >= 3:
        bits_original = img.shape[0] * img.shape[1] * 24
    else:
        bits_original = img.size * 8


    # Compressão LZW (por canal se RGB)

    inicio = time.perf_counter()

    if img.ndim == 3 and img.shape[2] >= 3:
        compressed_bits_total = 0
        num_codes_total = 0

        for c in range(3):
            canal = img[:, :, c]
            pixels = canal.flatten().tolist()

            bits_canal, num_codes_canal = lzw_compress_bits(pixels)

            compressed_bits_total += bits_canal
            num_codes_total += num_codes_canal

        compressed_bits = compressed_bits_total
        num_codes = num_codes_total

    else:
        canal = img
        pixels = canal.flatten().tolist()

        compressed_bits, num_codes = lzw_compress_bits(pixels)

    fim = time.perf_counter()

    tempo = fim - inicio
    taxa_compressao = bits_original / compressed_bits if compressed_bits > 0 else np.nan

    resultados.append({
        "Lena": nomes[i],
        "Tempo (s)": tempo,
        "Bits da Original": bits_original,
        "Bits da Comprimida": compressed_bits,
        "Taxa de Compressão": taxa_compressao,
        "Qtd. Códigos LZW": num_codes
    })

    i += 1

df = pd.DataFrame(resultados)

print("\nTabela Final (LZW):\n")
print(df)

df.to_csv(r"D:\carto\PDI2\TRABALHO02\tabelas\lzw_lena.csv", index=False)