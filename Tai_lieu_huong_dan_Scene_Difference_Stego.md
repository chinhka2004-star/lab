BÀI THỰC HÀNH: GIẤU TIN TRONG VIDEO DỰA TRÊN SỰ KHÁC BIỆT KHUNG CẢNH
Mục tiêu bài thực hành
Trong bài lab này, sinh viên sẽ tìm hiểu và thực hành kỹ thuật giấu tin trong video sử dụng thuật toán LSB (Least Significant Bit) kết hợp với thuật toán phát hiện sự biến đổi khung cảnh (Scene Difference) nhằm nâng cao tính bí mật và an toàn cho thông tin đa lớp.
Bài lab tập trung hoàn toàn vào việc thực thi tự động hóa hệ thống kịch bản, theo dõi và giám sát sự biến đổi dữ liệu, kiểm tra tính toàn vẹn của tệp tin mang thông điệp ẩn thông qua hệ thống chấm điểm tự động của Labtainer framework.
Kỹ năng đạt được
- Hiểu sâu sắc cấu trúc các khung hình video (video frames) và cơ chế chuyển cảnh (scene change) trong truyền thông đa phương tiện.
- Nắm vững ma trận biểu diễn ảnh RGB, cơ chế tính toán độ sai lệch giữa các khung hình liên tiếp thông qua phép trừ ảnh tuyệt đối trong Pillow (PIL).
- Thực hiện thuần thục quy trình nhúng và bóc tách thông điệp bí mật vào bit LSB của kênh màu RGB của các khung hình đã chọn.
- Kỹ năng kiểm thử tự động bài lab thông qua hệ thống kết xuất tang chứng vật lý tự động của Labtainers.
Yêu cầu đối với sinh viên
- Có kiến thức nền tảng vững chắc về xử lý ảnh số, cấu hình màu RGB và cấu trúc tệp video.
- Có khả năng sử dụng các lệnh điều khiển Linux nâng cao, quản lý gói phần mềm hệ thống hệ điều hành Debian/Ubuntu.
Kiến thức bổ trợ
Hệ thống bài thực hành sử dụng thư viện xử lý ảnh Pillow (PIL) của Python để thực hiện các thao tác toán học trên ma trận pixel của các khung hình, kết hợp với công cụ xử lý đa phương tiện ffmpeg/ffprobe có sẵn trong môi trường Linux để giải nén và đóng gói video lossless.
Thông tin lab
Thông tin
Chi tiết
Tên lab
scenediff-stego
Container
ubuntu
Công cụ chính
python3, pip, pillow, ffmpeg, ffprobe
Phương pháp
Phát hiện chuyển cảnh vi sai ảnh thang xám + Hệ giấu tin LSB RGB Lossless
Dữ liệu đầu vào
Thông điệp văn bản mục tiêu, file video cover gốc ảo

Vấn đề kỹ thuật
1. Thuật toán phát hiện sự biến đổi khung cảnh (Scene Difference)
Phương pháp này so khớp sự sai khác trung bình của ma trận ảnh thang xám của hai khung hình kề nhau $frame(n)$ và $frame(n-1)$. Khi sự sai khác vượt ngưỡng threshold quy định (thường do chuyển đổi góc máy hoặc đổi nền), khung hình đó sẽ được gắn nhãn là khung hình chuyển cảnh. Việc chỉ nhúng dữ liệu vào các khung hình này giúp phân tán thông tin ngẫu nhiên, khiến kẻ tấn công rất khó phân tích thống kê cảm quan.
2. Thuật toán giấu tin LSB trên khung hình video
Kỹ thuật nhúng thông tin vào bit cuối cùng (Least Significant Bit) của mỗi kênh màu đỏ (Red), xanh lá (Green), và xanh dương (Blue) của từng pixel trong khung hình đã chọn. Do biên độ màu chỉ lệch tối đa 1 đơn vị trên dải 0-255, mắt người hoàn toàn không thể nhận diện được sự thay đổi nhiễu này, đảm bảo tính tàng hình hoàn hảo.
Khởi động Lab
Chuẩn bị môi trường hệ thống:
1. Sử dụng lệnh imodule để nạp cấu hình bài thực hành từ kho lưu trữ về hệ thống cục bộ:
imodule https://github.com/chinhka2004-star/lab/raw/main/imodule.tar
2. Di chuyển vào không gian làm việc của sinh viên trong framework Labtainer:
cd ~/labtainer/labtainer-student
3. Biên dịch và xây dựng Docker Image cục bộ cho phòng Lab (Bắt buộc đối với bài Lab tùy chỉnh):
rebuild scenediff-stego
4. Khởi chạy bài lab để kích hoạt container ảo Ubuntu:
labtainer scenediff-stego
Nhiệm vụ
Task 1: Khởi động môi trường và kiểm tra các file thành phần
Bước 1: Sau khi hệ thống kích hoạt container thành công, màn hình xuất hiện dấu nhắc lệnh ubuntu@ubuntu:~$
Bước 2: Sử dụng lệnh liệt kê thư mục để xác minh các file kịch bản lập trình có sẵn:
ls -l
Yêu cầu bắt buộc: Sinh viên kiểm tra thấy sự hiện diện đầy đủ của 3 file lõi: stego.py, generate_video.py, và instructions.txt.
Task 2: Cấu hình môi trường và cài đặt các thư viện ảnh chuyên dụng
Bước 1: Tiến hành cập nhật danh sách các kho lưu trữ phần mềm hệ thống:
sudo apt-get update
Bước 2: Cài đặt thư viện xử lý ảnh Pillow cho Python 3:
sudo apt-get install python3-pillow -y
Bước 3: Cài đặt công cụ ffmpeg để giải nén video:
sudo apt-get install ffmpeg -y
Task 3: Thực thi sinh video mẫu động
Bước 1: Khởi chạy kịch bản sinh video tự động:
python3 generate_video.py
Hệ thống tự động tạo ra 120 khung hình với các chuyển cảnh nhân tạo và hình tròn chuyển động, sau đó dùng FFmpeg đóng gói thành video mẫu lossless.
Bước 2: Kiểm tra sự tồn tại vật lý của file video mẫu bằng lệnh:
ls -l input_video.mp4
Task 4: Thực thi quá trình giấu tin LSB vào khung hình chuyển cảnh (Encode)
Bước 1: Khởi chạy kịch bản nhúng tin stego.py với thông điệp bí mật chứa mã số sinh viên của bạn:
python3 stego.py encode -i input_video.mp4 -m "STUDENT_ID: SV123456 | Bi mat quan su: Tan cong luc binh minh!" -o stego.mp4 -t 10.0
Bước 2: Xác minh tệp tin video mang tin ngụy trang được tạo ra thành công:
ls -l stego.mp4
Task 5: Thực thi bóc tách bit LSB và giải mã thông điệp đầu ra (Decode)
Bước 1: Khởi chạy kịch bản giải mã thông tin để bóc tách thông điệp từ video stego.mp4 ra file văn bản thongdiep.txt:
python3 stego.py decode -i stego.mp4 -o thongdiep.txt -t 10.0
Bước 2: Đọc và hiển thị nội dung file tang chứng giải mã đầu ra để đối chiếu kết quả:
cat thongdiep.txt
Bước 3: Kiểm tra tính toàn vẹn (Integrity Check). Nếu kết quả trùng khớp với chuỗi đã nhúng ban đầu, ghi nhãn xác nhận vào file xác thực:
echo "INTEGRITY_OK" > xacthuc.txt
Kết Thúc Bài Lab
Trước khi kết thúc, sinh viên thực hiện kiểm thử tiến độ chấm điểm tự động bằng cách quay lại Terminal Host và thực thi lệnh giám định:
checkwork scenediff-stego
1. Tại Terminal máy ảo Ubuntu, nhập lệnh thoát:
exit
2. Tại Terminal hệ thống máy Host, gõ lệnh chấm dứt phiên làm việc:
stoplab
Để thực hiện lại bài thực hành từ đầu (Reset toàn bộ cấu hình), sử dụng lệnh cấu hình hệ thống:
labtainer -r scenediff-stego
