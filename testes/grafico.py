import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Caminho do CSV
caminho = r"D:\carto\PDI2\TRABALHO02\tabelas\lzw_limite_9a30_area17.csv"

# Ler dados
df = pd.read_csv(caminho)

# Encontrar menor tempo
idx_min = df["Tempo (s)"].idxmin()
min_row = df.loc[idx_min]

# Encontrar primeiro sem reset
df_sem_reset = df[df["Qtd. Resets"] == 0]
primeiro_sem_reset = df_sem_reset.iloc[0]

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

#  Menor tempo
plt.scatter(
    min_row["max_bits"],
    min_row["Tempo (s)"],
    color="red",
    s=120,
    zorder=5,
    label=f"Menor tempo ({int(min_row['max_bits'])} bits)"
)

#  Primeiro sem reinicialização
plt.scatter(
    primeiro_sem_reset["max_bits"],
    primeiro_sem_reset["Tempo (s)"],
    color="green",
    s=120,
    zorder=5,
    label=f"Primeiro sem reset ({int(primeiro_sem_reset['max_bits'])} bits)"
)

# Ajustes finais
plt.title("Tempo de Execução vs Limite Máximo de Bits (LZW)")
plt.xlabel("Limite Máximo de Bits")
plt.ylabel("Tempo de Execução (s)")
plt.legend()

plt.tight_layout()
plt.show()