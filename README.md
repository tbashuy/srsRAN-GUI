# srsRAN-GUI

Ứng dụng giao diện đồ họa (GUI) được viết bằng Python và PyQt6 nhằm mục đích đơn giản hóa và tự động hóa quá trình cấu hình, vận hành thiết bị đầu cuối (`srsUE`) trong hệ thống mạng di động 4G/5G mô phỏng.

Ứng dụng giúp loại bỏ thao tác can thiệp thủ công vào file cấu hình `ue.conf`, tự động đồng bộ hóa các thông số bảo mật (IMSI, K, OPc, APN) và khởi chạy tiến trình trực tiếp từ giao diện.

## Yêu cầu hệ thống 

Để ứng dụng có thể hoạt động hoàn chỉnh, máy trạm (Host) bắt buộc phải được cài đặt sẵn các thành phần hạ tầng sau:

1. **Hệ điều hành:** Linux (Khuyến nghị Ubuntu).
2. **Mạng lõi (Core Network):** Đã cài đặt và đang chạy dịch vụ [Open5GS](https://open5gs.org/).
3. **Mạng vô tuyến (RAN):** Phần mềm [srsRAN](https://github.com/srsran/srsRAN_4G) đã được biên dịch thành công.
4. **Môi trường Python:** Python 3.x và công cụ quản lý gói `pip`.

###  Lưu ý đặc biệt về ZeroMQ (ZMQ)
Dự án này sử dụng kết nối vô tuyến ảo qua **ZeroMQ**. Yêu cầu `srsRAN` trên máy chủ phải được biên dịch cùng với thư viện ZMQ. 
* Nếu `srsRAN` được cài đặt mà bỏ qua bước liên kết ZMQ, kết nối mạng sẽ thất bại (Lỗi cổng TCP 2000/2001).
* **Cách khắc phục nếu thiếu ZMQ:** Cần cài đặt gói `libzmq3-dev` (`sudo apt install libzmq3-dev`), sau đó tiến hành `cmake` và `make` lại toàn bộ mã nguồn `srsRAN`.

## Cài đặt

1. Clone kho lưu trữ này về máy:
   ```bash
   git clone <URL_Của_Repository>
   cd <Tên_Thư_Mục_Project>
   ```

2. Cài đặt các thư viện Python cần thiết (PyQt6):
   ```bash
   pip install -r requirements.txt
   ```

##  Hướng dẫn vận hành

Quá trình khởi động mạng cần tuân thủ nghiêm ngặt theo thứ tự: Mạng lõi -> Trạm phát -> Thiết bị đầu cuối (App GUI).

**Bước 1: Cấu hình Mạng lõi (WebUI)**
* Truy cập giao diện quản trị của Open5GS (thường là `http://localhost:3000`).
* Tạo mới hoặc chỉnh sửa thuê bao (Subscriber).
* Ghi nhận lại các thông số: `IMSI`, `Key (K)`, `OPc` (Lưu ý chọn định dạng OPc, không phải OP).
* Đảm bảo phần Session đã được cấp APN (ví dụ: `internet`) và cấu hình được lưu hoàn tất.

**Bước 2: Khởi động Trạm phát vô tuyến (srsENB)**
Mở terminal mới và chạy tiến trình trạm phát (srsENB) qua luồng ZMQ:
```bash
sudo srsenb enb.conf
```
*Đợi đến khi log hệ thống báo trạng thái `Setting frequency...` ổn định.*

**Bước 3: Vận hành Giao diện srsUE Manager**
Mở terminal mới tại thư mục chứa dự án và khởi chạy ứng dụng:
```bash
python3 main.py
```
1. Nhập chính xác các thông số `IMSI`, `K`, `OPc` và `APN` từ Bước 1 vào form giao diện.
2. Nhấn nút **"1. Save Config"** để ứng dụng tự động xử lý Regex và cập nhật vào file `ue.conf` của hệ thống.
3. Nhấn nút **"2. Start srsUE"** để bắt đầu quá trình Attach vào mạng. 
4. Theo dõi log trên terminal để xác nhận trạng thái `Network attach successful` và IP được cấp.

##  Khắc phục sự cố (Troubleshooting)

* **Lỗi `Address already in use`:** Xảy ra khi tiến trình cũ chưa được đóng hoàn toàn, chiếm dụng cổng ZMQ. Xử lý bằng lệnh: `sudo killall -9 srsenb srsue python3`, sau đó khởi động lại từ Bước 2.
* **Lỗi `IndentationError` khi chạy Python:** Kiểm tra lại định dạng thụt lề (spaces/tabs) bên trong file `main.py` nếu có sự thay đổi hoặc sao chép mã nguồn.
* **Lỗi `Attach Reject. Cause= 11`:** Thông số APN cấu hình trên Open5GS WebUI chưa được lưu chính xác hoặc thiết lập sai loại hình mạng. Kiểm tra lại WebUI.
