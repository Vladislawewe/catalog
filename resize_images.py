from PIL import Image
import os

input_dir = 'static/images'
output_dir = 'static/images/resized'
os.makedirs(output_dir, exist_ok=True)

target_size = (300, 450)

for filename in os.listdir(input_dir):
    if filename.endswith('.jpg'):
        img_path = os.path.join(input_dir, filename)
        img = Image.open(img_path)
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        output_path = os.path.join(output_dir, filename)
        img.save(output_path, 'JPEG', quality=85)
        print(f"Обработано: {filename}")

print("Все изображения приведены к 300x450px")