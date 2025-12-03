"""
Generate placeholder product images
"""
import os
from PIL import Image, ImageDraw, ImageFont
import random

# Create images directory if it doesn't exist
images_dir = os.path.join(os.path.dirname(__file__), 'frontend', 'images')
os.makedirs(images_dir, exist_ok=True)

# Product configurations with colors and details
products = {
    'laptop.jpg': {
        'name': 'Laptop',
        'emoji': '💻',
        'colors': [(52, 73, 94), (44, 62, 80)],
        'accents': [(41, 128, 185), (52, 152, 219)]
    },
    'mouse.jpg': {
        'name': 'Mouse',
        'emoji': '🖱️',
        'colors': [(52, 73, 94), (44, 62, 80)],
        'accents': [(231, 76, 60), (192, 57, 43)]
    },
    'keyboard.jpg': {
        'name': 'Keyboard',
        'emoji': '⌨️',
        'colors': [(44, 62, 80), (52, 73, 94)],
        'accents': [(46, 204, 113), (39, 174, 96)]
    },
    'monitor.jpg': {
        'name': 'Monitor',
        'emoji': '🖥️',
        'colors': [(52, 73, 94), (44, 62, 80)],
        'accents': [(155, 89, 182), (142, 68, 173)]
    },
    'headphones.jpg': {
        'name': 'Headphones',
        'emoji': '🎧',
        'colors': [(52, 73, 94), (44, 62, 80)],
        'accents': [(230, 126, 34), (211, 84, 0)]
    },
    'webcam.jpg': {
        'name': 'Webcam',
        'emoji': '📷',
        'colors': [(44, 62, 80), (52, 73, 94)],
        'accents': [(22, 160, 133), (26, 188, 156)]
    },
}

def create_product_image(filename, config):
    """Create a product image with gradient background and emoji"""
    # Create image
    img = Image.new('RGB', (400, 400), color=config['colors'][0])
    draw = ImageDraw.Draw(img)
    
    # Draw gradient background
    for y in range(400):
        r = int(config['colors'][0][0] + (config['colors'][1][0] - config['colors'][0][0]) * y / 400)
        g = int(config['colors'][0][1] + (config['colors'][1][1] - config['colors'][0][1]) * y / 400)
        b = int(config['colors'][0][2] + (config['colors'][1][2] - config['colors'][0][2]) * y / 400)
        draw.rectangle([(0, y), (400, y+1)], fill=(r, g, b))
    
    # Draw accent circles/shapes
    accent = config['accents'][0]
    for i in range(3):
        x = random.randint(50, 350)
        y = random.randint(50, 350)
        size = random.randint(20, 60)
        draw.ellipse([(x-size, y-size), (x+size, y+size)], fill=accent, outline=config['accents'][1], width=2)
    
    # Add product name text
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    text = config['name']
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (400 - text_width) // 2
    draw.text((text_x, 30), text, fill=(255, 255, 255), font=font)
    
    # Save image
    filepath = os.path.join(images_dir, filename)
    img.save(filepath)
    print(f"Created: {filepath}")

# Generate all product images
for filename, config in products.items():
    create_product_image(filename, config)

print(f"\n✅ All product images created in {images_dir}")
