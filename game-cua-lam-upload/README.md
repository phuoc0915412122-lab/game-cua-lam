# Vua Bóng Tối — Pixel Arena

Dự án game pixel art chạy trực tiếp trên trình duyệt. Mục tiêu của repository này là tập hợp mã game, công cụ xem hoạt ảnh và bộ đồ họa để mọi người cùng phát triển.

## Chạy game

Mở `index.html` bằng trình duyệt hiện đại. Game hiện là một trang HTML độc lập, không cần cài đặt thư viện.

## Xem hoạt ảnh nhân vật

Mở `vua_bong_toi_anim_viewer.html`. Bộ asset đã giải nén nằm trong `game-assets/`; nếu trình duyệt chặn tải file khi mở trực tiếp, chạy máy chủ tĩnh:

```powershell
py -m http.server 8000
```

Sau đó mở `http://localhost:8000/vua_bong_toi_anim_viewer.html`.

## Cấu trúc

- `index.html`: game Pixel Arena.
- `vua_bong_toi_anim_viewer.html`: trình xem hoạt ảnh.
- `game-assets/`: sprite, hiệu ứng và dữ liệu hoạt ảnh (giải nén từ ZIP).
- `scratch/`: script Python dựng/chỉnh sửa đồ họa và hoạt ảnh.
- `VUA_BONG_TOI_GRAPHICS_README.txt`: mô tả bộ đồ họa.
- `vua-bong-toi-game-graphics-128px.zip`: gói asset nguyên bản.

## Cùng đóng góp

Xem [CONTRIBUTING.md](CONTRIBUTING.md). Hãy tạo branch riêng, ghi rõ thay đổi và mở Pull Request để mọi người xem xét.

## Giấy phép

Chưa có giấy phép được chọn. Trước khi đặt repository ở chế độ Public, hãy xác nhận bạn có quyền chia sẻ toàn bộ mã và asset, rồi chọn giấy phép phù hợp. Nếu chưa quyết định, để repository Private trong lúc chuẩn bị.
