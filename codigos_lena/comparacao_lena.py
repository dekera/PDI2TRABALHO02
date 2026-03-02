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
df_huffman = df_huffman[["Lena", "Tempo (s)", "Algoritmo"]]
df_lzw = df_lzw[["Lena", "Tempo (s)", "Algoritmo"]]

# Concatenar
df_final = pd.concat([df_huffman, df_lzw], ignore_index=True)

# Gráfico
sns.set_theme(style="whitegrid")
plt.figure(figsize=(8, 5))

sns.barplot(
    data=df_final,
    x="Lena",
    y="Tempo (s)",
    hue="Algoritmo"
)

plt.title("Comparação do Tempo (s) - Lena")
plt.xlabel("Tipo de Imagem")
plt.ylabel("Tempo (s)")
plt.legend(title="Algoritmo")

plt.tight_layout()
plt.show()