#!/usr/bin/env python3
import os
import sys
import shutil
import argparse
import subprocess
from PIL import Image, ImageChops

def run_ffmpeg_extract(video_path, output_dir):
    """Trích xuất video thành các frame PNG Lossless"""
    os.makedirs(output_dir, exist_ok=True)
    cmd = ['ffmpeg', '-y', '-i', video_path, os.path.join(output_dir, 'frame_%04d.png')]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_ffmpeg_assemble(frames_dir, output_video_path):
    """Đóng gói các frame PNG thành video Lossless RGB sử dụng libx264rgb và CRF 0"""
    cmd = [
        'ffmpeg', '-y', '-framerate', '30',
        '-i', os.path.join(frames_dir, 'frame_%04d.png'),
        '-c:v', 'libx264rgb', '-crf', '0',
        output_video_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def calculate_frame_difference(img1_path, img2_path):
    """
    TASK 1: Tính toán sai biệt trung bình giữa 2 frame ảnh.
    Gợi ý: Sử dụng ImageChops.difference(img1, img2) để lấy ảnh hiệu số,
    sau đó chuyển về thang xám ("L") và tính giá trị pixel trung bình.
    """
    # TODO: Sinh viên viết mã tại đây
    # 1. Mở hai ảnh img1_path và img2_path bằng Image.open()
    # 2. Sử dụng ImageChops.difference() tính ảnh sai khác
    # 3. Chuyển đổi sang ảnh xám bằng .convert('L')
    # 4. Tính trung bình cộng của toàn bộ pixel bằng sum(diff_gray.getdata()) / tổng số pixel
    pass

def detect_scene_changes(frames_dir, threshold=10.0):
    """
    TASK 2: Duyệt qua tất cả các frame trong thư mục, tính toán sai khác giữa frame(n) và frame(n-1).
    Trả về danh sách đường dẫn tới các frame được chọn làm chuyển cảnh (difference > threshold).
    """
    selected_frames = []
    # Lấy danh sách các file frame ảnh sắp xếp theo thứ tự
    frame_files = sorted([f for f in os.listdir(frames_dir) if f.startswith('frame_')])
    
    # TODO: Sinh viên viết mã tại đây
    # Lặp từ index 1 đến cuối danh sách frame_files
    # Tính sai lệch giữa frame_files[i] và frame_files[i-1] bằng hàm calculate_frame_difference
    # Nếu kết quả > threshold: thêm đường dẫn đầy đủ của frame_files[i] vào selected_frames
    # Lưu ý: Không so sánh frame đầu tiên (frame_0001.png) vì không có frame trước nó.
    
    return selected_frames

def embed_bits_to_frames(selected_frames, message):
    """
    TASK 3: Nhúng chuỗi thông điệp vào LSB của các frame đã được chọn.
    """
    # 1. Chuyển đổi message thành chuỗi bit, nhớ thêm ký tự dừng '\0' vào cuối message
    msg_bytes = (message + '\0').encode('utf-8')
    bits = []
    for byte in msg_bytes:
        for i in range(8):
            bits.append((byte >> (7 - i)) & 1)
            
    num_bits = len(bits)
    bit_idx = 0
    
    # TODO: Sinh viên viết mã tại đây
    # Lặp qua từng frame trong danh sách selected_frames
    # Mở ảnh bằng Image.open(), dùng load() để truy cập mảng pixel
    # Lặp qua từng pixel theo trục y (height) và x (width)
    # Lần lượt sửa LSB của R, G, B bằng bit từ danh sách 'bits' tại chỉ số 'bit_idx'
    # Lưu ý: Dùng phép toán bit (pixel_channel & ~1) | bit để ghi đè LSB
    # Khi bit_idx >= num_bits thì dừng và lưu lại ảnh đã sửa
    
    if bit_idx < num_bits:
        print("[!] CẢNH BÁO: Kích thước các khung cảnh được chọn quá nhỏ không đủ nhúng toàn bộ thông điệp!")
    else:
        print(f"[+] Đã nhúng thành công {num_bits} bits vào video.")

def extract_bits_from_frames(selected_frames):
    """
    TASK 4: Trích xuất bit từ LSB của các pixel trong các frame đã chọn và dựng lại thông điệp.
    Quá trình dừng khi giải mã được ký tự null '\0'.
    """
    bits = []
    
    # TODO: Sinh viên viết mã tại đây
    # Lặp qua từng frame trong danh sách selected_frames
    # Mở ảnh, dùng load() để đọc pixel
    # Lần lượt đọc LSB của R, G, B từ mỗi pixel, thêm vào danh sách 'bits'
    # Cứ mỗi 8 bits gom lại thành 1 byte. Nếu byte đó là 0 (ký tự '\0'), dừng vòng lặp
    # Chuyển đổi mảng bytes thành chuỗi UTF-8 và trả về chuỗi thông điệp trích xuất
    
    return ""

def main():
    parser = argparse.ArgumentParser(description="Scene Difference Steganography Tool")
    parser.add_argument('action', choices=['encode', 'decode'], help="Hành động: encode hoặc decode")
    parser.add_argument('-i', '--input', required=True, help="Video đầu vào (mp4)")
    parser.add_argument('-o', '--output', required=True, help="File đầu ra (video stego cho encode / txt cho decode)")
    parser.add_argument('-m', '--message', help="Thông điệp cần nhúng (chỉ cho encode)")
    parser.add_argument('-t', '--threshold', type=float, default=10.0, help="Ngưỡng sai biệt chuyển cảnh (mặc định: 10.0)")
    args = parser.parse_args()
    
    temp_dir = 'temp_stego_frames'
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    try:
        if args.action == 'encode':
            if not args.message:
                print("Lỗi: Yêu cầu tham số --message (-m) để nhúng dữ liệu!")
                sys.exit(1)
            
            print(f"[*] Đang giải nén video {args.input}...")
            run_ffmpeg_extract(args.input, temp_dir)
            
            print("[*] Đang phân tích chuyển cảnh...")
            selected = detect_scene_changes(temp_dir, args.threshold)
            print(f"[+] Phát hiện {len(selected)} khung cảnh thay đổi vượt ngưỡng {args.threshold}:")
            for f in selected:
                print(f"    - {os.path.basename(f)}")
                
            if not selected:
                print("[!] Lỗi: Không phát hiện chuyển cảnh nào. Hãy giảm ngưỡng threshold!")
                sys.exit(1)
                
            print("[*] Đang tiến hành giấu tin LSB...")
            embed_bits_to_frames(selected, args.message)
            
            print(f"[*] Đang đóng gói video stego lossless {args.output}...")
            run_ffmpeg_assemble(temp_dir, args.output)
            print("[+] Hoàn thành giấu tin!")
            
        elif args.action == 'decode':
            print(f"[*] Đang giải nén video stego {args.input}...")
            run_ffmpeg_extract(args.input, temp_dir)
            
            print("[*] Đang phân tích chuyển cảnh để xác định vị trí nhúng...")
            selected = detect_scene_changes(temp_dir, args.threshold)
            print(f"[+] Tìm thấy {len(selected)} khung cảnh nhúng dữ liệu.")
            
            if not selected:
                print("[!] Lỗi: Không phát hiện vùng giấu tin.")
                sys.exit(1)
                
            print("[*] Đang trích xuất thông điệp bí mật...")
            extracted_msg = extract_bits_from_frames(selected)
            
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(extracted_msg)
            print(f"[+] Đã trích xuất thông điệp và lưu vào {args.output}!")
            
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == '__main__':
    main()
