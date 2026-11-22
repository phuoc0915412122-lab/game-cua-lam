import os, sys, math
sys.path.append(os.path.abspath('game-cua-lam/game-cua-lam-upload/scratch'))
from pixel_canvas import PixelCanvas

# ==============================================================================
# 🔥 HỎA KAGE (FIRE KAGE) — TRUE NATIVE 128x144 64-BIT PIXEL ART PALETTE
# ==============================================================================
C_OUTLINE       = '#140c10'

# Warm sunlit-tan muscular human skin (trắng nhưng rám nắng nhẹ)
C_SKIN_OUTLINE  = '#5c311b'
C_SKIN_CREVICE  = '#8f4f2e'
C_SKIN_DEEP     = '#b87249'
C_SKIN_SHADE    = '#d9986c'
C_SKIN_BASE     = '#f2be96'
C_SKIN_HILIGHT  = '#ffdfc2'
C_SKIN_SPEC     = '#fff2e3'

# Wild swept-back raven-black hair (no hat!)
C_HAIR_OUTLINE  = '#08060a'
C_HAIR_BASE     = '#14111a'
C_HAIR_MID      = '#252030'
C_HAIR_HILIGHT  = '#3e364f'
C_HAIR_SPEC     = '#5f5578'

# Crimson bead necklace & leather belt
C_BEAD_DEEP     = '#6e0d1c'
C_BEAD_BASE     = '#c91c33'
C_BEAD_HI       = '#ff5c72'

C_BELT_DEEP     = '#5e2c0c'
C_BELT_BASE     = '#a8531b'
C_BELT_HI       = '#de8233'
C_BUCKLE_DARK   = '#596173'
C_BUCKLE_BASE   = '#a3aec2'
C_BUCKLE_HI     = '#eef4ff'

# Masculine Pink Combat Shorts (quần màu hồng nam tính!)
C_PINK_OUTLINE  = '#4a0b28'
C_PINK_DEEP     = '#7d1544'
C_PINK_SHADE    = '#b32464'
C_PINK_BASE     = '#e33b84'
C_PINK_LIGHT    = '#ff6ea9'
C_PINK_SPEC     = '#ffa6cc'

# Rugged black combat boots
C_BOOT_OUTLINE  = '#09070d'
C_BOOT_DEEP     = '#15121c'
C_BOOT_BASE     = '#231e2e'
C_BOOT_HI       = '#3c354f'

# Sacred Blazing Fire wrapping both hands & forearms
C_FIRE_OUTER    = '#b8190d'
C_FIRE_RED      = '#e83415'
C_FIRE_ORANGE   = '#ff7817'
C_FIRE_GOLD     = '#ffd438'
C_FIRE_CORE     = '#fffbe0'


def draw_sacred_flame_cluster(c, cx, cy, phase=0.0, scale=1.0, dir_x=0.0, dir_y=-1.0):
    """
    Draws multi-layered sacred flames (2-pass: outer crimson-orange envelope,
    then blazing golden-white sacred core) licking dynamically around a hand or foot.
    """
    num_tongues = 5
    tongues = []
    for i in range(num_tongues):
        ang_off = (i - (num_tongues - 1) / 2.0) * 0.42
        base_ang = math.atan2(dir_y, dir_x) + ang_off
        h = int((14 + (i % 3) * 6) * scale)
        ox = cx + math.cos(base_ang + 1.57) * (i - 2) * 2.2 * scale
        oy = cy + math.sin(base_ang + 1.57) * (i - 2) * 1.4 * scale
        pts = []
        for s in range(h):
            t = s / float(max(1, h - 1))
            sway = math.sin(t * math.pi * 1.6 + phase * 2 * math.pi + i * 1.3) * 3.5 * scale
            px = ox + math.cos(base_ang) * s + sway
            py = oy + math.sin(base_ang) * s
            rad = (1.0 - t) * 3.0 * scale + 0.5
            pts.append((px, py, rad, t))
        tongues.append(pts)
    # Pass 1: Crimson-orange outer fire body
    for pts in tongues:
        for px, py, rad, t in pts:
            c.circle(px, py, rad + 1.1, (220, 44, 16, int(195 * (1.0 - t * 0.45))), fill=True)
            c.circle(px, py, rad * 0.78, C_FIRE_ORANGE, fill=True)
    # Pass 2: Blazing golden-yellow & sacred white-gold inner core
    for pts in tongues:
        for px, py, rad, t in pts:
            if t < 0.72:
                c.circle(px, py, rad * 0.5, C_FIRE_GOLD, fill=True)
            if t < 0.42:
                c.circle(px, py, rad * 0.28, C_FIRE_CORE, fill=True)
    # Floating fire embers
    for i in range(3):
        ex = cx + math.sin(phase * 2 * math.pi + i * 2.3) * 10 * scale
        ey = cy - (12 + ((phase * 22 + i * 7) % 16)) * scale
        c.set(ex, ey, C_FIRE_CORE if i == 0 else C_FIRE_GOLD)


def draw_ground_fire_aura_128(c, cx, phase=0.0, intensity=1.0, dash_trail=False, jump_sparks=False):
    """Draws warm heat-shadow under feet + optional dash ground fire trail or jump flame sparks."""
    gy = 135
    if not jump_sparks:
        c.ellipse(cx, gy, int(24 * intensity), 4, (24, 10, 8, 130), fill=True)
        c.ellipse(cx, gy, int(16 * intensity), 2.5, (235, 85, 20, 110), fill=True)

    if dash_trail:
        # Blazing fire trail left behind on the ground when dashing!
        for i in range(6):
            fx = cx - 12 - i * 9
            fy = gy - 1
            f_sc = max(0.35, 1.0 - i * 0.13)
            draw_sacred_flame_cluster(c, fx, fy, phase=phase + i * 0.15, scale=f_sc * 0.85, dir_x=-0.35, dir_y=-1.0)
        # Scorched glowing ember line on ground
        c.line(cx - 60, gy, cx + 6, gy, C_FIRE_ORANGE, thickness=2)
        c.line(cx - 46, gy, cx + 2, gy, C_FIRE_GOLD)

    if jump_sparks:
        # Little flame sparks bursting downward/outward on jump!
        for i in range(7):
            ang = math.radians(30 + i * 20)
            dist = 14 + (i % 3) * 8 + phase * 10
            sx = cx + math.cos(ang) * dist * (1 if i % 2 == 0 else -1) * 0.9
            sy = 122 + math.sin(ang) * 14
            c.circle(sx, sy, 2.2, C_FIRE_ORANGE, fill=True)
            c.set(sx, sy, C_FIRE_CORE)
            c.line(sx, sy, sx * 0.7 + cx * 0.3, sy - 6, C_FIRE_GOLD)


def draw_athletic_leg_128(c, hip_x, hip_y, knee_x, knee_y, ankle_x, ankle_y, is_front=True):
    """
    Draws muscular legs wearing masculine pink knee-length combat shorts,
    sculpted sunlit-tan calves, and rugged black combat boots.
    """
    # 1. Lower sculpted bare calf (knee -> boot top)
    skin_base  = C_SKIN_BASE if is_front else C_SKIN_SHADE
    skin_shade = C_SKIN_SHADE if is_front else C_SKIN_DEEP
    skin_hi    = C_SKIN_HILIGHT if is_front else C_SKIN_BASE
    boot_top_x = knee_x * 0.45 + ankle_x * 0.55
    boot_top_y = knee_y * 0.45 + ankle_y * 0.55

    c.capsule(knee_x, knee_y, boot_top_x, boot_top_y, 5.2, 4.4,
              skin_base, shade_col=skin_shade, hi_col=skin_hi, outline_col=C_SKIN_OUTLINE)

    # 2. Masculine Pink Shorts leg (hip -> just below knee, cuffed!)
    p_base  = C_PINK_BASE if is_front else C_PINK_SHADE
    p_shade = C_PINK_SHADE if is_front else C_PINK_DEEP
    p_hi    = C_PINK_LIGHT if is_front else C_PINK_BASE
    c.capsule(hip_x, hip_y, knee_x, knee_y + 1, 8.2, 6.8,
              p_base, shade_col=p_shade, hi_col=p_hi, outline_col=C_PINK_OUTLINE)
    # Rolled hem cuff on pink shorts
    c.line(knee_x - 6, knee_y + 1, knee_x + 6, knee_y + 1, C_PINK_DEEP, thickness=3)
    c.line(knee_x - 5, knee_y, knee_x + 5, knee_y, C_PINK_SPEC if is_front else C_PINK_LIGHT)
    # Cool dark leather thigh pouch strap on front thigh (Ace-inspired!)
    if is_front:
        mx = hip_x * 0.4 + knee_x * 0.6
        my = hip_y * 0.4 + knee_y * 0.6
        c.line(mx - 7, my - 1, mx + 7, my + 1, C_BOOT_DEEP, thickness=3)
        c.rect(mx + 3, my - 2, 4, 4, C_BUCKLE_BASE)
        c.set(mx + 4, my - 1, C_BUCKLE_HI)

    # 3. Rugged Black Combat Boot (boot_top -> ankle + toe)
    b_base = C_BOOT_BASE if is_front else C_BOOT_DEEP
    b_hi   = C_BOOT_HI if is_front else C_BOOT_BASE
    c.capsule(boot_top_x, boot_top_y, ankle_x, ankle_y, 5.0, 4.4,
              b_base, shade_col=C_BOOT_DEEP, hi_col=b_hi, outline_col=C_BOOT_OUTLINE)
    # Boot cuff & silver strap
    c.line(boot_top_x - 5, boot_top_y, boot_top_x + 5, boot_top_y, C_BOOT_HI, thickness=2)
    # Boot foot facing 3/4 forward-right
    ax, ay = int(round(ankle_x)), int(round(ankle_y))
    toe_len = 11 if is_front else 9
    foot_poly = [
        (ax - 5, ay - 2),
        (ax + 4, ay - 2),
        (ax + toe_len, ay + 2),
        (ax + toe_len + 1, ay + 6),
        (ax - 5, ay + 6)
    ]
    c.polygon(foot_poly, b_base, outline_col=C_BOOT_OUTLINE)
    c.line(ax - 4, ay + 5, ax + toe_len, ay + 5, C_BOOT_OUTLINE)
    if is_front:
        c.line(ax + 3, ay + 1, ax + 9, ay + 3, C_BOOT_HI)
        c.rect(ax + 1, ay - 1, 3, 2, C_BUCKLE_BASE)


def draw_sculpted_shirtless_torso_128(c, tx, ty, lean_dx=0):
    """
    Draws the shirtless, muscular, V-taper sunlit-tan human male torso in 3/4 view:
    - Broad sculpted shoulders & defined pectorals
    - Crisp 6-pack abs & oblique V-line
    - Ace-style crimson bead necklace
    - Masculine pink shorts waistband + rugged orange-brown leather belt & silver buckle
    """
    sx = tx + lean_dx
    sy = ty

    # 1. Muscular V-Taper Bare Torso Silhouette (shoulders ~30px -> lean waist ~19px)
    torso_poly = [
        (sx - 13, sy + 2),   # Back left shoulder/lat
        (sx - 6,  sy - 2),   # Traps
        (sx + 7,  sy - 2),   # Front traps
        (sx + 15, sy + 2),   # Front right shoulder
        (tx + 12, ty + 14),  # Ribcage right
        (tx + 10, ty + 24),  # Slim waist right
        (tx - 9,  ty + 24),  # Slim waist left
        (tx - 11, ty + 14)   # Lat curve left
    ]
    c.polygon(torso_poly, C_SKIN_BASE, outline_col=C_SKIN_OUTLINE)

    # 2. 3/4 Volumetric Muscle Shading (left/back side shaded, right chest lit)
    back_shade = [
        (sx - 12, sy + 3),
        (sx - 3,  sy + 1),
        (tx - 2,  ty + 23),
        (tx - 8,  ty + 23),
        (tx - 10, ty + 14)
    ]
    c.polygon(back_shade, C_SKIN_SHADE)

    # 3. Sculpted Pectoral Muscles (3/4 perspective: sternum at sx + 3)
    cx = sx + 3
    # Collarbones (clavicles)
    c.line(sx - 6, sy + 1, cx - 1, sy + 2, C_SKIN_DEEP)
    c.line(cx + 1, sy + 2, sx + 10, sy + 1, C_SKIN_DEEP)
    # Right pectoral (closer to camera, full sculpted highlight)
    c.polygon([(cx + 1, sy + 3), (sx + 13, sy + 4), (sx + 12, sy + 10), (cx + 1, sy + 10)], C_SKIN_HILIGHT)
    c.line(cx + 2, sy + 4, sx + 10, sy + 4, C_SKIN_SPEC)
    c.line(cx + 1, sy + 10, sx + 11, sy + 10, C_SKIN_DEEP) # Lower pec crease!
    # Left pectoral (receding 3/4)
    c.polygon([(sx - 8, sy + 4), (cx - 1, sy + 3), (cx - 1, sy + 10), (sx - 7, sy + 10)], C_SKIN_BASE)
    c.line(sx - 7, sy + 10, cx - 1, sy + 10, C_SKIN_CREVICE)
    # Center sternum cleavage line
    c.line(cx, sy + 3, cx, sy + 11, C_SKIN_DEEP)

    # 4. Crisp 6-Pack Abs (3 pairs of sculpted abdominal blocks!)
    ab_cx = int(round((cx + tx + 2) * 0.5))
    c.line(ab_cx, sy + 11, ab_cx, ty + 23, C_SKIN_DEEP) # Linea alba center line
    for row in range(3):
        ay = sy + 12 + row * 4
        # Left ab block (3/4 foreshortened)
        c.rect(ab_cx - 5, ay, 4, 3, C_SKIN_SHADE)
        c.rect(ab_cx - 4, ay, 3, 2, C_SKIN_BASE)
        c.line(ab_cx - 5, ay + 3, ab_cx - 1, ay + 3, C_SKIN_DEEP)
        # Right ab block (closer, highlighted!)
        c.rect(ab_cx + 1, ay, 5, 3, C_SKIN_BASE)
        c.rect(ab_cx + 2, ay, 3, 2, C_SKIN_HILIGHT)
        c.line(ab_cx + 1, ay + 3, ab_cx + 6, ay + 3, C_SKIN_DEEP)
    # Serratus / oblique V-lines on waist sides
    c.line(tx - 8, ty + 16, tx - 5, ty + 23, C_SKIN_DEEP)
    c.line(tx + 9, ty + 16, tx + 6, ty + 23, C_SKIN_DEEP)

    # 5. Ace-inspired Crimson Bead Necklace around collarbone
    for i in range(6):
        bx = sx - 5 + i * 2.4
        by = sy + (1 if i in (0, 5) else 2 if i in (1, 4) else 3)
        c.circle(bx, by, 1.5, C_BEAD_BASE, fill=True)
        c.set(bx, by - 1, C_BEAD_HI)

    # 6. Masculine Pink Shorts Pelvis + Rugged Leather Belt & Silver Buckle
    pelvis_poly = [
        (tx - 10, ty + 23),
        (tx + 11, ty + 23),
        (tx + 13, ty + 33),
        (tx + 1,  ty + 34),
        (tx - 12, ty + 33)
    ]
    c.polygon(pelvis_poly, C_PINK_BASE, outline_col=C_PINK_OUTLINE)
    c.line(tx + 2, ty + 26, tx + 10, ty + 26, C_PINK_LIGHT)
    # Slanted Ace-style orange-brown leather belt!
    c.line(tx - 10, ty + 25, tx + 11, ty + 22, C_BELT_DEEP, thickness=4)
    c.line(tx - 10, ty + 25, tx + 11, ty + 22, C_BELT_BASE, thickness=2)
    c.line(tx - 9,  ty + 24, tx + 10, ty + 21, C_BELT_HI)
    # Metallic Silver 'A'-style Belt Buckle
    c.rect(tx + 1, ty + 21, 6, 5, C_BUCKLE_DARK)
    c.rect(tx + 2, ty + 22, 4, 3, C_BUCKLE_BASE)
    c.set(tx + 3, ty + 22, C_BUCKLE_HI)


def draw_head_no_hat_128(c, hx, hy, expr='grin'):
    """
    Draws the handsome, free-spirited young male face in strict 3/4 side profile
    facing forward-right (+X) with wild raven-black hair (NO HAT!).
    """
    # 1. Strong Muscular Neck
    c.rect(hx - 4, hy + 11, 9, 8, C_SKIN_SHADE)
    c.rect(hx - 2, hy + 11, 6, 7, C_SKIN_BASE)
    c.line(hx - 4, hy + 11, hx - 4, hy + 18, C_SKIN_OUTLINE)
    c.line(hx + 5, hy + 12, hx + 5, hy + 18, C_SKIN_OUTLINE)
    c.line(hx, hy + 14, hx + 2, hy + 17, C_SKIN_DEEP) # Sternocleidomastoid tendon

    # 2. Wild Swept-Back Raven-Black Hair (Back spiky volume — NO HAT!)
    back_hair = [
        (hx - 12, hy - 8),
        (hx + 8,  hy - 10),
        (hx + 12, hy - 2),
        (hx - 8,  hy + 14),
        (hx - 16, hy + 10), # Wild lower neck spike
        (hx - 13, hy + 5),
        (hx - 17, hy + 2),  # Mid swept spike
        (hx - 13, hy - 2),
        (hx - 16, hy - 5)   # Upper wild spike
    ]
    c.polygon(back_hair, C_HAIR_BASE, outline_col=C_HAIR_OUTLINE)
    # Hair highlights on swept spikes
    c.line(hx - 11, hy - 5, hx - 6, hy - 7, C_HAIR_HILIGHT)
    c.line(hx - 13, hy + 2, hx - 8, hy + 2, C_HAIR_MID)

    # 3. Sculpted 3/4 Handsome Male Face Contour (facing forward-right!)
    face_poly = [
        (hx - 4, hy - 2),
        (hx + 8, hy - 2),
        (hx + 9, hy + 3),
        (hx + 11, hy + 6),  # Sharp 3/4 nose profile
        (hx + 9, hy + 9),
        (hx + 6, hy + 13),  # Defined masculine chin
        (hx - 1, hy + 12),  # Jaw angle
        (hx - 5, hy + 8)
    ]
    c.polygon(face_poly, C_SKIN_BASE)
    c.polygon([(hx - 5, hy - 1), (hx - 1, hy - 1), (hx, hy + 11), (hx - 4, hy + 9)], C_SKIN_SHADE)
    # Crisp 3/4 profile outline
    c.line(hx - 4, hy + 9, hx - 1, hy + 12, C_SKIN_OUTLINE)
    c.line(hx - 1, hy + 12, hx + 6, hy + 13, C_SKIN_OUTLINE)
    c.line(hx + 6, hy + 13, hx + 9, hy + 9, C_SKIN_OUTLINE)
    c.line(hx + 9, hy + 3, hx + 11, hy + 6, C_SKIN_OUTLINE)
    c.line(hx + 3, hy + 6, hx + 6, hy + 6, C_SKIN_HILIGHT)
    c.set(hx + 9, hy + 5, C_SKIN_SPEC)
    # Ear on left side
    c.rect(hx - 6, hy + 4, 2, 4, C_SKIN_SHADE)

    # 4. Fierce, Confident 3/4 Eyes Looking Forward-Right (+X)
    if expr == 'hit':
        # Wincing/gritting expression when taking damage
        c.line(hx + 1, hy + 4, hx + 4, hy + 5, C_OUTLINE)
        c.line(hx + 1, hy + 6, hx + 4, hy + 5, C_OUTLINE)
        c.line(hx + 7, hy + 4, hx + 9, hy + 5, C_OUTLINE)
        c.rect(hx + 5, hy + 9, 4, 2, '#ffffff')
        c.line(hx + 5, hy + 10, hx + 8, hy + 10, C_OUTLINE)
    else:
        # Near eye (left from viewer, pupil on RIGHT side looking forward-right!)
        c.line(hx, hy + 3, hx + 5, hy + 4, C_OUTLINE)
        c.line(hx - 1, hy + 2, hx + 4, hy + 3, C_HAIR_BASE) # Bold eyebrow
        c.rect(hx + 1, hy + 4, 4, 3, '#ffffff')
        c.rect(hx + 3, hy + 4, 2, 3, '#2b1810') # Dark fiery eyes looking right
        c.set(hx + 4, hy + 5, C_FIRE_ORANGE if expr == 'fierce' else '#110a08')
        c.set(hx + 2, hy + 4, '#ffffff')
        # Far eye (foreshortened at right edge)
        c.line(hx + 7, hy + 3, hx + 9, hy + 4, C_OUTLINE)
        c.rect(hx + 7, hy + 4, 2, 3, '#ffffff')
        c.rect(hx + 8, hy + 4, 2, 3, '#2b1810')
        # Carefree Ace grin / fierce battle shout!
        if expr == 'fierce':
            c.rect(hx + 5, hy + 9, 4, 3, '#7a1919')
            c.line(hx + 5, hy + 9, hx + 8, hy + 9, '#ffffff')
        else:
            # Iconic wide carefree grin!
            c.line(hx + 4, hy + 9, hx + 8, hy + 9, '#ffffff')
            c.line(hx + 3, hy + 10, hx + 8, hy + 10, C_SKIN_OUTLINE)
            c.set(hx + 8, hy + 9, C_SKIN_OUTLINE)

    # 5. Wild Spiky Top & Front Hair Bangs (NO HAT!)
    top_hair = [
        (hx - 11, hy - 9),
        (hx - 6,  hy - 13), # Wild spike 1
        (hx - 2,  hy - 10),
        (hx + 3,  hy - 14), # Tall wild spike 2
        (hx + 6,  hy - 10),
        (hx + 11, hy - 11), # Forward spike 3
        (hx + 11, hy - 2),
        (hx - 11, hy - 2)
    ]
    c.polygon(top_hair, C_HAIR_BASE, outline_col=C_HAIR_OUTLINE)
    c.line(hx - 6, hy - 7, hx + 6, hy - 7, C_HAIR_HILIGHT, thickness=2)
    c.line(hx - 2, hy - 8, hx + 4, hy - 8, C_HAIR_SPEC)
    # Framing sideburn & loose bangs
    c.polygon([(hx - 9, hy - 2), (hx - 4, hy - 2), (hx - 5, hy + 9), (hx - 10, hy + 10)], C_HAIR_BASE)
    c.polygon([(hx + 3, hy - 3), (hx + 7, hy - 3), (hx + 6, hy + 4)], C_HAIR_BASE)
    c.polygon([(hx + 8, hy - 3), (hx + 11, hy - 1), (hx + 10, hy + 4)], C_HAIR_BASE)


def draw_flaming_arm_128(c, sh_x, sh_y, el_x, el_y, wr_x, wr_y,
                         is_front=True, phase=0.0, flame_scale=1.0):
    """
    Draws a muscular bare human arm with sculpted deltoid/bicep, orange elbow band,
    and SACRED BLAZING FLAMES engulfing the forearm and fist!
    """
    s_base  = C_SKIN_BASE if is_front else C_SKIN_SHADE
    s_shade = C_SKIN_SHADE if is_front else C_SKIN_DEEP
    s_hi    = C_SKIN_HILIGHT if is_front else C_SKIN_BASE

    # Muscular Deltoid & Upper Arm
    c.capsule(sh_x, sh_y, el_x, el_y, 5.4, 4.4,
              s_base, shade_col=s_shade, hi_col=s_hi, outline_col=C_SKIN_OUTLINE)
    # Ace-style orange elbow/arm guard band
    c.circle(el_x, el_y, 4.5, C_BELT_BASE, fill=True)
    c.line(el_x - 3, el_y - 1, el_x + 3, el_y - 1, C_BELT_HI)

    # Muscular Forearm
    c.capsule(el_x, el_y, wr_x, wr_y, 4.4, 3.8,
              s_base, shade_col=s_shade, hi_col=s_hi, outline_col=C_SKIN_OUTLINE)
    # Clenched Muscular Fist
    c.circle(wr_x, wr_y, 4.2, C_SKIN_OUTLINE, fill=True)
    c.circle(wr_x, wr_y, 3.4, s_base, fill=True)
    c.set(wr_x + 1, wr_y - 1, s_hi)

    # SACRED FLAMES wrapping forearm & fist!
    if flame_scale > 0:
        mid_fx = el_x * 0.35 + wr_x * 0.65
        mid_fy = el_y * 0.35 + wr_y * 0.65
        draw_sacred_flame_cluster(c, mid_fx, mid_fy, phase=phase + 0.3, scale=flame_scale * 0.75)
        draw_sacred_flame_cluster(c, wr_x, wr_y, phase=phase, scale=flame_scale * 1.05)


def draw_hoa_kage_pose_128(c, pose):
    """Master 128x144 composite renderer for Hỏa Kage."""
    tx = pose.get('tx', 58)
    ty = pose.get('ty', 46)
    lean_dx = pose.get('lean_dx', 0)
    phase = pose.get('phase', 0.0)

    # 1. Ground shadow / dash fire trail / jump fire sparks
    draw_ground_fire_aura_128(
        c, tx, phase=phase,
        intensity=pose.get('aura_intensity', 1.0),
        dash_trail=pose.get('dash_trail', False),
        jump_sparks=pose.get('jump_sparks', False)
    )

    # 2. Back Flaming Arm (if behind torso)
    b_arm = pose['back_arm']
    if b_arm.get('layer', 'back') == 'back':
        draw_flaming_arm_128(c, b_arm['sh'][0], b_arm['sh'][1],
                             b_arm['el'][0], b_arm['el'][1],
                             b_arm['wr'][0], b_arm['wr'][1],
                             is_front=False, phase=phase + 0.5,
                             flame_scale=b_arm.get('flame', 0.95))

    # 3. Back Leg & Front Leg (masculine pink shorts + sunlit calves + black boots)
    bl = pose['back_leg']
    fl = pose['front_leg']
    draw_athletic_leg_128(c, bl['hip'][0], bl['hip'][1], bl['knee'][0], bl['knee'][1], bl['ankle'][0], bl['ankle'][1], is_front=False)
    draw_athletic_leg_128(c, fl['hip'][0], fl['hip'][1], fl['knee'][0], fl['knee'][1], fl['ankle'][0], fl['ankle'][1], is_front=True)

    # 4. Shirtless Muscular 6-Pack Torso + Pink Shorts Waist
    draw_sculpted_shirtless_torso_128(c, tx, ty, lean_dx=lean_dx)

    # 5. Handsome 3/4 Head (Wild Black Hair, NO HAT!)
    hx = pose.get('hx', tx + lean_dx + 1)
    hy = pose.get('hy', ty - 17)
    draw_head_no_hat_128(c, hx, hy, expr=pose.get('expr', 'grin'))

    # 6. Back Flaming Arm (if layered in front of torso, e.g. left hook punch)
    if b_arm.get('layer') == 'front':
        draw_flaming_arm_128(c, b_arm['sh'][0], b_arm['sh'][1],
                             b_arm['el'][0], b_arm['el'][1],
                             b_arm['wr'][0], b_arm['wr'][1],
                             is_front=False, phase=phase + 0.5,
                             flame_scale=b_arm.get('flame', 1.1))

    # 7. Front Flaming Arm
    f_arm = pose['front_arm']
    draw_flaming_arm_128(c, f_arm['sh'][0], f_arm['sh'][1],
                         f_arm['el'][0], f_arm['el'][1],
                         f_arm['wr'][0], f_arm['wr'][1],
                         is_front=True, phase=phase,
                         flame_scale=f_arm.get('flame', 1.05))
