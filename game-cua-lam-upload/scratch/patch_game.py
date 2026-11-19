import json, re

# 1. Update game-assets/animations.js
with open('game-assets/animations.js', 'r', encoding='utf-8') as f:
    anim_js = f.read()

anim_char3 = '''  3: {
    idle: {frames:[{src:"characters/3/idle_01.png",ms:240},{src:"characters/3/idle_02.png",ms:240}],loop:true,width:64,height:72,offsetY:6},
    move: {frames:[{src:"characters/3/move_01.png",ms:95},{src:"characters/3/move_02.png",ms:95},{src:"characters/3/move_03.png",ms:95},{src:"characters/3/move_04.png",ms:95}],loop:true,width:64,height:72,offsetY:6},
    jump: {frames:[{src:"characters/3/jump_01.png",ms:140}],loop:false,width:64,height:72,offsetY:6},
    fall: {frames:[{src:"characters/3/fall_01.png",ms:160}],loop:true,width:64,height:72,offsetY:6,flip:false},
    attack: {frames:[{src:"characters/3/attack_01.png",ms:75},{src:"characters/3/attack_02.png",ms:75},{src:"characters/3/attack_03.png",ms:110}],loop:false,width:64,height:72,offsetY:6},
    skill: {frames:[{src:"characters/3/skill_01.png",ms:110},{src:"characters/3/skill_02.png",ms:100},{src:"characters/3/skill_03.png",ms:140}],loop:false,width:64,height:72,offsetY:6},
    finisher: {frames:[{src:"characters/3/finisher_01.png",ms:110},{src:"characters/3/finisher_02.png",ms:90},{src:"characters/3/finisher_03.png",ms:160}],loop:false,width:64,height:72,offsetY:6},
    dash: {frames:[{src:"characters/3/dash_01.png",ms:70},{src:"characters/3/dash_02.png",ms:70}],loop:true,width:64,height:72,offsetY:6},
    defeat: {frames:[{src:"characters/3/defeat_01.png",ms:200}],loop:false,width:64,height:72,offsetY:6,flip:false}
  }'''

if 'characters/3/idle_01.png' not in anim_js:
    target = 'characters: {\n  0: {'
    replacement = 'characters: {\n' + anim_char3 + ',\n  0: {'
    if target in anim_js:
        anim_js = anim_js.replace(target, replacement, 1)
        with open('game-assets/animations.js', 'w', encoding='utf-8') as f:
            f.write(anim_js)
        print('Updated game-assets/animations.js successfully.')
    else:
        print('Could not find target in animations.js')
else:
    print('animations.js already contains characters/3.')

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

# Load b64 assets
with open('scratch/summoner_b64.json', 'r', encoding='utf-8') as f:
    b64_assets = json.load(f)

# Update GAME_ASSET_DATA
# Line 11 is <script>window.GAME_ASSET_DATA={...};
prefix = '<script>window.GAME_ASSET_DATA='
if prefix in index_html:
    start_pos = index_html.index(prefix) + len(prefix)
    end_pos = index_html.index('};', start_pos) + 1
    asset_data_json = index_html[start_pos:end_pos]
    try:
        data_obj = json.loads(asset_data_json)
        # merge b64_assets
        for k, v in b64_assets.items():
            data_obj[k] = v
        new_asset_json = json.dumps(data_obj)
        index_html = index_html[:start_pos] + new_asset_json + index_html[end_pos:]
        print('Merged base64 sprites into window.GAME_ASSET_DATA in index.html.')
    except Exception as e:
        print('Error parsing GAME_ASSET_DATA:', e)

# Update window.GAME_ANIMATIONS in index.html
if 'characters/3/idle_01.png' not in index_html:
    target_anim = 'characters: {\n  0: {'
    if target_anim in index_html:
        index_html = index_html.replace(target_anim, 'characters: {\n' + anim_char3 + ',\n  0: {', 1)
        print('Added character 3 to window.GAME_ANIMATIONS in index.html.')
    else:
        # maybe different indentation?
        target_anim2 = 'characters: {\n   0: {'
        if target_anim2 in index_html:
            index_html = index_html.replace(target_anim2, 'characters: {\n' + anim_char3 + ',\n   0: {', 1)
            print('Added character 3 (indent 3) to window.GAME_ANIMATIONS in index.html.')
        else:
            print('Could not find window.GAME_ANIMATIONS characters target in index.html.')

# Update silverAnimationFrame in index.html to support all characters
old_frame_fn = 'const silverFrameCache=new Map();function silverAnimationFrame(p,state){const root=window.GAME_ANIMATIONS?.characters?.[0],anim=root?.[state]||root?.idle;'
new_frame_fn = 'const silverFrameCache=new Map();function silverAnimationFrame(p,state){const cid=(p&&p.char!=null)?p.char:0;const root=window.GAME_ANIMATIONS?.characters?.[cid]||window.GAME_ANIMATIONS?.characters?.[0],anim=root?.[state]||root?.idle;'
if old_frame_fn in index_html:
    index_html = index_html.replace(old_frame_fn, new_frame_fn, 1)
    print('Updated silverAnimationFrame to support dynamic character sprite lookup.')
else:
    print('silverAnimationFrame signature not matched, checking if already updated...')

# Also make sure image.src falls back to src if not in window.GAME_ASSET_DATA
old_img_src = 'image.src=window.GAME_ASSET_DATA?.[src]||\'\';'
new_img_src = 'image.src=window.GAME_ASSET_DATA?.[src]||src||\'\';'
if old_img_src in index_html:
    index_html = index_html.replace(old_img_src, new_img_src)
    print('Updated image.src fallback to local file path.')

# Update drawFighter condition to check window.GAME_ANIMATIONS?.characters?.[p.char]
old_draw_cond = 'if(c.style===\'silver\'){const frame=silverAnimationFrame(p,preview?\'idle\':silverState(p,airborne,falling,defeated,actionOn));if(frame){ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(x,foot);ctx.scale(dir,1);ctx.drawImage(frame.image,-frame.anim.width/2,-frame.anim.height+(frame.anim.offsetY||0),frame.anim.width,frame.anim.height);ctx.restore();if(p.burnTimer>0)drawBurnParticles(x,foot-8,p.id||0)}return}'
new_draw_cond = '''if(window.GAME_ANIMATIONS?.characters?.[p.char]){const frame=silverAnimationFrame(p,preview?'idle':silverState(p,airborne,falling,defeated,actionOn));if(frame){ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(x,foot);ctx.scale(dir,1);ctx.drawImage(frame.image,-frame.anim.width/2,-frame.anim.height+(frame.anim.offsetY||0),frame.anim.width,frame.anim.height);ctx.restore();if(p.burnTimer>0)drawBurnParticles(x,foot-8,p.id||0);if(c.style==='summoner'&&!preview&&p.summonShield>0){ctx.save();const pulse=.5+.5*Math.sin(clock*7);ctx.globalAlpha=.22+.12*pulse;ctx.fillStyle='#a8e87944';ctx.shadowColor='#a2ef76';ctx.shadowBlur=18;ctx.beginPath();ctx.ellipse(x,foot-30,34,53,0,0,Math.PI*2);ctx.fill();ctx.globalAlpha=.82;ctx.strokeStyle='#b9ff9c';ctx.lineWidth=3;ctx.beginPath();ctx.ellipse(x,foot-30,32,51,Math.sin(clock*2)*.035,0,Math.PI*2);ctx.stroke();ctx.strokeStyle='#54d4ba';ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(x,foot-30,26,44,-Math.sin(clock*2)*.035,0,Math.PI*2);ctx.stroke();ctx.strokeStyle='#d9ffbd';ctx.lineWidth=1;ctx.beginPath();ctx.ellipse(x,foot-30,36,56,0,0,Math.PI*2);ctx.stroke();ctx.restore()}return}}'''

if old_draw_cond in index_html:
    index_html = index_html.replace(old_draw_cond, new_draw_cond, 1)
    print('Updated drawFighter condition in index.html to render characters with sprite animations.')
else:
    print('drawFighter old condition not matched, checking pattern...')
    # let's find c.style==='silver' in drawFighter
    patt = r"if\(c\.style==='silver'\)\{const frame=silverAnimationFrame\(p,preview\?'idle':silverState\(p,airborne,falling,defeated,actionOn\);if\(frame\)\{ctx\.save\(\);ctx\.imageSmoothingEnabled=false;ctx\.translate\(x,foot\);ctx\.scale\(dir,1\);ctx\.drawImage\(frame\.image,-frame\.anim\.width/2,-frame\.anim\.height\+\(frame\.anim\.offsetY\|\|0\),frame\.anim\.width,frame\.anim\.height\);ctx\.restore\(\);if\(p\.burnTimer>0\)drawBurnParticles\(x,foot-8,p\.id\|\|0\)\}return\}"
    if re.search(patt, index_html):
        index_html = re.sub(patt, new_draw_cond, index_html, count=1)
        print('Matched with regex and updated drawFighter condition!')

# Update chars[3] colors to match reference design
# Current: hair:'#d8c6a4',coat:'#26314b',accent:'#8ce6c2',skin:'#d5ab88'
# Update to: hair:'#ea8350',coat:'#232f4a',accent:'#6ee3bd',skin:'#fedecb'
old_char3 = "{name:'TRIỆU HỒI SƯ',side:'SHINOBI',desc:'Pháp sư áo choàng · triệu hồi linh thú',skills:['TRIỆU HỒI CỐT BINH','LINH VỰC HỒI PHỤC','VẠN THÚ TRIỀU TÔNG'],hair:'#d8c6a4',coat:'#26314b',accent:'#8ce6c2',skin:'#d5ab88',style:'summoner'}"
new_char3 = "{name:'TRIỆU HỒI SƯ',side:'SHINOBI',desc:'Pháp sư quỷ tộc · triệu hồi linh thú',skills:['TRIỆU HỒI CỐT BINH','LINH VỰC HỒI PHỤC','VẠN THÚ TRIỀU TÔNG'],hair:'#ea8350',coat:'#232f4a',accent:'#6ee3bd',skin:'#fedecb',style:'summoner'}"
if old_char3 in index_html:
    index_html = index_html.replace(old_char3, new_char3)
    print('Updated Triệu Hồi Sư character description and color definition.')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print('Finished updating index.html.')
