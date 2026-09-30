# Tsingtao Vietnam — Landing Page

Trang giới thiệu sản phẩm Tsingtao với nền video bể cá, 9 sản phẩm nổi trong
nước (hiệu ứng 3D) và popup chi tiết khi bấm vào từng sản phẩm.
Hỗ trợ song ngữ **Tiếng Việt / English**.

## Cấu trúc dự án

```
Tsingtao_LandingPage_02/
├── index.html                      ← toàn bộ giao diện (1 file, không phụ thuộc thư viện)
├── assets/
│   ├── hero-aquarium-1080p.mp4     ← video nền, màn hình lớn (1.94 MB)
│   └── hero-aquarium-720p.mp4      ← video nền, mobile (0.76 MB)
├── products/
│   ├── *.jpg                       ← ảnh gốc chụp trên nền trắng
│   ├── cutout/*.png                ← ảnh PNG đã xóa nền (dùng làm mask)
│   └── cutout/webp/*.webp          ← ảnh WebP dùng thực tế trên web
├── tools/
│   ├── cutout.py                   ← xóa nền trắng bằng flood-fill
│   └── optimize.py                 ← nén PNG sang WebP
└── README.md
```

## Chạy thử

Mở trực tiếp: `index.html` (không cần máy chủ, dùng `file://` được).

Hoặc chạy máy chủ tĩnh:

```bash
python -m http.server 8000
# rồi mở http://localhost:8000
```

## Ghi chú kỹ thuật

**Video nền được crop bằng CSS.** Video gốc có đầu người trong bể kính ở khoảng
53.7%–88% chiều ngang. Trang chỉ hiển thị 50% bên trái (vùng nước mở) bằng:

```css
.hero-video { width: max(200vw, 177.78vh); }
```

Dùng `max()` để chiều cao luôn phủ kín màn hình ở mọi tỉ lệ. Không cần cắt video.

**Video đã nén lại.** File gốc là 4K 3840×2160, 14 MB. Đã nén thành 1080p (1.94 MB)
và 720p (0.76 MB), giảm 86% dung lượng tải về.

**Hiệu ứng 3D giới hạn ở ±18°.** Ảnh sản phẩm chỉ có một góc chính diện, nên xoay
360° thật sẽ làm mất nhãn và đảo chữ ở mặt sau. Giới hạn góc xoay giúp nhãn hiệu
luôn nằm đúng mặt, đọc rõ.

**Lớp ánh sáng mask theo ảnh sản phẩm** (`mask: url(...)`) nên vệt loé bám đúng
hình chai, không thành hình chữ nhật bao quanh.

**Bố cục responsive.** Trên ≥1280px: sản phẩm trôi trong nước bên phải, vùng sản phẩm
bắt đầu từ 720px nên không bao giờ chồng lên tiêu đề. Dưới 1280px: chuyển thành lưới
2–3 cột (5 cột khi xoay ngang) bên dưới phần chữ, ô cao cố định để trang không bị dài.

## Thêm sửa sản phẩm

Mỗi sản phẩm nằm trong mảng `PRODUCTS` trong `index.html`:

```js
{
  img: 'bia-500ml',        // tên file trong products/cutout/webp/
  pos: [30, 44],           // vị trí [x%, y%] trong vùng sản phẩm
  h: 38,                   // chiều cao (% chiều cao vùng sản phẩm)
  dur: 7.4, delay: -0.6,  // nhịp lắc
  turn: 14, shine: 6.4,    // nhịp xoay 3D và loé sáng
  vi: { kicker, name, sub, desc, specs: [] },
  en: { kicker, name, sub, desc, specs: [] },
}
```

## Công cụ xử lý ảnh

Cần Python và Pillow (`pip install pillow`).

```bash
# 1. xóa nền trắng -> products/cutout/*.png
python tools/cutout.py

# 2. nén sang WebP -> products/cutout/webp/*.webp
python tools/optimize.py
```

## Đẩy lên GitHub

```bash
cd D:\AI_PROJECTS\Tsingtao_LandingPage_02
git init
git branch -M main
git remote add origin <URL-repo>
git add .
git commit -m "Tsingtao Vietnam landing page"
git push -u origin main
```
