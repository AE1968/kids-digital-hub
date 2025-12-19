import os
from PIL import Image

# Paths
source_img = "assets/images/promo_family.png"
# Save LOCALLY since Desktop access failed
local_video_path = "reclama_animata.gif"

def generate_zoom_gif():
    print(f"Loading image from {source_img}...")
    try:
        base_img = Image.open(source_img).convert("RGBA")
        base_w, base_h = base_img.size
        
        frames = []
        # Create 30 frames for a smooth animation (Zoom In)
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
        
        print(f"Saving GIF to {local_video_path}...")
        frames[0].save(
            local_video_path,
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=50, # 50ms = 20fps
            loop=0
        )
        print("Success! GIF created in project folder.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_zoom_gif()
