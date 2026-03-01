import os
import json
import cv2
import pytesseract
from PIL import Image
import numpy as np

# -------------------------------
# 1. SET TESSERACT PATH (UPDATE THIS)
# -------------------------------
# Example for Windows:
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# -------------------------------
# 2. DIRECTORY CONFIG
# -------------------------------
PRODUCT_DIR = "../assets/products"
OUTPUT_JSON = "../products.json"

# -------------------------------
# 3. OCR CLEANING FUNCTION
# -------------------------------
def preprocess_image(image_path):
    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    return thresh

# -------------------------------
# 4. TEXT EXTRACTION FUNCTION
# -------------------------------
def extract_text(image_path):
    processed = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed)

    return text.strip()

# -------------------------------
# 5. PARSE NAME + PRICE FROM TEXT
# -------------------------------
def extract_name_and_price(text):
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    name = None
    price = None

    for line in lines:
        line_lower = line.lower()

        if any(x in line_lower for x in ["rs", "₹", "price", "/-"]):
            price = line
        else:
            if name is None:
                name = line

    return name or "Unknown Product", price or "Price Not Found"

# -------------------------------
# 6. MAIN SCRIPT
# -------------------------------
def main():
    products = []

    for file in os.listdir(PRODUCT_DIR):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(PRODUCT_DIR, file)

            print(f"Extracting from: {file}")

            raw_text = extract_text(img_path)
            name, price = extract_name_and_price(raw_text)

            products.append({
                "image": f"assets/products/{file}",
                "name": name,
                "price": price
            })

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4, ensure_ascii=False)

    print("\nExtraction complete! JSON saved as products.json.")

if __name__ == "__main__":
    main()