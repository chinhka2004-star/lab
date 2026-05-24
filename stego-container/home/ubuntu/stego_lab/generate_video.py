import os
import math
import subprocess
from PIL import Image, ImageDraw

def generate():
    width, height = 320, 240
    fps = 30
    num_frames = 120
    frames_dir = 'temp_orig_frames'
    os.makedirs(frames_dir, exist_ok=True)
    
    print("[*] Đang tự động tạo 120 khung hình cho video mẫu...")
    for i in range(num_frames):
        # Tạo scene change đột ngột tại các mốc khung hình
        if 0 <= i < 30:
            bg_color = (0, 0, 255)      # Blue scene
        elif 30 <= i < 60:
            bg_color = (255, 0, 0)      # Red scene
        elif 60 <= i < 90:
            bg_color = (0, 255, 0)      # Green scene
        else:
            bg_color = (255, 255, 0)    # Yellow scene
            
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Hình tròn chuyển động quỹ đạo mượt mà để sinh chênh lệch pixel nhỏ
        cx = int(width / 2 + 80 * math.cos(2 * math.pi * i / 60))
        cy = int(height / 2 + 60 * math.sin(2 * math.pi * i / 60))
        draw.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(255, 255, 255))
        
        img.save(os.path.join(frames_dir, f"frame_{i:04d}.png"))
        
    print("[*] Đang dùng ffmpeg đóng gói video Lossless RGB (input_video.mp4)...")
    # Sử dụng libx264rgb -crf 0 để bảo toàn bit hoàn hảo
    subprocess.run([
        'ffmpeg', '-y',
        '-framerate', str(fps),
        '-i', os.path.join(frames_dir, 'frame_%04d.png'),
        '-c:v', 'libx264rgb', '-crf', '0',
        'input_video.mp4'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Dọn dẹp các frame ảnh tạm thời
    for f in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f))
    os.rmdir(frames_dir)
    print("[+] Sinh video input_video.mp4 thành công!")

if __name__ == '__main__':
    generate()
