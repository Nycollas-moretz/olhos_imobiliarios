import cv2
import pathlib 
import numpy as np
import os

if not pathlib.Path('./img').exists():
    os.makedirs("img")

if not pathlib.Path('./output').exists():
    os.makedirs("output")

output_path = pathlib.Path("./output")
input_path = pathlib.Path("./img")

if not os.listdir(input_path):
    raise ValueError("Pasta vazia para input")

img_1 = input_path / "img_sala.png"

img = cv2.imread(str(img_1))

print(img.shape)

cv2.imwrite(str(output_path / "copia.png"), img)
