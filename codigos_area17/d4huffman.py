import cv2
from dahuffman import HuffmanCodec
import time
import pandas as pd
import numpy as np

# Caminho da imagem (1 imagem)
caminho = r"D:\carto\PDI2\TRABALHO02\imagens_originais\top_mosaic_09cm_area17.tif"

resultados = []

# lê a imagem mantendo os canais (se existir)
img = cv2.imread(caminho, cv2.IMREAD_UNCHANGED)

if img is None:
    raise ValueError(f"Erro ao carregar a imagem: {caminho}")

# Bits originais conforme tipo
if img.ndim == 3 and img.shape[2] >= 3:
    # 3 canais 8-bit -> 24 bpp
    bits_original = img.shape[0] * img.shape[1] * 24
else:
    # 1 canal 8-bit -> 8 bpp
    bits_original = img.size * 8

# Compressão Huffman
inicio = time.perf_counter()

if img.ndim == 3 and img.shape[2] >= 3:
    compressed_bits_total = 0

    for c in range(3):
        canal = img[:, :, c]
        pixels = canal.flatten().tolist()

        codec = HuffmanCodec.from_data(pixels)
        encoded = codec.encode(pixels)

        compressed_bits_total += len(encoded) * 8  # bytes -> bits

    compressed_bits = compressed_bits_total

else:
    pixels = img.flatten().tolist()

    codec = HuffmanCodec.from_data(pixels)
    encoded = codec.encode(pixels)

    compressed_bits = len(encoded) * 8

fim = time.perf_counter()

tempo = fim - inicio
taxa_compressao = bits_original / compressed_bits if compressed_bits > 0 else np.nan

resultados.append({
    "Imagem": "Area17",
    "Tempo (s)": tempo,
    "Bits da Original": bits_original,
    "Bits da Comprimida": compressed_bits,
    "Taxa de Compressão": taxa_compressao
})

df = pd.DataFrame(resultados)

print("\nTabela (Huffman):\n")
print(df)

df.to_csv(r"D:\carto\PDI2\TRABALHO02\tabelas\huffman_area17.csv", index=False)