import os, base64, re

HTML_PATH = 'game-cua-lam/game-cua-lam-upload/index.html'
ANIM_PATH = 'game-cua-lam/game-cua-lam-upload/game-assets/animations.js'
CHAR2_DIR = 'game-cua-lam/game-cua-lam-upload/game-assets/characters/2'

def main():
    files = sorted([f for f in os.listdir(CHAR2_DIR) if f.endswith('.png') and 'spritesheet' not in f])
    assert len(files) == 44, f"Expected 44 Hỏa Kage frames, got {len(files)}"

    b64_entries = []
    for f in files:
        with open(os.path.join(CHAR2_DIR, f), 'rb') as img_f:
            b64 = base64.b64encode(img_f.read()).decode('ascii')
            b64_entries.append(f'"characters/2/{f}":"data:image/png;base64,{b64}"')

    char2_anim_js = '''  2: {
    idle: {frames:[{src:"characters/2/idle_01.png",ms:135},{src:"characters/2/idle_02.png",ms:135},{src:"characters/2/idle_03.png",ms:135},{src:"characters/2/idle_04.png",ms:135},{src:"characters/2/idle_05.png",ms:135},{src:"characters/2/idle_06.png",ms:135}],loop:true,width:64,height:72,offsetY:6},
    move: {frames:[{src:"characters/2/move_01.png",ms:65},{src:"characters/2/move_02.png",ms:65},{src:"characters/2/move_03.png",ms:65},{src:"characters/2/move_04.png",ms:65},{src:"characters/2/move_05.png",ms:65},{src:"characters/2/move_06.png",ms:65},{src:"characters/2/move_07.png",ms:65},{src:"characters/2/move_08.png",ms:65}],loop:true,width:64,height:72,offsetY:6},
    jump: {frames:[{src:"characters/2/jump_01.png",ms:65},{src:"characters/2/jump_02.png",ms:90},{src:"characters/2/jump_03.png",ms:140}],loop:false,width:64,height:72,offsetY:6},
    fall: {frames:[{src:"characters/2/fall_01.png",ms:90},{src:"characters/2/fall_02.png",ms:90},{src:"characters/2/fall_03.png",ms:110}],loop:true,width:64,height:72,offsetY:6,flip:false},
    attack: {frames:[{src:"characters/2/attack_01.png",ms:55},{src:"characters/2/attack_02.png",ms:65},{src:"characters/2/attack_03.png",ms:55},{src:"characters/2/attack_04.png",ms:65},{src:"characters/2/attack_05.png",ms:75},{src:"characters/2/attack_06.png",ms:75}],loop:false,width:64,height:72,offsetY:6},
    skill: {frames:[{src:"characters/2/skill_01.png",ms:80},{src:"characters/2/skill_02.png",ms:85},{src:"characters/2/skill_03.png",ms:95},{src:"characters/2/skill_04.png",ms:110}],loop:false,width:64,height:72,offsetY:6},
    finisher: {frames:[{src:"characters/2/finisher_01.png",ms:85},{src:"characters/2/finisher_02.png",ms:90},{src:"characters/2/finisher_03.png",ms:105},{src:"characters/2/finisher_04.png",ms:130}],loop:false,width:64,height:72,offsetY:6},
    dash: {frames:[{src:"characters/2/dash_01.png",ms:50},{src:"characters/2/dash_02.png",ms:50},{src:"characters/2/dash_03.png",ms:50},{src:"characters/2/dash_04.png",ms:50}],loop:true,width:64,height:72,offsetY:6},
    hit: {frames:[{src:"characters/2/hit_01.png",ms:80},{src:"characters/2/hit_02.png",ms:100}],loop:false,width:64,height:72,offsetY:6},
    defeat: {frames:[{src:"characters/2/defeat_01.png",ms:90},{src:"characters/2/defeat_02.png",ms:100},{src:"characters/2/defeat_03.png",ms:110},{src:"characters/2/defeat_04.png",ms:250}],loop:false,width:64,height:72,offsetY:6,flip:false}
  },'''

    # 1. Update game-assets/animations.js
    with open(ANIM_PATH, 'r', encoding='utf-8') as f:
        anim_js = f.read()
    pattern_c2 = re.compile(r'  2:\s*\{[\s\S]*?defeat:\s*\{[^\}]+\}\s*\},')
    if pattern_c2.search(anim_js):
        anim_js = pattern_c2.sub(char2_anim_js, anim_js, count=1)
    else:
        anim_js = anim_js.replace('  3: {\n', char2_anim_js + '\n  3: {\n', 1)
    with open(ANIM_PATH, 'w', encoding='utf-8') as f:
        f.write(anim_js)

    # 2. Patch index.html
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # Clean old characters/2 base64 if any, then inject all 44 frames
    html = re.sub(r'"characters/2/[^"]+":\s*"data:image/png;base64,[^"]+",?', '', html)
    marker_asset = 'window.GAME_ASSET_DATA={'
    assert marker_asset in html
    html = html.replace(marker_asset, marker_asset + ','.join(b64_entries) + ',', 1)

    # Register character 2 in GAME_ANIMATIONS inside index.html
    if pattern_c2.search(html):
        html = pattern_c2.sub(char2_anim_js, html, count=1)
    else:
        html = html.replace('  3: {\n', char2_anim_js + '\n  3: {\n', 1)

    # Enable 'hit' animation state in silverState for characters that define 'hit' (Hỏa Kage!)
    old_ss = "if(defeated)return'defeat';if(p.silverLiftTime>0)return'jump';"
    new_ss = "if(defeated)return'defeat';if(p.hitFlash>0&&window.GAME_ANIMATIONS?.characters?.[p.char]?.hit)return'hit';if(p.silverLiftTime>0)return'jump';"
    if "?.hit)return'hit'" not in html:
        assert old_ss in html, "silverState anchor not found"
        html = html.replace(old_ss, new_ss, 1)

    # Add 100x Upgraded Hỏa Kage Skill & Movement VFX Renderer Functions!
    html = re.sub(r'// === HOA KAGE 100X VFX START ===[\s\S]*?// === HOA KAGE 100X VFX END ===\n?', '', html)
    fire_vfx_helpers = r'''// === HOA KAGE 100X VFX START ===
function drawFireGroundTrailVfx(e,a){
 ctx.save();
 const k=1-a,d=e.dir||1,awakened=!!e.awakened;
 ctx.globalCompositeOperation='lighter';
 // Scorched glowing ember seam on the ground
 const len=44*(0.5+a*0.6);
 const g=ctx.createLinearGradient(e.x,e.y,e.x-d*len,e.y);
 g.addColorStop(0,awakened?'rgba(56,189,248,0.85)':'rgba(255,212,56,0.9)');
 g.addColorStop(0.5,awakened?'rgba(232,59,80,0.65)':'rgba(255,106,23,0.75)');
 g.addColorStop(1,'rgba(0,0,0,0)');
 ctx.strokeStyle=g;ctx.lineWidth=4*a+1;ctx.lineCap='round';
 ctx.beginPath();ctx.moveTo(e.x,e.y);ctx.lineTo(e.x-d*len,e.y);ctx.stroke();
 // Flickering fire tongues rising off the ground trail
 for(let i=0;i<6;i++){
  const fx=e.x-d*(i*7+k*10),fh=(12+(i%3)*7)*a;
  ctx.fillStyle=awakened?(i%2?'#38bdf8cc':'#ff3b5ccc'):(i%2?'#ff7817cc':'#ffd438cc');
  ctx.beginPath();ctx.moveTo(fx-4,e.y);ctx.quadraticCurveTo(fx+Math.sin(clock*24+i)*4,e.y-fh,fx+4,e.y);ctx.fill();
  ctx.fillStyle='#fffbe0aa';
  ctx.beginPath();ctx.moveTo(fx-1.5,e.y);ctx.quadraticCurveTo(fx,e.y-fh*0.6,fx+1.5,e.y);ctx.fill();
 }
 // Rising sparks
 for(let i=0;i<5;i++){
  const sx=e.x-d*(i*8+k*14),sy=e.y-k*(16+(i%3)*10);
  ctx.fillStyle=i%2?'#fffbe0':(awakened?'#60d8ff':'#ff922b');
  ctx.fillRect(Math.round(sx),Math.round(sy),2,2);
 }
 ctx.restore();
}
function drawFireJumpSparksVfx(e,a){
 ctx.save();
 const k=1-a,awakened=!!e.awakened;
 ctx.globalCompositeOperation='lighter';
 // Fiery takeoff ring
 ctx.strokeStyle=awakened?'#45baff':'#ff922b';ctx.globalAlpha=a*0.85;ctx.lineWidth=2.5*a+0.5;
 ctx.beginPath();ctx.ellipse(e.x,e.y,10+k*22,3+k*5,0,0,Math.PI*2);ctx.stroke();
 // Small flame sparks bursting outward & upward!
 for(let i=0;i<10;i++){
  const ang=-Math.PI+(i/9)*Math.PI;
  const dist=8+k*(26+(i%3)*12);
  const px=e.x+Math.cos(ang)*dist,py=e.y+Math.sin(ang)*dist*0.75-k*8;
  ctx.globalAlpha=a;
  ctx.fillStyle=i%3===0?'#fffbe0':(awakened?(i%2?'#38bdf8':'#ff3b5c'):(i%2?'#ffd438':'#ff6b1a'));
  ctx.beginPath();ctx.arc(px,py,2.2*a+0.6,0,Math.PI*2);ctx.fill();
 }
 ctx.restore();
}
function drawEpicFireSlashVfx(e,a){
 ctx.save();
 const k=1-a,d=e.dir||1,awakened=!!e.awakened;
 ctx.globalCompositeOperation='lighter';ctx.translate(e.x,e.y);ctx.scale(d,1);
 // Giant blazing flame crescent arc!
 const r=(awakened?52:38)+k*(awakened?34:22);
 ctx.globalAlpha=Math.min(1,a*1.25);ctx.lineCap='round';
 ctx.strokeStyle=awakened?'#e83b50':'#cc2200';ctx.lineWidth=(awakened?20:14)*a+2;
 ctx.beginPath();ctx.arc(-14,0,r,-Math.PI*.48,Math.PI*.48);ctx.stroke();
 ctx.strokeStyle=awakened?'#22aaff':'#ff7b1c';ctx.lineWidth=(awakened?12:8)*a+1;
 ctx.beginPath();ctx.arc(-10,0,r+2,-Math.PI*.44,Math.PI*.44);ctx.stroke();
 ctx.strokeStyle=awakened?'#a5f3fc':'#ffe047';ctx.lineWidth=(awakened?6:4)*a;
 ctx.beginPath();ctx.arc(-6,0,r+4,-Math.PI*.38,Math.PI*.38);ctx.stroke();
 ctx.strokeStyle='#ffffff';ctx.lineWidth=2*a;
 ctx.beginPath();ctx.arc(-4,0,r+5,-Math.PI*.32,Math.PI*.32);ctx.stroke();
 // Roaring fire tongues & sparks along the crescent
 for(let i=0;i<9;i++){
  const ang=-1.1+i*0.275,rr=r+4+Math.sin(clock*30+i)*5;
  const fx=Math.cos(ang)*rr-8,fy=Math.sin(ang)*rr;
  ctx.fillStyle=i%3===0?'#ffffff':(awakened?(i%2?'#38bdf8':'#ff4769'):(i%2?'#ffd438':'#ff6b1a'));
  ctx.fillRect(Math.round(fx),Math.round(fy),3,3);
 }
 ctx.restore();
}
function drawEpicFireTornadoVfx(e,a){
 ctx.save();
 const k=1-a,sc=e.scale||(e.awakened?1.65:1.15),awakened=!!e.awakened;
 const h=(52+(1-k)*160)*sc,r=(16+(1-k)*34)*sc;
 ctx.globalCompositeOperation='lighter';ctx.globalAlpha=Math.min(1,a*1.2);
 // Molten ground crater & heat ring
 const cg=ctx.createRadialGradient(e.x,e.y,4,e.x,e.y,r*1.5);
 cg.addColorStop(0,awakened?'rgba(56,189,248,0.8)':'rgba(255,212,56,0.85)');
 cg.addColorStop(0.5,awakened?'rgba(232,59,80,0.45)':'rgba(255,90,20,0.5)');
 cg.addColorStop(1,'rgba(0,0,0,0)');
 ctx.fillStyle=cg;ctx.beginPath();ctx.ellipse(e.x,e.y,r*1.5,14*sc,0,0,Math.PI*2);ctx.fill();
 // 10 Spiraling 3D Flame Dragon Vortex Rings!
 for(let i=0;i<10;i++){
  const t=i/9,yy=e.y-t*h,rr=(r*(0.3+t*0.95))*(0.85+0.15*Math.sin(clock*22+i));
  const swX=e.x+Math.sin(clock*11+i*1.4)*10*sc;
  ctx.strokeStyle=awakened?(i%2?'#38bdf8':'#ff3b5c'):(i%3===0?'#fff099':i%2?'#ff7817':'#e02414');
  ctx.lineWidth=(5.5-t*2.5)*sc;
  ctx.beginPath();ctx.ellipse(swX,yy,rr,8*sc,Math.sin(clock*6+i)*0.25,0,Math.PI*2);ctx.stroke();
 }
 // Blazing central plasma pillar
 const pg=ctx.createLinearGradient(e.x-14*sc,0,e.x+14*sc,0);
 pg.addColorStop(0,'rgba(0,0,0,0)');
 pg.addColorStop(0.3,awakened?'rgba(232,59,80,0.6)':'rgba(255,100,20,0.65)');
 pg.addColorStop(0.5,'rgba(255,252,225,0.85)');
 pg.addColorStop(0.7,awakened?'rgba(56,189,248,0.6)':'rgba(255,100,20,0.65)');
 pg.addColorStop(1,'rgba(0,0,0,0)');
 ctx.fillStyle=pg;ctx.fillRect(e.x-14*sc,e.y-h,28*sc,h);
 // Orbiting blazing embers
 for(let i=0;i<16;i++){
  const q=clock*9+i*Math.PI/8,rr=12+((i*17+k*40)%(r*1.3));
  const ey=e.y-((clock*110+i*23)%h);
  ctx.fillStyle=i%3===0?'#ffffff':(awakened?(i%2?'#38bdf8':'#ff4769'):(i%2?'#ffd438':'#ff6b1a'));
  ctx.fillRect(Math.round(e.x+Math.cos(q)*rr),Math.round(ey),3,4);
 }
 ctx.restore();
}
function drawEpicFireBeamVfx(e,a){
 ctx.save();
 const ang=Math.atan2(e.dirY||0,e.dirX||1),len=e.range||260,awakened=!!e.awakened;
 ctx.translate(e.x,e.y);ctx.rotate(ang);ctx.globalCompositeOperation='lighter';
 // Origin shockwave rings at Hỏa Kage's fist!
 ctx.strokeStyle=awakened?'#38bdf8':'#ffd438';ctx.lineWidth=3*a;
 ctx.beginPath();ctx.ellipse(8,0,6,22+Math.sin(clock*25)*4,0,0,Math.PI*2);ctx.stroke();
 ctx.strokeStyle=awakened?'#ff3b5c':'#ff6b1a';ctx.lineWidth=2*a;
 ctx.beginPath();ctx.ellipse(24,0,5,16,0,0,Math.PI*2);ctx.stroke();
 // Multi-layered blazing solar beam
 const w=(awakened?44:34)*a+6;
 ctx.fillStyle=awakened?'rgba(232,59,80,0.45)':'rgba(220,40,12,0.5)';ctx.fillRect(0,-w/2,len,w);
 ctx.fillStyle=awakened?'rgba(56,189,248,0.75)':'rgba(255,120,23,0.8)';ctx.fillRect(6,-w*0.32,len-12,w*0.64);
 ctx.fillStyle='#fffbe6';ctx.fillRect(10,-w*0.14,len-20,w*0.28);
 // Two roaring sinusoidal flame ribbons twisting down the beam!
 for(let s=0;s<2;s++){
  ctx.strokeStyle=s===0?(awakened?'#38bdf8':'#ffd438'):(awakened?'#ff4769':'#ff5e1a');
  ctx.lineWidth=3.5*a;ctx.beginPath();
  for(let x=0;x<=len;x+=12){const y=Math.sin(x*0.055-clock*26+s*Math.PI)*(w*0.42);if(x===0)ctx.moveTo(x,y);else ctx.lineTo(x,y)}
  ctx.stroke();
 }
 ctx.restore();
}
function drawEpicFireAwakenVfx(e,a){
 ctx.save();
 const k=1-a,pulse=.5+.5*Math.sin(clock*22);
 ctx.globalCompositeOperation='lighter';ctx.globalAlpha=Math.min(1,a*1.3);
 // Blazing Giant Phoenix Fire Wings unfolding behind Hỏa Kage!
 for(const side of [-1,1]){
  ctx.fillStyle='rgba(255,95,20,0.55)';
  ctx.beginPath();ctx.moveTo(e.x,e.y);
  ctx.quadraticCurveTo(e.x+side*(44+k*38),e.y-46-k*20,e.x+side*(74+k*44),e.y-22-k*14);
  ctx.quadraticCurveTo(e.x+side*(48+k*26),e.y+2,e.x+side*(18+k*12),e.y+12);ctx.closePath();ctx.fill();
  ctx.strokeStyle='#ffd438';ctx.lineWidth=2.5*a;ctx.stroke();
  ctx.fillStyle='rgba(255,235,140,0.75)';
  ctx.beginPath();ctx.moveTo(e.x,e.y);
  ctx.quadraticCurveTo(e.x+side*(32+k*26),e.y-30-k*12,e.x+side*(52+k*30),e.y-12-k*8);
  ctx.quadraticCurveTo(e.x+side*(28+k*14),e.y+2,e.x,e.y+6);ctx.closePath();ctx.fill();
 }
 // Solar shockwave rings
 ctx.strokeStyle='#ff6b1a';ctx.lineWidth=4*a;ctx.beginPath();ctx.arc(e.x,e.y,18+k*56,0,Math.PI*2);ctx.stroke();
 ctx.strokeStyle='#fff3a0';ctx.lineWidth=2*a;ctx.beginPath();ctx.arc(e.x,e.y,12+k*42+pulse*4,0,Math.PI*2);ctx.stroke();
 ctx.restore();
}
// === HOA KAGE 100X VFX END ===
'''
    assert 'function drawDarkKingOrb(' in html
    html = html.replace('function drawDarkKingOrb(', fire_vfx_helpers + 'function drawDarkKingOrb(', 1)

    # Hook new fire VFX inside drawCombatVfx so BOTH PvP and RPG automatically get the 100x upgraded visuals!
    old_vfx_hook = "if(e.type==='silverGrandSlash'){drawSilverGrandSlash(e,a);return}"
    new_vfx_hook = "if(e.type==='silverGrandSlash'){drawSilverGrandSlash(e,a);return}if(e.type==='fireGroundTrail'){drawFireGroundTrailVfx(e,a);return}if(e.type==='fireJumpSparks'){drawFireJumpSparksVfx(e,a);return}if(e.type==='fireslash'){drawEpicFireSlashVfx(e,a);return}if(e.type==='firetornado'){drawEpicFireTornadoVfx(e,a);return}if(e.type==='firebreath'||e.type==='firebeam'){drawEpicFireBeamVfx(e,a);return}if(e.type==='fireawaken'){drawEpicFireAwakenVfx(e,a);return}"
    assert old_vfx_hook in html, "drawCombatVfx hook not found"
    html = html.replace(old_vfx_hook, new_vfx_hook, 1)

    # Suppress old boxy duplicate fireslash/fireawaken/firebreath draws in PvP & RPG effect loops so only our 100x upgraded VFX renders!
    html = html.replace("if(e.type==='fireslash'){", "if(false&&e.type==='fireslash'){")
    html = html.replace("if(e.type==='fireawaken'){", "if(false&&e.type==='fireawaken'){")
    html = html.replace("if(e.type==='firebreath'){", "if(false&&e.type==='firebreath'){")

    # Spawn fireGroundTrail when Hỏa Kage dashes (PvP & RPG) AND fireJumpSparks when Hỏa Kage jumps (PvP & RPG)!
    # PvP jump
    old_pvp_jump = "addEffect({type:'dust',x:p.x,y:FLOOR-3,life:.28,max:.28,c:chars[p.char].accent})"
    new_pvp_jump = "addEffect({type:chars[p.char].style==='fire'?'fireJumpSparks':'dust',x:p.x,y:FLOOR-3,life:.34,max:.34,c:chars[p.char].accent,awakened:p.fireUlt>0})"
    assert old_pvp_jump in html, "PvP jump dust not found"
    html = html.replace(old_pvp_jump, new_pvp_jump, 1)

    # PvP dash
    old_pvp_dash = "addEffect({type:'dash',x:p.x,y:p.y-20,life:.25,max:.25,dir:p.face,c:c.accent})"
    new_pvp_dash = "addEffect({type:'dash',x:p.x,y:p.y-20,life:.25,max:.25,dir:p.face,c:c.accent});if(c.style==='fire')addEffect({type:'fireGroundTrail',x:p.x,y:FLOOR-2,life:.55,max:.55,dir:p.face,awakened:p.fireUlt>0})"
    assert old_pvp_dash in html, "PvP dash not found"
    html = html.replace(old_pvp_dash, new_pvp_dash, 1)

    # RPG jump & dash for Hỏa Kage
    old_rpg_dash = "p.dash=.2;p.dashCd=chars[p.char].style==='void'&&p.domain>0?.75:.2;p.vx=p.face*7.5;p.invuln=.2"
    new_rpg_dash = "p.dash=.2;p.dashCd=chars[p.char].style==='void'&&p.domain>0?.75:.2;p.vx=p.face*7.5;p.invuln=.2;if(chars[p.char].style==='fire')addEffect({type:'fireGroundTrail',x:p.x-rpg.camera,y:FLOOR-2,life:.55,max:.55,dir:p.face,awakened:p.fireUlt>0})"
    assert old_rpg_dash in html, "RPG dash not found"
    html = html.replace(old_rpg_dash, new_rpg_dash, 1)

    # Continuous fire ground embers while Hỏa Kage is dashing in drawFighter
    old_df_burn = "if(p.burnTimer>0)drawBurnParticles(x,foot-8,p.id||0);"
    new_df_burn = "if(p.burnTimer>0)drawBurnParticles(x,foot-8,p.id||0);if(!preview&&c.style==='fire'&&p.dash>0&&Math.random()<.55)addEffect({type:'fireGroundTrail',x,y:FLOOR-2,life:.42,max:.42,dir,awakened:p.fireUlt>0});"
    assert old_df_burn in html, "drawFighter burn anchor not found"
    html = html.replace(old_df_burn, new_df_burn, 1)

    # Update Hỏa Kage description & colors in chars array
    html = html.replace(
        "{name:'HỎA KAGE',side:'SHINOBI',desc:'Hỏa quyền · cầu lửa và thiên thạch',skills:['CỘT LỬA','HỎA QUYỀN','PHƯỢNG VŨ'],hair:'#17151a',coat:'#b62d34',accent:'#ff8733',skin:'#e4b18c',style:'fire'}",
        "{name:'HỎA KAGE',side:'SHINOBI',desc:'Hỏa Thần Phóng Khoáng · hỏa quyền và phượng hoàng lửa',skills:['CỘT LỬA','HỎA QUYỀN','PHƯỢNG VŨ'],hair:'#14111a',coat:'#e33b84',accent:'#ff7817',skin:'#f2be96',style:'fire'}"
    )

    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully integrated 44 native 128x144 Hỏa Kage frames + 100x upgraded fire VFX into index.html and animations.js!")

if __name__ == '__main__':
    main()
