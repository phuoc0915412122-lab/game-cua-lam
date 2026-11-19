import sys, os, math
sys.path.append(os.path.abspath('scratch'))
from pixel_canvas import PixelCanvas
from test_head import (
    draw_head_and_face,
    C_OUTLINE, C_SKIN_BASE, C_SKIN_SHADE, C_SKIN_DEEP, C_SKIN_HILIGHT,
    C_HAIR_BASE, C_HAIR_SHADE, C_HAIR_DEEP, C_HAIR_HILIGHT, C_HAIR_SHINE,
    C_ROBE_BASE, C_ROBE_SHADE, C_ROBE_DEEP, C_ROBE_HILIGHT, C_ROBE_WHITE, C_ROBE_WHITE_SHADE,
    C_GOLD_BASE, C_GOLD_SHADE, C_GOLD_HILIGHT,
    C_MINT_CORE, C_MINT_BRIGHT, C_MINT_BASE, C_MINT_SHADE, C_MINT_DEEP,
    C_BOOT_BASE, C_BOOT_SHADE, C_BOOT_HILIGHT,
    C_STAFF_WOOD, C_STAFF_WOOD_DARK, C_STAFF_WOOD_LIGHT
)

def draw_staff(c, sx, sy, angle_deg=0, length=44, orb_pulse=0, cast_glow=False):
    # Staff anchored or centered at (sx, sy) where orb / top is
    # Angle 0 means vertical pointing down, or specify angle
    # For pixel art, let's draw direct line or parametric
    rad = math.radians(angle_deg)
    dx = math.sin(rad)
    dy = math.cos(rad)
    
    # Staff shaft
    for d in range(6, length):
        px = int(sx + dx * d)
        py = int(sy + dy * d)
        c.set(px, py, C_STAFF_WOOD)
        c.set(px - 1, py, C_STAFF_WOOD_DARK)
        if d % 8 == 0: # gold band rings on staff
            c.set(px, py, C_GOLD_BASE)
            c.set(px + 1, py, C_GOLD_HILIGHT)
            
    # Bottom pommel
    bx = int(sx + dx * length)
    by = int(sy + dy * length)
    c.rect(bx - 1, by, 3, 2, C_GOLD_BASE)
    c.set(bx, by + 2, C_MINT_BASE) # small bottom crystal
    
    # Staff Headpiece (golden crescent/lotus embracing orb)
    c.rect(sx - 3, sy + 3, 7, 3, C_GOLD_BASE)
    c.line(sx - 4, sy + 4, sx - 4, sy - 1, C_GOLD_BASE)
    c.set(sx - 4, sy - 2, C_GOLD_HILIGHT)
    c.line(sx + 4, sy + 4, sx + 4, sy - 1, C_GOLD_BASE)
    c.set(sx + 4, sy - 2, C_GOLD_HILIGHT)
    c.set(sx, sy + 5, C_GOLD_SHADE)
    c.set(sx, sy + 2, C_GOLD_HILIGHT)

    # Spirit Crystal Orb
    r = 3 + (1 if orb_pulse > 0.5 else 0)
    # Outer glow
    if cast_glow or orb_pulse > 0:
        c.circle(sx, sy, r + 2, C_MINT_SHADE, fill=False)
        c.circle(sx, sy, r + 3, (110, 227, 189, 120), fill=False)
    # Orb body
    c.circle(sx, sy, r, C_MINT_BASE, fill=True)
    c.circle(sx, sy, r - 1, C_MINT_BRIGHT, fill=True)
    c.set(sx - 1, sy - 1, C_MINT_CORE) # core shine
    c.set(sx, sy - 1, C_MINT_CORE)
    c.set(sx - 1, sy, C_MINT_CORE)

def draw_flowing_hair_back(c, hx, hy, flow_x=0, flow_y=0, billow=0):
    # Long peachy locks flowing down behind back
    for i in range(16, 42):
        t = (i - 16) / 26.0
        curve_l = int(-9 - t*4 + flow_x * t*1.5 + math.sin(t*3 + billow)*2)
        curve_r = int(9 + t*4 + flow_x * t*1.5 + math.sin(t*3 + billow)*2)
        y = hy + i + int(flow_y * t)
        w = max(4, int(18 + t*8))
        c.line(hx + curve_l, y, hx + curve_r, y, C_HAIR_SHADE)
        c.line(hx + curve_l + 1, y, hx + curve_r - 1, y, C_HAIR_BASE)
        # strand highlights
        c.set(hx + curve_l + 2, y, C_HAIR_HILIGHT)
        c.set(hx + curve_r - 2, y, C_HAIR_DEEP)
    # strand tips
    c.set(hx - 12 + int(flow_x), hy + 42, C_HAIR_DEEP)
    c.set(hx - 11 + int(flow_x), hy + 43, C_HAIR_SHADE)
    c.set(hx + 12 + int(flow_x), hy + 42, C_HAIR_DEEP)
    c.set(hx + 11 + int(flow_x), hy + 43, C_HAIR_SHADE)

def draw_torso_and_robe(c, tx, ty, breath=0, twist=0):
    # Torso centered at tx, ty ~ 28 (neck) to 48 (waist/hips)
    # Neck & Choker
    c.rect(tx - 2, ty, 4, 3, C_SKIN_BASE)
    c.line(tx - 2, ty + 1, tx + 1, ty + 1, C_OUTLINE) # black velvet choker
    c.set(tx, ty + 1, C_GOLD_BASE) # choker gold pendant

    # Shoulders & Upper Chest (bare shoulders like img 1 & img 3)
    c.rect(tx - 7, ty + 3, 14, 4, C_SKIN_BASE)
    c.set(tx - 7, ty + 3, C_SKIN_HILIGHT)
    c.set(tx + 6, ty + 3, C_SKIN_HILIGHT)
    # Collarbone & cleavage shading
    c.set(tx - 1, ty + 4, C_SKIN_SHADE)
    c.set(tx, ty + 4, C_SKIN_SHADE)
    c.set(tx - 3, ty + 3, C_SKIN_SHADE)
    c.set(tx + 2, ty + 3, C_SKIN_SHADE)

    # Midnight Navy Halter / Bodice (inspired by img 1 navy top)
    b_y = ty + 5 + int(breath)
    # Bodice cup shapes
    c.rect(tx - 6, b_y, 12, 7, C_ROBE_BASE)
    c.rect(tx - 5, b_y + 1, 10, 6, C_ROBE_HILIGHT)
    c.line(tx - 6, b_y, tx + 5, b_y, C_GOLD_BASE) # gold trim on neckline
    c.set(tx - 1, b_y + 2, C_ROBE_SHADE)
    c.set(tx, b_y + 2, C_ROBE_SHADE)
    # Mint talisman gem in center of bodice
    c.rect(tx - 1, b_y + 3, 2, 2, C_MINT_BASE)
    c.set(tx, b_y + 3, C_MINT_CORE)

    # Waist & Corset
    w_y = b_y + 7
    c.rect(tx - 5, w_y, 10, 5, C_ROBE_SHADE)
    c.rect(tx - 4, w_y + 1, 8, 4, C_ROBE_BASE)
    # Gold & Mint Sash belt
    c.line(tx - 5, w_y + 4, tx + 4, w_y + 4, C_GOLD_BASE)
    c.line(tx - 5, w_y + 5, tx + 4, w_y + 5, C_MINT_BASE)
    # Floating mint sash ribbons hanging from waist
    c.line(tx + 3, w_y + 5, tx + 6, w_y + 14, C_MINT_BASE)
    c.set(tx + 7, w_y + 15, C_MINT_BRIGHT)
    c.line(tx + 4, w_y + 5, tx + 7, w_y + 14, C_MINT_SHADE)

    # Robe Skirt (splits in front, navy with white silk lining)
    s_y = w_y + 6
    for i in range(11):
        flare = int(i * 0.7)
        c.rect(tx - 5 - flare, s_y + i, 3, 1, C_ROBE_BASE)
        c.rect(tx - 5 - flare + 2, s_y + i, max(1, flare), 1, C_ROBE_WHITE)
        c.rect(tx + 3 + flare - 2, s_y + i, max(1, flare), 1, C_ROBE_WHITE)
        c.rect(tx + 3 + flare, s_y + i, 3, 1, C_ROBE_BASE)
    # Gold hem border
    c.line(tx - 12, s_y + 10, tx - 7, s_y + 10, C_GOLD_BASE)
    c.line(tx + 7, s_y + 10, tx + 12, s_y + 10, C_GOLD_BASE)

def draw_legs_idle(c, lx, ly, bob=0):
    # Thighs visible through robe split
    c.rect(lx - 4, ly, 3, 6, C_SKIN_BASE)
    c.rect(lx + 1, ly, 3, 6, C_SKIN_BASE)
    c.set(lx - 3, ly + 2, C_SKIN_SHADE)
    c.set(lx + 2, ly + 2, C_SKIN_SHADE)

    # Thigh-high boots (knees at ly + 6)
    # Left boot
    c.line(lx - 5, ly + 6, lx - 1, ly + 6, C_GOLD_BASE) # gold cuff band
    c.rect(lx - 4, ly + 7, 3, 11, C_BOOT_BASE)
    c.rect(lx - 4, ly + 8, 1, 9, C_BOOT_HILIGHT)
    c.rect(lx - 5, ly + 18, 4, 2, C_BOOT_BASE) # shoe foot planted
    c.set(lx - 5, ly + 19, C_BOOT_SHADE)

    # Right boot
    c.line(lx + 1, ly + 6, lx + 5, ly + 6, C_GOLD_BASE) # gold cuff band
    c.rect(lx + 1, ly + 7, 3, 11, C_BOOT_BASE)
    c.rect(lx + 3, ly + 8, 1, 9, C_BOOT_HILIGHT)
    c.rect(lx + 1, ly + 18, 5, 2, C_BOOT_BASE) # shoe foot planted
    c.set(lx + 5, ly + 19, C_BOOT_SHADE)

print('Drawing routines loaded.')
