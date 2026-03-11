import os

W, H   = 1920, 1080
step   = 13
min_r  = 0.25
max_r  = 5.2
dot_op = 0.18
bg     = '#F4F3EE'
dot_c  = '#0A0A0A'

circles = []
half = step / 2.0
y = half
while y < H:
    x = half
    while x < W:
        t = (x / W * 0.5 + y / H * 0.5)
        t = t * t * (3 - 2 * t)
        r = min_r + (max_r - min_r) * t
        if r > 0.18:
            circles.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}"/>')
        x += step
    y += step

inner = '\n    '.join(circles)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
     width="1920" height="1080" viewBox="0 0 1920 1080">
  <rect width="1920" height="1080" fill="{bg}"/>
  <g fill="{dot_c}" opacity="{dot_op}">
    {inner}
  </g>
</svg>'''

out = r'd:\desktop\picture prompt\openclaw-bg-dots.svg'
with open(out, 'w', encoding='utf-8') as f:
    f.write(svg)

size = os.path.getsize(out)
print(f'Done | circles={len(circles)} | size={size//1024} KB')
print(out)
