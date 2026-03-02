import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Caminhos dos arquivos
caminho_huffman = r"D:\carto\PDI2\TRABALHO02\tabelas\huffman_lena.csv"
caminho_lzw = r"D:\carto\PDI2\TRABALHO02\tabelas\lzw_lena.csv"

# Ler arquivos
df_huffman = pd.read_csv(caminho_huffman)
df_lzw = pd.read_csv(caminho_lzw)

# Adicionar coluna identificando o algoritmo
df_huffman["Algoritmo"] = "Huffman"
df_lzw["Algoritmo"] = "LZW"

# Manter apenas colunas necessárias
df_huffman = df_huffman[["Lena", "Taxa de Compressão", "Algoritmo"]]
df_lzw = df_lzw[["Lena", "Taxa de Compressão", "Algoritmo"]]

# Concatenar
df_final = pd.concat([df_huffman, df_lzw], ignore_index=True)

# Gráfico
sns.set_theme(style="whitegrid")
plt.figure(figsize=(8, 5))

sns.barplot(
    data=df_final,
    x="Lena",
    y="Taxa de Compressão",
    hue="Algoritmo"
)

plt.title("Comparação da Taxa de Compressão - Lena")
plt.xlabel("Tipo de Imagem")
plt.ylabel("Taxa de Compressão")
plt.legend(title="Algoritmo")

plt.tight_layout()
plt.show()