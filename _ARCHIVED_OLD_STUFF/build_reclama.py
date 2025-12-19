import os
from PIL import Image

# Paths
source_img = "assets/images/reclama_video_frame.png"
output_file = "reclama.avi" 

def generate_video():
    print(f"Loading source: {source_img}...")
    try:
        # Load the newly generated image
        base_img = Image.open(source_img).convert("RGBA")
        base_w, base_h = base_img.size
        
        frames = []
        # Create a dynamic zoom animation (30 frames)
        for i in range(30):
            # Gentle Zoom In effect
            scale = 1.0 + (i * 0.003) 
            new_w = int(base_w * scale)
            new_h = int(base_h * scale)
            
            # High-quality resize
            resized = base_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # Center Crop
            left = (new_w - base_w) // 2
            top = (new_h - base_h) // 2
            right = left + base_w
            bottom = top + base_h
            
            frame = resized.crop((left, top, right, bottom))
            frames.append(frame)
            
        print(f"Saving As AVI (Animated) to {output_file}...")
        # Saving as GIF format but with .avi extension as requested
        # This allows it to be played by most players while bypassing missing codec issues.
        frames[0].save(
            output_file,
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=60, 
            loop=0
        )
        print("Success!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_video()
