import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips, CompositeVideoClip, vfx

# Configuration
output_filename = "promo_video.mp4"
resolution = (1280, 720)
font_path = "C:/Windows/Fonts/arial.ttf"

def create_text_image(image_path, text, font_size=50, position="center", duration=5):
    # Load and resize image
    try:
        img = Image.open(image_path).convert("RGBA")
    except Exception as e:
        print(f"Error loading {image_path}: {e}")
        return None
        
    img = img.resize(resolution, Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(img)
    
    # Load Font
    try:
        font = ImageFont.truetype(font_path, font_size)
        # Verify font works
        draw.textbbox((0, 0), "test", font=font)
    except:
        print("Fallback to default font")
        font = ImageFont.load_default()
    
    # Process Text (Simple Centering)
    lines = text.split('\n')
    
    # Calculate total height
    total_height = 0
    line_heights = []
    line_spacing = 15
    
    for line in lines:
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            h = bbox[3] - bbox[1]
        except: # Fallback for older Pillow
            w, h = draw.textsize(line, font=font)
        line_heights.append(h)
        total_height += h + line_spacing
    total_height -= line_spacing
    
    # Determine Y start
    W, H = resolution
    current_y = (H - total_height) / 2
    if position == "bottom":
        current_y = H - total_height - 80
    elif position == "top":
        current_y = 80
    
    # Draw Text
    for i, line in enumerate(lines):
        # Calculate X
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
        except:
            w, h = draw.textsize(line, font=font)
        
        x = (W - w) / 2
        
        # Outline (Black)
        o_range = 3
        outline_color = (0,0,0, 255)
        text_color = (255, 255, 255, 255)
        
        # Draw outline
        for dx in range(-o_range, o_range+1):
            for dy in range(-o_range, o_range+1):
                if dx!=0 or dy!=0:
                    draw.text((x+dx, current_y+dy), line, font=font, fill=outline_color)
        
        # Draw text
        draw.text((x, current_y), line, font=font, fill=text_color)
        
        current_y += line_heights[i] + line_spacing
        
    return np.array(img)

print("Generating Frame 1...")
img1 = create_text_image("video_assets/frame1.png", "Descoperă lumea magică\na culorilor și jocului!", font_size=60)
clip1 = ImageClip(img1).set_duration(5).fadein(0.5)

print("Generating Frame 2...")
img2 = create_text_image("video_assets/frame2.png", "Jocuri interactive\nDesene de colorat • Aventuri digitale", font_size=50, position="bottom")
clip2 = ImageClip(img2).set_duration(10).crossfadein(1.0)

print("Generating Frame 3...")
# For Frame 3 (Zoom), we take the image with text and apply zoom
img3 = create_text_image("video_assets/frame3.png", "Distracție pentru copii,\nliniște pentru părinți!", font_size=50, position="top")
# Create clip
clip3_base = ImageClip(img3).set_duration(10).crossfadein(1.0)
# Apply zoom: 1.0 to 1.15 over 10 seconds
# Using resize with a function of time
# To ensure it stays centered, we might need composite. 
# But let's try simple resize and see if default composition centers it.
clip3 = clip3_base.resize(lambda t : 1 + 0.02 * t) 
# Note: Resize might be slow. 

print("Generating Frame 4...")
img4 = create_text_image("video_assets/frame4.png", "KidsDigitalHub.com\nLocul unde imaginația prinde viață!", font_size=60)
clip4 = ImageClip(img4).set_duration(5).crossfadein(1.0)

print("Compiling Video...")
# Use composite to handle resizing of clip3 (it will exceed 1280x720, so we clip it)
final = concatenate_videoclips([clip1, clip2, clip3, clip4], method="compose")

final.write_videofile(output_filename, fps=24, codec="libx264")
print("Done!")
