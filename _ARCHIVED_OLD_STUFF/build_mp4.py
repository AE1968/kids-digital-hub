import imageio
import numpy as np
from PIL import Image
import os

source = "assets/images/reclama_final.png"
output = "reclama.avi" 

def make_video():
    print(f"Loading image from {source}...")
    try:
        img = Image.open(source).convert("RGB")
        w, h = img.size
        
        # Ensure even dimensions
        if w % 2 != 0: w -= 1
        if h % 2 != 0: h -= 1
        img = img.resize((w, h))
        
        print(f"Rendering 15-second video to {output}...")
        # codec 'libx264' is good, 'pixelformat' yuv420p for compatibility
        writer = imageio.get_writer(output, fps=24, codec='libx264', pixelformat='yuv420p')
        
        # 15 seconds * 24 fps = 360 frames
        total_frames = 360
        
        for i in range(total_frames):
            # Slow, cinematic zoom (10% total zoom over 15s)
            scale = 1.0 + (i / total_frames) * 0.10 
            
            nw = int(w * scale)
            nh = int(h * scale)
            
            # High quality resize
            tmp = img.resize((nw, nh), Image.Resampling.LANCZOS)
            
            # Center Crop to original WxH
            l = (nw - w) // 2
            t = (nh - h) // 2
            tmp = tmp.crop((l, t, l+w, t+h))
            
            writer.append_data(np.array(tmp))
            
            if i % 24 == 0:
                print(f"Rendered {i//24}/15 seconds...")
            
        writer.close()
        print("Success! Video updated to exactly 15 seconds.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    make_video()
