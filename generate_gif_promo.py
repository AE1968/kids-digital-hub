import os
from PIL import Image, ImageSequence

# Paths
source_img = "assets/images/promo_family.png"
desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'reclama_animata.gif')
site_path = "assets/videos/promo.gif"

def generate_zoom_gif():
    print("Loading image...")
    try:
        base_img = Image.open(source_img).convert("RGBA")
        base_w, base_h = base_img.size
        
        frames = []
        # Create 30 frames for a smooth 2-second loop
        for i in range(30):
            scale = 1.0 + (i * 0.005) # Zoom up to 15%
            new_w = int(base_w * scale)
            new_h = int(base_h * scale)
            
            # Resize
            resized = base_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # Center Crop back to original size
            left = (new_w - base_w) // 2
            top = (new_h - base_h) // 2
            right = left + base_w
            bottom = top + base_h
            
            frame = resized.crop((left, top, right, bottom))
            frames.append(frame)
            
        print(f"Saving GIF to {desktop_path}...")
        frames[0].save(
            desktop_path,
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=50, # 50ms per frame = 20 fps
            loop=0
        )
        print("Success! GIF created.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_zoom_gif()
