import fitz
import os

pdf_path = r"d:\下载\传德logo.pdf"
out_dir  = r"d:\desktop\picture prompt"

doc = fitz.open(pdf_path)
print(f"PDF pages: {len(doc)}")

for i, page in enumerate(doc):
    # 先检查页面尺寸
    rect = page.rect
    print(f"  Page {i}: {rect.width:.0f} x {rect.height:.0f} pt")

    # 高分辨率导出：4x 放大（适合 logo）
    zoom   = 4
    mat    = fitz.Matrix(zoom, zoom)

    # 透明背景 PNG（alpha=True）
    pix = page.get_pixmap(matrix=mat, alpha=True)
    out_path = os.path.join(out_dir, f"chuande-logo-p{i+1}-4x.png")
    pix.save(out_path)
    print(f"  Saved: {out_path}  ({pix.width}x{pix.height}px)")

    # 也导出白底版
    pix_white = page.get_pixmap(matrix=mat, alpha=False)
    out_w = os.path.join(out_dir, f"chuande-logo-p{i+1}-white.png")
    pix_white.save(out_w)
    print(f"  Saved: {out_w}  (white bg)")

doc.close()
print("Done!")
