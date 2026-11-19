import os, sys, base64, json
sys.path.append(os.path.abspath('scratch'))
from frame_generators import (
    create_idle_frame, create_move_frame, create_jump_frame, create_fall_frame,
    create_attack_frame, create_skill_frame, create_finisher_frame,
    create_dash_frame, create_defeat_frame
)

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

for fn, gen in frame_map.items():
    canvas = gen()
    png_bytes = canvas.to_png_bytes(scale=4)
    out_path = os.path.join(out_dir, fn)
    with open(out_path, 'wb') as f:
        f.write(png_bytes)
    
    b64_str = 'data:image/png;base64,' + base64.b64encode(png_bytes).decode('ascii')
    asset_key = f'characters/3/{fn}'
    b64_assets[asset_key] = b64_str
    print(f'Generated {fn}: size={len(png_bytes)} bytes')

# Save b64 json
with open('scratch/summoner_b64.json', 'w', encoding='utf-8') as f:
    json.dump(b64_assets, f)

print('All 20 frames generated successfully and b64 json saved.')
