"""Tối ưu ảnh sản phẩm sang WebP (giữ kênh alpha) để giảm dung lượng.

Chạy từ thư mục gốc dự án (sau khi đã chạy cutout.py):
    python tools/optimize.py
"""
from PIL import Image
import os

# thư mục gốc dự án (cha của tools/)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'products', 'cutout')
DST = os.path.join(SRC, 'webp')
os.makedirs(DST, exist_ok=True)

# Toàn bộ sản phẩm dùng trong giao diện
HERO = ['bia-500ml', 'bia-century', 'bia-2025', 'bia-1903', 'bia-0do',
        'bia-0do-chai', 'bia-lemon-0do', 'bia-soda-seaweed', 'bia-export']

for name in HERO:
    im = Image.open(os.path.join(SRC, name + '.png')).convert('RGBA')
    # giới hạn chiều cao để đủ cho màn hình retina mà không phí dung lượng
    if im.height > 1000:
        w = round(im.width * 1000 / im.height)
        im = im.resize((w, 1000), Image.LANCZOS)
    out = os.path.join(DST, name + '.webp')
    im.save(out, 'WEBP', quality=90, method=6)
    kb_old = os.path.getsize(os.path.join(SRC, name + '.png')) / 1024
    kb_new = os.path.getsize(out) / 1024
    print(f"{name:20s} {im.size[0]}x{im.size[1]}  {kb_old:.0f}KB -> {kb_new:.0f}KB")
