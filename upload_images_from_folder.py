import os
import requests

# Configuration
PRESTASHOP_API_URL = "http://localhost:8080/api/images/products/{product_id}"
API_KEY = "API_KEY"  # Replace with your PrestaShop API key
IMAGES_DIR = "images"

def upload_image(product_id, image_path):
    url = PRESTASHOP_API_URL.format(product_id=product_id)
    with open(image_path, 'rb') as img_file:
        files = {'image': img_file}
        response = requests.post(
            url,
            auth=(API_KEY, ''),
            files=files
        )
    return response.status_code, response.text

def main():
    for product_id in os.listdir(IMAGES_DIR):
        product_folder = os.path.join(IMAGES_DIR, product_id)
        if os.path.isdir(product_folder):
            for image_name in os.listdir(product_folder):
                image_path = os.path.join(product_folder, image_name)
                if os.path.isfile(image_path):
                    status, resp = upload_image(product_id, image_path)


if __name__ == "__main__":
    main()