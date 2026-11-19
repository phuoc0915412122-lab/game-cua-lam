import os, sys, math
sys.path.append(os.path.abspath('scratch'))
from pixel_canvas import PixelCanvas
from design_dark_king_128 import (
    draw_dark_king_pose_128,
    draw_dark_aura_128,
    draw_flowing_royal_cape_128,
    draw_boot_leg_128,
    draw_royal_torso_128,
    draw_flared_collar_back_128,
    draw_head_and_golden_crown_128,
    draw_arm_and_gauntlet_128,
    draw_obsidian_sword_128,
    C_OUTLINE, C_VOID_BLACK, C_SUIT_DEEP, C_SUIT_BASE, C_SUIT_MID, C_SUIT_LIGHT, C_SUIT_SPEC,
    C_CAPE_OUTER, C_CAPE_FOLD, C_CAPE_RIM, C_CAPE_INNER_DP, C_CAPE_INNER, C_CAPE_INNER_HI,
    C_PURPLE_DARK, C_PURPLE_ROYAL, C_PURPLE_BRIGHT, C_PURPLE_GLOW, C_PURPLE_CORE,
    C_CRIMSON_DEEP, C_CRIMSON_BASE, C_CRIMSON_GLOW,
    C_GOLD_OUTLINE, C_GOLD_DEEP, C_GOLD_SHADE, C_GOLD_BASE, C_GOLD_BRIGHT, C_GOLD_SPEC,
    C_BLADE_BLACK, C_BLADE_CORE, C_BLADE_EDGE, C_BLADE_GLOW, C_BLADE_WHITE
)

# ==============================================================================
# HELPER VFX RENDERERS FOR CHARACTER FRAMES
# ==============================================================================
def draw_crescent_slash_arc(c, cx, cy, radius, ang_start_deg, ang_end_deg, thickness=12, col_outer=C_PURPLE_ROYAL, col_mid=C_PURPLE_GLOW, col_core=C_BLADE_WHITE):
    """Draws a solid, razor-sharp 64-bit dark-purple crescent slash arc with zero pixel gaps."""
    steps = 260
    # Pass 1: dark shadow outer body
    for s in range(steps + 1):
        t = s / float(steps)
        ang = math.radians(ang_start_deg + (ang_end_deg - ang_start_deg) * t)
        taper = math.sin(t * math.pi)
        w = thickness * taper
        if w < 0.6:
            continue
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        px = cx + cos_a * (radius - w * 0.25)
        py = cy + sin_a * (radius - w * 0.25)
        c.circle(px, py, max(1.0, w * 0.55), (18, 8, 36, 215), fill=True)
    # Pass 2: royal purple main energy wave
    for s in range(steps + 1):
        t = s / float(steps)
        ang = math.radians(ang_start_deg + (ang_end_deg - ang_start_deg) * t)
        taper = math.sin(t * math.pi)
        w = thickness * taper
        if w < 0.6:
            continue
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        px = cx + cos_a * (radius + w * 0.05)
        py = cy + sin_a * (radius + w * 0.05)
        c.circle(px, py, max(0.8, w * 0.42), col_outer, fill=True)
    # Pass 3: glowing violet mid-edge
    for s in range(steps + 1):
        t = s / float(steps)
        ang = math.radians(ang_start_deg + (ang_end_deg - ang_start_deg) * t)
        taper = math.sin(t * math.pi)
        w = thickness * taper
        if w < 0.6:
            continue
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        px = cx + cos_a * (radius + w * 0.28)
        py = cy + sin_a * (radius + w * 0.28)
        c.circle(px, py, max(0.7, w * 0.24), col_mid, fill=True)
    # Pass 4: razor white leading edge
    for s in range(steps + 1):
        t = s / float(steps)
        ang = math.radians(ang_start_deg + (ang_end_deg - ang_start_deg) * t)
        taper = math.sin(t * math.pi)
        w = thickness * taper
        if w < 1.0:
            continue
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        px = cx + cos_a * (radius + w * 0.45)
        py = cy + sin_a * (radius + w * 0.45)
        c.set(px, py, col_core)


def draw_shadow_claws_vfx(c, base_x, base_y, count=3, scale=1.0):
    """Draws erupting dark shadow tendrils / claws with glowing purple-violet cores."""
    for i in range(count):
        ox = base_x + (i - 1) * int(12 * scale)
        oy = base_y
        h = int((26 + (i % 2) * 10) * scale)
        # Pass 1: black shadow outline
        for s in range(h):
            t = s / float(max(1, h - 1))
            cx = ox + math.sin(t * math.pi * 1.2 + i) * 6 * scale + t * 5 * scale
            cy = oy - s
            rad = (1.0 - t) * 3.8 * scale + 0.7
            c.circle(cx, cy, rad + 0.8, C_VOID_BLACK, fill=True)
        # Pass 2: vivid royal purple energy core
        for s in range(h):
            t = s / float(max(1, h - 1))
            cx = ox + math.sin(t * math.pi * 1.2 + i) * 6 * scale + t * 5 * scale
            cy = oy - s
            rad = (1.0 - t) * 2.1 * scale + 0.4
            c.circle(cx, cy, rad, C_PURPLE_ROYAL if t < 0.65 else C_PURPLE_GLOW, fill=True)
            if t > 0.8:
                c.set(cx, cy, C_PURPLE_CORE)


# ==============================================================================
# 1. IDLE (6 FRAMES: idle_01 .. idle_06) — 3/4 Stance, Smooth Breathing & Cape Wave
# ==============================================================================
def make_idle_frame(idx, total=6):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / float(total)
    ang = phase * 2.0 * math.pi
    # Smooth sinusoidal breathing & knee flexion
    bob_y = int(round(math.sin(ang) * 1.6))
    cape_billow = -25 + math.sin(ang - 0.6) * 5.0
    sword_sway = int(round(math.cos(ang) * 2.0))

    tx = 58
    ty = 46 + bob_y
    pose = {
        'tx': tx, 'ty': ty, 'lean_dx': 0,
        'hx': tx + 1, 'hy': ty - 17,
        'expr': 'confident',
        'aura_phase': phase, 'aura_intensity': 1.0 + 0.15 * math.sin(ang),
        'cape_dx': cape_billow, 'cape_dy': 0, 'cape_spread': 1.0, 'cape_phase': phase,
        'back_leg':  {'hip': (tx - 5, ty + 28), 'knee': (tx - 7, 100 + bob_y // 2), 'ankle': (tx - 9, 129)},
        'front_leg': {'hip': (tx + 5, ty + 28), 'knee': (tx + 9, 100 + bob_y // 2), 'ankle': (tx + 11, 130)},
        'back_arm':  {'sh': (tx - 11, ty + 4), 'el': (tx - 18, ty + 16), 'wr': (tx - 21, ty + 27 + bob_y // 2),
                      'open_hand': True, 'hand_dir': (-0.6, 0.8), 'layer': 'back'},
        'front_arm': {'sh': (tx + 12, ty + 4), 'el': (tx + 18, ty + 17), 'wr': (tx + 22, ty + 28),
                      'open_hand': False},
        'sword':     {'hilt': (tx + 22, ty + 28), 'tip': (tx + 38 + sword_sway, 130), 'aura': 1.0, 'layer': 'front'}
    }
    draw_dark_king_pose_128(c, pose)
    return c


# ==============================================================================
# 2. WALK / RUN (8 FRAMES: move_01 .. move_08) — Fluid 8-Frame Human Stride
# ==============================================================================
def make_move_frame(idx, total=8):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / float(total)
    ang = phase * 2.0 * math.pi

    # Natural double-bounce vertical bob per full stride cycle
    bob_y = int(round(-abs(math.cos(ang)) * 3.5 + 1.5))
    tx = 58
    ty = 47 + bob_y
    lean_dx = 4  # Athletic forward torso lean in 3/4 view

    # Front (right) leg angle & Back (left) leg angle (180 deg out of phase)
    stride_f = math.sin(ang)
    lift_f   = max(0.0, math.cos(ang))
    stride_b = math.sin(ang + math.pi)
    lift_b   = max(0.0, math.cos(ang + math.pi))

    # Front leg joints
    f_hip = (tx + 4, ty + 27)
    f_knee = (tx + 6 + stride_f * 13 + lift_f * 5, ty + 51 - lift_f * 7)
    f_ankle = (tx + 4 + stride_f * 19 - lift_f * 4, 129 - lift_f * 11)

    # Back leg joints
    b_hip = (tx - 4, ty + 27)
    b_knee = (tx - 2 + stride_b * 13 + lift_b * 5, ty + 50 - lift_b * 7)
    b_ankle = (tx - 4 + stride_b * 19 - lift_b * 4, 128 - lift_b * 11)

    # Counter-swinging arms (opposite to legs for realistic human biomechanics!)
    arm_swing = -stride_f
    b_arm_wr = (tx - 8 - arm_swing * 12, ty + 24 - arm_swing * 4)
    b_arm_el = (tx - 10 - arm_swing * 6, ty + 15)

    f_arm_wr = (tx + 16 + arm_swing * 10, ty + 25 - arm_swing * 3)
    f_arm_el = (tx + 13 + arm_swing * 5, ty + 16)

    pose = {
        'tx': tx, 'ty': ty, 'lean_dx': lean_dx,
        'hx': tx + lean_dx + 2, 'hy': ty - 17,
        'expr': 'confident',
        'aura_phase': phase, 'aura_intensity': 1.1,
        'cape_dx': -38 + math.sin(ang) * 4, 'cape_dy': -5, 'cape_spread': 1.15, 'cape_phase': phase,
        'back_leg':  {'hip': b_hip, 'knee': b_knee, 'ankle': b_ankle},
        'front_leg': {'hip': f_hip, 'knee': f_knee, 'ankle': f_ankle},
        'back_arm':  {'sh': (tx + lean_dx - 10, ty + 4), 'el': b_arm_el, 'wr': b_arm_wr,
                      'open_hand': True, 'hand_dir': (1 if arm_swing < 0 else -1, 0.5),
                      'layer': 'front' if arm_swing < -0.2 else 'back'},
        'front_arm': {'sh': (tx + lean_dx + 12, ty + 4), 'el': f_arm_el, 'wr': f_arm_wr,
                      'open_hand': False},
        'sword':     {'hilt': f_arm_wr, 'tip': (f_arm_wr[0] - 28, f_arm_wr[1] + 24),
                      'aura': 1.0, 'layer': 'front'}
    }
    draw_dark_king_pose_128(c, pose)
    return c


# ==============================================================================
# 3. BASIC ATTACKS (6 FRAMES: attack_01 .. attack_06) — Multi-Hit Melee Combo
# ==============================================================================
def make_attack_frame(idx):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / 6.0

    if idx == 1:
        # Frame 1: Anticipation / Coiled Wind-up (sword drawn across chest, weight on back leg)
        tx, ty, lean = 54, 48, -2
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean,
            'hx': tx + lean + 2, 'hy': ty - 17, 'expr': 'confident',
            'aura_phase': phase, 'aura_intensity': 1.2,
            'cape_dx': -22, 'cape_dy': 0, 'cape_spread': 1.05, 'cape_phase': phase,
            'back_leg':  {'hip': (tx - 6, ty + 27), 'knee': (tx - 14, 102), 'ankle': (tx - 18, 129)},
            'front_leg': {'hip': (tx + 6, ty + 27), 'knee': (tx + 14, 102), 'ankle': (tx + 18, 130)},
            'back_arm':  {'sh': (tx - 11, ty + 4), 'el': (tx - 20, ty + 14), 'wr': (tx - 26, ty + 20),
                          'open_hand': True, 'hand_dir': (-1, 0.3), 'layer': 'back'},
            'front_arm': {'sh': (tx + 10, ty + 4), 'el': (tx + 2, ty + 14), 'wr': (tx - 6, ty + 10),
                          'open_hand': False},
            'sword':     {'hilt': (tx - 6, ty + 10), 'tip': (tx - 38, ty - 24), 'aura': 1.3, 'layer': 'front'}
        }
        draw_dark_king_pose_128(c, pose)

    elif idx == 2:
        # Frame 2: Fast Horizontal Outward Slash + Wide Dark Crescent Wave!
        tx, ty, lean = 62, 48, 5
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean,
            'hx': tx + lean + 2, 'hy': ty - 17, 'expr': 'fierce',
            'aura_phase': phase, 'aura_intensity': 1.35,
            'cape_dx': -38, 'cape_dy': -4, 'cape_spread': 1.2, 'cape_phase': phase,
            'back_leg':  {'hip': (tx - 6, ty + 27), 'knee': (tx - 16, 103), 'ankle': (tx - 24, 129)},
            'front_leg': {'hip': (tx + 6, ty + 27), 'knee': (tx + 18, 101), 'ankle': (tx + 22, 130)},
            'back_arm':  {'sh': (tx - 8, ty + 4), 'el': (tx - 18, ty + 12), 'wr': (tx - 26, ty + 16),
                          'open_hand': True, 'hand_dir': (-1, 0.2), 'layer': 'back'},
            'front_arm': {'sh': (tx + 15, ty + 4), 'el': (tx + 28, ty + 7), 'wr': (tx + 40, ty + 9),
                          'open_hand': False},
            'sword':     {'hilt': (tx + 40, ty + 9), 'tip': (124, ty + 4), 'aura': 1.5, 'layer': 'front'}
        }
        draw_dark_king_pose_128(c, pose)
        draw_crescent_slash_arc(c, tx + 18, ty + 12, 46, -55, 45, thickness=13)

    elif idx == 3:
        # Frame 3: Follow-through of Slash 1 & Transition into High Overhead Chamber
        tx, ty, lean = 60, 47, 3
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean,
            'hx': tx + lean + 2, 'hy': ty - 17, 'expr': 'fierce',
            'aura_phase': phase, 'aura_intensity': 1.25,
            'cape_dx': -34, 'cape_dy': -2, 'cape_spread': 1.15, 'cape_phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 27), 'knee': (tx - 14, 102), 'ankle': (tx - 20, 129)},
            'front_leg': {'hip': (tx + 6, ty + 27), 'knee': (tx + 16, 102), 'ankle': (tx + 20, 130)},
            'back_arm':  {'sh': (tx - 9, ty + 4), 'el': (tx - 4, ty + 14), 'wr': (tx + 6, ty + 16),
                          'open_hand': True, 'hand_dir': (1, 0), 'layer': 'front'},
            'front_arm': {'sh': (tx + 14, ty + 3), 'el': (tx + 18, ty - 8), 'wr': (tx + 12, ty - 18),
                          'open_hand': False},
            'sword':     {'hilt': (tx + 12, ty - 18), 'tip': (tx - 24, 6), 'aura': 1.4, 'layer': 'front'}
        }
        draw_dark_king_pose_128(c, pose)

    elif idx == 4:
        # Frame 4: Devastating Overhead Vertical-Diagonal Cleave!
        tx, ty, lean = 64, 49, 6
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean,
            'hx': tx + lean + 2, 'hy': ty - 16, 'expr': 'fierce',
            'aura_phase': phase, 'aura_intensity': 1.5,
            'cape_dx': -42, 'cape_dy': -6, 'cape_spread': 1.25, 'cape_phase': phase,
            'back_leg':  {'hip': (tx - 6, ty + 26), 'knee': (tx - 18, 103), 'ankle': (tx - 28, 129)},
            'front_leg': {'hip': (tx + 6, ty + 26), 'knee': (tx + 20, 100), 'ankle': (tx + 24, 130)},
            'back_arm':  {'sh': (tx - 8, ty + 4), 'el': (tx - 20, ty + 10), 'wr': (tx - 30, ty + 14),
                          'open_hand': True, 'hand_dir': (-1, 0.2), 'layer': 'back'},
            'front_arm': {'sh': (tx + 16, ty + 5), 'el': (tx + 26, ty + 16), 'wr': (tx + 34, ty + 28),
                          'open_hand': False},
            'sword':     {'hilt': (tx + 34, ty + 28), 'tip': (118, 124), 'aura': 1.6, 'layer': 'front'}
        }
        draw_dark_king_pose_128(c, pose)
        draw_crescent_slash_arc(c, tx + 14, ty + 18, 52, -75, 58, thickness=15,
                                col_outer=C_CRIMSON_BASE, col_mid=C_PURPLE_GLOW, col_core=C_BLADE_WHITE)

    elif idx == 5:
        # Frame 5: Piercing Void Lunge Thrust (3rd hit of combo)
        tx, ty, lean = 66, 50, 7
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean,
            'hx': tx + lean + 2, 'hy': ty - 16, 'expr': 'fierce',
            'aura_phase': phase, 'aura_intensity': 1.4,
            'cape_dx': -44, 'cape_dy': -8, 'cape_spread': 1.25, 'cape_phase': phase,
            'back_leg':  {'hip': (tx - 6, ty + 25), 'knee': (tx - 20, 104), 'ankle': (tx - 32, 129)},
            'front_leg': {'hip': (tx + 6, ty + 25), 'knee': (tx + 22, 100), 'ankle': (tx + 26, 130)},
            'back_arm':  {'sh': (tx - 8, ty + 4), 'el': (tx - 18, ty + 12), 'wr': (tx - 26, ty + 18),
                          'open_hand': True, 'hand_dir': (-1, 0.3), 'layer': 'back'},
            'front_arm': {'sh': (tx + 16, ty + 4), 'el': (tx + 30, ty + 5), 'wr': (tx + 44, ty + 5),
                          'open_hand': False},
            'sword':     {'hilt': (tx + 44, ty + 5), 'tip': (126, ty + 5), 'aura': 1.6, 'layer': 'front'}
        }
        draw_dark_king_pose_128(c, pose)
        # Piercing thrust shockwave rings & linear void beam
        c.ellipse(tx + 48, ty + 5, 4, 14, C_PURPLE_GLOW, fill=False)
        c.ellipse(tx + 58, ty + 5, 3, 10, C_BLADE_WHITE, fill=False)
        c.line(tx + 36, ty + 2, 126, ty + 5, C_PURPLE_GLOW)
        c.line(tx + 36, ty + 8, 126, ty + 5, C_PURPLE_GLOW)

    else:
        # Frame 6: Smooth Recovery Flourish back toward 3/4 Idle Stance
        tx, ty, lean = 60, 47, 2
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean,
            'hx': tx + lean + 1, 'hy': ty - 17, 'expr': 'confident',
            'aura_phase': phase, 'aura_intensity': 1.1,
            'cape_dx': -30, 'cape_dy': -2, 'cape_spread': 1.05, 'cape_phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 27), 'knee': (tx - 10, 101), 'ankle': (tx - 14, 129)},
            'front_leg': {'hip': (tx + 5, ty + 27), 'knee': (tx + 12, 101), 'ankle': (tx + 15, 130)},
            'back_arm':  {'sh': (tx - 10, ty + 4), 'el': (tx - 17, ty + 15), 'wr': (tx - 20, ty + 25),
                          'open_hand': True, 'hand_dir': (-0.6, 0.8), 'layer': 'back'},
            'front_arm': {'sh': (tx + 13, ty + 4), 'el': (tx + 22, ty + 14), 'wr': (tx + 26, ty + 24),
                          'open_hand': False},
            'sword':     {'hilt': (tx + 26, ty + 24), 'tip': (tx + 46, 118), 'aura': 1.1, 'layer': 'front'}
        }
        draw_dark_king_pose_128(c, pose)

    return c


# ==============================================================================
# 4. DASH / LUNGE (4 FRAMES: dash_01 .. dash_04) — High-Speed Horizontal Burst
# ==============================================================================
def make_dash_frame(idx):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / 4.0

    # Low center of gravity, intense forward lean, shadow afterimage silhouette behind
    tx = 64 + (idx % 2) * 3
    ty = 52
    lean = 8

    # Trailing Shadow Afterimage Ghost (drawn at tx - 22)
    ghost_x = tx - 20
    c.ellipse(ghost_x, ty + 12, 12, 26, (75, 30, 130, 85), fill=True)
    c.circle(ghost_x + 6, ty - 14, 8, (147, 70, 240, 90), fill=True)
    for s_line in range(6):
        ly = ty - 14 + s_line * 12
        c.line(8 + s_line * 3, ly, tx - 14, ly, (147, 70, 240, 150), thickness=2)
        c.line(16 + s_line * 4, ly + 3, tx - 8, ly + 3, C_PURPLE_CORE)

    pose = {
        'tx': tx, 'ty': ty, 'lean_dx': lean,
        'hx': tx + lean + 3, 'hy': ty - 16, 'expr': 'fierce',
        'aura_phase': phase, 'aura_intensity': 1.4,
        'cape_dx': -50, 'cape_dy': -16, 'cape_spread': 1.35, 'cape_phase': phase,
        'back_leg':  {'hip': (tx - 6, ty + 24), 'knee': (tx - 22, ty + 38), 'ankle': (tx - 38, 124)},
        'front_leg': {'hip': (tx + 6, ty + 24), 'knee': (tx + 22, ty + 36), 'ankle': (tx + 14, 126)},
        'back_arm':  {'sh': (tx - 6, ty + 4), 'el': (tx - 20, ty + 10), 'wr': (tx - 34, ty + 14),
                      'open_hand': True, 'hand_dir': (-1, 0.1), 'layer': 'back'},
        'front_arm': {'sh': (tx + 16, ty + 4), 'el': (tx + 28, ty + 10), 'wr': (tx + 40, ty + 12),
                      'open_hand': False},
        'sword':     {'hilt': (tx + 40, ty + 12), 'tip': (tx - 16, ty + 26), 'aura': 1.5, 'layer': 'front'}
    }
    draw_dark_king_pose_128(c, pose)
    return c


# ==============================================================================
# 5. JUMP & FALL / LAND (jump_01..03, fall_01..03) — Complete Aerial Arc
# ==============================================================================
def make_jump_frame(idx):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / 3.0

    if idx == 1:
        # Frame 1: Deep Crouch Anticipation before leap
        tx, ty, lean = 58, 56, 3
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean,
            'hx': tx + lean + 1, 'hy': ty - 17, 'expr': 'confident',
            'aura_phase': phase, 'aura_intensity': 1.2,
            'cape_dx': -24, 'cape_dy': 2, 'cape_spread': 1.1, 'cape_phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 24), 'knee': (tx - 14, 106), 'ankle': (tx - 10, 129)},
            'front_leg': {'hip': (tx + 5, ty + 24), 'knee': (tx + 18, 106), 'ankle': (tx + 12, 130)},
            'back_arm':  {'sh': (tx - 10, ty + 4), 'el': (tx - 20, ty + 16), 'wr': (tx - 26, ty + 24),
                          'open_hand': True, 'hand_dir': (-0.8, 0.6), 'layer': 'back'},
            'front_arm': {'sh': (tx + 13, ty + 4), 'el': (tx + 8, ty + 18), 'wr': (tx + 16, ty + 26),
                          'open_hand': False},
            'sword':     {'hilt': (tx + 16, ty + 26), 'tip': (tx - 18, 122), 'aura': 1.1, 'layer': 'front'}
        }
    elif idx == 2:
        # Frame 2: Explosive Upward Leap Posture
        tx, ty, lean = 58, 36, 2
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean,
            'hx': tx + lean + 1, 'hy': ty - 17, 'expr': 'fierce',
            'aura_phase': phase, 'aura_intensity': 1.3,
            'cape_dx': -22, 'cape_dy': 8, 'cape_spread': 1.15, 'cape_phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 27), 'knee': (tx - 10, ty + 52), 'ankle': (tx - 14, ty + 78)},
            'front_leg': {'hip': (tx + 5, ty + 27), 'knee': (tx + 16, ty + 44), 'ankle': (tx + 10, ty + 66)},
            'back_arm':  {'sh': (tx - 10, ty + 4), 'el': (tx - 18, ty + 12), 'wr': (tx - 22, ty + 22),
                          'open_hand': True, 'hand_dir': (-0.7, 0.7), 'layer': 'back'},
            'front_arm': {'sh': (tx + 13, ty + 4), 'el': (tx + 22, ty + 12), 'wr': (tx + 28, ty + 20),
                          'open_hand': False},
            'sword':     {'hilt': (tx + 28, ty + 20), 'tip': (tx + 46, ty + 74), 'aura': 1.2, 'layer': 'front'}
        }
    else:
        # Frame 3: Mid-Air Apex Pose (matching Reference Image 3 dynamic floating posture!)
        tx, ty, lean = 58, 34, 1
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean,
            'hx': tx + lean + 1, 'hy': ty - 17, 'expr': 'confident',
            'aura_phase': phase, 'aura_intensity': 1.35,
            'cape_dx': -32, 'cape_dy': 4, 'cape_spread': 1.3, 'cape_phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 27), 'knee': (tx - 12, ty + 46), 'ankle': (tx - 20, ty + 62)},
            'front_leg': {'hip': (tx + 5, ty + 27), 'knee': (tx + 10, ty + 52), 'ankle': (tx + 12, ty + 78)},
            'back_arm':  {'sh': (tx - 10, ty + 4), 'el': (tx - 18, ty + 14), 'wr': (tx - 24, ty + 24),
                          'open_hand': True, 'hand_dir': (-0.5, 0.8), 'layer': 'back'},
            'front_arm': {'sh': (tx + 13, ty + 4), 'el': (tx + 22, ty - 4), 'wr': (tx + 28, ty - 10),
                          'open_hand': True, 'hand_dir': (0.8, -0.5)},
            'sword':     {'hilt': (tx + 26, ty - 8), 'tip': (tx + 48, ty + 68), 'aura': 1.3, 'layer': 'front'}
        }
    draw_dark_king_pose_128(c, pose)
    return c


def make_fall_frame(idx):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / 3.0

    if idx in (1, 2):
        # Frames 1 & 2: Graceful Airborne Descent with billowing upward cloak
        bob = 0 if idx == 1 else 3
        tx, ty, lean = 58, 38 + bob, 2
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean,
            'hx': tx + lean + 1, 'hy': ty - 17, 'expr': 'confident',
            'aura_phase': phase, 'aura_intensity': 1.25,
            'cape_dx': -36 - bob * 2, 'cape_dy': -14, 'cape_spread': 1.35, 'cape_phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 27), 'knee': (tx - 12, ty + 48), 'ankle': (tx - 16, ty + 72)},
            'front_leg': {'hip': (tx + 5, ty + 27), 'knee': (tx + 12, ty + 52), 'ankle': (tx + 14, ty + 80)},
            'back_arm':  {'sh': (tx - 10, ty + 4), 'el': (tx - 20, ty + 8), 'wr': (tx - 28, ty + 12),
                          'open_hand': True, 'hand_dir': (-0.8, 0.4), 'layer': 'back'},
            'front_arm': {'sh': (tx + 13, ty + 4), 'el': (tx + 24, ty + 10), 'wr': (tx + 32, ty + 18),
                          'open_hand': False},
            'sword':     {'hilt': (tx + 32, ty + 18), 'tip': (tx + 50, ty + 78), 'aura': 1.2, 'layer': 'front'}
        }
    else:
        # Frame 3: Cushioned Landing Impact Absorption
        tx, ty, lean = 58, 52, 3
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean,
            'hx': tx + lean + 1, 'hy': ty - 17, 'expr': 'confident',
            'aura_phase': phase, 'aura_intensity': 1.3,
            'cape_dx': -30, 'cape_dy': -4, 'cape_spread': 1.2, 'cape_phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 25), 'knee': (tx - 12, 104), 'ankle': (tx - 14, 129)},
            'front_leg': {'hip': (tx + 5, ty + 25), 'knee': (tx + 16, 104), 'ankle': (tx + 16, 130)},
            'back_arm':  {'sh': (tx - 10, ty + 4), 'el': (tx - 18, ty + 16), 'wr': (tx - 24, ty + 26),
                          'open_hand': True, 'hand_dir': (-0.6, 0.8), 'layer': 'back'},
            'front_arm': {'sh': (tx + 13, ty + 4), 'el': (tx + 20, ty + 16), 'wr': (tx + 26, ty + 26),
                          'open_hand': False},
            'sword':     {'hilt': (tx + 26, ty + 26), 'tip': (tx + 44, 128), 'aura': 1.2, 'layer': 'front'}
        }
    draw_dark_king_pose_128(c, pose)
    return c


# ==============================================================================
# 6. SKILL CASTING (skill_01..04) & FINISHER (finisher_01..04)
# ==============================================================================
def make_skill_frame(idx):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / 4.0
    tx = 56
    ty = 47

    # Outstretched left/front casting hand summoning dark vortex & shadow claws
    pose = {
        'tx': tx, 'ty': ty, 'lean_dx': 2,
        'hx': tx + 3, 'hy': ty - 17, 'expr': 'fierce',
        'aura_phase': phase, 'aura_intensity': 1.4 + idx * 0.1,
        'cape_dx': -32 - idx * 3, 'cape_dy': -2 * idx, 'cape_spread': 1.2 + idx * 0.05, 'cape_phase': phase,
        'back_leg':  {'hip': (tx - 6, ty + 27), 'knee': (tx - 14, 102), 'ankle': (tx - 18, 129)},
        'front_leg': {'hip': (tx + 6, ty + 27), 'knee': (tx + 16, 101), 'ankle': (tx + 20, 130)},
        'back_arm':  {'sh': (tx - 10, ty + 4), 'el': (tx - 18, ty + 16), 'wr': (tx - 14, ty + 26),
                      'open_hand': False, 'layer': 'back'},
        'front_arm': {'sh': (tx + 13, ty + 4), 'el': (tx + 25, ty + 6), 'wr': (tx + 37, ty + 4),
                      'open_hand': True, 'hand_dir': (1, -0.2)},
        'sword':     {'hilt': (tx - 14, ty + 26), 'tip': (tx - 32, 124), 'aura': 1.2, 'layer': 'behind_arm'}
    }
    draw_dark_king_pose_128(c, pose)

    # Dark Magic Projectile / Vortex Orb forming in front of his outstretched palm
    orb_x, orb_y = tx + 48, ty + 3
    orb_r = 5 + idx * 2.5
    c.circle(orb_x, orb_y, orb_r + 4, (98, 40, 168, 120), fill=True)
    c.circle(orb_x, orb_y, orb_r, C_VOID_BLACK, fill=True)
    c.circle(orb_x, orb_y, orb_r, C_PURPLE_GLOW, fill=False)
    c.circle(orb_x, orb_y, orb_r * 0.45, C_PURPLE_CORE, fill=True)
    if idx >= 3:
        draw_shadow_claws_vfx(c, tx + 34, 132, count=3, scale=0.8 + (idx - 2) * 0.25)

    return c


def make_finisher_frame(idx):
    """
    Ultimate Finisher ('I AM ATOMIC' / Bành Trướng Lãnh Địa):
    Raised Obsidian Blade channeling sovereign purple-crimson void energy.
    """
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / 4.0
    tx = 58
    ty = 45 - (1 if idx in (2, 3) else 0)

    # Sovereign Dark Aura Rings behind character
    if idx >= 2:
        ring_r = 26 + (idx - 1) * 10
        c.circle(tx + 2, ty + 12, ring_r, (147, 70, 240, 110), fill=False)
        c.circle(tx + 2, ty + 12, ring_r - 6, (255, 71, 114, 130), fill=False)

    pose = {
        'tx': tx, 'ty': ty, 'lean_dx': 1,
        'hx': tx + 2, 'hy': ty - 17, 'expr': 'fierce',
        'aura_phase': phase, 'aura_intensity': 1.6,
        'cape_dx': -36 - idx * 2, 'cape_dy': -6, 'cape_spread': 1.35, 'cape_phase': phase,
        'back_leg':  {'hip': (tx - 6, ty + 28), 'knee': (tx - 14, 101), 'ankle': (tx - 18, 129)},
        'front_leg': {'hip': (tx + 6, ty + 28), 'knee': (tx + 14, 101), 'ankle': (tx + 18, 130)},
        'back_arm':  {'sh': (tx - 10, ty + 4), 'el': (tx - 20, ty + 12), 'wr': (tx - 28, ty + 18),
                      'open_hand': True, 'hand_dir': (-0.9, 0.4), 'layer': 'back'},
        'front_arm': {'sh': (tx + 13, ty + 3), 'el': (tx + 20, ty - 9), 'wr': (tx + 22, ty - 21),
                      'open_hand': False},
        'sword':     {'hilt': (tx + 22, ty - 21), 'tip': (tx + 26, 3), 'aura': 1.8, 'layer': 'front'}
    }
    draw_dark_king_pose_128(c, pose)

    # Atomic Void Sphere & Lightning arcs at sword tip
    tip_x, tip_y = tx + 25, 10
    sphere_r = 4 + idx * 2
    c.circle(tip_x, tip_y, sphere_r + 3, (147, 70, 240, 140), fill=True)
    c.circle(tip_x, tip_y, sphere_r, C_VOID_BLACK, fill=True)
    c.circle(tip_x, tip_y, sphere_r, C_PURPLE_CORE, fill=False)
    if idx >= 3:
        draw_shadow_claws_vfx(c, tx, 133, count=4, scale=1.0)

    return c


# ==============================================================================
# 7. KNOCKDOWN / DEFEATED (4 FRAMES: defeat_01 .. defeat_04) — Stagger to Collapse
# ==============================================================================
def make_defeat_frame(idx):
    c = PixelCanvas(128, 144)
    phase = (idx - 1) / 4.0

    if idx == 1:
        # Frame 1: Staggered Hit Reaction (knocked backward)
        tx, ty, lean = 54, 49, -4
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean,
            'hx': tx + lean, 'hy': ty - 16, 'expr': 'fierce',
            'aura_phase': phase, 'aura_intensity': 0.8,
            'cape_dx': -16, 'cape_dy': 2, 'cape_spread': 0.95, 'cape_phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 27), 'knee': (tx - 16, 104), 'ankle': (tx - 22, 129)},
            'front_leg': {'hip': (tx + 5, ty + 27), 'knee': (tx + 10, 103), 'ankle': (tx + 14, 130)},
            'back_arm':  {'sh': (tx - 12, ty + 4), 'el': (tx - 22, ty + 14), 'wr': (tx - 28, ty + 22),
                          'open_hand': True, 'hand_dir': (-1, 0.5), 'layer': 'back'},
            'front_arm': {'sh': (tx + 10, ty + 4), 'el': (tx + 18, ty + 16), 'wr': (tx + 24, ty + 26),
                          'open_hand': False},
            'sword':     {'hilt': (tx + 24, ty + 26), 'tip': (tx + 38, 128), 'aura': 0.7, 'layer': 'front'}
        }
    elif idx == 2:
        # Frame 2: Buckling Drop toward One Knee
        tx, ty, lean = 56, 58, 2
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean,
            'hx': tx + lean + 1, 'hy': ty - 16, 'expr': 'fierce',
            'aura_phase': phase, 'aura_intensity': 0.65,
            'cape_dx': -18, 'cape_dy': 4, 'cape_spread': 0.9, 'cape_phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 25), 'knee': (tx - 14, 114), 'ankle': (tx - 24, 129)},
            'front_leg': {'hip': (tx + 5, ty + 25), 'knee': (tx + 16, 108), 'ankle': (tx + 14, 130)},
            'back_arm':  {'sh': (tx - 10, ty + 4), 'el': (tx - 16, ty + 16), 'wr': (tx - 20, ty + 28),
                          'open_hand': True, 'hand_dir': (-0.6, 0.8), 'layer': 'back'},
            'front_arm': {'sh': (tx + 12, ty + 4), 'el': (tx + 20, ty + 16), 'wr': (tx + 26, ty + 26),
                          'open_hand': False},
            'sword':     {'hilt': (tx + 26, ty + 26), 'tip': (tx + 28, 130), 'aura': 0.6, 'layer': 'front'}
        }
    elif idx == 3:
        # Frame 3: Sovereign Kneeling Impact (planting sword vertically into the earth)
        tx, ty, lean = 58, 66, 3
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean,
            'hx': tx + lean + 2, 'hy': ty - 15, 'expr': 'confident',
            'aura_phase': phase, 'aura_intensity': 0.55,
            'cape_dx': -20, 'cape_dy': 6, 'cape_spread': 0.85, 'cape_phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 24), 'knee': (tx - 8, 126), 'ankle': (tx - 24, 129)},
            'front_leg': {'hip': (tx + 5, ty + 24), 'knee': (tx + 18, 110), 'ankle': (tx + 16, 130)},
            'back_arm':  {'sh': (tx - 9, ty + 4), 'el': (tx - 2, ty + 16), 'wr': (tx + 10, ty + 28),
                          'open_hand': True, 'hand_dir': (0.6, 0.8), 'layer': 'front'},
            'front_arm': {'sh': (tx + 12, ty + 4), 'el': (tx + 20, ty + 14), 'wr': (tx + 26, ty + 22),
                          'open_hand': False},
            'sword':     {'hilt': (tx + 26, ty + 22), 'tip': (tx + 26, 132), 'aura': 0.5, 'layer': 'front'}
        }
    else:
        # Frame 4: Final Defeated Kneeling Pose (head slightly bowed in 3/4, cape draped on ground)
        tx, ty, lean = 58, 70, 4
        pose = {
            'tx': tx, 'ty': ty, 'lean_dx': lean,
            'hx': tx + lean + 3, 'hy': ty - 14, 'expr': 'confident',
            'aura_phase': phase, 'aura_intensity': 0.45,
            'cape_dx': -22, 'cape_dy': 6, 'cape_spread': 0.85, 'cape_phase': phase,
            'back_leg':  {'hip': (tx - 5, ty + 22), 'knee': (tx - 6, 128), 'ankle': (tx - 24, 130)},
            'front_leg': {'hip': (tx + 5, ty + 22), 'knee': (tx + 18, 112), 'ankle': (tx + 16, 130)},
            'back_arm':  {'sh': (tx - 8, ty + 4), 'el': (tx + 2, ty + 18), 'wr': (tx + 12, 126),
                          'open_hand': True, 'hand_dir': (0.5, 0.8), 'layer': 'front'},
            'front_arm': {'sh': (tx + 12, ty + 4), 'el': (tx + 20, ty + 14), 'wr': (tx + 26, ty + 20),
                          'open_hand': False},
            'sword':     {'hilt': (tx + 26, ty + 20), 'tip': (tx + 26, 132), 'aura': 0.4, 'layer': 'front'}
        }
    draw_dark_king_pose_128(c, pose)
    return c


# ==============================================================================
# 8. STANDALONE SKILL VFX & ABILITY TEXTURES (TRANSPARENT PNGs)
# ==============================================================================
def make_vfx_dark_orb_frame(idx, total=4):
    """64x64 Dark Magic Projectile Orb with orbiting shadow tendrils and dark-purple core."""
    c = PixelCanvas(64, 64)
    cx, cy = 32, 32
    phase = (idx - 1) / float(total)
    ang_base = phase * 2.0 * math.pi

    # Outer dark aura halo
    c.circle(cx, cy, 22, (35, 14, 62, 110), fill=True)
    c.circle(cx, cy, 17, (98, 40, 168, 150), fill=True)

    # 4 Swirling shadow tendrils orbiting the orb
    for i in range(4):
        a0 = ang_base + i * (math.pi / 2.0)
        for s in range(12):
            t = s / 11.0
            r = 11 + t * 14
            a = a0 - t * 1.1
            tx = cx + math.cos(a) * r
            ty = cy + math.sin(a) * r
            c.circle(tx, ty, (1.0 - t) * 2.5 + 0.5, C_PURPLE_BRIGHT if s < 6 else C_VOID_BLACK, fill=True)

    # Inner event-horizon black core & glowing purple rim
    c.circle(cx, cy, 11, C_VOID_BLACK, fill=True)
    c.circle(cx, cy, 11, C_PURPLE_GLOW, fill=False)
    c.circle(cx, cy, 10, C_PURPLE_BRIGHT, fill=False)
    c.circle(cx - 2, cy - 2, 4, C_PURPLE_GLOW, fill=True)
    c.circle(cx - 3, cy - 3, 2, C_PURPLE_CORE, fill=True)
    return c


def make_vfx_dark_slash_frame(idx, total=4):
    """128x128 Dark Crescent Slash Wave & Sharp Shadow Energy Trails."""
    c = PixelCanvas(128, 128)
    cx, cy = 44, 64
    r = 34 + idx * 8
    thickness = 18 - idx * 2
    draw_crescent_slash_arc(c, cx, cy, r, -68, 68, thickness=thickness,
                            col_outer=C_PURPLE_ROYAL, col_mid=C_PURPLE_GLOW, col_core=C_BLADE_WHITE)
    # Sharp shadow energy spikes trailing behind crescent
    for i in range(5):
        ang = math.radians(-50 + i * 25)
        sx = cx + math.cos(ang) * (r - 6)
        sy = cy + math.sin(ang) * (r - 6)
        tx = cx + math.cos(ang) * (r - 24 - (i % 2) * 8)
        ty = cy + math.sin(ang) * (r - 24 - (i % 2) * 8)
        c.line(tx, ty, sx, sy, C_PURPLE_BRIGHT, thickness=2)
        c.set(sx, sy, C_PURPLE_CORE)
    return c


def make_vfx_dark_vortex_frame(idx, total=4):
    """128x128 Ground Impact Rift, Shadow Tendrils/Claws & Dark Shockwave Rings."""
    c = PixelCanvas(128, 128)
    cx, cy = 64, 96
    phase = (idx - 1) / float(total)
    rx = 26 + idx * 8
    ry = 8 + idx * 2

    # Ground abyss rift
    c.ellipse(cx, cy, rx + 6, ry + 3, (14, 10, 24, 190), fill=True)
    c.ellipse(cx, cy, rx, ry, C_VOID_BLACK, fill=True)
    c.ellipse(cx, cy, rx, ry, C_PURPLE_GLOW, fill=False)
    c.ellipse(cx, cy, int(rx * 0.7), int(ry * 0.7), C_CRIMSON_GLOW, fill=False)

    # Erupting shadow claws / tendrils from the ground rift (2-pass for glowing violet core!)
    num_claws = 4 + idx
    for i in range(num_claws):
        t_pos = (i / float(max(1, num_claws - 1))) * 2.0 - 1.0
        bx = cx + t_pos * (rx * 0.75)
        by = cy + math.sin(i * 1.7) * 3
        claw_h = 28 + (i % 3) * 14 + idx * 6
        # Pass 1: Void black body
        for s in range(claw_h):
            t = s / float(max(1, claw_h - 1))
            wx = bx + math.sin(t * math.pi * 1.5 + phase * 2 * math.pi + i) * 7 - t_pos * t * 12
            wy = by - s
            rad = (1.0 - t) * 4.2 + 0.7
            c.circle(wx, wy, rad + 1.0, C_VOID_BLACK, fill=True)
        # Pass 2: Glowing royal-purple & lavender inner energy veins
        for s in range(claw_h):
            t = s / float(max(1, claw_h - 1))
            wx = bx + math.sin(t * math.pi * 1.5 + phase * 2 * math.pi + i) * 7 - t_pos * t * 12
            wy = by - s
            rad = (1.0 - t) * 2.2 + 0.4
            c.circle(wx, wy, rad, C_PURPLE_ROYAL if t < 0.55 else C_PURPLE_BRIGHT, fill=True)
            if t > 0.78:
                c.set(wx, wy, C_PURPLE_CORE)
    return c


def make_vfx_dark_impact_frame(idx, total=4):
    """128x128 Exploding Dark-Purple Energy Orb & Lingering Shadowy Particle Burst."""
    c = PixelCanvas(128, 128)
    cx, cy = 64, 64
    r = 12 + idx * 11
    c.circle(cx, cy, r + 6, (98, 40, 168, max(30, 180 - idx * 35)), fill=True)
    if idx <= 2:
        c.circle(cx, cy, r * 0.6, C_VOID_BLACK, fill=True)
    c.circle(cx, cy, r, C_PURPLE_GLOW, fill=False)
    c.circle(cx, cy, int(r * 0.75), C_PURPLE_CORE, fill=False)

    # Radial dark shards & embers
    for i in range(10):
        ang = i * (2.0 * math.pi / 10.0) + idx * 0.25
        r0 = r * 0.5
        r1 = r * 1.35
        x0, y0 = cx + math.cos(ang) * r0, cy + math.sin(ang) * r0
        x1, y1 = cx + math.cos(ang) * r1, cy + math.sin(ang) * r1
        c.line(x0, y0, x1, y1, C_PURPLE_GLOW if i % 2 == 0 else C_CRIMSON_GLOW, thickness=2)
        c.set(x1, y1, C_PURPLE_CORE)
    return c


def build_all():
    char_dir = os.path.abspath('game-assets/characters/1')
    fx_dir = os.path.abspath('game-assets/effects/dark_king')
    os.makedirs(char_dir, exist_ok=True)
    os.makedirs(fx_dir, exist_ok=True)

    # Remove any test file
    test_f = os.path.join(char_dir, 'test_idle.png')
    if os.path.exists(test_f):
        os.remove(test_f)

    all_char_canvases = []

    # 1. Idle (6 frames)
    for i in range(1, 7):
        cv = make_idle_frame(i, 6)
        fname = f'idle_0{i}.png'
        with open(os.path.join(char_dir, fname), 'wb') as f:
            f.write(cv.to_png_bytes(1))
        all_char_canvases.append((fname, cv))

    # 2. Move (8 frames)
    for i in range(1, 9):
        cv = make_move_frame(i, 8)
        fname = f'move_0{i}.png'
        with open(os.path.join(char_dir, fname), 'wb') as f:
            f.write(cv.to_png_bytes(1))
        all_char_canvases.append((fname, cv))

    # 3. Jump (3 frames) & Fall (3 frames)
    for i in range(1, 4):
        cv = make_jump_frame(i)
        fname = f'jump_0{i}.png'
        with open(os.path.join(char_dir, fname), 'wb') as f:
            f.write(cv.to_png_bytes(1))
        all_char_canvases.append((fname, cv))

    for i in range(1, 4):
        cv = make_fall_frame(i)
        fname = f'fall_0{i}.png'
        with open(os.path.join(char_dir, fname), 'wb') as f:
            f.write(cv.to_png_bytes(1))
        all_char_canvases.append((fname, cv))

    # 4. Basic Attack Combo (6 frames)
    for i in range(1, 7):
        cv = make_attack_frame(i)
        fname = f'attack_0{i}.png'
        with open(os.path.join(char_dir, fname), 'wb') as f:
            f.write(cv.to_png_bytes(1))
        all_char_canvases.append((fname, cv))

    # 5. Dash / Lunge (4 frames)
    for i in range(1, 5):
        cv = make_dash_frame(i)
        fname = f'dash_0{i}.png'
        with open(os.path.join(char_dir, fname), 'wb') as f:
            f.write(cv.to_png_bytes(1))
        all_char_canvases.append((fname, cv))

    # 6. Skill Casting (4 frames) & Finisher (4 frames)
    for i in range(1, 5):
        cv = make_skill_frame(i)
        fname = f'skill_0{i}.png'
        with open(os.path.join(char_dir, fname), 'wb') as f:
            f.write(cv.to_png_bytes(1))
        all_char_canvases.append((fname, cv))

    for i in range(1, 5):
        cv = make_finisher_frame(i)
        fname = f'finisher_0{i}.png'
        with open(os.path.join(char_dir, fname), 'wb') as f:
            f.write(cv.to_png_bytes(1))
        all_char_canvases.append((fname, cv))

    # 7. Defeat / Knockdown (4 frames)
    for i in range(1, 5):
        cv = make_defeat_frame(i)
        fname = f'defeat_0{i}.png'
        with open(os.path.join(char_dir, fname), 'wb') as f:
            f.write(cv.to_png_bytes(1))
        all_char_canvases.append((fname, cv))

    # Build Master 128x144 Character Spritesheet (6 columns x 7 rows = 42 frames)
    cols = 6
    rows = math.ceil(len(all_char_canvases) / float(cols))
    sheet = PixelCanvas(cols * 128, rows * 144)
    for idx, (fname, cv) in enumerate(all_char_canvases):
        c_idx = idx % cols
        r_idx = idx // cols
        ox, oy = c_idx * 128, r_idx * 144
        for y in range(144):
            for x in range(128):
                px = cv.pixels[y][x]
                if px[3] > 0:
                    sheet.pixels[oy + y][ox + x] = px
    sheet_path = os.path.join(char_dir, 'vua_bong_toi_spritesheet.png')
    with open(sheet_path, 'wb') as f:
        f.write(sheet.to_png_bytes(1))

    # 8. Build Skill VFX Textures (16 frames)
    for i in range(1, 5):
        with open(os.path.join(fx_dir, f'dark_orb_0{i}.png'), 'wb') as f:
            f.write(make_vfx_dark_orb_frame(i).to_png_bytes(1))
        with open(os.path.join(fx_dir, f'dark_slash_0{i}.png'), 'wb') as f:
            f.write(make_vfx_dark_slash_frame(i).to_png_bytes(1))
        with open(os.path.join(fx_dir, f'dark_vortex_0{i}.png'), 'wb') as f:
            f.write(make_vfx_dark_vortex_frame(i).to_png_bytes(1))
        with open(os.path.join(fx_dir, f'dark_impact_0{i}.png'), 'wb') as f:
            f.write(make_vfx_dark_impact_frame(i).to_png_bytes(1))

    print(f"Successfully generated {len(all_char_canvases)} native 128x144 character frames, master spritesheet, and 16 VFX textures!")

if __name__ == '__main__':
    build_all()
