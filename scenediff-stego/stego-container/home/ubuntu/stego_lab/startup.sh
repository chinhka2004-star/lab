#!/bin/bash
# Sinh video đầu vào tự động
python3 /home/ubuntu/stego_lab/generate_video.py

# Đảm bảo quyền thực thi cho các script của sinh viên và kiểm thử
chmod +x /home/ubuntu/stego_lab/stego.py
chmod +x /home/ubuntu/stego_lab/checkwork.sh

echo "========================================================="
echo "  CHÀO MỪNG BẠN ĐẾN VỚI LAB: SCENE DIFFERENCE STEGO"
echo "========================================================="
echo "[*] Video mẫu 'input_video.mp4' đã được sinh tự động."
echo "[*] Hãy mở file 'instructions.txt' để đọc hướng dẫn chi tiết."
echo "========================================================="
