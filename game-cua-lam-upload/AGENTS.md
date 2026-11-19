# Hướng dẫn cho AI khi sửa dự án

- Đọc `README.md` và `VUA_BONG_TOI_GRAPHICS_README.txt` trước khi sửa.
- Game chính là `index.html`; viewer là `vua_bong_toi_anim_viewer.html`.
- Giữ dự án chạy được trong trình duyệt. Tránh thêm framework hoặc dịch vụ ngoài nếu chưa thật sự cần.
- Không xóa hay đổi tên file trong `game-assets/` nếu chưa cập nhật mọi nơi đang tham chiếu đến chúng.
- Giữ nguyên kích thước, tên và alpha của sprite theo quy ước đồ họa hiện có.
- Không ghi API key, mật khẩu, token hoặc thông tin cá nhân vào mã nguồn, HTML, file cấu hình được commit hay câu trả lời của AI.
- Nếu đề xuất tích hợp AI chạy bên trong game, giải thích backend cần thiết và lưu key ở biến môi trường phía máy chủ; không gọi API bí mật trực tiếp từ HTML trên trình duyệt.
- Khi hoàn tất thay đổi, tóm tắt file đã sửa và cách người dùng có thể kiểm tra bằng trình duyệt.
