#!/bin/bash
# Script chấm điểm tự động tại chỗ cho sinh viên

# Điểm số ban đầu
SCORE_ENCODE=0
SCORE_DECODE=0
SCORE_STEGO=0
SCORE_INTEGRITY=0

echo "[*] Bắt đầu chấm điểm tự động bài thực hành Steganography..."

# 1. Kiểm tra tiêu chí 1: Chạy đúng pipeline encoding (40%)
# Thực hiện chạy encode thử nghiệm bằng file stego.py của sinh viên
if [ -f "stego.py" ]; then
    echo "[*] Kiểm tra tính đúng đắn của tính năng ENCODE..."
    python3 stego.py encode -i input_video.mp4 -m "STUDENT_TEST_MESSAGE_123" -o test_stego.mp4 -t 10.0 &> /dev/null
    if [ $? -eq 0 ] && [ -f "test_stego.mp4" ]; then
        SCORE_ENCODE=40
        echo "[+] Tiêu chí 1 đạt: Chạy thành công pipeline encoding (40%)"
    else
        echo "[-] Tiêu chí 1 thất bại: Lỗi chạy encode hoặc không sinh ra video stego thử nghiệm."
    fi
    rm -f test_stego.mp4
else
    echo "[-] Lỗi: Không tìm thấy file stego.py của sinh viên."
fi

# 2. Kiểm tra tiêu chí 2: Decode chính xác thông điệp (30%)
# Sử dụng giải pháp tham chiếu stego_sol.py để nhúng một thông điệp test bí mật,
# sau đó dùng stego.py của sinh viên để giải mã xem có chính xác không.
if [ -f "stego.py" ]; then
    echo "[*] Kiểm tra tính đúng đắn của tính năng DECODE..."
    # Tạo video stego chuẩn từ giải pháp
    python3 solution/stego_sol.py encode -i input_video.mp4 -m "SECRET_FLAG_ABC_XYZ" -o secret_stego.mp4 -t 10.0 &> /dev/null
    
    # Dùng script sinh viên để decode
    python3 stego.py decode -i secret_stego.mp4 -o test_output.txt -t 10.0 &> /dev/null
    if [ -f "test_output.txt" ]; then
        DECODED_TEXT=$(cat test_output.txt)
        if [ "$DECODED_TEXT" = "SECRET_FLAG_ABC_XYZ" ]; then
            SCORE_DECODE=30
            echo "[+] Tiêu chí 2 đạt: Giải mã chính xác thông điệp bí mật (30%)"
        else
            echo "[-] Tiêu chí 2 thất bại: Nội dung giải mã không khớp. Nhận được: '$DECODED_TEXT'"
        fi
    else
        echo "[-] Tiêu chí 2 thất bại: Không sinh ra file kết quả giải mã."
    fi
    rm -f secret_stego.mp4 test_output.txt
fi

# 3. Kiểm tra tiêu chí 3: Tạo file stego.mp4 hợp lệ của sinh viên (20%)
if [ -f "stego.mp4" ]; then
    # Kiểm tra kích thước file stego.mp4 và định dạng qua ffprobe
    ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1 stego.mp4 | grep -q "h264"
    if [ $? -eq 0 ]; then
        SCORE_STEGO=20
        echo "[+] Tiêu chí 3 đạt: Video stego.mp4 hợp lệ (20%)"
    else
        echo "[-] Tiêu chí 3 thất bại: stego.mp4 không đúng định dạng H.264 Lossless RGB."
    fi
else
    echo "[-] Tiêu chí 3 thất bại: Chưa tạo file stego.mp4 trong thư mục làm việc."
fi

# 4. Kiểm tra tiêu chí 4: Integrity check thành công (10%)
if [ -f "thongdiep.txt" ] && [ -f "xacthuc.txt" ]; then
    grep -qi "INTEGRITY_OK" xacthuc.txt
    if [ $? -eq 0 ]; then
        # Kiểm tra chéo xem thongdiep.txt có chứa STUDENT_ID hay không
        grep -q "STUDENT_ID" thongdiep.txt
        if [ $? -eq 0 ]; then
            SCORE_INTEGRITY=10
            echo "[+] Tiêu chí 4 đạt: Integrity check thành công (10%)"
        else
            echo "[-] Tiêu chí 4 thất bại: Nội dung thongdiep.txt không hợp lệ hoặc thiếu STUDENT_ID."
        fi
    else
        echo "[-] Tiêu chí 4 thất bại: File xacthuc.txt không chứa nhãn xác nhận 'INTEGRITY_OK'."
    fi
else
    echo "[-] Tiêu chí 4 thất bại: Chưa hoàn thành trích xuất thongdiep.txt hoặc xác thực xacthuc.txt."
fi

# Tổng kết điểm số
TOTAL_SCORE=$((SCORE_ENCODE + SCORE_DECODE + SCORE_STEGO + SCORE_INTEGRITY))
echo "---------------------------------------------------------"
echo ">>> TỔNG ĐIỂM BÀI LAB: $TOTAL_SCORE / 100 <<<"
echo "---------------------------------------------------------"

# Ghi kết quả vào thư mục log của Labtainer để hệ thống chấm điểm tự động thu thập
mkdir -p /home/ubuntu/.local/result
echo "ENCODE_SCORE=$SCORE_ENCODE" > /home/ubuntu/.local/result/stego.grade
echo "DECODE_SCORE=$SCORE_DECODE" >> /home/ubuntu/.local/result/stego.grade
echo "STEGO_SCORE=$SCORE_STEGO" >> /home/ubuntu/.local/result/stego.grade
echo "INTEGRITY_SCORE=$SCORE_INTEGRITY" >> /home/ubuntu/.local/result/stego.grade
echo "TOTAL_SCORE=$TOTAL_SCORE" >> /home/ubuntu/.local/result/stego.grade
