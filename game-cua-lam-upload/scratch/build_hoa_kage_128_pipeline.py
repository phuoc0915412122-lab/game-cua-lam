import os, sys, math
sys.path.append(os.path.abspath('game-cua-lam/game-cua-lam-upload/scratch'))
from pixel_canvas import PixelCanvas
from design_hoa_kage_128 import (
    draw_hoa_kage_pose_128,
    draw_sacred_flame_cluster,
    C_FIRE_OUTER, C_FIRE_RED, C_FIRE_ORANGE, C_FIRE_GOLD, C_FIRE_CORE
)

# 1. IDLE (6 frames: idle_01 .. idle_06)
def make_idle(idx, total=6):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / float(total)
    ang = phase * 2.0 * math.pi
    bob = int(round(math.sin(ang) * 1.6))
    tx, ty = 58, 46 + bob
    pose = {
        'tx': tx, 'ty': ty, 'lean_dx': 1,
        'hx': tx + 2, 'hy': ty - 17, 'expr': 'grin', 'phase': phase,
        'back_leg':  {'hip': (tx - 5, ty + 29), 'knee': (tx - 9, 100 + bob // 2), 'ankle': (tx - 12, 129)},
        'front_leg': {'hip': (tx + 5, ty + 29), 'knee': (tx + 11, 100 + bob // 2), 'ankle': (tx + 14, 130)},
        'back_arm':  {'sh': (tx - 10, ty + 4), 'el': (tx - 19, ty + 16), 'wr': (tx - 24, ty + 24 + bob // 2), 'layer': 'back', 'flame': 0.95},
        'front_arm': {'sh': (tx + 13, ty + 4), 'el': (tx + 21, ty + 15), 'wr': (tx + 28, ty + 19 - bob // 2), 'flame': 1.05}
    }
    draw_hoa_kage_pose_128(c, pose)
    return c

# 2. MOVE / RUN (8 frames: move_01 .. move_08)
def make_move(idx, total=8):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / float(total)
    ang = phase * 2.0 * math.pi
    bob = int(round(-abs(math.cos(ang)) * 3.5 + 1.5))
    tx, ty, lean = 58, 47 + bob, 4
    sf, lf = math.sin(ang), max(0.0, math.cos(ang))
    sb, lb = math.sin(ang + math.pi), max(0.0, math.cos(ang + math.pi))
    arm = -sf
    pose = {
        'tx': tx, 'ty': ty, 'lean_dx': lean,
        'hx': tx + lean + 2, 'hy': ty - 17, 'expr': 'grin', 'phase': phase,
        'back_leg':  {'hip': (tx - 4, ty + 28), 'knee': (tx - 2 + sb * 13 + lb * 5, ty + 51 - lb * 7), 'ankle': (tx - 4 + sb * 19 - lb * 4, 128 - lb * 11)},
        'front_leg': {'hip': (tx + 4, ty + 28), 'knee': (tx + 6 + sf * 13 + lf * 5, ty + 51 - lf * 7), 'ankle': (tx + 4 + sf * 19 - lf * 4, 129 - lf * 11)},
        'back_arm':  {'sh': (tx + lean - 10, ty + 4), 'el': (tx - 10 - arm * 8, ty + 15), 'wr': (tx - 8 - arm * 16, ty + 22 - arm * 5), 'layer': 'front' if arm < -0.2 else 'back', 'flame': 0.95},
        'front_arm': {'sh': (tx + lean + 12, ty + 4), 'el': (tx + 14 + arm * 8, ty + 15), 'wr': (tx + 18 + arm * 15, ty + 21 - arm * 4), 'flame': 1.05}
    }
    draw_hoa_kage_pose_128(c, pose)
    return c

# 3. JUMP (3 frames: jump_01 .. jump_03 — with flame sparks shooting out!)
def make_jump(idx):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / 3.0
    if idx == 1:
        tx, ty, lean = 58, 56, 3
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + 4, 'hy': ty - 17, 'expr': 'grin', 'phase': phase,
            'jump_sparks': True,
            'back_leg':  {'hip': (tx - 5, ty + 25), 'knee': (tx - 14, 106), 'ankle': (tx - 10, 129)},
            'front_leg': {'hip': (tx + 5, ty + 25), 'knee': (tx + 18, 106), 'ankle': (tx + 12, 130)},
            'back_arm':  {'sh': (tx - 10, ty + 4), 'el': (tx - 20, ty + 14), 'wr': (tx - 28, ty + 22), 'layer': 'back', 'flame': 1.0},
            'front_arm': {'sh': (tx + 13, ty + 4), 'el': (tx + 22, ty + 14), 'wr': (tx + 30, ty + 22), 'flame': 1.05}
        }
    elif idx == 2:
        tx, ty, lean = 58, 35, 2
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + 3, 'hy': ty - 17, 'expr': 'fierce', 'phase': phase,
            'jump_sparks': True,
            'back_leg':  {'hip': (tx - 5, ty + 28), 'knee': (tx - 10, ty + 54), 'ankle': (tx - 14, ty + 80)},
            'front_leg': {'hip': (tx + 5, ty + 28), 'knee': (tx + 18, ty + 44), 'ankle': (tx + 10, ty + 66)},
            'back_arm':  {'sh': (tx - 10, ty + 4), 'el': (tx - 22, ty + 6), 'wr': (tx - 30, ty - 4), 'layer': 'back', 'flame': 1.15},
            'front_arm': {'sh': (tx + 13, ty + 4), 'el': (tx + 22, ty - 4), 'wr': (tx + 28, ty - 14), 'flame': 1.2}
        }
    else:
        tx, ty, lean = 58, 33, 2
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + 3, 'hy': ty - 17, 'expr': 'grin', 'phase': phase,
            'jump_sparks': True,
            'back_leg':  {'hip': (tx - 5, ty + 28), 'knee': (tx - 14, ty + 46), 'ankle': (tx - 20, ty + 64)},
            'front_leg': {'hip': (tx + 5, ty + 28), 'knee': (tx + 12, ty + 52), 'ankle': (tx + 14, ty + 78)},
            'back_arm':  {'sh': (tx - 10, ty + 4), 'el': (tx - 20, ty + 10), 'wr': (tx - 26, ty + 18), 'layer': 'back', 'flame': 1.05},
            'front_arm': {'sh': (tx + 13, ty + 4), 'el': (tx + 24, ty + 4), 'wr': (tx + 34, ty + 2), 'flame': 1.1}
        }
    draw_hoa_kage_pose_128(c, pose)
    return c

# 4. FALL & LAND (3 frames: fall_01 .. fall_03)
def make_fall(idx):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / 3.0
    if idx in (1, 2):
        bob = 0 if idx == 1 else 3
        tx, ty, lean = 58, 38 + bob, 2
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + 3, 'hy': ty - 17, 'expr': 'grin', 'phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 28), 'knee': (tx - 12, ty + 50), 'ankle': (tx - 16, ty + 74)},
            'front_leg': {'hip': (tx + 5, ty + 28), 'knee': (tx + 12, ty + 52), 'ankle': (tx + 14, ty + 80)},
            'back_arm':  {'sh': (tx - 10, ty + 4), 'el': (tx - 22, ty + 4), 'wr': (tx - 30, ty - 2), 'layer': 'back', 'flame': 1.0},
            'front_arm': {'sh': (tx + 13, ty + 4), 'el': (tx + 24, ty + 6), 'wr': (tx + 32, ty + 0), 'flame': 1.05}
        }
    else:
        tx, ty, lean = 58, 52, 3
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + 4, 'hy': ty - 17, 'expr': 'grin', 'phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 25), 'knee': (tx - 12, 105), 'ankle': (tx - 14, 129)},
            'front_leg': {'hip': (tx + 5, ty + 25), 'knee': (tx + 16, 105), 'ankle': (tx + 16, 130)},
            'back_arm':  {'sh': (tx - 10, ty + 4), 'el': (tx - 20, ty + 16), 'wr': (tx - 26, ty + 24), 'layer': 'back', 'flame': 0.95},
            'front_arm': {'sh': (tx + 13, ty + 4), 'el': (tx + 22, ty + 16), 'wr': (tx + 28, ty + 24), 'flame': 1.0}
        }
    draw_hoa_kage_pose_128(c, pose)
    return c

# 5. DASH (4 frames: dash_01 .. dash_04 — blazing ground fire trail behind feet!)
def make_dash(idx):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / 4.0
    tx = 66 + (idx % 2) * 3
    ty, lean = 52, 8
    pose = {
        'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + lean + 3, 'hy': ty - 16, 'expr': 'fierce', 'phase': phase,
        'dash_trail': True,
        'back_leg':  {'hip': (tx - 6, ty + 24), 'knee': (tx - 22, ty + 38), 'ankle': (tx - 38, 126)},
        'front_leg': {'hip': (tx + 6, ty + 24), 'knee': (tx + 22, ty + 36), 'ankle': (tx + 14, 128)},
        'back_arm':  {'sh': (tx - 5, ty + 4), 'el': (tx - 20, ty + 10), 'wr': (tx - 34, ty + 14), 'layer': 'back', 'flame': 1.2},
        'front_arm': {'sh': (tx + 17, ty + 4), 'el': (tx + 28, ty + 10), 'wr': (tx + 38, ty + 12), 'flame': 1.3}
    }
    draw_hoa_kage_pose_128(c, pose)
    return c

# 6. BASIC ATTACKS (6 frames: attack_01 .. attack_06 — Hỏa Quyền Fire Fist Combo!)
def make_attack(idx):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / 6.0
    if idx == 1:
        tx, ty, lean = 54, 48, -2
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + 1, 'hy': ty - 17, 'expr': 'grin', 'phase': phase,
            'back_leg':  {'hip': (tx - 6, ty + 28), 'knee': (tx - 14, 102), 'ankle': (tx - 18, 129)},
            'front_leg': {'hip': (tx + 6, ty + 28), 'knee': (tx + 14, 102), 'ankle': (tx + 18, 130)},
            'back_arm':  {'sh': (tx - 11, ty + 4), 'el': (tx - 22, ty + 14), 'wr': (tx - 18, ty + 22), 'layer': 'back', 'flame': 1.1},
            'front_arm': {'sh': (tx + 10, ty + 4), 'el': (tx + 2, ty + 14), 'wr': (tx - 4, ty + 16), 'flame': 1.2}
        }
        draw_hoa_kage_pose_128(c, pose)
    elif idx == 2:
        # Blazing Right Straight Fire Fist!
        tx, ty, lean = 64, 48, 6
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + 8, 'hy': ty - 17, 'expr': 'fierce', 'phase': phase,
            'back_leg':  {'hip': (tx - 6, ty + 28), 'knee': (tx - 18, 103), 'ankle': (tx - 26, 129)},
            'front_leg': {'hip': (tx + 6, ty + 28), 'knee': (tx + 18, 101), 'ankle': (tx + 22, 130)},
            'back_arm':  {'sh': (tx - 7, ty + 4), 'el': (tx - 18, ty + 12), 'wr': (tx - 26, ty + 16), 'layer': 'back', 'flame': 1.0},
            'front_arm': {'sh': (tx + 16, ty + 4), 'el': (tx + 30, ty + 6), 'wr': (tx + 46, ty + 6), 'flame': 1.5}
        }
        draw_hoa_kage_pose_128(c, pose)
        draw_sacred_flame_cluster(c, tx + 52, ty + 6, phase=phase, scale=1.5, dir_x=1.0, dir_y=0.0)
    elif idx == 3:
        # Left Cross Fire Hook!
        tx, ty, lean = 62, 47, 5
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + 7, 'hy': ty - 17, 'expr': 'fierce', 'phase': phase,
            'back_leg':  {'hip': (tx - 6, ty + 28), 'knee': (tx - 16, 102), 'ankle': (tx - 22, 129)},
            'front_leg': {'hip': (tx + 6, ty + 28), 'knee': (tx + 16, 102), 'ankle': (tx + 20, 130)},
            'back_arm':  {'sh': (tx - 6, ty + 4), 'el': (tx + 14, ty + 6), 'wr': (tx + 38, ty + 3), 'layer': 'front', 'flame': 1.45},
            'front_arm': {'sh': (tx + 14, ty + 5), 'el': (tx + 6, ty + 16), 'wr': (tx - 4, ty + 22), 'flame': 1.0}
        }
        draw_hoa_kage_pose_128(c, pose)
    elif idx == 4:
        # Rising Fire Uppercut!
        tx, ty, lean = 64, 45, 4
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + 6, 'hy': ty - 17, 'expr': 'fierce', 'phase': phase,
            'back_leg':  {'hip': (tx - 6, ty + 28), 'knee': (tx - 14, 101), 'ankle': (tx - 20, 129)},
            'front_leg': {'hip': (tx + 6, ty + 28), 'knee': (tx + 16, 101), 'ankle': (tx + 20, 130)},
            'back_arm':  {'sh': (tx - 8, ty + 4), 'el': (tx - 18, ty + 14), 'wr': (tx - 24, ty + 22), 'layer': 'back', 'flame': 1.0},
            'front_arm': {'sh': (tx + 15, ty + 3), 'el': (tx + 24, ty - 6), 'wr': (tx + 32, ty - 22), 'flame': 1.55}
        }
        draw_hoa_kage_pose_128(c, pose)
        draw_sacred_flame_cluster(c, tx + 34, ty - 26, phase=phase, scale=1.4, dir_x=0.3, dir_y=-1.0)
    elif idx == 5:
        # Double-Fist Hiken Flame Burst!
        tx, ty, lean = 66, 49, 7
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + 9, 'hy': ty - 16, 'expr': 'fierce', 'phase': phase,
            'back_leg':  {'hip': (tx - 6, ty + 26), 'knee': (tx - 20, 104), 'ankle': (tx - 30, 129)},
            'front_leg': {'hip': (tx + 6, ty + 26), 'knee': (tx + 20, 101), 'ankle': (tx + 24, 130)},
            'back_arm':  {'sh': (tx - 5, ty + 5), 'el': (tx + 16, ty + 10), 'wr': (tx + 38, ty + 10), 'layer': 'front', 'flame': 1.4},
            'front_arm': {'sh': (tx + 17, ty + 4), 'el': (tx + 32, ty + 5), 'wr': (tx + 48, ty + 5), 'flame': 1.6}
        }
        draw_hoa_kage_pose_128(c, pose)
        draw_sacred_flame_cluster(c, tx + 54, ty + 6, phase=phase, scale=1.6, dir_x=1.0, dir_y=0.0)
    else:
        tx, ty, lean = 60, 47, 2
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + 3, 'hy': ty - 17, 'expr': 'grin', 'phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 28), 'knee': (tx - 10, 101), 'ankle': (tx - 14, 129)},
            'front_leg': {'hip': (tx + 5, ty + 28), 'knee': (tx + 12, 101), 'ankle': (tx + 15, 130)},
            'back_arm':  {'sh': (tx - 10, ty + 4), 'el': (tx - 18, ty + 15), 'wr': (tx - 22, ty + 24), 'layer': 'back', 'flame': 1.0},
            'front_arm': {'sh': (tx + 13, ty + 4), 'el': (tx + 22, ty + 14), 'wr': (tx + 28, ty + 19), 'flame': 1.1}
        }
        draw_hoa_kage_pose_128(c, pose)
    return c

# 7. SKILL CASTING (4 frames: skill_01 .. skill_04 — Hỏa Quyền / Cột Lửa)
def make_skill(idx):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / 4.0
    tx, ty, lean = 58, 47, 4
    pose = {
        'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + 6, 'hy': ty - 17, 'expr': 'fierce', 'phase': phase,
        'back_leg':  {'hip': (tx - 6, ty + 28), 'knee': (tx - 16, 102), 'ankle': (tx - 22, 129)},
        'front_leg': {'hip': (tx + 6, ty + 28), 'knee': (tx + 18, 101), 'ankle': (tx + 22, 130)},
        'back_arm':  {'sh': (tx - 8, ty + 4), 'el': (tx - 20, ty + 12), 'wr': (tx - 28, ty + 16), 'layer': 'back', 'flame': 1.25},
        'front_arm': {'sh': (tx + 15, ty + 4), 'el': (tx + 30, ty + 5), 'wr': (tx + 46, ty + 4), 'flame': 1.5 + idx * 0.12}
    }
    draw_hoa_kage_pose_128(c, pose)
    draw_sacred_flame_cluster(c, tx + 52, ty + 4, phase=phase, scale=1.3 + idx * 0.18, dir_x=1.0, dir_y=-0.1)
    return c

# 8. FINISHER / ULTIMATE (4 frames: finisher_01 .. finisher_04 — Đại Viêm Giới / Phượng Vũ)
def make_finisher(idx):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / 4.0
    tx, ty, lean = 58, 45, 2
    # Blazing sun-fire rings behind Hỏa Kage
    if idx >= 2:
        r = 26 + idx * 8
        c.circle(tx + 2, ty + 10, r, (255, 120, 23, 125), fill=False)
        c.circle(tx + 2, ty + 10, r - 6, (255, 212, 56, 155), fill=False)
    pose = {
        'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + 3, 'hy': ty - 17, 'expr': 'fierce', 'phase': phase,
        'back_leg':  {'hip': (tx - 6, ty + 28), 'knee': (tx - 14, 101), 'ankle': (tx - 18, 129)},
        'front_leg': {'hip': (tx + 6, ty + 28), 'knee': (tx + 14, 101), 'ankle': (tx + 18, 130)},
        'back_arm':  {'sh': (tx - 9, ty + 3), 'el': (tx - 22, ty - 8), 'wr': (tx - 26, ty - 22), 'layer': 'back', 'flame': 1.55},
        'front_arm': {'sh': (tx + 14, ty + 3), 'el': (tx + 26, ty - 8), 'wr': (tx + 30, ty - 22), 'flame': 1.65}
    }
    draw_hoa_kage_pose_128(c, pose)
    # Giant solar fireball overhead
    orb_r = 6 + idx * 3.2
    c.circle(tx + 2, 16, orb_r + 3, (232, 52, 21, 140), fill=True)
    c.circle(tx + 2, 16, orb_r, C_FIRE_ORANGE, fill=True)
    c.circle(tx + 2, 16, orb_r * 0.65, C_FIRE_GOLD, fill=True)
    c.circle(tx + 2, 16, orb_r * 0.35, C_FIRE_CORE, fill=True)
    return c

# 9. HIT / TAKE DAMAGE (2 frames: hit_01 .. hit_02 — Chịu sát thương!)
def make_hit(idx):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / 2.0
    tx, ty, lean = 54 - idx * 2, 49, -5 - idx
    pose = {
        'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + lean, 'hy': ty - 16, 'expr': 'hit', 'phase': phase,
        'back_leg':  {'hip': (tx - 5, ty + 27), 'knee': (tx - 16, 104), 'ankle': (tx - 22, 129)},
        'front_leg': {'hip': (tx + 5, ty + 27), 'knee': (tx + 10, 103), 'ankle': (tx + 14, 130)},
        'back_arm':  {'sh': (tx - 12, ty + 4), 'el': (tx - 24, ty + 12), 'wr': (tx - 30, ty + 20), 'layer': 'back', 'flame': 0.65},
        'front_arm': {'sh': (tx + 10, ty + 4), 'el': (tx + 18, ty + 14), 'wr': (tx + 14, ty + 24), 'flame': 0.65}
    }
    draw_hoa_kage_pose_128(c, pose)
    return c

# 10. DEFEAT / KNOCKDOWN (4 frames: defeat_01 .. defeat_04 — Bị hạ gục!)
def make_defeat(idx):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / 4.0
    if idx == 1:
        tx, ty, lean = 54, 52, -4
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + lean, 'hy': ty - 16, 'expr': 'hit', 'phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 26), 'knee': (tx - 16, 106), 'ankle': (tx - 22, 129)},
            'front_leg': {'hip': (tx + 5, ty + 26), 'knee': (tx + 12, 106), 'ankle': (tx + 14, 130)},
            'back_arm':  {'sh': (tx - 12, ty + 4), 'el': (tx - 22, ty + 16), 'wr': (tx - 28, ty + 26), 'layer': 'back', 'flame': 0.55},
            'front_arm': {'sh': (tx + 10, ty + 4), 'el': (tx + 18, ty + 16), 'wr': (tx + 24, ty + 26), 'flame': 0.55}
        }
    elif idx == 2:
        tx, ty, lean = 56, 62, 2
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + 3, 'hy': ty - 16, 'expr': 'hit', 'phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 24), 'knee': (tx - 12, 118), 'ankle': (tx - 24, 129)},
            'front_leg': {'hip': (tx + 5, ty + 24), 'knee': (tx + 16, 110), 'ankle': (tx + 14, 130)},
            'back_arm':  {'sh': (tx - 10, ty + 4), 'el': (tx - 16, ty + 18), 'wr': (tx - 18, 126), 'layer': 'back', 'flame': 0.4},
            'front_arm': {'sh': (tx + 12, ty + 4), 'el': (tx + 20, ty + 18), 'wr': (tx + 24, 126), 'flame': 0.4}
        }
    elif idx == 3:
        tx, ty, lean = 58, 72, 4
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + 6, 'hy': ty - 15, 'expr': 'hit', 'phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 22), 'knee': (tx - 8, 128), 'ankle': (tx - 26, 130)},
            'front_leg': {'hip': (tx + 5, ty + 22), 'knee': (tx + 18, 114), 'ankle': (tx + 16, 130)},
            'back_arm':  {'sh': (tx - 8, ty + 4), 'el': (tx - 12, ty + 20), 'wr': (tx - 14, 130), 'layer': 'back', 'flame': 0.25},
            'front_arm': {'sh': (tx + 13, ty + 4), 'el': (tx + 22, ty + 18), 'wr': (tx + 26, 130), 'flame': 0.25}
        }
    else:
        tx, ty, lean = 58, 78, 6
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean, 'hx': tx + 8, 'hy': ty - 14, 'expr': 'hit', 'phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 20), 'knee': (tx - 10, 129), 'ankle': (tx - 28, 130)},
            'front_leg': {'hip': (tx + 5, ty + 20), 'knee': (tx + 16, 122), 'ankle': (tx + 22, 130)},
            'back_arm':  {'sh': (tx - 7, ty + 4), 'el': (tx - 10, ty + 20), 'wr': (tx - 12, 131), 'layer': 'back', 'flame': 0.0},
            'front_arm': {'sh': (tx + 14, ty + 4), 'el': (tx + 24, ty + 18), 'wr': (tx + 30, 131), 'flame': 0.0}
        }
    draw_hoa_kage_pose_128(c, pose)
    return c


def build_all():
    out_dir = os.path.abspath('game-cua-lam/game-cua-lam-upload/game-assets/characters/2')
    os.makedirs(out_dir, exist_ok=True)
    test_f = os.path.join(out_dir, 'test_idle.png')
    if os.path.exists(test_f):
        os.remove(test_f)

    frames = []
    for i in range(1, 7): frames.append((f'idle_0{i}.png', make_idle(i, 6)))
    for i in range(1, 9): frames.append((f'move_0{i}.png', make_move(i, 8)))
    for i in range(1, 4): frames.append((f'jump_0{i}.png', make_jump(i)))
    for i in range(1, 4): frames.append((f'fall_0{i}.png', make_fall(i)))
    for i in range(1, 7): frames.append((f'attack_0{i}.png', make_attack(i)))
    for i in range(1, 5): frames.append((f'dash_0{i}.png', make_dash(i)))
    for i in range(1, 5): frames.append((f'skill_0{i}.png', make_skill(i)))
    for i in range(1, 5): frames.append((f'finisher_0{i}.png', make_finisher(i)))
    for i in range(1, 3): frames.append((f'hit_0{i}.png', make_hit(i)))
    for i in range(1, 5): frames.append((f'defeat_0{i}.png', make_defeat(i)))

    for fname, cv in frames:
        with open(os.path.join(out_dir, fname), 'wb') as f:
            f.write(cv.to_png_bytes(1))

    # Master Spritesheet (6 columns x 8 rows)
    cols = 6
    rows = math.ceil(len(frames) / float(cols))
    sheet = PixelCanvas(cols * 128, rows * 144)
    for idx, (fname, cv) in enumerate(frames):
        ox, oy = (idx % cols) * 128, (idx // cols) * 144
        for y in range(144):
            for x in range(128):
                px = cv.pixels[y][x]
                if px[3] > 0:
                    sheet.pixels[oy + y][ox + x] = px
    with open(os.path.join(out_dir, 'hoa_kage_spritesheet.png'), 'wb') as f:
        f.write(sheet.to_png_bytes(1))
    print(f"Generated {len(frames)} native 128x144 Hỏa Kage frames + master spritesheet!")

if __name__ == '__main__':
    build_all()
