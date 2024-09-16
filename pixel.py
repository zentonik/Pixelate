from PIL import Image
import requests
from io import BytesIO
import os

def pixelate_image_from_url(image_url, output_image_path, pixel_size):
    response = requests.get(image_url)
    response.raise_for_status() 

    img = Image.open(BytesIO(response.content))

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    small = img.resize(
        (img.width // pixel_size, img.height // pixel_size),
        resample=Image.NEAREST
    )
    result = small.resize(img.size, Image.NEAREST)
 
    try:
        result.save(output_image_path)
        print(f"Image saved as {output_image_path}")
    except ValueError as e:
        print(f"Error saving image: {e}")

def main():
    image_url = input("Enter the URL of the image: ")
    output_path = input("Enter the path to save the pixelated image (e.g., pixelated_output.jpg): ")

    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    if not any(output_path.lower().endswith(ext) for ext in valid_extensions):
        print(f"Invalid file extension. Please use one of the following: {', '.join(valid_extensions)}")
        return
    
    while True:
        try:
            pixel_size = int(input("Enter the pixel size for pixelation: "))
            if pixel_size <= 0:
                raise ValueError("Pixel size must be a positive integer.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a valid number.")

    pixelate_image_from_url(image_url, output_path, pixel_size)

if __name__ == "__main__":
    main()
