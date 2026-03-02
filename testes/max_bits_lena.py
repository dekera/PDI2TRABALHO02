import cv2  # lê imagens (OpenCV)
import time  # mede tempo de execução
import pandas as pd  # cria tabela final
import numpy as np  # funções numéricas auxiliares

# LZW com LIMITE de bits (max_bits) e RESET do dicionário
# - data: lista de inteiros 0..255
# - max_bits: limite máximo de bits por código (ex: 12)
# Retorna:
#   bits_total_comprimidos: tamanho estimado em bits do fluxo comprimido
#   num_codes: quantidade de códigos emitidos
#   num_resets: quantas vezes o dicionário foi reinicializado
def lzw_compress_bits_limited(data, max_bits):
    max_dict_size = 2 ** max_bits  # tamanho máximo do dicionário permitido (ex: 2^12 = 4096)

    dictionary = {(i,): i for i in range(256)}  # dicionário inicial com símbolos 0..255
    next_code = 256  # próximo código disponível após o dicionário inicial

    w = ()  # sequência corrente (tupla)
    bits_total = 0  # acumulador de bits do fluxo comprimido
    num_codes = 0  # contador de códigos emitidos
    num_resets = 0  # contador de resets do dicionário

    for k in data:  # percorre cada símbolo (pixel) da entrada
        wk = w + (k,)  # tenta estender a sequência w com o símbolo k

        if wk in dictionary:  # se a sequência estendida já existe
            w = wk  # aceita a sequência maior
        else:
            # ---------------------------
            # emite o código de w
            # ---------------------------
            if w != ():  # se w não está vazio
                code_out = dictionary[w]  # código de w
            else:
                code_out = dictionary[(k,)]  # caso inicial: emite o próprio símbolo

            # bits necessários para representar o código emitido no "estado atual"
            # (número mínimo de bits para representar next_code-1)
            current_code_bits = max(8, int(np.ceil(np.log2(next_code))))  # bits atuais do dicionário
            bits_total += current_code_bits  # soma bits do código emitido
            num_codes += 1  # incrementa contador de códigos

            # ---------------------------
            # tenta adicionar wk no dicionário
            # ---------------------------
            if next_code < max_dict_size:  # se ainda cabe no dicionário
                dictionary[wk] = next_code  # adiciona a nova sequência
                next_code += 1  # avança o próximo código
            else:
                # dicionário cheio -> RESET (estratégia prática)
                dictionary = {(i,): i for i in range(256)}  # reinicializa dicionário
                next_code = 256  # reinicializa próximo código
                num_resets += 1  # conta o reset

            w = (k,)  # reinicia w com o símbolo atual

    # ---------------------------
    # emite o último w, se existir
    # ---------------------------
    if w != ():  # se sobrou sequência final
        code_out = dictionary[w]  # obtém o código final
        current_code_bits = max(8, int(np.ceil(np.log2(next_code))))  # bits atuais
        bits_total += current_code_bits  # soma bits do último código
        num_codes += 1  # conta o último código

    return bits_total, num_codes, num_resets  # retorna métricas do LZW

# Executa LZW (com limite) em 1 canal (grayscale) OU em RGB por canal
# - img: matriz numpy lida pelo OpenCV
# Retorna:
#   bits_comprimidos_total, num_codes_total, num_resets_total
def compress_image_lzw_limited(img, max_bits):
    if img.ndim == 3 and img.shape[2] >= 3:  # verifica se é RGB (ou BGR)
        bits_total = 0  # soma de bits nos 3 canais
        codes_total = 0  # soma de códigos nos 3 canais
        resets_total = 0  # soma de resets nos 3 canais

        for c in range(3):  # percorre os 3 canais
            canal = img[:, :, c]  # extrai canal c
            data = canal.flatten().tolist()  # transforma em sequência 1D de símbolos 0..255

            bits_c, codes_c, resets_c = lzw_compress_bits_limited(data, max_bits)  # comprime o canal

            bits_total += bits_c  # acumula bits
            codes_total += codes_c  # acumula códigos
            resets_total += resets_c  # acumula resets

        return bits_total, codes_total, resets_total  # retorna somatórios dos canais

    else:
        data = img.flatten().tolist()  # imagem 1 canal -> sequência 1D
        return lzw_compress_bits_limited(data, max_bits)  # comprime direto

# CONFIG: escolha a imagem aqui
caminho = r"D:\carto\PDI2\TRABALHO02\imagens_originais\lena-Color.png"  # caminho da imagem

# Leitura da imagem (mantendo canais)
img = cv2.imread(caminho, cv2.IMREAD_UNCHANGED)  # lê a imagem mantendo número de canais

if img is None:  # valida se carregou
    raise ValueError(f"Erro ao carregar a imagem: {caminho}")  # interrompe com erro claro

# Bits originais (referência) — 24 bpp para RGB, 8 bpp para 1 canal
if img.ndim == 3 and img.shape[2] >= 3:  # se for RGB
    bits_original = img.shape[0] * img.shape[1] * 24  # 24 bits por pixel
else:
    bits_original = img.size * 8  # 8 bits por pixel

# Experimento automático: max_bits de 9 a 30
resultados = []  # lista de linhas da tabela

for max_bits in range(9, 31):  
    inicio = time.perf_counter()  # inicia o cronômetro

    bits_comprimidos, num_codes, num_resets = compress_image_lzw_limited(img, max_bits)  # comprime com limite

    fim = time.perf_counter()  # termina o cronômetro

    tempo = fim - inicio  # tempo total do experimento para este max_bits
    taxa = bits_original / bits_comprimidos if bits_comprimidos > 0 else np.nan  # taxa de compressão

    resultados.append({  # adiciona uma linha na tabela
        "Imagem": "Lena",
        "max_bits": max_bits,
        "Tempo (s)": tempo,
        "Bits da Original": int(bits_original),
        "Bits da Comprimida": int(bits_comprimidos),
        "Taxa de Compressão": taxa,
        "Qtd. Códigos LZW": int(num_codes),
        "Qtd. Resets": int(num_resets)
    })

# Tabela final + salvar CSV
df = pd.DataFrame(resultados)  # cria DataFrame com os resultados
print("\nTabela Final (LZW limitado 9-30 bits):\n")  # título no terminal
print(df)  # imprime tabela

saida_csv = r"D:\carto\PDI2\TRABALHO02\tabelas\lzw_limite_9a30_lena.csv"  # caminho de saída
df.to_csv(saida_csv, index=False)  # salva CSV
print(f"\nCSV salvo em: {saida_csv}")  # confirma onde salvou