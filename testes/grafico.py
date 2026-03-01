import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Caminho do CSV
caminho = r"D:\carto\PDI2\TRABALHO02\tabelas\lzw_limite_9a30_area17.csv"

# Ler os dados
df = pd.read_csv(caminho)

# Encontrar menor tempo
idx_min = df["Tempo (s)"].idxmin()   # índice do menor tempo
min_row = df.loc[idx_min]            # linha correspondente

# Configuração visual
sns.set_theme(style="whitegrid")

plt.figure(figsize=(9, 5))

# Linha principal
sns.lineplot(
    data=df,
    x="max_bits",
    y="Tempo (s)",
    marker="o",
    color="steelblue"
)

# Destacar o menor tempo em vermelho
plt.scatter(
    min_row["max_bits"],
    min_row["Tempo (s)"],
    color="red",
    s=120,
    zorder=5,
    label=f"Menor tempo ({min_row['max_bits']} bits)"
)

# Ajustes finais
plt.title("Tempo de Execução vs Limite Máximo de Bits (LZW)")
plt.xlabel("Limite Máximo de Bits")
plt.ylabel("Tempo de Execução (s)")
plt.legend()

plt.tight_layout()
plt.show()