import os, sys, json, base64, re, zipfile

def main():
    char_dir = os.path.abspath('game-assets/characters/1')
    fx_dir = os.path.abspath('game-assets/effects/dark_king')

    char_files = sorted([f for f in os.listdir(char_dir) if f.endswith('.png')])
    fx_files = sorted([f for f in os.listdir(fx_dir) if f.endswith('.png')])
    print(f"Found {len(char_files)} character PNGs and {len(fx_files)} VFX PNGs.")

    b64_dict = {}
    for f in char_files:
        path = os.path.join(char_dir, f)
        with open(path, 'rb') as img_f:
            b64 = base64.b64encode(img_f.read()).decode('ascii')
            key = f"characters/1/{f}"
            b64_dict[key] = f"data:image/png;base64,{b64}"

    for f in fx_files:
        path = os.path.join(fx_dir, f)
        with open(path, 'rb') as img_f:
            b64 = base64.b64encode(img_f.read()).decode('ascii')
            key = f"effects/dark_king/{f}"
            b64_dict[key] = f"data:image/png;base64,{b64}"

    # 1. Update game-assets/animations.js
    anim_char1_block = '''  1: {
    idle: {frames:[{src:"characters/1/idle_01.png",ms:140},{src:"characters/1/idle_02.png",ms:140},{src:"characters/1/idle_03.png",ms:140},{src:"characters/1/idle_04.png",ms:140},{src:"characters/1/idle_05.png",ms:140},{src:"characters/1/idle_06.png",ms:140}],loop:true,width:64,height:72,offsetY:6},
    move: {frames:[{src:"characters/1/move_01.png",ms:65},{src:"characters/1/move_02.png",ms:65},{src:"characters/1/move_03.png",ms:65},{src:"characters/1/move_04.png",ms:65},{src:"characters/1/move_05.png",ms:65},{src:"characters/1/move_06.png",ms:65},{src:"characters/1/move_07.png",ms:65},{src:"characters/1/move_08.png",ms:65}],loop:true,width:64,height:72,offsetY:6},
    jump: {frames:[{src:"characters/1/jump_01.png",ms:70},{src:"characters/1/jump_02.png",ms:90},{src:"characters/1/jump_03.png",ms:140}],loop:false,width:64,height:72,offsetY:6},
    fall: {frames:[{src:"characters/1/fall_01.png",ms:90},{src:"characters/1/fall_02.png",ms:90},{src:"characters/1/fall_03.png",ms:110}],loop:true,width:64,height:72,offsetY:6,flip:false},
    attack: {frames:[{src:"characters/1/attack_01.png",ms:55},{src:"characters/1/attack_02.png",ms:65},{src:"characters/1/attack_03.png",ms:55},{src:"characters/1/attack_04.png",ms:70},{src:"characters/1/attack_05.png",ms:75},{src:"characters/1/attack_06.png",ms:80}],loop:false,width:64,height:72,offsetY:6},
    skill: {frames:[{src:"characters/1/skill_01.png",ms:80},{src:"characters/1/skill_02.png",ms:85},{src:"characters/1/skill_03.png",ms:95},{src:"characters/1/skill_04.png",ms:110}],loop:false,width:64,height:72,offsetY:6},
    finisher: {frames:[{src:"characters/1/finisher_01.png",ms:85},{src:"characters/1/finisher_02.png",ms:90},{src:"characters/1/finisher_03.png",ms:105},{src:"characters/1/finisher_04.png",ms:130}],loop:false,width:64,height:72,offsetY:6},
    dash: {frames:[{src:"characters/1/dash_01.png",ms:50},{src:"characters/1/dash_02.png",ms:50},{src:"characters/1/dash_03.png",ms:50},{src:"characters/1/dash_04.png",ms:50}],loop:true,width:64,height:72,offsetY:6},
    defeat: {frames:[{src:"characters/1/defeat_01.png",ms:90},{src:"characters/1/defeat_02.png",ms:100},{src:"characters/1/defeat_03.png",ms:110},{src:"characters/1/defeat_04.png",ms:250}],loop:false,width:64,height:72,offsetY:6,flip:false}
  },'''

    with open('game-assets/animations.js', 'r', encoding='utf-8') as f:
        anim_js = f.read()

    # Replace character 1 block in animations.js
    pattern_c1 = re.compile(r'  1:\s*\{[\s\S]*?defeat:\s*\{[^\}]+\}\s*\},')
    if pattern_c1.search(anim_js):
        anim_js = pattern_c1.sub(anim_char1_block, anim_js, count=1)
    else:
        anim_js = anim_js.replace(' characters: {\n', ' characters: {\n' + anim_char1_block + '\n', 1)

    # Add darkorb projectile & darkKing effects to animations.js if not present
    if 'darkorb:' not in anim_js:
        anim_js = anim_js.replace(
            'projectiles: {\n',
            'projectiles: {\n  darkorb: {frames:[{src:"effects/dark_king/dark_orb_01.png",ms:65},{src:"effects/dark_king/dark_orb_02.png",ms:65},{src:"effects/dark_king/dark_orb_03.png",ms:65},{src:"effects/dark_king/dark_orb_04.png",ms:65}],loop:true,width:36,height:36,anchorX:0.5,anchorY:0.5},\n'
        )
    if 'darkSlash:' not in anim_js:
        anim_js = anim_js.replace(
            'effects: {\n',
            'effects: {\n  darkSlash: {frames:[{src:"effects/dark_king/dark_slash_01.png",ms:45},{src:"effects/dark_king/dark_slash_02.png",ms:45},{src:"effects/dark_king/dark_slash_03.png",ms:45},{src:"effects/dark_king/dark_slash_04.png",ms:45}],loop:false,width:76,height:76,anchorX:0.45,anchorY:0.5},\n  darkVortex: {frames:[{src:"effects/dark_king/dark_vortex_01.png",ms:75},{src:"effects/dark_king/dark_vortex_02.png",ms:75},{src:"effects/dark_king/dark_vortex_03.png",ms:75},{src:"effects/dark_king/dark_vortex_04.png",ms:75}],loop:true,width:96,height:96,anchorX:0.5,anchorY:0.78},\n  darkOrbImpact: {frames:[{src:"effects/dark_king/dark_impact_01.png",ms:55},{src:"effects/dark_king/dark_impact_02.png",ms:55},{src:"effects/dark_king/dark_impact_03.png",ms:55},{src:"effects/dark_king/dark_impact_04.png",ms:55}],loop:false,width:72,height:72,anchorX:0.5,anchorY:0.5},\n'
        )

    with open('game-assets/animations.js', 'w', encoding='utf-8') as f:
        f.write(anim_js)
    print("Updated game-assets/animations.js")

    # 2. Patch index.html (clean old character 1 & dark_king base64 entries, inject new ones, upgrade animation & VFX definitions)
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Remove any old characters/1/... or effects/dark_king/... base64 entries from GAME_ASSET_DATA
    html = re.sub(r'"characters/1/[^"]+":\s*"data:image/png;base64,[^"]+",?', '', html)
    html = re.sub(r'"effects/dark_king/[^"]+":\s*"data:image/png;base64,[^"]+",?', '', html)

    marker_asset = 'window.GAME_ASSET_DATA={'
    if marker_asset in html:
        entries = [f'"{k}":"{v}"' for k, v in b64_dict.items()]
        html = html.replace(marker_asset, marker_asset + ','.join(entries) + ',', 1)
        print(f"Injected {len(entries)} high-res 128x144 base64 textures into index.html")

    # Update character 1 animation block inside index.html
    html = pattern_c1.sub(anim_char1_block, html, count=1)

    # Also register darkorb projectile & darkVortex/darkSlash/darkOrbImpact effects in index.html GAME_ANIMATIONS
    if 'darkorb:{frames:' not in html and 'darkorb: {frames:' not in html:
        html = html.replace(
            'projectiles: {\n',
            'projectiles: {\n  darkorb: {frames:[{src:"effects/dark_king/dark_orb_01.png",ms:65},{src:"effects/dark_king/dark_orb_02.png",ms:65},{src:"effects/dark_king/dark_orb_03.png",ms:65},{src:"effects/dark_king/dark_orb_04.png",ms:65}],loop:true,width:36,height:36,anchorX:0.5,anchorY:0.5},\n',
            1
        )
    if 'darkSlash:' not in html:
        html = html.replace(
            'effects: {\n',
            'effects: {\n  darkSlash: {frames:[{src:"effects/dark_king/dark_slash_01.png",ms:45},{src:"effects/dark_king/dark_slash_02.png",ms:45},{src:"effects/dark_king/dark_slash_03.png",ms:45},{src:"effects/dark_king/dark_slash_04.png",ms:45}],loop:false,width:76,height:76,anchorX:0.45,anchorY:0.5},\n  darkVortex: {frames:[{src:"effects/dark_king/dark_vortex_01.png",ms:75},{src:"effects/dark_king/dark_vortex_02.png",ms:75},{src:"effects/dark_king/dark_vortex_03.png",ms:75},{src:"effects/dark_king/dark_vortex_04.png",ms:75}],loop:true,width:96,height:96,anchorX:0.5,anchorY:0.78},\n  darkOrbImpact: {frames:[{src:"effects/dark_king/dark_impact_01.png",ms:55},{src:"effects/dark_king/dark_impact_02.png",ms:55},{src:"effects/dark_king/dark_impact_03.png",ms:55},{src:"effects/dark_king/dark_impact_04.png",ms:55}],loop:false,width:72,height:72,anchorX:0.5,anchorY:0.5},\n',
            1
        )

    # Render darkorb sprite texture in PvP & RPG projectiles when available
    if 'drawDarkKingOrb' not in html:
        helper_fn = '''function drawDarkKingOrb(x,y,phase=clock*1000){const anim=window.GAME_ANIMATIONS?.projectiles?.darkorb,im=silverFrameAt(anim,phase);if(!im)return false;ctx.save();ctx.translate(x,y);ctx.imageSmoothingEnabled=false;ctx.drawImage(im,-anim.width/2,-anim.height/2,anim.width,anim.height);ctx.restore();return true}
function drawDarkKingFx(key,e,a){const anim=window.GAME_ANIMATIONS?.effects?.[key],im=silverFrameAt(anim,(e.max-e.life)*1000);if(!im)return false;ctx.save();ctx.globalAlpha=Math.min(1,a*1.15);ctx.imageSmoothingEnabled=false;ctx.translate(e.x,e.y);if(e.dir<0)ctx.scale(-1,1);ctx.drawImage(im,-anim.width*(anim.anchorX??.5),-anim.height*(anim.anchorY??.5),anim.width,anim.height);ctx.restore();return true}
function drawSilverBird('''
        html = html.replace('function drawSilverBird(', helper_fn, 1)
        html = html.replace("else if(q.name==='silverbird'){drawSilverBird(q.x,q.y,Math.sign(q.vx)||1,(q.age||clock)*1000)}",
                            "else if(q.name==='silverbird'){drawSilverBird(q.x,q.y,Math.sign(q.vx)||1,(q.age||clock)*1000)}else if(q.name==='darkorb'&&drawDarkKingOrb(q.x,q.y,(q.age||clock)*1000)){}", 1)
        html = html.replace("else if(s.name==='darkorb'){",
                            "else if(s.name==='darkorb'&&drawDarkKingOrb(s.x-cam,s.y,clock*1000)){}else if(s.name==='darkorb'){", 1)
        html = html.replace("if(e.type==='darkVortex'){",
                            "if(e.type==='darkVortex'&&drawDarkKingFx('darkVortex',e,a)){}else if(e.type==='darkVortex'){")
        html = html.replace("else if(e.type==='darkOrbImpact'){",
                            "else if(e.type==='darkOrbImpact'&&drawDarkKingFx('darkOrbImpact',e,a)){}else if(e.type==='darkOrbImpact'){")
        html = html.replace("if(e.type==='slash'){",
                            "if(e.type==='slash'&&(e.c==='#8b64db'||e.c==='#9c55f1')&&drawDarkKingFx('darkSlash',e,a)){}else if(e.type==='slash'){")

    # Also upgrade Vua Bóng Tối accent color & description in chars array if needed
    html = html.replace(
        "{name:'VUA BÓNG TỐI',side:'SOUL REAPER',desc:'Bóng tối · cận chiến tốc độ và cầu hắc ám',skills:['XUNG KÍCH','HẮC QUANG','BÀNH TRƯỚNG LÃNH ĐỊA'],hair:'#15151a',coat:'#19131a',accent:'#f33f5d',skin:'#dcd8d2',style:'void'}",
        "{name:'VUA BÓNG TỐI',side:'SOUL REAPER',desc:'Đế Vương Hắc Ám · kiếm khí hư không và lãnh địa bóng tối',skills:['XUNG KÍCH','HẮC QUANG','BÀNH TRƯỚNG LÃNH ĐỊA'],hair:'#110f1a',coat:'#14111f',accent:'#9346f0',skin:'#f7d4c1',style:'void'}"
    )

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Saved updated index.html")

    # 3. Create Interactive Animation & VFX Viewer (vua_bong_toi_anim_viewer.html)
    viewer_html = f'''<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vua Bóng Tối (Dark King) — True Native 128×144 Pixel Art & Skill VFX Viewer</title>
<style>
  :root {{
    --bg: #07050e;
    --panel: #110d1f;
    --panel-border: #2c204d;
    --purple-main: #9346f0;
    --purple-glow: rgba(147, 70, 240, 0.45);
    --gold: #ffd24c;
    --gold-glow: rgba(255, 210, 76, 0.35);
    --text: #f3f4f6;
    --text-dim: #a19bb5;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
  body {{
    background: radial-gradient(circle at 50% 0%, #1b1136 0%, var(--bg) 70%);
    color: var(--text);
    min-height: 100vh;
    padding: 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  header {{ text-align: center; margin-bottom: 22px; max-width: 900px; }}
  h1 {{
    font-size: 28px;
    font-weight: 800;
    color: var(--gold);
    text-shadow: 0 0 18px var(--gold-glow);
    letter-spacing: 1px;
    margin-bottom: 8px;
  }}
  p.subtitle {{ color: var(--text-dim); font-size: 14px; line-height: 1.5; }}
  .badge {{
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    background: #2b144d;
    color: #e9d5ff;
    border: 1px solid #7e22ce;
    margin: 4px 3px;
  }}
  .badge.gold {{ background: #4d3208; color: #fef3c7; border-color: #eab308; }}
  .main-layout {{
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    max-width: 1240px;
    width: 100%;
    justify-content: center;
  }}
  .card {{
    background: var(--panel);
    border: 1px solid var(--panel-border);
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 14px 40px rgba(0,0,0,0.65);
  }}
  .player-card {{
    flex: 1 1 500px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .spritesheet-card {{ flex: 1 1 640px; }}
  .canvas-stage {{
    border-radius: 10px;
    overflow: hidden;
    border: 2px solid #4a1d85;
    box-shadow: 0 0 28px var(--purple-glow);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 16px;
  }}
  .bg-check {{
    background-color: #100d1c;
    background-image: linear-gradient(45deg, #19152b 25%, transparent 25%), linear-gradient(-45deg, #19152b 25%, transparent 25%), linear-gradient(45deg, transparent 75%, #19152b 75%), linear-gradient(-45deg, transparent 75%, #19152b 75%);
    background-size: 20px 20px;
    background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
  }}
  .bg-grid {{
    background-color: #0b0914;
    background-image: linear-gradient(#1f1a36 1px, transparent 1px), linear-gradient(90deg, #1f1a36 1px, transparent 1px);
    background-size: 16px 16px;
  }}
  .bg-dark {{ background: #07050c; }}
  canvas {{ display: block; image-rendering: pixelated; }}
  .anim-btn-bar {{
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    margin-bottom: 14px;
    justify-content: center;
  }}
  button.anim-btn {{
    background: #1b1630;
    color: #d1cde0;
    border: 1px solid #352b59;
    padding: 7px 12px;
    border-radius: 7px;
    cursor: pointer;
    font-size: 12px;
    font-weight: 600;
    transition: all 0.15s ease;
  }}
  button.anim-btn:hover {{ background: #2d2352; border-color: var(--purple-main); color: #fff; }}
  button.anim-btn.active {{
    background: linear-gradient(135deg, #6d28d9, #9333ea);
    border-color: #d8b4fe;
    color: #fff;
    box-shadow: 0 0 12px var(--purple-glow);
  }}
  .controls-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    align-items: center;
    justify-content: center;
    width: 100%;
    margin-top: 8px;
  }}
  .control-group {{ display: flex; align-items: center; gap: 6px; font-size: 13px; color: var(--text-dim); }}
  select {{
    background: #1b1630;
    color: #f3f4f6;
    border: 1px solid #352b59;
    padding: 5px 9px;
    border-radius: 5px;
    font-size: 12px;
  }}
  .frame-indicator {{
    font-family: monospace;
    color: var(--gold);
    font-size: 13px;
    font-weight: bold;
    min-width: 110px;
    text-align: center;
  }}
  h3 {{ font-size: 17px; color: var(--gold); margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; }}
  .thumb-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(76px, 1fr));
    gap: 8px;
    max-height: 540px;
    overflow-y: auto;
    padding-right: 4px;
  }}
  .thumb-item {{
    background: #161229;
    border: 1px solid #2a224a;
    border-radius: 7px;
    padding: 5px;
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: all 0.15s;
  }}
  .thumb-item:hover {{ border-color: var(--gold); transform: translateY(-2px); }}
  .thumb-item img {{ width: 64px; height: 72px; object-fit: contain; image-rendering: pixelated; }}
  .thumb-item span {{ font-size: 10px; color: var(--text-dim); margin-top: 4px; text-align: center; word-break: break-all; }}
</style>
</head>
<body>
<header>
  <h1>👑 VUA BÓNG TỐI (DARK KING) — 128×144 PIXEL ART & SKILL VFX</h1>
  <p class="subtitle">
    Toàn bộ <strong>42 Frames Nhân Vật (128×144 px)</strong> & <strong>16 Textures Hiệu Ứng Kỹ Năng (VFX)</strong> được vẽ mới 100% từ đầu với nền trong suốt (Pure Alpha), góc nhìn 3/4 nghiêng về phía trước, vương miện vàng hoàng gia sắc nét, áo choàng đen phấp phới và bá khí hắc ám.
  </p>
  <div style="margin-top: 8px;">
    <span class="badge gold">Native 128×144 px</span>
    <span class="badge">Góc nghiêng 3/4 (Không nhìn trực diện)</span>
    <span class="badge gold">Vương Miện Vàng Hoàng Gia</span>
    <span class="badge">Áo Choàng Đen & Bá Khí Hắc Ám</span>
    <span class="badge gold">42 Character Frames + 16 VFX Frames</span>
    <span class="badge">100% Transparent PNG</span>
  </div>
</header>

<div class="main-layout">
  <div class="card player-card">
    <div class="canvas-stage bg-check" id="stage">
      <canvas id="animCanvas" width="256" height="288"></canvas>
    </div>
    <div class="anim-btn-bar" id="animButtons"></div>
    <div class="controls-row">
      <button class="anim-btn" id="playPauseBtn">⏸ Tạm dừng</button>
      <button class="anim-btn" id="prevFrameBtn">⏮ Trước</button>
      <button class="anim-btn" id="nextFrameBtn">⏭ Tiếp</button>
      <div class="frame-indicator" id="frameLabel">Frame 1/6</div>
    </div>
    <div class="controls-row" style="margin-top: 12px;">
      <div class="control-group">
        <label>Tốc độ:</label>
        <select id="speedSelect">
          <option value="0.25">0.25x</option>
          <option value="0.5">0.5x</option>
          <option value="1.0" selected>1.0x (Chuẩn)</option>
          <option value="1.5">1.5x</option>
        </select>
      </div>
      <div class="control-group">
        <label>Phóng to:</label>
        <select id="zoomSelect">
          <option value="1">1x (128×144)</option>
          <option value="2" selected>2x (256×288)</option>
          <option value="3">3x (384×432)</option>
        </select>
      </div>
      <div class="control-group">
        <label>Nền:</label>
        <select id="bgSelect">
          <option value="bg-check" selected>Caro Trong Suốt</option>
          <option value="bg-grid">Lưới Kỹ Thuật</option>
          <option value="bg-dark">Đen Hư Không</option>
        </select>
      </div>
    </div>
  </div>

  <div class="card spritesheet-card">
    <h3>
      <span>🖼️ Toàn Bộ 42 Character Frames & 16 Skill VFX Textures</span>
      <a href="game-assets/characters/1/vua_bong_toi_spritesheet.png" target="_blank" style="color:var(--gold); font-size:12px; text-decoration:none; border:1px solid var(--gold); padding:4px 10px; border-radius:6px;">Mở Master Spritesheet</a>
    </h3>
    <div class="thumb-grid" id="thumbGrid"></div>
  </div>
</div>

<script>
const ASSETS = {json.dumps(b64_dict)};

const ANIMATIONS = {{
  idle: {{ name: "1. Idle (6f)", prefix: "characters/1/", frames: ["idle_01.png","idle_02.png","idle_03.png","idle_04.png","idle_05.png","idle_06.png"], ms: [140,140,140,140,140,140], loop: true }},
  move: {{ name: "2. Walk/Run (8f)", prefix: "characters/1/", frames: ["move_01.png","move_02.png","move_03.png","move_04.png","move_05.png","move_06.png","move_07.png","move_08.png"], ms: [65,65,65,65,65,65,65,65], loop: true }},
  attack: {{ name: "3. Basic Attack Combo (6f)", prefix: "characters/1/", frames: ["attack_01.png","attack_02.png","attack_03.png","attack_04.png","attack_05.png","attack_06.png"], ms: [75,85,75,90,95,100], loop: true }},
  dash: {{ name: "4. Dash / Lunge (4f)", prefix: "characters/1/", frames: ["dash_01.png","dash_02.png","dash_03.png","dash_04.png"], ms: [60,60,60,60], loop: true }},
  jump: {{ name: "5a. Jump Leap (3f)", prefix: "characters/1/", frames: ["jump_01.png","jump_02.png","jump_03.png"], ms: [90,110,160], loop: true }},
  fall: {{ name: "5b. Fall & Land (3f)", prefix: "characters/1/", frames: ["fall_01.png","fall_02.png","fall_03.png"], ms: [100,100,130], loop: true }},
  skill: {{ name: "6a. Skill Cast (4f)", prefix: "characters/1/", frames: ["skill_01.png","skill_02.png","skill_03.png","skill_04.png"], ms: [95,100,110,130], loop: true }},
  finisher: {{ name: "6b. Finisher Atomic (4f)", prefix: "characters/1/", frames: ["finisher_01.png","finisher_02.png","finisher_03.png","finisher_04.png"], ms: [100,110,120,160], loop: true }},
  defeat: {{ name: "7. Knockdown / Defeated (4f)", prefix: "characters/1/", frames: ["defeat_01.png","defeat_02.png","defeat_03.png","defeat_04.png"], ms: [110,120,130,300], loop: true }},
  vfx_slash: {{ name: "✨ VFX: Crescent Slash (4f)", prefix: "effects/dark_king/", frames: ["dark_slash_01.png","dark_slash_02.png","dark_slash_03.png","dark_slash_04.png"], ms: [70,70,70,90], loop: true }},
  vfx_orb: {{ name: "🔮 VFX: Dark Orb (4f)", prefix: "effects/dark_king/", frames: ["dark_orb_01.png","dark_orb_02.png","dark_orb_03.png","dark_orb_04.png"], ms: [80,80,80,80], loop: true }},
  vfx_vortex: {{ name: "🕳️ VFX: Ground Rift & Claws (4f)", prefix: "effects/dark_king/", frames: ["dark_vortex_01.png","dark_vortex_02.png","dark_vortex_03.png","dark_vortex_04.png"], ms: [90,90,90,110], loop: true }},
  vfx_impact: {{ name: "💥 VFX: Dark Explosion (4f)", prefix: "effects/dark_king/", frames: ["dark_impact_01.png","dark_impact_02.png","dark_impact_03.png","dark_impact_04.png"], ms: [75,75,75,95], loop: true }}
}};

const imgCache = {{}};
for (const [k, b64] of Object.entries(ASSETS)) {{
  const im = new Image();
  im.src = b64;
  imgCache[k] = im;
}}

let currentAnimKey = 'idle';
let currentFrameIdx = 0;
let isPlaying = true;
let speed = 1.0;
let zoom = 2;
let timer = null;

const canvas = document.getElementById('animCanvas');
const ctx = canvas.getContext('2d');
const btnBar = document.getElementById('animButtons');
const thumbGrid = document.getElementById('thumbGrid');
const frameLabel = document.getElementById('frameLabel');
const playPauseBtn = document.getElementById('playPauseBtn');

for (const [key, anim] of Object.entries(ANIMATIONS)) {{
  const btn = document.createElement('button');
  btn.className = 'anim-btn' + (key === currentAnimKey ? ' active' : '');
  btn.dataset.key = key;
  btn.textContent = anim.name;
  btn.onclick = () => switchAnimation(key);
  btnBar.appendChild(btn);
}}

for (const [key, b64] of Object.entries(ASSETS)) {{
  if (key.includes('spritesheet')) continue;
  const item = document.createElement('div');
  item.className = 'thumb-item';
  const fname = key.split('/').pop();
  item.innerHTML = `<img src="${{b64}}"><span>${{fname}}</span>`;
  item.onclick = () => {{
    for (const [aKey, aData] of Object.entries(ANIMATIONS)) {{
      const idx = aData.frames.indexOf(fname);
      if (idx !== -1) {{
        switchAnimation(aKey);
        currentFrameIdx = idx;
        drawCurrentFrame();
        break;
      }}
    }}
  }};
  thumbGrid.appendChild(item);
}}

function switchAnimation(key) {{
  currentAnimKey = key;
  currentFrameIdx = 0;
  document.querySelectorAll('.anim-btn').forEach(b => {{
    if (b.dataset.key) b.classList.toggle('active', b.dataset.key === key);
  }});
  restartTimer();
  drawCurrentFrame();
}}

function drawCurrentFrame() {{
  const anim = ANIMATIONS[currentAnimKey];
  const fname = anim.frames[currentFrameIdx];
  const key = anim.prefix + fname;
  const img = imgCache[key];
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  if (img && img.complete) {{
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
  }}
  frameLabel.textContent = `${{fname}} (${{currentFrameIdx + 1}}/${{anim.frames.length}})`;
}}

function stepAnimation() {{
  const anim = ANIMATIONS[currentAnimKey];
  currentFrameIdx = (currentFrameIdx + 1) % anim.frames.length;
  drawCurrentFrame();
  restartTimer();
}}

function restartTimer() {{
  if (timer) clearTimeout(timer);
  if (!isPlaying) return;
  const anim = ANIMATIONS[currentAnimKey];
  const ms = (anim.ms[currentFrameIdx] || 90) / speed;
  timer = setTimeout(stepAnimation, ms);
}}

playPauseBtn.onclick = () => {{
  isPlaying = !isPlaying;
  playPauseBtn.textContent = isPlaying ? '⏸ Tạm dừng' : '▶ Tiếp tục';
  if (isPlaying) restartTimer();
  else if (timer) clearTimeout(timer);
}};

document.getElementById('prevFrameBtn').onclick = () => {{
  isPlaying = false;
  playPauseBtn.textContent = '▶ Tiếp tục';
  if (timer) clearTimeout(timer);
  const anim = ANIMATIONS[currentAnimKey];
  currentFrameIdx = (currentFrameIdx - 1 + anim.frames.length) % anim.frames.length;
  drawCurrentFrame();
}};

document.getElementById('nextFrameBtn').onclick = () => {{
  isPlaying = false;
  playPauseBtn.textContent = '▶ Tiếp tục';
  if (timer) clearTimeout(timer);
  const anim = ANIMATIONS[currentAnimKey];
  currentFrameIdx = (currentFrameIdx + 1) % anim.frames.length;
  drawCurrentFrame();
}};

document.getElementById('speedSelect').onchange = (e) => {{
  speed = parseFloat(e.target.value);
  restartTimer();
}};

document.getElementById('zoomSelect').onchange = (e) => {{
  zoom = parseInt(e.target.value);
  canvas.width = 128 * zoom;
  canvas.height = 144 * zoom;
  drawCurrentFrame();
}};

document.getElementById('bgSelect').onchange = (e) => {{
  document.getElementById('stage').className = 'canvas-stage ' + e.target.value;
}};

window.onload = () => {{
  drawCurrentFrame();
  restartTimer();
}};
</script>
</body>
</html>'''

    with open('vua_bong_toi_anim_viewer.html', 'w', encoding='utf-8') as f:
        f.write(viewer_html)
    print("Created vua_bong_toi_anim_viewer.html")

    # 4. Create README
    readme = '''================================================================================
👑 VUA BÓNG TỐI (DARK KING) — TRUE NATIVE 128x144 PIXEL ART & SKILL VFX PACK
================================================================================

1. THIẾT KẾ NHÂN VẬT & QUY CHUẨN GÓC NHÌN:
- Độ phân giải gốc (Native Resolution): 128×144 px mỗi frame, nền trong suốt 100% (PNG Alpha = 0).
- Ngoại hình: Nam nhân trẻ tuổi, khuôn mặt sắc nét chuẩn anime dark-fantasy, đầu đội Vương Miện Vàng (Golden Crown) chạm khắc tinh xảo đính hồng ngọc & thạch anh tím.
- Trang phục: Chiến phục hoàng gia đen tuyền ôm dáng (chevron breastplate, thắt lưng vàng bắt chéo, cổ áo choàng dựng cao viền vàng-tím) kết hợp áo choàng đen dài bay phất phới.
- Bá khí hắc ám (Dark Aura): Luồng hắc khí tím-đen hình chữ S và tàn lửa năng lượng bao quanh cơ thể.
- Góc nhìn (3/4 Side Profile): Luôn đứng và hành động ở góc nghiêng 3/4 hướng về phía trước (+X), tuyệt đối KHÔNG nhìn trực diện vào màn hình/camera.

2. DANH SÁCH 42 FRAMES HOẠT ẢNH NHÂN VẬT (game-assets/characters/1/):
- IDLE (Đứng yên - 6 frames): idle_01.png .. idle_06.png (Thở nhịp nhàng, nhún gối nhẹ, áo choàng lượn sóng, bá khí hắc ám).
- WALK / RUN (Di chuyển - 8 frames): move_01.png .. move_08.png (Chu kỳ chạy 8 bước tự nhiên, đánh tay đối xứng, nghiêng người, áo choàng bay mượt).
- BASIC ATTACKS (Đánh thường combo 3 đòn - 6 frames): attack_01.png .. attack_06.png (Tụ lực -> Chém ngang trăng khuyết -> Thu kiếm -> Bổ dọc -> Đâm xuyên hư không -> Thu thế).
- DASH / LUNGE (Lướt tốc độ cao - 4 frames): dash_01.png .. dash_04.png (Hạ thấp trọng tâm, lao ngang kèm tàn ảnh bóng tối).
- JUMP & LAND (Nhảy & Tiếp đất - 6 frames): jump_01.png .. jump_03.png (Nhún lấy đà, bật nhảy, đạt đỉnh) & fall_01.png .. fall_03.png (Rơi xuống, áo choàng cuộn gió, chùng gối tiếp đất).
- SKILL CASTING & FINISHER (Tung chiêu - 8 frames): skill_01.png .. skill_04.png (Triệu hồi cầu hắc ám & vuốt bóng tối) & finisher_01.png .. finisher_04.png (Tuyệt kỹ Bành Trướng Lãnh Địa / "I AM ATOMIC").
- KNOCKDOWN / DEFEATED (Bị gục - 4 frames): defeat_01.png .. defeat_04.png (Trúng đòn lảo đảo -> khuỵu gối -> cắm kiếm xuống đất gục xuống).
- Bảng tổng hợp: vua_bong_toi_spritesheet.png (768×1008 px, lưới 6×7 gồm toàn bộ 42 frames).

3. BỘ 16 TEXTURES HIỆU ỨNG KỸ NĂNG (game-assets/effects/dark_king/):
- dark_slash_01.png .. dark_slash_04.png (128×128 px): Kiếm khí trăng khuyết hắc ám & vệt năng lượng sắc bén.
- dark_orb_01.png .. dark_orb_04.png (64×64 px): Cầu ma thuật bóng tối với xúc tu hắc ám xoay quanh.
- dark_vortex_01.png .. dark_vortex_04.png (128×128 px): Vết nứt mặt đất & vuốt bóng tối trồi lên.
- dark_impact_01.png .. dark_impact_04.png (128×128 px): Vụ nổ cầu năng lượng tím-đen & hạt bóng tối.
'''
    with open('VUA_BONG_TOI_GRAPHICS_README.txt', 'w', encoding='utf-8') as f:
        f.write(readme)

    # 5. Package clean zip archive: vua-bong-toi-game-graphics-128px.zip
    zip_path = 'vua-bong-toi-game-graphics-128px.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write('index.html')
        zf.write('vua_bong_toi_anim_viewer.html')
        zf.write('VUA_BONG_TOI_GRAPHICS_README.txt')
        zf.write('game-assets/animations.js')
        for f in char_files:
            zf.write(os.path.join('game-assets/characters/1', f))
        for f in fx_files:
            zf.write(os.path.join('game-assets/effects/dark_king', f))
    print(f"Packaged {zip_path} ({os.path.getsize(zip_path)} bytes)")

if __name__ == '__main__':
    main()
