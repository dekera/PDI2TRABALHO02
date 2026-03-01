import cv2
from dahuffman import HuffmanCodec
import time
import pandas as pd
import numpy as np

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

    # lê a imagem mantendo os canais (BGR se for colorida)
    img = cv2.imread(caminho, cv2.IMREAD_UNCHANGED)

    if img is None:
        print(f"Erro ao carregar {caminho}")
        continue

    # Define bits originais conforme o tipo
    if img.ndim == 3 and img.shape[2] >= 3:
        # RGB (na verdade BGR no OpenCV): 3 canais de 8 bits -> 24 bpp
        bits_original = img.shape[0] * img.shape[1] * 24
    else:
        # grayscale/binária: 8 bpp
        bits_original = img.size * 8

    # Compressão Huffman (por canal se RGB)
    inicio = time.perf_counter()

    if img.ndim == 3 and img.shape[2] >= 3:
        # separa os 3 canais (B, G, R) e comprime cada um
        compressed_bits_total = 0

        for c in range(3):
            canal = img[:, :, c]
            pixels = canal.flatten().tolist()

            codec = HuffmanCodec.from_data(pixels)
            encoded = codec.encode(pixels)

            compressed_bits_total += len(encoded) * 8  # bytes -> bits

        compressed_bits = compressed_bits_total

    else:
        # imagem 1 canal (grayscale/binária)
        canal = img
        pixels = canal.flatten().tolist()

        codec = HuffmanCodec.from_data(pixels)
        encoded = codec.encode(pixels)

        compressed_bits = len(encoded) * 8  # bytes -> bits

    fim = time.perf_counter()

    tempo = fim - inicio
    taxa_compressao = bits_original / compressed_bits if compressed_bits > 0 else np.nan

    resultados.append({
        "Imagem": nomes[i],
        "Tempo (s)": tempo,
        "Bits da Original": bits_original,
        "Bits da Comprimida": compressed_bits,
        "Taxa de Compressão": taxa_compressao
    })

    i += 1

df = pd.DataFrame(resultados)

print("\nTabela Final (Huffman):\n")
print(df)

df.to_csv(r"D:\carto\PDI2\TRABALHO02\tabelas\huffman_lena.csv", index=False)