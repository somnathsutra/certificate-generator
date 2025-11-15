from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os

# --- CONFIG ---
TEMPLATE_PATH = r"E:/certificate.py/certificate_templates.png.png"   # Full path to template
CSV_FILE = r"E:/certificate.py/names.csv"                      # Full path to names file
OUTPUT_DIR = r"E:/certificate.py/certificates"                 # Output folder

FONT_PATH = r"C:/Windows/Fonts/arial.ttf"   # Arial on Windows
FONT_SIZE = 150
TEXT_Y_POSITION = 600
TEXT_COLOR = "#B87333"   # Copper color


# --- CREATE OUTPUT FOLDER ---
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- LOAD NAMES ---
df = pd.read_csv(CSV_FILE)

# --- GENERATE CERTIFICATES ---
for index, row in df.iterrows():
    name = str(row['Name']).strip()
    print(f"Generating certificate for {name}...")

    # Open template
    try:
        img = Image.open(TEMPLATE_PATH).convert("RGB")
    except FileNotFoundError:
        print("❌ Template file not found. Check TEMPLATE_PATH.")
        break

    draw = ImageDraw.Draw(img)

    # Load font (with fallback)
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except OSError:
        print("⚠️ Font not found, using default font.")
        font = ImageFont.load_default()

    # Center text horizontally
    text_width = draw.textlength(name, font=font)
    image_width = img.width
    x_position = (image_width - text_width) / 2

    # Draw name
    draw.text((x_position, TEXT_Y_POSITION), name, font=font, fill=TEXT_COLOR)

    # Save
    output_path = os.path.join(OUTPUT_DIR, f"{name}.pdf")
    img.save(output_path, "PDF")

print("✅ Done! Certificates are saved in:", OUTPUT_DIR)


