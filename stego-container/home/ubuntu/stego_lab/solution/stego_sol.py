#!/usr/bin/env python3
import os
import sys
import shutil
import argparse
import subprocess
from PIL import Image, ImageChops

def run_ffmpeg_extract(video_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    cmd = ['ffmpeg', '-y', '-i', video_path, os.path.join(output_dir, 'frame_%04d.png')]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_ffmpeg_assemble(frames_dir, output_video_path):
    cmd = [
        'ffmpeg', '-y', '-framerate', '30',
        '-i', os.path.join(frames_dir, 'frame_%04d.png'),
        '-c:v', 'libx264rgb', '-crf', '0',
        output_video_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def calculate_frame_difference(img1_path, img2_path):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    diff = ImageChops.difference(img1, img2)
    diff_gray = diff.convert('L')
    pixels = list(diff_gray.getdata())
    return sum(pixels) / len(pixels)

def detect_scene_changes(frames_dir, threshold=10.0):
    selected_frames = []
    frame_files = sorted([f for f in os.listdir(frames_dir) if f.startswith('frame_')])
    
    for i in range(1, len(frame_files)):
        f1 = os.path.join(frames_dir, frame_files[i-1])
        f2 = os.path.join(frames_dir, frame_files[i])
        diff = calculate_frame_difference(f1, f2)
        if diff > threshold:
            selected_frames.append(f2)
            
    return selected_frames

def embed_bits_to_frames(selected_frames, message):
    msg_bytes = (message + '\0').encode('utf-8')
    bits = []
    for byte in msg_bytes:
        for i in range(8):
            bits.append((byte >> (7 - i)) & 1)
            
    num_bits = len(bits)
    bit_idx = 0
    
    for frame_path in selected_frames:
        if bit_idx >= num_bits:
            break
        img = Image.open(frame_path)
        pixels = img.load()
        width, height = img.size
        
        modified = False
        for y in range(height):
            for x in range(width):
                if bit_idx >= num_bits:
                    break
                r, g, b = pixels[x, y]
                
                if bit_idx < num_bits:
                    r = (r & ~1) | bits[bit_idx]
                    bit_idx += 1
                if bit_idx < num_bits:
                    g = (g & ~1) | bits[bit_idx]
                    bit_idx += 1
                if bit_idx < num_bits:
                    b = (b & ~1) | bits[bit_idx]
                    bit_idx += 1
                    
                pixels[x, y] = (r, g, b)
                modified = True
                
        if modified:
            img.save(frame_path)
            
    if bit_idx < num_bits:
        print("[!] CẢNH BÁO: Không đủ dung lượng nhúng!")
    else:
        print(f"[+] Đã nhúng thành công {num_bits} bits.")

def extract_bits_from_frames(selected_frames):
    bits = []
    byte_list = []
    stop = False
    
    for frame_path in selected_frames:
        if stop:
            break
        img = Image.open(frame_path)
        pixels = img.load()
        width, height = img.size
        
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                
                bits.append(r & 1)
                bits.append(g & 1)
                bits.append(b & 1)
                
                # Gom byte
                while len(bits) >= 8:
                    byte_val = 0
                    for i in range(8):
                        byte_val = (byte_val << 1) | bits[i]
                    bits = bits[8:]
                    
                    if byte_val == 0:
                        stop = True
                        break
                    byte_list.append(byte_val)
                    
                if stop:
                    break
            if stop:
                break
                
    return bytes(byte_list).decode('utf-8', errors='ignore')

def main():
    parser = argparse.ArgumentParser(description="Stego Solution")
    parser.add_argument('action', choices=['encode', 'decode'])
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-m', '--message')
    parser.add_argument('-t', '--threshold', type=float, default=10.0)
    args = parser.parse_args()
    
    temp_dir = 'temp_sol_frames'
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    try:
        if args.action == 'encode':
            run_ffmpeg_extract(args.input, temp_dir)
            selected = detect_scene_changes(temp_dir, args.threshold)
            embed_bits_to_frames(selected, args.message)
            run_ffmpeg_assemble(temp_dir, args.output)
        elif args.action == 'decode':
            run_ffmpeg_extract(args.input, temp_dir)
            selected = detect_scene_changes(temp_dir, args.threshold)
            extracted = extract_bits_from_frames(selected)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(extracted)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == '__main__':
    main()
