import os, sys, json, base64, shutil, zipfile
sys.path.append(os.path.abspath('scratch'))
from build_all_frames_v3 import (
    create_idle_frame, create_move_frame, create_jump_frame, create_fall_frame,
    create_attack_frame, create_skill_frame, create_finisher_frame,
    create_dash_frame, create_defeat_frame
)
from pixel_canvas import PixelCanvas

out_dir = os.path.abspath('game-assets/characters/3')
os.makedirs(out_dir, exist_ok=True)

frame_map = {
    'idle_01.png': lambda: create_idle_frame(1),
    'idle_02.png': lambda: create_idle_frame(2),
    'move_01.png': lambda: create_move_frame(1),
    'move_02.png': lambda: create_move_frame(2),
    'move_03.png': lambda: create_move_frame(3),
    'move_04.png': lambda: create_move_frame(4),
    'jump_01.png': lambda: create_jump_frame(),
    'fall_01.png': lambda: create_fall_frame(),
    'attack_01.png': lambda: create_attack_frame(1),
    'attack_02.png': lambda: create_attack_frame(2),
    'attack_03.png': lambda: create_attack_frame(3),
    'skill_01.png': lambda: create_skill_frame(1),
    'skill_02.png': lambda: create_skill_frame(2),
    'skill_03.png': lambda: create_skill_frame(3),
    'finisher_01.png': lambda: create_finisher_frame(1),
    'finisher_02.png': lambda: create_finisher_frame(2),
    'finisher_03.png': lambda: create_finisher_frame(3),
    'dash_01.png': lambda: create_dash_frame(1),
    'dash_02.png': lambda: create_dash_frame(2),
    'defeat_01.png': lambda: create_defeat_frame(),
}

b64_assets = {}
rendered_canvases = {}

for fn, gen in frame_map.items():
    canvas = gen()
    rendered_canvases[fn] = canvas
    png_bytes = canvas.to_png_bytes(scale=4)
    out_path = os.path.join(out_dir, fn)
    with open(out_path, 'wb') as f:
        f.write(png_bytes)
    
    b64_str = 'data:image/png;base64,' + base64.b64encode(png_bytes).decode('ascii')
    asset_key = f'characters/3/{fn}'
    b64_assets[asset_key] = b64_str
    print(f'Rendered {fn}: {len(png_bytes)} bytes (256x288)')

# Save Base64 json
with open('scratch/summoner_b64.json', 'w', encoding='utf-8') as f:
    json.dump(b64_assets, f)

# Build Spritesheet (5 columns x 4 rows)
sheet_cols = 5
sheet_rows = 4
sheet_w = 64 * sheet_cols
sheet_h = 72 * sheet_rows
sheet_canvas = PixelCanvas(sheet_w, sheet_h)

ordered_keys = [
    'idle_01.png', 'idle_02.png', 'move_01.png', 'move_02.png', 'move_03.png',
    'move_04.png', 'jump_01.png', 'fall_01.png', 'attack_01.png', 'attack_02.png',
    'attack_03.png', 'skill_01.png', 'skill_02.png', 'skill_03.png', 'finisher_01.png',
    'finisher_02.png', 'finisher_03.png', 'dash_01.png', 'dash_02.png', 'defeat_01.png'
]

for idx, k in enumerate(ordered_keys):
    c = rendered_canvases[k]
    col_idx = idx % sheet_cols
    row_idx = idx // sheet_cols
    ox = col_idx * 64
    oy = row_idx * 72
    for y in range(72):
        for x in range(64):
            pixel = c.get(x, y)
            sheet_canvas.set(ox + x, oy + y, pixel)

sheet_bytes = sheet_canvas.to_png_bytes(scale=4)
sheet_path = os.path.join(out_dir, 'summoner_spritesheet.png')
with open(sheet_path, 'wb') as f:
    f.write(sheet_bytes)
print(f'Spritesheet rendered: {len(sheet_bytes)} bytes (1280x1152)')

# Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_text = f.read()

prefix = '<script>window.GAME_ASSET_DATA='
if prefix in index_text:
    start_pos = index_text.index(prefix) + len(prefix)
    end_pos = index_text.index('};', start_pos) + 1
    current_data = json.loads(index_text[start_pos:end_pos])
    for k, v in b64_assets.items():
        current_data[k] = v
    new_json = json.dumps(current_data, separators=(',', ':'))
    index_text = index_text[:start_pos] + new_json + index_text[end_pos:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_text)
    print('Updated index.html Base64 assets!')

# Update summoner_anim_viewer.html
with open('summoner_anim_viewer.html', 'r', encoding='utf-8') as f:
    v_html = f.read()

b64_start = 'window.B64_ASSETS = '
if b64_start in v_html:
    sp = v_html.index(b64_start) + len(b64_start)
    ep = v_html.index(';\n</script>', sp)
    v_html = v_html[:sp] + json.dumps(b64_assets) + v_html[ep:]
    with open('summoner_anim_viewer.html', 'w', encoding='utf-8') as f:
        f.write(v_html)
    print('Updated summoner_anim_viewer.html Base64 data!')

# Copy to artifact dir
art_dir = r'C:\Users\ADMIN\.gemini\antigravity\brain\704b332d-44e7-4fab-a752-6a15e1db316e'
shutil.copy2(sheet_path, os.path.join(art_dir, 'summoner_spritesheet.png'))
for fn in ['idle_01.png', 'move_01.png', 'jump_01.png', 'attack_02.png', 'skill_02.png', 'finisher_02.png', 'dash_01.png', 'defeat_01.png']:
    src = os.path.join(out_dir, fn)
    dst = os.path.join(art_dir, 'summoner_' + fn)
    shutil.copy2(src, dst)
print('Copied files to artifact directory!')

# Re-pack zip
zip_path = 'shinobi-soul-reaper-game-graphics-2026-11-13.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk('game-assets'):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, '.')
            z.write(full, rel)
    z.write('index.html', 'index.html')
    z.write('summoner_anim_viewer.html', 'summoner_anim_viewer.html')
    if os.path.exists('GAME_GRAPHICS_README.txt'):
        z.write('GAME_GRAPHICS_README.txt', 'GAME_GRAPHICS_README.txt')
print(f'Repacked zip archive: {os.path.getsize(zip_path)} bytes')
