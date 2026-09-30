"""Xóa nền trắng cho ảnh sản phẩm Tsingtao, xuất PNG nền trong suốt.

Chạy từ thư mục gốc dự án:
    python tools/cutout.py
"""
from PIL import Image, ImageFilter
from collections import deque
import os

# thư mục gốc dự án (cha của tools/)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'products')
OUT = os.path.join(SRC, 'cutout')
os.makedirs(OUT, exist_ok=True)


def remove_white_bg(name, tol=222, feather=1.1, pad=6):
    src = os.path.join(SRC, name)
    dst = os.path.join(OUT, os.path.splitext(name)[0] + '.png')

    im = Image.open(src).convert('RGB')
    w, h = im.size
    px = im.load()

    visited = bytearray(w * h)
    alpha = bytearray([255]) * (w * h)
    q = deque()

    def is_bg(x, y):
        r, g, b = px[x, y]
        return r >= tol and g >= tol and b >= tol

    # flood fill bắt đầu từ 4 cạnh
    for x in range(w):
        for y in (0, h - 1):
            if is_bg(x, y) and not visited[y * w + x]:
                visited[y * w + x] = 1
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_bg(x, y) and not visited[y * w + x]:
                visited[y * w + x] = 1
                q.append((x, y))

    while q:
        x, y = q.popleft()
        alpha[y * w + x] = 0
        if x > 0:
            nx, ny = x - 1, y
            if not visited[ny * w + nx] and is_bg(nx, ny):
                visited[ny * w + nx] = 1; q.append((nx, ny))
        if x < w - 1:
            nx, ny = x + 1, y
            if not visited[ny * w + nx] and is_bg(nx, ny):
                visited[ny * w + nx] = 1; q.append((nx, ny))
        if y > 0:
            nx, ny = x, y - 1
            if not visited[ny * w + nx] and is_bg(nx, ny):
                visited[ny * w + nx] = 1; q.append((nx, ny))
        if y < h - 1:
            nx, ny = x, y + 1
            if not visited[ny * w + nx] and is_bg(nx, ny):
                visited[ny * w + nx] = 1; q.append((nx, ny))

    a = Image.frombytes('L', (w, h), bytes(alpha))
    a = a.filter(ImageFilter.GaussianBlur(feather))   # làm mượt viền

    out = im.convert('RGBA')
    out.putalpha(a)

    bbox = a.getbbox()
    if bbox:
        bbox = (max(0, bbox[0] - pad), max(0, bbox[1] - pad),
                min(w, bbox[2] + pad), min(h, bbox[3] + pad))
        out = out.crop(bbox)

    out.save(dst)
    print(f"{os.path.basename(dst):24s} {out.size[0]}x{out.size[1]}")


if __name__ == '__main__':
    # (tên file, ngưỡng) — ngưỡng cao hơn cho ảnh có nền trắng bị lẫn vào sản phẩm
    targets = [
        ('bia-500ml.jpg', 222),        # chai xanh Premium Lager 500ml
        ('bia-nho.jpg', 222),          # chai nhỏ Premium Lager
        ('bia-century.jpg', 238),      # chai swing-top 百年之旅 (nắp kim loại sáng)
        ('bia-2025.jpg', 240),         # Special Edition 2025 (nắp vàng rất sáng)
        ('bia-1903.jpg', 235),         # lon vàng 1903
        ('bia-0do.jpg', 222),          # lon Zero Alcohol 0.0%
        ('bia-0do-chai.jpg', 222),     # chai Zero Alcohol
        ('bia-lemon-0do.jpg', 226),    # lon Lemon Pilsner 0.0%
        ('bia-soda-seaweed.jpg', 232), # lon SODA rong biển
        ('bia-export.jpg', 222),       # chai xuất khẩu
    ]
    for name, tol in targets:
        remove_white_bg(name, tol=tol)
