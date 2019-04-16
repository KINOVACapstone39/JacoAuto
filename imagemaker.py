from PIL import Image

img = Image.new('RGB', (1080, 1920), color='black')
img.save('black.png')