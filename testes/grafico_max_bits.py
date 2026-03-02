import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Caminho do CSV
caminho = r"D:\carto\PDI2\TRABALHO02\tabelas\lzw_limite_9a30_area17.csv"

df = pd.read_csv(caminho)

# Encontrar menor tempo
idx_min = df["Tempo (s)"].idxmin()
min_row = df.loc[idx_min]

# Primeiro sem reset
df_sem_reset = df[df["Qtd. Resets"] == 0]
primeiro_sem_reset = df_sem_reset.iloc[0]

sns.set_theme(style="whitegrid")

fig, ax1 = plt.subplots(figsize=(10, 5))

# ===== Tempo =====
linha_tempo = ax1.plot(
    df["max_bits"],
    df["Tempo (s)"],
    marker="o",
    linewidth=2,
    label="Tempo (s)"
)

ax1.set_xlabel("Limite Máximo de Bits")
ax1.set_ylabel("Tempo de Execução (s)")
ax1.grid(True)

# ===== Taxa =====
ax2 = ax1.twinx()

linha_taxa = ax2.plot(
    df["max_bits"],
    df["Taxa de Compressão"],
    marker="s",
    linewidth=2,
    color="gold",  # amarelo
    label="Taxa de Compressão"
)

ax2.set_ylabel("Taxa de Compressão")
ax2.grid(False)

# ===== Destaques =====
ax1.scatter(
    min_row["max_bits"],
    min_row["Tempo (s)"],
    color="red",
    s=120,
    zorder=6,
    label="Menor tempo (25 bits)"
)

ax1.scatter(
    primeiro_sem_reset["max_bits"],
    primeiro_sem_reset["Tempo (s)"],
    color="green",
    s=120,
    zorder=6,
    label="Primeiro sem reset (21 bits)"
)

plt.title("Tempo e Taxa de Compressão vs Limite Máximo de Bits (LZW)")

# ===== Legenda =====
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()

ax1.legend(
    handles1 + handles2,
    labels1 + labels2,
    loc="center right"  # meio à direita
)

plt.tight_layout()
plt.show()