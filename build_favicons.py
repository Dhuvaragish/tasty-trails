import os
from PIL import Image, ImageDraw

def main():
    # 1. Load the user's uploaded image
    uploaded_path = r'C:/Users/Dhuvaragish/.gemini/antigravity/brain/52d3be4c-f207-44f0-903d-37db8aa479e3/.user_uploaded/media_1793606694524_189c6b47.png'
    img = Image.open(uploaded_path).convert('RGBA')

    # Crop the exact 55x55 icon box (x from 19 to 74, y from 9 to 64)
    icon_crop = img.crop((19, 9, 74, 64))

    # The corners of the crop in the source image have a cream background (#FFF8EF / ~255, 248, 239).
    # To make a professional favicon that looks crisp on dark and light browser themes,
    # let's mask the outer corners with a clean smooth rounded rectangle mask.
    w, h = icon_crop.size # 55 x 55
    
    # We can create a super-sampled high-res version (512x512)
    # First, let's make the 55x55 transparent at the corners
    # Corner radius is ~13px
    mask_55 = Image.new('L', (w, h), 0)
    draw_mask = ImageDraw.Draw(mask_55)
    draw_mask.rounded_rectangle([0, 0, w - 1, h - 1], radius=13, fill=255)

    # Apply mask
    icon_clean = icon_crop.copy()
    icon_clean.putalpha(mask_55)

    # Also build a pristine high-resolution vector-rendered master at 512x512
    # with antialiased paths matching the exact coordinates:
    master_size = 512
    scale = master_size / 55.0
    master = Image.new('RGBA', (master_size, master_size), (0, 0, 0, 0))
    master_draw = ImageDraw.Draw(master)
    
    # Background burgundy
    bg_color = (109, 30, 46, 255) # #6D1E2E
    gold_color = (217, 164, 65, 255) # #D9A441
    
    radius = 13.0 * scale
    master_draw.rounded_rectangle([0, 0, master_size - 1, master_size - 1], radius=radius, fill=bg_color)
    
    # Draw fork tines
    tine_w = 2.4 * scale
    tine_h = 7.0 * scale
    tine_y = 16.5 * scale
    
    # Left, middle, right tine x positions
    tine_x_coords = [16.0 * scale, 21.0 * scale, 26.0 * scale]
    for tx in tine_x_coords:
        # Pill tine
        master_draw.rounded_rectangle([tx, tine_y, tx + tine_w, tine_y + tine_h], radius=tine_w/2, fill=gold_color)
        
    # Fork base & curve
    # Points for the lower fork bowl and handle
    base_left = 16.0 * scale
    base_right = 26.0 * scale + tine_w
    base_top = 23.0 * scale
    base_bottom = 29.5 * scale
    handle_x = 21.3 * scale
    handle_w = 2.4 * scale
    handle_bottom = 40.0 * scale
    
    # Bowl polygon/curves
    bowl_pts = [
        (base_left, base_top),
        (base_right, base_top),
        (base_right, base_top + 2.5 * scale),
        (handle_x + handle_w + 1.5 * scale, base_bottom),
        (handle_x + handle_w, base_bottom),
        (handle_x + handle_w, handle_bottom),
        (handle_x, handle_bottom),
        (handle_x, base_bottom),
        (handle_x - 1.5 * scale, base_bottom),
        (base_left, base_top + 2.5 * scale),
    ]
    master_draw.polygon(bowl_pts, fill=gold_color)
    # Round the handle bottom
    master_draw.ellipse([handle_x, handle_bottom - handle_w/2, handle_x + handle_w, handle_bottom + handle_w/2], fill=gold_color)
    
    # Knife
    # Spine at x = 37.5 * scale
    knife_spine_x = 37.5 * scale
    knife_tip_y = 15.5 * scale
    knife_bolster_y = 29.5 * scale
    knife_belly_x = 32.5 * scale
    knife_belly_mid_y = 25.5 * scale
    knife_handle_w = 2.7 * scale
    knife_handle_x = knife_spine_x - knife_handle_w
    
    knife_pts = [
        (knife_spine_x, knife_tip_y),
        (knife_spine_x, handle_bottom),
        (knife_handle_x, handle_bottom),
        (knife_handle_x, knife_bolster_y),
        (knife_belly_x, knife_bolster_y),
        (knife_belly_x, knife_belly_mid_y),
        (knife_belly_x + 1.5 * scale, 20.0 * scale),
        (knife_spine_x - 0.5 * scale, knife_tip_y),
    ]
    master_draw.polygon(knife_pts, fill=gold_color)
    master_draw.ellipse([knife_handle_x, handle_bottom - knife_handle_w/2, knife_spine_x, handle_bottom + knife_handle_w/2], fill=gold_color)

    # Produce outputs:
    dest_dirs = ['images', 'Tasty-Trails/images']
    for d in dest_dirs:
        os.makedirs(d, exist_ok=True)
    
    # High-res PNGs
    sizes = {
        'favicon-16x16.png': (16, 16),
        'favicon-32x32.png': (32, 32),
        'favicon-48x48.png': (48, 48),
        'apple-touch-icon.png': (180, 180),
        'favicon.png': (192, 192),
    }

    for name, sz in sizes.items():
        resized = master.resize(sz, Image.Resampling.LANCZOS)
        for d in dest_dirs:
            resized.save(os.path.join(d, name))
            
    # Save multi-size favicon.ico (16, 32, 48) in root and images
    ico_targets = ['favicon.ico', 'images/favicon.ico', 'Tasty-Trails/favicon.ico', 'Tasty-Trails/images/favicon.ico']
    for t in ico_targets:
        master.save(t, format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
        
    print("Successfully generated all favicon assets!")

if __name__ == '__main__':
    main()
