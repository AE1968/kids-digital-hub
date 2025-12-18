import os
import shutil
from moviepy.editor import ImageClip

image_path = "assets/images/promo_family.png"
output_filename = "reclama.mp4"
desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'reclama.mp4')
site_video_path = "assets/videos/kids_digital_hub_promo.mp4"

def generate_video():
    print(f"Loading {image_path}...")
    try:
        clip = ImageClip(image_path).set_duration(15)
        # Pan/Zoom Effect (1.0 -> 1.1) to create life
        clip = clip.resize(lambda t: 1 + 0.005 * t).set_position(('center', 'center'))
        
        print("Rendering Video (15s)...")
        # Preset ultrafast for speed, crf 22 for quality
        clip.write_videofile(output_filename, fps=24, codec="libx264", audio=False, preset='ultrafast')
        
        print(f"Copying to Desktop: {desktop_path}")
        try:
            shutil.copy(output_filename, desktop_path)
            print("Desktop Copy Success.")
        except Exception as e:
            print(f"Desktop Copy Failed: {e}")

        print(f"Copying to Site Assets: {site_video_path}")
        if not os.path.exists(os.path.dirname(site_video_path)):
            os.makedirs(os.path.dirname(site_video_path))
        shutil.copy(output_filename, site_video_path)
        print("Site Assets Copy Success.")
        
    except Exception as e:
        print(f"Video Gen Error: {e}")

if __name__ == "__main__":
    generate_video()
