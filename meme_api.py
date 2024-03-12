from fastapi import FastAPI, HTTPException, File, UploadFile
from PIL import Image, ImageDraw, ImageFont
import random
import os

# Crear una instancia de FastAPI
app = FastAPI()

# Ruta para generar un meme personalizado
@app.post("/generate-meme/")
async def generate_meme(top_text: str, bottom_text: str, image_file: UploadFile = File(...)):
    # Verificar si el archivo enviado es una imagen
    if image_file.content_type.split('/')[0] != 'image':
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")

    # Guardar la imagen en un archivo temporal
    file_extension = os.path.splitext(image_file.filename)[-1]
    temp_image_path = f"temp_image{file_extension}"
    with open(temp_image_path, "wb") as temp_image:
        temp_image.write(image_file.file.read())

    # Abrir la imagen con Pillow
    img = Image.open(temp_image_path)
    draw = ImageDraw.Draw(img)

    # Definir las dimensiones y el tipo de fuente del texto
    font_path = "arial.ttf"  # Puedes usar una fuente diferente si lo deseas
    font_size = int(min(img.size) / 10)
    font = ImageFont.truetype(font_path, font_size)

    # Calcular las coordenadas del texto superior
    text_width, text_height = draw.textsize(top_text, font=font)
    text_x = (img.width - text_width) / 2
    text_y = img.height * 0.05

    # Dibujar el texto superior en la imagen
    draw.text((text_x, text_y), top_text, fill="white", font=font, align="center")

    # Calcular las coordenadas del texto inferior
    text_width, text_height = draw.textsize(bottom_text, font=font)
    text_x = (img.width - text_width) / 2
    text_y = img.height * 0.95 - text_height

    # Dibujar el texto inferior en la imagen
    draw.text((text_x, text_y), bottom_text, fill="white", font=font, align="center")

    # Guardar la imagen generada
    output_image_path = f"meme{random.randint(1, 100000)}.png"
    img.save(output_image_path)

    # Eliminar el archivo temporal de la imagen
    os.remove(temp_image_path)

    return {"message": "Meme generado exitosamente", "image_path": output_image_path}

# Si ejecutamos este script, podemos ejecutar el servidor de desarrollo con:
# uvicorn nombre_del_archivo:app --reload



