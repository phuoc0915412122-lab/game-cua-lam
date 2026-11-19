import os, sys, math
sys.path.append(os.path.abspath('scratch'))
from pixel_canvas import PixelCanvas

# Palette from Mage concept sheet & anime beauty aesthetics
C_OUTLINE = '#13111c'
C_SKIN_HILIGHT = '#fff6ee'
C_SKIN_BASE = '#fde5d7'
C_SKIN_SHADE = '#f7c2aa'
C_SKIN_DEEP = '#d88f72'
C_SKIN_CREVICE = '#a85b40'
C_BLUSH = '#ff9dae'

C_EYE_WHITE = '#ffffff'
C_EYE_PUPIL = '#400c24'
C_EYE_IRIS_DEEP = '#9c1c58'
C_EYE_IRIS = '#e04882'
C_EYE_IRIS_LIGHT = '#ff7bb2'
C_EYE_HILIGHT = '#ffffff'

C_HAIR_SHINE = '#ffffff'
C_HAIR_BASE = '#e8ecf4'
C_HAIR_MID = '#d2dbee'
C_HAIR_SHADE = '#b5c2d9'
C_HAIR_DEEP = '#8393af'
C_HAIR_HORN = '#241e2e'

C_CAPE_WHITE = '#ffffff'
C_CAPE_BASE = '#f0f3f8'
C_CAPE_MID = '#d8e0ed'
C_CAPE_SHADE = '#b8c5d9'
C_CAPE_DEEP = '#8f9fb8'

C_RUBY_HILIGHT = '#ff6b84'
C_RUBY_BASE = '#d8203c'
C_RUBY_SHADE = '#7a0d1e'

C_SUIT_BASE = '#1e1b26'
C_SUIT_SHADE = '#121018'
C_SUIT_DEEP = '#0a080f'
C_SUIT_HILIGHT = '#3e384f'
C_SUIT_SHEEN = '#62597d'

C_GOLD_BASE = '#f5c442'
C_GOLD_SHADE = '#9e7317'
C_GOLD_HILIGHT = '#fff099'

C_STOCKING_LIGHT = (90, 75, 110, 160)
C_STOCKING_BASE = (42, 34, 52, 215)
C_STOCKING_SHADE = (24, 18, 30, 245)

C_BOOT_BASE = '#14121b'
C_BOOT_SHADE = '#0a0910'
C_BOOT_HILIGHT = '#363045'

C_ORB_CORE = '#ffffff'
C_ORB_BRIGHT = '#f4b8ff'
C_ORB_BASE = '#c866f5'
C_ORB_SHADE = '#7422b8'
C_ORB_GLOW = (200, 100, 245, 90)

C_MAGIC_CYAN = '#70f3ff'
C_MAGIC_PINK = '#ff71ce'

def draw_limb_segment(c, x0, y0, x1, y1, r0, r1, color, shade_color=None, hi_color=None):
    """Draws a smooth, volumetric 3D limb at 128x144 resolution."""
    dx = x1 - x0
    dy = y1 - y0
    dist = math.hypot(dx, dy)
    steps = max(int(dist * 2.5), 1)
    for s in range(steps + 1):
        t = s / float(steps)
        cx = x0 + dx * t
        cy = y0 + dy * t
        cr = r0 + (r1 - r0) * t
        ir = int(math.ceil(cr))
        for iy in range(-ir, ir + 1):
            for ix in range(-ir, ir + 1):
                d = math.hypot(ix, iy)
                if d <= cr:
                    px = int(round(cx + ix))
                    py = int(round(cy + iy))
                    col = color
                    if shade_color and (ix < -cr * 0.35 or iy > cr * 0.5):
                        col = shade_color
                    elif hi_color and (ix > cr * 0.35 and iy < cr * 0.2):
                        col = hi_color
                    c.set(px, py, col)

def draw_staff_128(c, sx, sy, angle_deg=0, length=88, orb_pulse=0, cast_swirl=False):
    rad = math.radians(angle_deg)
    dx = math.sin(rad)
    dy = math.cos(rad)

    # 3px-thick golden shaft with edge shading
    for d in range(14, length):
        px = sx + dx * d
        py = sy + dy * d
        c.circle(px, py, 1.6, C_GOLD_BASE, fill=True)
        c.set(int(px - 1), int(py), C_GOLD_SHADE)
        if d % 16 == 0:
            c.circle(px, py, 2.2, C_GOLD_HILIGHT, fill=True)

    # Bottom Pommel
    bx = sx + dx * length
    by = sy + dy * length
    c.rect(int(bx - 3), int(by), 7, 4, C_GOLD_BASE)
    c.circle(bx, by + 5, 2.5, C_ORB_BASE, fill=True)
    c.set(int(bx), int(by + 7), C_ORB_BRIGHT)

    # Golden Ring Headpiece (outer radius ~11, inner ~7)
    for ay in range(-12, 13):
        for ax in range(-12, 13):
            d2 = ax*ax + ay*ay
            if 48 <= d2 <= 132:
                if 72 <= d2 <= 132:
                    c.set(int(sx + ax), int(sy + ay), C_GOLD_BASE)
                else:
                    c.set(int(sx + ax), int(sy + ay), C_ORB_SHADE)
    c.set(int(sx - 8), int(sy - 7), C_GOLD_HILIGHT)
    c.set(int(sx - 7), int(sy - 8), C_GOLD_HILIGHT)
    c.set(int(sx + 8), int(sy + 7), C_GOLD_SHADE)
    c.rect(int(sx - 4), int(sy + 10), 9, 5, C_GOLD_BASE)

    # Glowing Purple Orb (radius ~5.5)
    r = 5.5 + (1.2 if orb_pulse > 0.5 else 0)
    if cast_swirl or orb_pulse > 0:
        c.circle(sx, sy, r + 6, C_ORB_GLOW, fill=False)
        c.circle(sx, sy, r + 4, (200, 100, 245, 120), fill=False)
    c.circle(sx, sy, r, C_ORB_BASE, fill=True)
    c.circle(sx, sy, r - 1.8, C_ORB_BRIGHT, fill=True)
    c.circle(sx - 1.5, sy - 1.5, 2.0, C_ORB_CORE, fill=True)

    # Swirling pastel magic arcs from concept sheet
    if cast_swirl:
        for rad_r in [14, 20]:
            c.circle(sx, sy, rad_r, (112, 243, 255, 130), fill=False)
            c.circle(sx, sy, rad_r + 3, (255, 113, 206, 120), fill=False)
        c.set(int(sx - 12), int(sy - 11), C_MAGIC_CYAN)
        c.set(int(sx + 14), int(sy + 10), C_MAGIC_PINK)
        c.set(int(sx + 16), int(sy - 8), C_ORB_CORE)

def draw_head_128(c, hx, hy, expr='normal', mouth='smirk'):
    # Silver hair mass in back
    c.rect(hx - 20, hy - 8, 36, 32, C_HAIR_DEEP)
    c.rect(hx - 18, hy - 6, 34, 34, C_HAIR_SHADE)
    c.rect(hx - 24, hy + 4, 10, 36, C_HAIR_SHADE)

    # Dark hair horn / accessory from concept
    c.rect(hx - 7, hy - 14, 4, 9, C_HAIR_HORN)
    c.set(hx - 7, hy - 15, C_HAIR_SHADE)
    c.rect(hx + 7, hy - 14, 4, 9, C_HAIR_HORN)
    c.set(hx + 8, hy - 15, C_HAIR_SHADE)

    # 3/4 Face contour (delicate anime beauty profile)
    c.rect(hx - 11, hy - 2, 24, 20, C_SKIN_BASE)
    c.rect(hx - 8, hy + 18, 20, 6, C_SKIN_BASE)
    c.rect(hx - 4, hy + 24, 14, 4, C_SKIN_BASE)
    c.rect(hx, hy + 28, 6, 2, C_SKIN_BASE) # chin

    # Jawline shading
    c.line(hx - 7, hy + 20, hx - 4, hy + 24, C_SKIN_SHADE)
    c.line(hx + 12, hy + 18, hx + 8, hy + 24, C_SKIN_SHADE)
    c.line(hx - 4, hy + 25, hx + 6, hy + 25, C_SKIN_SHADE)
    c.rect(hx, hy + 28, 6, 2, C_SKIN_DEEP)

    # Silvery bangs & framing hair
    c.rect(hx - 14, hy - 8, 30, 8, C_HAIR_BASE)
    c.rect(hx - 12, hy - 9, 26, 4, C_HAIR_SHINE)
    # Bang strands
    c.rect(hx - 12, hy, 6, 12, C_HAIR_BASE)
    c.rect(hx - 4, hy, 7, 13, C_HAIR_BASE)
    c.rect(hx + 5, hy, 6, 16, C_HAIR_BASE)
    c.rect(hx - 16, hy + 2, 5, 28, C_HAIR_BASE)

    # Anime Eyes (High-res 128x144 detail!)
    # Left eye (further back)
    c.rect(hx - 7, hy + 8, 6, 7, C_EYE_WHITE)
    c.rect(hx - 5, hy + 9, 4, 6, C_EYE_IRIS)
    c.rect(hx - 5, hy + 11, 4, 3, C_EYE_PUPIL)
    c.set(hx - 6, hy + 9, C_EYE_HILIGHT)
    c.line(hx - 8, hy + 7, hx - 1, hy + 7, C_OUTLINE)
    c.set(hx - 8, hy + 6, C_OUTLINE)

    # Right eye (closer, full anime eye with gradient)
    c.rect(hx + 4, hy + 8, 7, 7, C_EYE_WHITE)
    c.rect(hx + 6, hy + 9, 5, 6, C_EYE_IRIS)
    c.rect(hx + 6, hy + 11, 5, 3, C_EYE_PUPIL)
    c.set(hx + 7, hy + 13, C_EYE_IRIS_LIGHT)
    c.set(hx + 5, hy + 9, C_EYE_HILIGHT)
    c.set(hx + 8, hy + 10, C_EYE_HILIGHT)
    c.line(hx + 3, hy + 7, hx + 11, hy + 7, C_OUTLINE)
    c.set(hx + 11, hy + 6, C_OUTLINE)

    # Delicate blush & cute nose
    c.rect(hx - 6, hy + 15, 4, 2, C_BLUSH)
    c.rect(hx + 7, hy + 15, 5, 2, C_BLUSH)
    c.set(hx + 4, hy + 15, C_SKIN_SHADE)

    # Glossy lips
    if mouth == 'smirk':
        c.rect(hx + 2, hy + 21, 5, 2, C_RUBY_BASE)
        c.set(hx + 4, hy + 20, C_RUBY_HILIGHT)
    elif mouth == 'open':
        c.rect(hx + 1, hy + 20, 6, 4, C_RUBY_BASE)
        c.rect(hx + 2, hy + 21, 4, 2, C_SKIN_DEEP)
    else:
        c.rect(hx + 2, hy + 21, 4, 2, C_RUBY_BASE)

def draw_white_cape_128(c, tx, ty, billow_dx=0, billow_w=0):
    """Draws the luxurious white cape draped over back, billowing behind her."""
    for cy in range(ty + 4, ty + 76):
        t = (cy - (ty + 4)) / 72.0
        left_e = int(tx - 20 - t * (16 + billow_w) + billow_dx * t)
        right_e = int(tx - 6 - t * 4)
        c.line(left_e, cy, right_e, cy, C_CAPE_SHADE)
        c.line(left_e + 2, cy, right_e - 1, cy, C_CAPE_BASE)
        c.line(left_e + 4, cy, right_e - 2, cy, C_CAPE_WHITE)

def draw_beauty_queen_body_128(c, tx, ty, breath=0):
    """
    Renders the Hoa Hậu / Pageant Queen proportioned body (1.67m, 58kg):
    - V1 ~100cm: very full, voluptuous, forward-projecting bust with deep cleavage and sweetheart gold trim
    - V2 ~60cm: slender, flat, corseted waist with double-breasted gold buttons
    - V3 ~90cm: shapely, curvy hips and round derriere (S-curve profile)
    """
    # 1. Neck & Ruby Brooch
    c.rect(tx - 3, ty, 10, 8, C_SKIN_BASE)
    c.rect(tx - 6, ty + 4, 14, 4, C_CAPE_BASE)
    # Gold setting + Ruby Brooch
    c.circle(tx, ty + 5, 4.0, C_GOLD_BASE, fill=True)
    c.circle(tx, ty + 5, 2.5, C_RUBY_BASE, fill=True)
    c.set(tx, ty + 4, C_RUBY_HILIGHT)

    # 2. Shoulders & Upper Chest (Exposed bust)
    c.rect(tx - 12, ty + 8, 30, 6, C_SKIN_BASE)
    c.set(tx - 12, ty + 8, C_SKIN_HILIGHT)
    c.set(tx + 16, ty + 9, C_SKIN_HILIGHT)
    # Delicate clavicles
    c.line(tx - 5, ty + 10, tx - 1, ty + 10, C_SKIN_SHADE)
    c.line(tx + 4, ty + 10, tx + 9, ty + 10, C_SKIN_SHADE)

    # 3. VÒNG 1 (~100cm) - HUGE, VOLUPTUOUS, SHAPELY BUST (Natural 3D fullness!)
    b_y = ty + 14 + int(breath)

    # Left Breast dome (further back in 3/4)
    c.circle(tx - 5, b_y + 6, 8.0, C_SKIN_BASE, fill=True)
    c.circle(tx - 5, b_y + 3, 5.0, C_SKIN_HILIGHT, fill=True)

    # Right Breast dome (PROMINENT FORWARD PROJECTION in 3/4 profile like Image 4!)
    c.circle(tx + 9, b_y + 6, 9.5, C_SKIN_BASE, fill=True)
    c.circle(tx + 9, b_y + 3, 6.0, C_SKIN_HILIGHT, fill=True)
    # Extra side projection curve
    c.rect(tx + 16, b_y + 4, 3, 5, C_SKIN_BASE)
    c.rect(tx + 17, b_y + 5, 2, 4, C_SKIN_BASE)

    # Deep 3/4 Cleavage shadow
    c.line(tx + 2, b_y, tx + 2, b_y + 8, C_SKIN_DEEP)
    c.line(tx + 2, b_y + 3, tx + 2, b_y + 7, C_SKIN_CREVICE)

    # Corset with Gold Sweetheart Trim embracing breasts
    c.line(tx - 14, b_y + 6, tx + 1, b_y + 8, C_GOLD_BASE)
    c.line(tx + 2, b_y + 8, tx + 19, b_y + 5, C_GOLD_BASE)
    c.set(tx + 19, b_y + 5, C_GOLD_HILIGHT)
    c.set(tx + 2, b_y + 8, C_GOLD_HILIGHT)

    c.rect(tx - 14, b_y + 8, 14, 8, C_SUIT_BASE)
    c.rect(tx + 1, b_y + 8, 19, 8, C_SUIT_BASE)
    c.rect(tx + 17, b_y + 8, 3, 6, C_SUIT_BASE)

    # Gloss sheen on rounded bust
    c.line(tx - 7, b_y + 10, tx - 3, b_y + 10, C_SUIT_SHEEN)
    c.line(tx + 8, b_y + 10, tx + 14, b_y + 10, C_SUIT_SHEEN)
    c.line(tx + 9, b_y + 11, tx + 13, b_y + 11, C_SUIT_HILIGHT)

    # 4. VÒNG 2 (~60cm) - SLENDER, TIGHT CORSET WAIST (Beauty Queen 58kg!)
    w_y = b_y + 15
    c.rect(tx - 10, w_y, 22, 5, C_SUIT_BASE)
    c.rect(tx - 8, w_y + 5, 18, 8, C_SUIT_BASE)
    c.line(tx - 8, w_y + 5, tx - 8, w_y + 12, C_SUIT_SHADE)
    c.line(tx + 10, w_y + 5, tx + 10, w_y + 12, C_SUIT_SHADE)

    # Double-breasted 6 Gold Buttons (from concept sheet)
    c.circle(tx - 2, w_y + 2, 1.6, C_GOLD_BASE, fill=True)
    c.circle(tx + 4, w_y + 2, 1.6, C_GOLD_BASE, fill=True)
    c.circle(tx - 2, w_y + 6, 1.6, C_GOLD_BASE, fill=True)
    c.circle(tx + 4, w_y + 6, 1.6, C_GOLD_BASE, fill=True)
    c.circle(tx - 2, w_y + 10, 1.6, C_GOLD_BASE, fill=True)
    c.circle(tx + 4, w_y + 10, 1.6, C_GOLD_BASE, fill=True)

    # 5. VÒNG 3 (~90cm) - CURVACEOUS HIPS & ROUND REAR (S-curve posture like Image 4!)
    h_y = w_y + 13
    c.circle(tx - 3, h_y + 5, 15.0, C_SUIT_BASE, fill=True)
    c.rect(tx - 14, h_y + 3, 32, 8, C_SUIT_BASE)
    # High-cut leg openings showing bare thigh skin
    c.rect(tx - 14, h_y + 6, 4, 6, C_SKIN_BASE)
    c.rect(tx + 15, h_y + 6, 4, 6, C_SKIN_BASE)
    # Hip gloss
    c.line(tx - 9, h_y + 5, tx - 4, h_y + 5, C_SUIT_HILIGHT)
    c.line(tx + 6, h_y + 5, tx + 12, h_y + 5, C_SUIT_HILIGHT)

def draw_toned_leg_128(c, x_hip, y_hip, x_knee, y_knee, x_ankle, y_ankle, foot_dx=4):
    """
    Draws a long, slender yet toned and shapely leg (Hoa hậu 1m67, 58kg):
    - Thigh radius: 9.5 tapering to 7.0 -> thickness 19 to 14px!
    - Calf radius: 7.0 swelling to 7.5, tapering to 5.0 -> thickness 15 to 10px!
    - Sheer stockings with gold garter
    - High-heeled boot with pointed toe
    """
    # 1. Thigh
    draw_limb_segment(c, x_hip, y_hip, x_knee, y_knee, 9.5, 7.0, C_STOCKING_BASE, C_STOCKING_SHADE, C_STOCKING_LIGHT)

    # Ornate Gold Garter Band
    gx = x_hip
    gy = y_hip + 2
    c.line(int(gx - 7), int(gy), int(gx + 7), int(gy), C_GOLD_BASE)
    c.line(int(gx - 6), int(gy + 1), int(gx + 6), int(gy + 1), C_GOLD_SHADE)
    c.set(int(gx + 3), int(gy), C_GOLD_HILIGHT)

    # 2. Round Kneecap
    c.circle(x_knee, y_knee, 6.8, C_STOCKING_BASE, fill=True)
    c.set(int(x_knee + 1), int(y_knee), C_STOCKING_LIGHT)

    # 3. Toned Shapely Calf (graceful curve)
    mid_calf_x = (x_knee * 0.4 + x_ankle * 0.6) - 2.5
    mid_calf_y = (y_knee * 0.4 + y_ankle * 0.6)
    draw_limb_segment(c, x_knee, y_knee, mid_calf_x, mid_calf_y, 7.0, 7.6, C_BOOT_BASE, C_BOOT_SHADE, C_BOOT_HILIGHT)
    draw_limb_segment(c, mid_calf_x, mid_calf_y, x_ankle, y_ankle, 7.6, 5.0, C_BOOT_BASE, C_BOOT_SHADE, C_BOOT_HILIGHT)

    # 4. High-heeled Boot
    fx = int(x_ankle)
    fy = int(y_ankle)
    c.rect(fx - 4, fy, 9, 5, C_BOOT_BASE)
    c.rect(fx - 2 + foot_dx, fy + 4, 10, 4, C_BOOT_BASE)
    # Heel tap
    c.line(fx - 3, fy + 2, fx - 3, fy + 8, C_GOLD_BASE)
    c.set(fx - 3, fy + 8, C_GOLD_SHADE)

def draw_toned_arm_128(c, x_sh, y_sh, x_el, y_el, x_wr, y_wr, color=C_SKIN_BASE, shade=C_SKIN_SHADE):
    """Draws a slender yet toned female arm (radius 5.0 upper, 4.0 forearm -> 10px and 8px thick)."""
    draw_limb_segment(c, x_sh, y_sh, x_el, y_el, 5.2, 4.2, color, shade, C_SKIN_HILIGHT)
    draw_limb_segment(c, x_el, y_el, x_wr, y_wr, 4.2, 3.4, color, shade, C_SKIN_HILIGHT)
    c.circle(x_wr, y_wr, 4.0, color, fill=True)
    c.set(int(x_wr), int(y_wr), C_SKIN_HILIGHT)

print("design_128_summoner ready.")
