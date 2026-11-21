import os, base64, re

HTML_PATH = 'game-cua-lam/game-cua-lam-upload/index.html'
THRONE_PATH = 'game-cua-lam/game-cua-lam-upload/game-assets/effects/dark_king/dark_throne.png'

def main():
    with open(THRONE_PATH, 'rb') as f:
        throne_b64 = 'data:image/png;base64,' + base64.b64encode(f.read()).decode('ascii')

    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Inject dark_throne.png into GAME_ASSET_DATA
    html = re.sub(r'"effects/dark_king/dark_throne\.png":"data:image/png;base64,[^"]+",?', '', html)
    marker_asset = 'window.GAME_ASSET_DATA={'
    assert marker_asset in html, "GAME_ASSET_DATA marker not found"
    html = html.replace(marker_asset, marker_asset + f'"effects/dark_king/dark_throne.png":"{throne_b64}",', 1)

    # 2. Add helper VFX & Domain rendering functions right before drawSilverBird
    # Remove old helpers if re-running
    html = re.sub(r'// === DARK KING UPGRADED VFX START ===[\s\S]*?// === DARK KING UPGRADED VFX END ===\n?', '', html)

    upgraded_helpers = r'''// === DARK KING UPGRADED VFX START ===
let darkThroneImg=null;
function getDarkThroneImg(){if(!darkThroneImg){darkThroneImg=new Image();darkThroneImg.src=window.GAME_ASSET_DATA?.['effects/dark_king/dark_throne.png']||'';}return darkThroneImg.complete&&darkThroneImg.naturalWidth?darkThroneImg:null}
function drawShadowTentacle(bx,by,len,baseW,ang,phase,colCore='#07050c',colEdge='#8d42f0'){
 ctx.save();const segs=10,pts=[];let cx=bx,cy=by;
 for(let i=0;i<=segs;i++){const t=i/segs,sway=Math.sin(clock*3.4+phase+t*3.8)*(6+t*14),a=ang+sway*.025;cx+=Math.cos(a)*(len/segs);cy+=Math.sin(a)*(len/segs);pts.push({x:cx,y:cy,w:Math.max(1.2,baseW*(1-t*.86))})}
 ctx.lineCap='round';ctx.lineJoin='round';
 // Outer eerie purple-crimson aura
 for(let i=0;i<segs;i++){ctx.strokeStyle=colEdge+'66';ctx.lineWidth=pts[i].w+4;ctx.beginPath();ctx.moveTo(pts[i].x,pts[i].y);ctx.lineTo(pts[i+1].x,pts[i+1].y);ctx.stroke()}
 // Solid pitch-black tentacle body
 for(let i=0;i<segs;i++){ctx.strokeStyle=colCore;ctx.lineWidth=pts[i].w;ctx.beginPath();ctx.moveTo(pts[i].x,pts[i].y);ctx.lineTo(pts[i+1].x,pts[i+1].y);ctx.stroke()}
 // Inner glowing rim vein
 ctx.strokeStyle=colEdge+'aa';ctx.lineWidth=1.2;ctx.beginPath();ctx.moveTo(pts[0].x,pts[0].y);for(let i=1;i<=segs;i++)ctx.lineTo(pts[i].x,pts[i].y);ctx.stroke();
 ctx.restore();
}
function drawDarkDomainBackdrop(domainUser,isRpg=false){
 ctx.save();
 // Deep abyssal dark-crimson & void-purple gradient sky
 const topY=isRpg?42:0;
 const grad=ctx.createRadialGradient(240,145,24,240,145,270);
 grad.addColorStop(0,'rgba(42,10,36,0.78)');
 grad.addColorStop(0.55,'rgba(14,6,26,0.86)');
 grad.addColorStop(1,'rgba(3,1,8,0.94)');
 ctx.fillStyle=grad;ctx.fillRect(0,topY,W,H-topY);
 // Subtle pulsing crimson moon halo behind throne
 const pulse=.5+.5*Math.sin(clock*4.5);
 ctx.fillStyle=`rgba(168,24,64,${0.12+pulse*0.08})`;
 ctx.beginPath();ctx.arc(240,142,78+pulse*8,0,Math.PI*2);ctx.fill();
 // Ground dark rune circle under throne
 ctx.strokeStyle=`rgba(168,78,245,${0.38+pulse*0.22})`;ctx.lineWidth=2;
 ctx.beginPath();ctx.ellipse(240,FLOOR-2,96+pulse*6,11,0,0,Math.PI*2);ctx.stroke();
 ctx.strokeStyle=`rgba(230,45,86,${0.32+pulse*0.18})`;ctx.lineWidth=1.5;
 ctx.beginPath();ctx.ellipse(240,FLOOR-2,68,7,0,0,Math.PI*2);ctx.stroke();
 // Gothic Vampire Dark Throne centered in the arena
 const throne=getDarkThroneImg();
 if(throne){
  ctx.imageSmoothingEnabled=false;
  const tw=152,th=126;
  ctx.drawImage(throne,240-tw/2,FLOOR-th+4,tw,th);
  // Subtle pulsing crimson glow on the two side crystal orbs
  ctx.globalCompositeOperation='lighter';
  ctx.fillStyle=`rgba(255,42,75,${0.22+pulse*0.18})`;
  ctx.beginPath();ctx.arc(240-50,FLOOR-68,10+pulse*3,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(240+50,FLOOR-68,10+pulse*3,0,Math.PI*2);ctx.fill();
  ctx.globalCompositeOperation='source-over';
 }
 // Writhing Shadow Tentacles around the entire arena (left, right, floor, and upper corners)
 drawShadowTentacle(14,FLOOR+6,105,13,-Math.PI*.42,0.2,'#06040a','#8f3ef0');
 drawShadowTentacle(48,FLOOR+6,82,10,-Math.PI*.48,1.5,'#090512','#c92852');
 drawShadowTentacle(86,FLOOR+6,66,8,-Math.PI*.52,2.7,'#06040a','#7a35d9');
 drawShadowTentacle(W-14,FLOOR+6,105,13,-Math.PI*.58,0.9,'#06040a','#8f3ef0');
 drawShadowTentacle(W-48,FLOOR+6,82,10,-Math.PI*.52,2.2,'#090512','#c92852');
 drawShadowTentacle(W-86,FLOOR+6,66,8,-Math.PI*.48,3.6,'#06040a','#7a35d9');
 // Upper hanging tentacles draping down from top corners
 drawShadowTentacle(24,topY-4,76,10,Math.PI*.36,1.1,'#05030a','#7a35d9');
 drawShadowTentacle(78,topY-4,56,7,Math.PI*.46,2.8,'#080410','#b8254e');
 drawShadowTentacle(W-24,topY-4,76,10,Math.PI*.64,1.9,'#05030a','#7a35d9');
 drawShadowTentacle(W-78,topY-4,56,7,Math.PI*.54,3.4,'#080410','#b8254e');
 // Floating eerie dark embers & shadow wisps
 for(let i=0;i<22;i++){
  const ex=(i*53+Math.sin(clock*1.4+i)*18+W)%W;
  const ey=FLOOR-((clock*(22+(i%4)*9)+i*37)%(FLOOR-topY-10));
  ctx.fillStyle=i%3===0?'#ff4772aa':i%2?'#c17dff99':'#6b28b888';
  ctx.fillRect(Math.round(ex),Math.round(ey),i%3===0?3:2,i%3===0?3:2);
 }
 text(domainUser.domainCast>0?'BÀNH TRƯỚNG LÃNH ĐỊA':'LÃNH ĐỊA · '+Math.ceil(domainUser.domain)+'s',240,86,9,'#f0d4ff','center');
 ctx.restore();
}
function drawDashTrailVfx(e,a){
 ctx.save();
 const d=e.dir||1,k=1-a,col=e.c||'#9c55f1';
 ctx.translate(e.x,e.y);
 // Aerodynamic glowing wind crescent + speed streaks (no boxy rectangles!)
 ctx.globalAlpha=a*.85;
 ctx.strokeStyle=col;ctx.lineWidth=3*a+1;ctx.lineCap='round';
 ctx.beginPath();ctx.arc(d*4,0,10+k*12,d>0?-Math.PI*.42:Math.PI*.58,d>0?Math.PI*.42:Math.PI*1.42);ctx.stroke();
 ctx.strokeStyle='#ffffff';ctx.globalAlpha=a*.65;ctx.lineWidth=1.5;
 ctx.beginPath();ctx.arc(d*6,0,8+k*10,d>0?-Math.PI*.35:Math.PI*.65,d>0?Math.PI*.35:Math.PI*1.35);ctx.stroke();
 // 4 tapered horizontal energy speedlines
 for(let i=0;i<4;i++){
  const ly=(i-1.5)*7,len=(14+i%2*10)*(0.4+a*0.8);
  ctx.globalAlpha=a*(0.75-i*0.1);
  ctx.strokeStyle=i%2?col:'#e9d8ff';ctx.lineWidth=2.2-i*0.3;
  ctx.beginPath();ctx.moveTo(-d*(4+k*12),ly);ctx.lineTo(-d*(4+k*12+len),ly);ctx.stroke();
 }
 // Sparkle motes
 ctx.globalAlpha=a*.9;
 for(let i=0;i<4;i++){
  const sx=-d*(6+k*18+i*5),sy=(i%2?1:-1)*(5+i*2.5);
  ctx.fillStyle=i%2?'#ffffff':col;
  ctx.fillRect(Math.round(sx),Math.round(sy),2,2);
 }
 ctx.restore();
}
function drawShadowAfterimageVfx(e,a){
 ctx.save();
 const d=e.dir||1,k=1-a;
 ctx.translate(e.x,e.y);
 // Swirling gothic dark-smoke ribbon & violet lightning streaks
 ctx.globalAlpha=a*.78;
 for(let i=0;i<5;i++){
  const yOff=-16+i*8,wLen=16+(i%2)*10+k*14;
  ctx.strokeStyle=i%2?'#11091f':'#8b42eb';ctx.lineWidth=4.5-i*0.5;ctx.lineCap='round';
  ctx.beginPath();
  ctx.moveTo(0,yOff);
  ctx.quadraticCurveTo(-d*wLen*0.5,yOff+Math.sin(clock*16+i)*5,-d*wLen,yOff-2);
  ctx.stroke();
 }
 ctx.globalAlpha=a*.9;ctx.strokeStyle='#e2c4ff';ctx.lineWidth=1.4;
 ctx.beginPath();ctx.moveTo(-d*2,-10);ctx.lineTo(-d*12,-3);ctx.lineTo(-d*8,2);ctx.lineTo(-d*22,8);ctx.stroke();
 ctx.restore();
}
function drawDarkPullVfx(e,a){
 ctx.save();
 const k=1-a,cx=e.x,cy=e.y,pulse=.5+.5*Math.sin(clock*22);
 // 1. Swirling Black Hole Sphere around caster (matching Blox Fruits X-move reference video!)
 const r=14+Math.sin(Math.min(1,k*2.2)*Math.PI)*18;
 ctx.globalAlpha=Math.min(1,a*1.35);
 const g=ctx.createRadialGradient(cx,cy,2,cx,cy,r+14);
 g.addColorStop(0,'rgba(4,2,10,0.95)');
 g.addColorStop(0.55,'rgba(32,12,58,0.75)');
 g.addColorStop(0.8,'rgba(147,70,240,0.45)');
 g.addColorStop(1,'rgba(147,70,240,0)');
 ctx.fillStyle=g;ctx.beginPath();ctx.arc(cx,cy,r+14,0,Math.PI*2);ctx.fill();
 ctx.fillStyle='#06040c';ctx.beginPath();ctx.arc(cx,cy,r*0.72,0,Math.PI*2);ctx.fill();
 ctx.strokeStyle='#c994ff';ctx.lineWidth=2;ctx.beginPath();ctx.arc(cx,cy,r*0.85,clock*5,clock*5+Math.PI*1.4);ctx.stroke();
 // 2. Long, whipping curved jet-black shadow tendrils shooting outward & pulling inward!
 const tendrils=e.targets&&e.targets.length?e.targets:null;
 for(let i=0;i<7;i++){
  const baseAng=(e.dir<0?Math.PI:0)+((i-3)*0.34)+Math.sin(clock*9+i)*0.18;
  const reach=55+Math.sin(k*Math.PI)*115+(i%2)*24;
  const tx=cx+Math.cos(baseAng)*reach;
  const ty=cy+Math.sin(baseAng)*(reach*0.45)-Math.abs(i-3)*6;
  const mx=(cx+tx)*0.5+Math.sin(clock*12+i*1.7)*22;
  const my=(cy+ty)*0.5-26-(i%3)*12;
  // Pitch-black razor whip with purple rim
  ctx.strokeStyle='#7a32d688';ctx.lineWidth=5.5*a+1.5;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(cx,cy);ctx.quadraticCurveTo(mx,my,tx,ty);ctx.stroke();
  ctx.strokeStyle='#05030a';ctx.lineWidth=3.5*a+1;
  ctx.beginPath();ctx.moveTo(cx,cy);ctx.quadraticCurveTo(mx,my,tx,ty);ctx.stroke();
 }
 // 3. Direct latched shadow ribbons wrapping onto pulled enemy(ies)
 if(tendrils){
  for(const tgt of tendrils){
   const tx=tgt.x,ty=tgt.y;
   for(let j=-1;j<=1;j++){
    const mx=(cx+tx)*0.5,my=(cy+ty)*0.5+j*24+Math.sin(clock*16+j)*10;
    ctx.strokeStyle='#a855f7aa';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(cx,cy);ctx.quadraticCurveTo(mx,my,tx,ty);ctx.stroke();
    ctx.strokeStyle='#040208';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(cx,cy);ctx.quadraticCurveTo(mx,my,tx,ty);ctx.stroke();
   }
   ctx.strokeStyle='#d8b4fe';ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(tx,ty,14+pulse*4,8,clock*4,0,Math.PI*2);ctx.stroke();
  }
 }
 ctx.restore();
}
// === DARK KING UPGRADED VFX END ===
'''
    assert 'function drawSilverBird(' in html
    html = html.replace('function drawSilverBird(', upgraded_helpers + 'function drawSilverBird(', 1)

    # 3. Upgrade silverState so Vua Bóng Tối animates 'dash' while rushing and 'attack' while multi-slashing during Skill I!
    old_silver_state = "function silverState(p,airborne,falling,defeated,actionOn){if(defeated)return'defeat';if(p.dash>0)return'dash';if(actionOn&&p.fighterAnim.type==='attack')return'attack';if(actionOn&&p.fighterAnim.type==='finisher')return'finisher';if(actionOn&&p.fighterAnim.type==='skill')return'skill';if(airborne)return falling?'fall':'jump';return Math.abs(p.vx||0)>.25?'move':'idle'}"
    new_silver_state = "function silverState(p,airborne,falling,defeated,actionOn){if(defeated)return'defeat';if(p.voidRushAttacking||p.rpgRushAttacking)return'attack';if(p.dash>0||p.voidRush>0||p.rpgRush>0)return'dash';if(actionOn&&p.fighterAnim.type==='attack')return'attack';if(actionOn&&p.fighterAnim.type==='finisher')return'finisher';if(actionOn&&p.fighterAnim.type==='skill')return'skill';if(airborne)return falling?'fall':'jump';return Math.abs(p.vx||0)>.25?'move':'idle'}"
    assert old_silver_state in html, "silverState not found"
    html = html.replace(old_silver_state, new_silver_state, 1)

    # 4. Upgrade Skill I (PvP voidRush & RPG rpgRush) so each hit triggers rapid attack slash animation + darkSlash VFX!
    old_pvp_rush_hit = "addEffect({type:'slash',x:foe.x-p.face*8,y:foe.y-26,life:.14,max:.14,c:'#9c55f1',dir:p.face});addEffect({type:'shadowAfterimage',x:p.x,y:p.y-24,life:.28,max:.28,dir:p.face,c:'#d7b9ff'})}p.voidRushHits++;p.voidRushTick=.095}"
    new_pvp_rush_hit = "triggerFighterAnimation(p,'attack',-1,.26);addEffect({type:'slash',x:foe.x-p.face*4,y:foe.y-26+(p.voidRushHits%2?-6:4),life:.16,max:.16,c:'#9c55f1',dir:p.face});addEffect({type:'shadowAfterimage',x:p.x-p.face*10,y:p.y-24,life:.26,max:.26,dir:p.face,c:'#d7b9ff'})}p.voidRushHits++;p.voidRushTick=.095}"
    assert old_pvp_rush_hit in html, "PvP voidRush hit block not found"
    html = html.replace(old_pvp_rush_hit, new_pvp_rush_hit, 1)

    # Reset voidRushAttacking when voidRush ends
    html = html.replace("p.voidRush=0;p.voidRushTarget=-1;", "p.voidRush=0;p.voidRushTarget=-1;p.voidRushAttacking=false;")
    html = html.replace("p.voidRush=Math.max(0,p.voidRush-dt);", "p.voidRush=Math.max(0,p.voidRush-dt);if(p.voidRush<=0)p.voidRushAttacking=false;")

    # RPG rpgRush: set rpgRushAttacking=true when hitting & trigger rapid attack animation on every slash!
    old_rpg_rush_hit = "else{p.x=e.x-p.face*24;p.rpgRushTick-=dt;if(p.rpgRushTick<=0&&p.rpgRushHits<6){rpgDamageEnemy(e,5.5*rpg.damage,p);e.stun=.12;p.rpgRushHits++;p.rpgRushTick=.095;addEffect({type:'slash',x:e.x-rpg.camera,y:e.y-24,life:.14,max:.14,c:'#9c55f1',dir:p.face});addEffect({type:'shadowAfterimage',x:p.x-rpg.camera,y:p.y-24,life:.28,max:.28,dir:p.face,c:'#d7b9ff'})}}}"
    new_rpg_rush_hit = "else{p.rpgRushAttacking=true;p.x=e.x-p.face*24;p.rpgRushTick-=dt;if(p.rpgRushTick<=0&&p.rpgRushHits<6){triggerFighterAnimation(p,'attack',-1,.26);rpgDamageEnemy(e,5.5*rpg.damage,p);e.stun=.12;p.rpgRushHits++;p.rpgRushTick=.095;addEffect({type:'slash',x:e.x-rpg.camera,y:e.y-24+(p.rpgRushHits%2?-6:4),life:.16,max:.16,c:'#9c55f1',dir:p.face});addEffect({type:'shadowAfterimage',x:p.x-rpg.camera-p.face*10,y:p.y-24,life:.26,max:.26,dir:p.face,c:'#d7b9ff'})}}}"
    assert old_rpg_rush_hit in html, "RPG rpgRush hit block not found"
    html = html.replace(old_rpg_rush_hit, new_rpg_rush_hit, 1)
    html = html.replace("p.rpgRush=0;p.rpgRushTarget=null", "p.rpgRush=0;p.rpgRushTarget=null;p.rpgRushAttacking=false")
    html = html.replace("if(p.rpgRush>0){p.rpgRush=Math.max(0,p.rpgRush-dt);", "if(p.rpgRush>0){p.rpgRush=Math.max(0,p.rpgRush-dt);if(p.rpgRush<=0)p.rpgRushAttacking=false;")

    # 5. Upgrade Skill U (n===1, HẮC QUANG) in PvP & RPG to shoot black shadow tendrils from Vua Bóng Tối pulling enemy toward him (like the video!)
    old_pvp_u = "else if(n===1){p.skillCd[1]=4;const cx=Math.max(35,Math.min(445,p.x+p.face*68));if(foe.invuln<=0&&Math.hypot(foe.x-cx,(foe.y-p.y)*.7)<205){hitBy(p,foe,p.domain>0?12:9,p.face,0);foe.darkPull=.9;foe.darkPullDuration=.9;foe.darkPullOwner=p.id;foe.darkPullStartX=foe.x;foe.darkPullBurstDone=false;foe.stun=Math.max(foe.stun,.18);foe.vx=foe.vy=0}addEffect({type:'darkVortex',x:cx,y:FLOOR-24,life:.95,max:.95,c:'#9d62ef'});addEffect({type:'voidbeamwarning',x1:p.x,y1:p.y-28,x2:cx,y2:FLOOR-24,life:.34,max:.34,c:'#a278ed'})}"
    new_pvp_u = "else if(n===1){p.skillCd[1]=4;triggerFighterAnimation(p,'skill',1,.95);const cx=Math.max(35,Math.min(445,p.x+p.face*68)),hitTargets=[];if(foe.invuln<=0&&Math.hypot(foe.x-cx,(foe.y-p.y)*.7)<215){hitBy(p,foe,p.domain>0?12:9,p.face,0);foe.darkPull=.9;foe.darkPullDuration=.9;foe.darkPullOwner=p.id;foe.darkPullStartX=foe.x;foe.darkPullBurstDone=false;foe.stun=Math.max(foe.stun,.28);foe.vx=foe.vy=0;hitTargets.push(foe)}addEffect({type:'darkPullRays',x:p.x,y:p.y-28,dir:p.face,life:.95,max:.95,c:'#9d62ef',ownerId:p.id,targets:hitTargets});addEffect({type:'darkVortex',x:p.x+p.face*22,y:FLOOR-18,life:.95,max:.95,c:'#9d62ef'})}"
    assert old_pvp_u in html, "PvP Skill U block not found"
    html = html.replace(old_pvp_u, new_pvp_u, 1)

    old_rpg_u = "addEffect({type:'darkVortex',x:screenCx,y:cy,life:.95,max:.95,c:'#9d62ef',followOwner:p.id});"
    new_rpg_u = "triggerFighterAnimation(p,'skill',1,.95);addEffect({type:'darkPullRays',x:screenCx,y:p.y-28,dir:p.face,life:.95,max:.95,c:'#9d62ef',followOwner:p.id,isRpg:true});addEffect({type:'darkVortex',x:screenCx,y:cy,life:.95,max:.95,c:'#9d62ef',followOwner:p.id});"
    assert old_rpg_u in html, "RPG Skill U block not found"
    html = html.replace(old_rpg_u, new_rpg_u, 1)

    # Render darkPullRays inside drawCombatVfx (so it works in BOTH PvP and RPG automatically!)
    old_vfx_entry = "function drawCombatVfx(e,a){const t=1-a;"
    new_vfx_entry = "function drawCombatVfx(e,a){const t=1-a;if(e.type==='darkPullRays'){let txList=[];if(e.isRpg&&rpg){const own=rpg.players[e.followOwner];if(own){e.x=own.x-rpg.camera;e.y=own.y-28}txList=(rpg.enemies||[]).filter(en=>en.life&&en.rpgPull>0).map(en=>({x:en.x-rpg.camera,y:en.y-28}))}else if(game&&e.ownerId!=null){const own=game.players[e.ownerId],foe=game.players[1-e.ownerId];if(own){e.x=own.x;e.y=own.y-28}if(foe&&foe.darkPull>0)txList=[{x:foe.x,y:foe.y-28}]}drawDarkPullVfx({...e,targets:txList},a);return}"
    assert old_vfx_entry in html, "drawCombatVfx entry not found"
    html = html.replace(old_vfx_entry, new_vfx_entry, 1)

    # 6. Replace ALL ugly rectangular dash/clone/afterimage effects across ALL 4 characters!
    # 6a. In drawFighter (p.dash > 0): replace the 2 ugly colored rectangles with aerodynamic speed trails
    old_fighter_dash = "if(!preview&&p.dash>0){ctx.save();ctx.globalAlpha=.22;rect(x-dir*12,base-37,18,34,c.accent);ctx.globalAlpha=.13;rect(x-dir*23,base-34,16,30,c.accent);ctx.globalAlpha=.8;ctx.strokeStyle=c.accent;ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(x,base-2,16+Math.sin(clock*25)*3,4,0,0,Math.PI*2);ctx.stroke();ctx.restore();rect(x-dir*14,base-22,5,5,c.accent+'99');rect(x-dir*20,base-18,3,3,'#ffffff77')}"
    new_fighter_dash = "if(!preview&&p.dash>0){ctx.save();ctx.globalAlpha=.85;ctx.strokeStyle=c.accent;ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(x,base-2,16+Math.sin(clock*25)*3,4,0,0,Math.PI*2);ctx.stroke();for(let k=0;k<4;k++){const yy=base-10-k*9,len=16+(k%2)*10;ctx.globalAlpha=.7-k*.12;ctx.strokeStyle=k%2?'#ffffff':c.accent;ctx.lineWidth=2.4-k*.35;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(x-dir*8,yy);ctx.lineTo(x-dir*(8+len),yy);ctx.stroke()}ctx.restore()}"
    assert old_fighter_dash in html, "drawFighter dash block not found"
    html = html.replace(old_fighter_dash, new_fighter_dash, 1)

    # 6b. Replace clone/dash boxy rectangles in BOTH PvP and RPG effect loops!
    old_clone_dash = "if(e.type==='clone'||e.type==='dash'){rect(e.x-8,e.y-14,16,22,e.c+'77');rect(e.x-4,e.y-21,8,8,'#e6e7efaa')}"
    new_clone_dash = "if(e.type==='clone'||e.type==='dash'){drawDashTrailVfx(e,a)}"
    assert html.count(old_clone_dash) == 2, f"Expected 2 clone/dash blocks, found {html.count(old_clone_dash)}"
    html = html.replace(old_clone_dash, new_clone_dash)

    # Also pass dir:p.face on void basic attack dash trail so the crescent trail faces the right direction!
    html = html.replace("addEffect({type:'dash',x:p.x-p.face*8,y:p.y-18,life:.12,max:.12,c:'#8b64db'})",
                        "addEffect({type:'dash',x:p.x-p.face*8,y:p.y-20,life:.16,max:.16,dir:p.face,c:'#9346f0'})")
    html = html.replace("addEffect({type:'dash',x:p.x-rpg.camera-p.face*8,y:p.y-18,life:.12,max:.12,c:'#8b64db'})",
                        "addEffect({type:'dash',x:p.x-rpg.camera-p.face*8,y:p.y-20,life:.16,max:.16,dir:p.face,c:'#9346f0'})")
    html = html.replace("addEffect({type:'dash',x:p.x,y:p.y-18,life:.25,max:.25,c:c.accent})",
                        "addEffect({type:'dash',x:p.x,y:p.y-20,life:.25,max:.25,dir:p.face,c:c.accent})")
    html = html.replace("addEffect({type:'dash',x:p.x-p.face*10,y:p.y-20,life:.28,max:.28,c:'#9c55f1'})",
                        "addEffect({type:'dash',x:p.x-p.face*10,y:p.y-20,life:.28,max:.28,dir:p.face,c:'#9c55f1'})")
    html = html.replace("addEffect({type:'dash',x:p.x-rpg.camera-p.face*10,y:p.y-20,life:.28,max:.28,c:'#9c55f1'})",
                        "addEffect({type:'dash',x:p.x-rpg.camera-p.face*10,y:p.y-20,life:.28,max:.28,dir:p.face,c:'#9c55f1'})")

    # 6c. Replace blocky shadowAfterimage in BOTH PvP and RPG effect loops!
    old_afterimg = "else if(e.type==='shadowAfterimage'){ctx.save();ctx.globalAlpha=a*.48;const d=e.dir||1;ctx.translate(e.x,e.y);ctx.scale(d,1);rect(-12,-31,24,22,'#7d4acb88');rect(-8,-42,16,12,'#d4b9ff88');rect(-15,-10,12,9,'#4c326e88');rect(3,-10,12,9,'#4c326e88');rect(-17,-35,5,13,'#a879ed88');rect(12,-35,5,13,'#a879ed88');ctx.restore()}"
    new_afterimg = "else if(e.type==='shadowAfterimage'){drawShadowAfterimageVfx(e,a)}"
    assert html.count(old_afterimg) == 2, f"Expected 2 shadowAfterimage blocks, found {html.count(old_afterimg)}"
    html = html.replace(old_afterimg, new_afterimg)

    # 7. Replace Skill O (Domain Expansion) arena backdrop in BOTH PvP (drawDomainArena) and RPG (domainUser)!
    old_pvp_domain = "function drawDomainArena(){if(!game||!game.players.some(p=>p.domain>0||p.domainCast>0))return;ctx.fillStyle='rgba(3,2,10,.82)';ctx.fillRect(0,0,W,H);const pulse=Math.floor(clock*8)%2;rect(212,160,56,76,'#171323');rect(201,151,78,12,'#241a33');rect(218,137,44,22,'#30213f');rect(225,123,30,17,'#21182d');rect(229,117,6,8,'#eee5ff');rect(239,112,5,13,'#d9c9ff');rect(248,117,6,8,'#eee5ff');rect(227,142,8,4,'#f34d70');rect(245,142,8,4,'#f34d70');rect(217,176,46,5,'#70429a');rect(220,184,40,3,pulse?'#9d63dc':'#542b83');for(const p of game.players)if(p.domainCast>0||p.domain>0){text(p.domainCast>0?'BÀNH TRƯỚNG LÃNH ĐỊA':'LÃNH ĐỊA · '+Math.ceil(p.domain)+'s',240,91,9,'#d5baff','center');break}}"
    new_pvp_domain = "function drawDomainArena(){if(!game)return;const du=game.players.find(p=>p.domain>0||p.domainCast>0);if(!du)return;drawDarkDomainBackdrop(du,false)}"
    assert old_pvp_domain in html, "PvP drawDomainArena not found"
    html = html.replace(old_pvp_domain, new_pvp_domain, 1)

    old_rpg_domain = "const domainUser=rpg.players.slice(0,rpg.partySize).find(p=>p.domain>0||p.domainCast>0);if(domainUser){ctx.fillStyle='rgba(5,3,14,.72)';ctx.fillRect(0,42,W,H-42);const pulse=Math.floor(clock*8)%2;rect(205,169,70,66,'#171323');rect(194,159,92,12,'#241a33');rect(213,144,54,22,'#30213f');rect(222,130,36,17,'#21182d');rect(227,124,7,9,'#eee5ff');rect(238,119,6,14,'#d9c9ff');rect(249,124,7,9,'#eee5ff');rect(222,149,10,4,'#f34d70');rect(246,149,10,4,'#f34d70');rect(215,184,50,5,'#70429a');rect(219,193,42,3,pulse?'#9d63dc':'#542b83');text(domainUser.domainCast>0?'BÀNH TRƯỚNG LÃNH ĐỊA':'LÃNH ĐỊA · '+Math.ceil(domainUser.domain)+'s',240,91,8,'#d5baff','center')}"
    new_rpg_domain = "const domainUser=rpg.players.slice(0,rpg.partySize).find(p=>p.domain>0||p.domainCast>0);if(domainUser){drawDarkDomainBackdrop(domainUser,true)}"
    assert old_rpg_domain in html, "RPG domainUser block not found"
    html = html.replace(old_rpg_domain, new_rpg_domain, 1)

    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully patched game-cua-lam/game-cua-lam-upload/index.html with all 4 upgrades!")

if __name__ == '__main__':
    main()
