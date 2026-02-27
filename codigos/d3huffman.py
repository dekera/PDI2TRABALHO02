import cv2
from dahuffman import HuffmanCodec
import time
import pandas as pd
import numpy as np

# Lista das imagens
imagens = [r"D:\carto\PDI2\TRABALHO02\imagens_originais\lena-Color.png", r"D:\carto\PDI2\TRABALHO02\imagens_geradas\lena_binaria.jpg", r"D:\carto\PDI2\TRABALHO02\imagens_geradas\lena_cinza.jpg"]

resultados = []
nomes= ["RGB", "Binária","Pancromática"]
i=0
for nome in imagens:

    # leitura da imagem em escala de cinza
    img = cv2.imread(nome, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"Erro ao carregar {nome}")
        continue

    pixels = img.flatten().tolist()

    bits_original = img.size * 8  # 8 bits por pixel (grayscale)

    # inicia contagem de tempo
    inicio = time.perf_counter()

    codec = HuffmanCodec.from_data(pixels)
    encoded = codec.encode(pixels)

    fim = time.perf_counter()

    tempo = fim - inicio

    compressed_bits = len(encoded) * 8  # bytes → bits

    taxa_compressao = bits_original / compressed_bits
    bpp = compressed_bits / img.size
    
    resultados.append({
        "Imagem": nomes[i],
        "Tempo (s)": tempo,
        "Taxa de Compressão": taxa_compressao,
        "bpp": bpp,
        "Bits da Original": bits_original,
        "Bits da Comprimida": compressed_bits
    })
    i+=1
# Criar tabela final
df = pd.DataFrame(resultados)

print("\nTabela Final:\n")
print(df)

# salvar CSV (opcional)
df.to_csv(r"D:\carto\PDI2\TRABALHO02\tabelas\huffman_lena.csv", index=False)