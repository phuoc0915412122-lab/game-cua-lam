import json

with open('scratch/summoner_b64.json', 'r', encoding='utf-8') as f:
    b64_dict = json.load(f)

with open('summoner_anim_viewer.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update specs table
old_specs = '''    <table class="specs-table">
      <tr><td>Phái / Phe</td><td>SHINOBI (Pháp sư linh thú)</td></tr>
      <tr><td>Nguồn cảm hứng</td><td>Pixel art quỷ tộc (Sừng đỏ crimson, tóc cam đào, áo xanh thẫm, gậy phép ngọc bích)</td></tr>
      <tr><td>Độ phân giải Sprite</td><td>64 x 72 px (Render scale 4x: 256 x 288 px, RGBA)</td></tr>
      <tr><td>Vũ khí xúc tác</td><td>Trượng Triệu Hồi Cổ Ngân (Khảm ngọc linh hồn xanh mint)</td></tr>
      <tr><td>Tổng số Frame</td><td>20 frame hoàn chỉnh (Idle, Move, Jump, Fall, Attack, Skill, Finisher, Dash, Defeat)</td></tr>
    </table>'''

new_specs = '''    <table class="specs-table">
      <tr><td>Nhân vật / Giới tính</td><td>Triệu Hồi Sư — Con người (Nữ)</td></tr>
      <tr><td>Số đo hình thể</td><td>Vòng 1 ~100cm (hở cúp ngực đầy đặn) · Vòng 2 ~60cm (eo thon corset) · Vòng 3 ~90cm (hông cong gợi cảm)</td></tr>
      <tr><td>Trang phục</td><td>Đồ bó Bodysuit / Corset (giống hình 4), cổ sơ mi nơ đỏ, hở vòng 1 quyến rũ, quần tất và bốt cao gót</td></tr>
      <tr><td>Vũ khí xúc tác</td><td>Gậy phép Triệu Hồi Hoàng Kim (khảm bảo ngọc ma thuật Arcane tím & cyan)</td></tr>
      <tr><td>Độ phân giải Sprite</td><td>64 x 72 px (Render scale 4x: 256 x 288 px, định dạng PNG trong suốt)</td></tr>
      <tr><td>Tổng số Frame</td><td>20 frame hoàn chỉnh (Idle, Move, Jump, Fall, Attack, Skill, Finisher, Dash, Defeat)</td></tr>
    </table>'''

if old_specs in html:
    html = html.replace(old_specs, new_specs)

# Update palette chips
old_palette = '''    <div class="palette-strip">
      <div class="palette-chip" style="background:#e62846" data-col="Sừng Quỷ #e62846"></div>
      <div class="palette-chip" style="background:#ea8350" data-col="Tóc Cam Đào #ea8350"></div>
      <div class="palette-chip" style="background:#fedecb" data-col="Màu Da #fedecb"></div>
      <div class="palette-chip" style="background:#f03678" data-col="Mắt Ruby #f03678"></div>
      <div class="palette-chip" style="background:#232f4a" data-col="Áo Choàng Đêm #232f4a"></div>
      <div class="palette-chip" style="background:#6ee3bd" data-col="Khí Linh Xanh #6ee3bd"></div>
      <div class="palette-chip" style="background:#f3c445" data-col="Chỉ Vàng Kim #f3c445"></div>
      <div class="palette-chip" style="background:#7d522c" data-col="Thân Trượng Cổ #7d522c"></div>
    </div>'''

new_palette = '''    <div class="palette-strip">
      <div class="palette-chip" style="background:#e8ecf4" data-col="Tóc Bạch Kim #e8ecf4"></div>
      <div class="palette-chip" style="background:#fde3d4" data-col="Màu Da Hồng Hào #fde3d4"></div>
      <div class="palette-chip" style="background:#d83a8b" data-col="Mắt Tím Amethyst #d83a8b"></div>
      <div class="palette-chip" style="background:#1e1c2b" data-col="Bodysuit Đen Bóng #1e1c2b"></div>
      <div class="palette-chip" style="background:#c02640" data-col="Nơ Cổ Đỏ #c02640"></div>
      <div class="palette-chip" style="background:#f5c542" data-col="Vàng Hoàng Kim #f5c542"></div>
      <div class="palette-chip" style="background:#bd34e8" data-col="Ngọc Arcane Tím #bd34e8"></div>
      <div class="palette-chip" style="background:#70f3ff" data-col="Khí Triệu Hồi Cyan #70f3ff"></div>
    </div>'''

if old_palette in html:
    html = html.replace(old_palette, new_palette)

# Inject fallback Base64 data so viewer works 100% even from local file://
b64_inject = f'''<script>
window.B64_ASSETS = {json.dumps(b64_dict)};
</script>
<script src="game-assets/animations.js"></script>'''

if '<script src="game-assets/animations.js"></script>' in html:
    html = html.replace('<script src="game-assets/animations.js"></script>', b64_inject)

# Also update getImage to check B64_ASSETS first
old_get_img = '''function getImage(src) {
  if (loadedImages.has(src)) return loadedImages.get(src);
  const img = new Image();
  img.src = src;
  loadedImages.set(src, img);
  return img;
}'''

new_get_img = '''function getImage(src) {
  if (loadedImages.has(src)) return loadedImages.get(src);
  const img = new Image();
  const b64 = window.B64_ASSETS ? (window.B64_ASSETS[src] || window.B64_ASSETS['characters/3/' + src.split('/').pop()] || window.B64_ASSETS[src.replace('characters/3/', 'characters/3/')]) : null;
  img.src = b64 || ('game-assets/' + src);
  loadedImages.set(src, img);
  return img;
}'''

if old_get_img in html:
    html = html.replace(old_get_img, new_get_img)

with open('summoner_anim_viewer.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated summoner_anim_viewer.html successfully!')
