import json

with open('summoner_anim_viewer.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update specs table
old_table = """    <table class="specs-table">
      <tr><td>Nhân vật / Giới tính</td><td>Triệu Hồi Sư — Con người (Nữ)</td></tr>
      <tr><td>Số đo hình thể</td><td>Vòng 1 ~100cm (hở cúp ngực đầy đặn) · Vòng 2 ~60cm (eo thon corset) · Vòng 3 ~90cm (hông cong gợi cảm)</td></tr>
      <tr><td>Trang phục</td><td>Đồ bó Bodysuit / Corset (giống hình 4), cổ sơ mi nơ đỏ, hở vòng 1 quyến rũ, quần tất và bốt cao gót</td></tr>
      <tr><td>Vũ khí xúc tác</td><td>Gậy phép Triệu Hồi Hoàng Kim (khảm bảo ngọc ma thuật Arcane tím & cyan)</td></tr>
      <tr><td>Độ phân giải Sprite</td><td>64 x 72 px (Render scale 4x: 256 x 288 px, định dạng PNG trong suốt)</td></tr>
      <tr><td>Tổng số Frame</td><td>20 frame hoàn chỉnh (Idle, Move, Jump, Fall, Attack, Skill, Finisher, Dash, Defeat)</td></tr>
    </table>"""

new_table = """    <table class="specs-table">
      <tr><td>Nhân vật / Giới tính</td><td>Triệu Hồi Sư — Con người (Nữ) · Hoa Hậu Thần Thoại</td></tr>
      <tr><td>Chiều cao & Cân nặng</td><td>Cao 1.67m · Nặng 58kg · Thân hình thanh thoát, thon gọn, không béo phì</td></tr>
      <tr><td>Số đo hình thể</td><td>V1 ~100cm (hở cúp ngực đầy đặn) · V2 ~60cm (eo thon corset phẳng) · V3 ~90cm (mông & hông nở cong chữ S)</td></tr>
      <tr><td>Dáng đứng & Phong cách</td><td>Đứng nghiêng góc 3/4 uốn lượn chữ S tự nhiên (giống hình 4), không đứng trực diện phẳng</td></tr>
      <tr><td>Trang phục</td><td>Bodysuit Corset đen 6 nút vàng, áo choàng trắng trâm ngọc Ruby, tất đen sheer & garter vàng</td></tr>
      <tr><td>Vũ khí xúc tác</td><td>Gậy phép Vòng Hoàng Kim (khảm bảo ngọc ma thuật Arcane tím & vòng xoáy cyan/pink)</td></tr>
      <tr><td>Độ phân giải Sprite</td><td>128 × 144 px (Native Pixel Art chi tiết cao, nền trong suốt RGBA)</td></tr>
      <tr><td>Tổng số Frame</td><td>20 frame hoàn chỉnh (Idle, Move, Jump, Fall, Attack, Skill, Finisher, Dash, Defeat)</td></tr>
    </table>"""

if old_table in html:
    html = html.replace(old_table, new_table)

# Update canvas resolution handling
old_scale_js = """scaleBtn.onclick = () => {
  scaleLevel = scaleLevel === 4 ? 2 : scaleLevel === 2 ? 3 : 4;
  scaleBtn.textContent = `Phóng to (${scaleLevel}x)`;
  canvas.width = 64 * scaleLevel;
  canvas.height = 72 * scaleLevel;
};"""

new_scale_js = """scaleBtn.onclick = () => {
  scaleLevel = scaleLevel === 2 ? 1 : scaleLevel === 1 ? 3 : 2;
  scaleBtn.textContent = `Phóng to (${scaleLevel}x)`;
  canvas.width = 128 * scaleLevel;
  canvas.height = 144 * scaleLevel;
};"""

if old_scale_js in html:
    html = html.replace(old_scale_js, new_scale_js)

# Set initial canvas width and height
html = html.replace('let scaleLevel = 4;', 'let scaleLevel = 2;')
html = html.replace('<canvas id="preview" width="256" height="288"></canvas>', '<canvas id="preview" width="256" height="288"></canvas>')

with open('summoner_anim_viewer.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated summoner_anim_viewer.html for 128x144!")
