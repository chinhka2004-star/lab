# 🎬 Labtainer: Giấu tin trong Video dựa trên sự khác biệt khung cảnh (Scene Difference Steganography)

[![Labtainers](https://img.shields.io/badge/Framework-Labtainers-blue.svg)](https://labtainers.nps.edu/)
[![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange.svg)]()
[![OS](https://img.shields.io/badge/Platform-Ubuntu%20Container-red.svg)]()

Bài thực hành thiết kế môi trường ảo hóa container hoàn chỉnh sử dụng **Labtainers**, giúp sinh viên ngành An toàn thông tin / An ninh mạng tiếp cận phương pháp giấu tin mật mã nâng cao trong truyền thông đa phương tiện.

---

## 📖 1. Giới thiệu lý thuyết
Thông thường, kỹ thuật giấu tin LSB (Least Significant Bit) trên video sẽ nhúng dữ liệu tuần tự vào toàn bộ các frame. Điều này rất dễ bị phát hiện bởi các phân tích thống kê cảm quan hoặc công cụ steganalysis vì nhiễu LSB được phân bố đều.

Phương pháp **Scene Difference Steganography** giải quyết điểm yếu này bằng cách:
1. **Phân tích sai khác động:** So sánh sự khác biệt giữa khung hình $frame(n)$ và $frame(n-1)$.
2. **Nhận diện chuyển cảnh (Scene Change):** Xác định các frame có độ biến động hình ảnh vượt quá ngưỡng `threshold` cho trước (chuyển đổi góc máy, đổi màu nền đột ngột).
3. **Giấu tin chọn lọc:** Chỉ nhúng dữ liệu vào các khung hình chuyển cảnh đã được chọn. Mắt người có xu hướng kém nhạy cảm với các thay đổi vi mô (LSB) ngay tại thời khắc chuyển giao khung cảnh lớn, giúp thông điệp giấu kín cực kỳ bảo mật.

---

## 🛠️ 2. Môi trường bài Lab
- **Hệ điều hành:** Ubuntu Container (Labtainers).
- **Công cụ tích hợp:** `FFmpeg` (xử lý video lossless) và `Pillow (PIL)` trong Python 3 để trích xuất, phân tích pixel và đóng gói.
- **Video mẫu:** Tự động sinh ngẫu nhiên khi sinh viên bắt đầu lab, đảm bảo độc lập và không cần file ngoài.

---

## 🚀 3. Hướng dẫn Deploy & Khởi chạy (Dành cho Giảng viên & Sinh viên)

### Đăng ký bài Lab với Labtainers
Để tích hợp bài lab này từ GitHub vào môi trường Labtainers cục bộ của bạn, chạy lệnh sau trong terminal của máy host Labtainers:

```bash
imodule -a https://github.com/chinhka2004-star/lab
```

### Bắt đầu thực hành
Sau khi đăng ký thành công, sinh viên bắt đầu làm bài bằng lệnh:

```bash
labtainer lab
```

Hệ thống sẽ tự động build Docker image, chạy script `startup.sh` sinh video mẫu và hiển thị Terminal làm bài cho sinh viên.

---

## 📝 4. Nhiệm vụ của Sinh viên (Student Tasks)

* **Tác vụ 1:** Kiểm tra môi trường và tệp video đầu vào `input_video.mp4` bằng `ffprobe` hoặc `ffmpeg`.
* **Tác vụ 2:** Hoàn thiện mã nguồn Python skeleton `stego.py` tại các hàm `TODO`:
  - `calculate_frame_difference`: Tính độ sai biệt pixel trung bình tuyệt đối của kênh màu xám.
  - `detect_scene_changes`: Lọc ra các frame có sai số lớn hơn `threshold`.
  - `embed_bits_to_frames`: Nhúng chuỗi bit của thông điệp (kết thúc bằng `\0`) vào LSB của các kênh RGB.
  - `extract_bits_from_frames`: Trích xuất chuỗi bit từ LSB của pixel đến khi gặp `\0`.
* **Tác vụ 3:** Nhúng mã sinh viên `STUDENT_ID` và thông điệp bí mật vào video stego:
  ```bash
  python3 stego.py encode -i input_video.mp4 -m "STUDENT_ID: SV123456 | Bi mat: Tan cong luc binh minh!" -o stego.mp4 -t 10.0
  ```
* **Tác vụ 4:** Giải mã để trích xuất thông điệp từ `stego.mp4` ra file văn bản, tiến hành đối chứng độ toàn vẹn hình ảnh:
  ```bash
  python3 stego.py decode -i stego.mp4 -o thongdiep.txt -t 10.0
  ```
  Nếu trùng khớp tuyệt đối, ghi nhãn xác thực vào file:
  ```bash
  echo "INTEGRITY_OK" > xacthuc.txt
  ```
* **Tác vụ 5:** Chạy chương trình chấm điểm tự động tại chỗ:
  ```bash
  ./checkwork.sh
  ```

---

## 📊 5. Tiêu chí chấm điểm tự động (Grading Benchmarks)
Hệ thống chấm điểm tự động tích hợp sẵn sẽ quét thư mục làm việc của sinh viên để cho điểm dựa trên cấu hình `results.config` và `goals.config`:

- **40% (40 điểm):** Chạy thành công pipeline encoding bằng script `stego.py` của sinh viên mà không gặp lỗi.
- **30% (30 điểm):** Giải mã (decode) chính xác thông điệp thử nghiệm ngẫu nhiên được nhúng bằng script giải pháp tham chiếu của giảng viên.
- **20% (20 điểm):** Tạo ra file video `stego.mp4` đúng định dạng H.264 Lossless RGB (`libx264rgb`).
- **10% (10 điểm):** Thực hiện so khớp tính toàn vẹn thành công, sinh viên tạo file `xacthuc.txt` và `thongdiep.txt` hợp lệ chứa đúng mã sinh viên.
