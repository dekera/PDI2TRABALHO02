import cv2
import numpy as np

# Ler imagem RGB
img = cv2.imread(r"D:\carto\PDI2\TRABALHO02\imagens_originais\lena-Color.png")

# Converter para escala de cinza
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicar limiar de 50%
limiar = 127
_, binaria = cv2.threshold(gray, limiar, 255, cv2.THRESH_BINARY)

# Salvar resultado
cv2.imwrite(r"D:\carto\PDI2\TRABALHO02\imagens_geradas\lena_binaria.jpg", binaria)
cv2.imwrite(r"D:\carto\PDI2\TRABALHO02\imagens_geradas\lena_cinza.jpg", gray)