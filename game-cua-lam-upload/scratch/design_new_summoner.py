import sys, os, math
sys.path.append(os.path.abspath('scratch'))
from pixel_canvas import PixelCanvas

# Palette
C_OUTLINE = '#110f1a'
C_SKIN_HILIGHT = '#fff5ee'
C_SKIN_BASE = '#fde3d4'
C_SKIN_SHADE = '#f2b8a0'
C_SKIN_DEEP = '#d9856c'
C_SKIN_CREVICE = '#b85e45'
C_BLUSH = '#ff9aa8'

C_EYE_WHITE = '#ffffff'
C_EYE_PUPIL = '#3b0d28'
C_EYE_IRIS = '#d83a8b'
C_EYE_HILIGHT = '#ffffff'

C_HAIR_SHINE = '#ffffff'
C_HAIR_BASE = '#e8ecf4'
C_HAIR_SHADE = '#b8c5de'
C_HAIR_DEEP = '#7a8ba8'
C_HAIR_ACCENT = '#d83a8b'

# Bodysuit (like image 4: tight corset / bunny-style bodysuit with white collar, bowtie, deep neckline)
C_COLLAR = '#f8f9fc'
C_COLLAR_SHADE = '#cbd2e0'
C_BOWTIE = '#c02640'
C_BOWTIE_HILIGHT = '#ff5470'

C_SUIT_BASE = '#1e1c2b'
C_SUIT_SHADE = '#12111c'
C_SUIT_HILIGHT = '#45405e'
C_SUIT_SHEEN = '#6e6794'

C_STOCKING = (30, 24, 42, 210)
C_STOCKING_SHADE = (18, 14, 26, 235)
C_BOOT_BASE = '#151320'
C_BOOT_SHADE = '#0d0c14'
C_BOOT_HILIGHT = '#3b3652'

C_GOLD_BASE = '#f5c542'
C_GOLD_SHADE = '#9e7317'
C_GOLD_HILIGHT = '#fff099'

C_ORB_CORE = '#ffffff'
C_ORB_BRIGHT = '#f093fb'
C_ORB_BASE = '#bd34e8'
C_ORB_SHADE = '#6a1b9a'
C_ORB_GLOW = (220, 100, 255, 90)

C_MAGIC_CYAN = '#70f3ff'
C_MAGIC_PINK = '#ff71ce'

def draw_staff(c, sx, sy, angle_deg=0, length=44, orb_pulse=0, cast_glow=False):
    rad = math.radians(angle_deg)
    dx = math.sin(rad)
    dy = math.cos(rad)
    
    # Shaft
    for d in range(6, length):
        px = int(sx + dx * d)
        py = int(sy + dy * d)
        c.set(px, py, C_GOLD_BASE)
        c.set(px - 1, py, C_GOLD_SHADE)
        if d % 9 == 0:
            c.set(px, py, C_GOLD_HILIGHT)
            c.set(px + 1, py, C_SUIT_BASE)
            
    # Bottom pommel
    bx = int(sx + dx * length)
    by = int(sy + dy * length)
    c.rect(bx - 1, by, 3, 3, C_GOLD_BASE)
    c.set(bx, by + 3, C_ORB_BRIGHT)
    
    # Staff Headpiece: ornate gilded crescent with summoner wings
    c.rect(sx - 4, sy + 3, 9, 3, C_GOLD_BASE)
    c.line(sx - 5, sy + 4, sx - 5, sy - 2, C_GOLD_BASE)
    c.set(sx - 5, sy - 3, C_GOLD_HILIGHT)
    c.line(sx + 5, sy + 4, sx + 5, sy - 2, C_GOLD_BASE)
    c.set(sx + 5, sy - 3, C_GOLD_HILIGHT)
    c.set(sx, sy + 5, C_GOLD_SHADE)
    c.set(sx, sy + 2, C_GOLD_HILIGHT)

    # Summoner Crystal Orb
    r = 3 + (1 if orb_pulse > 0.5 else 0)
    if cast_glow or orb_pulse > 0:
        c.circle(sx, sy, r + 3, C_ORB_GLOW, fill=False)
        c.circle(sx, sy, r + 2, C_ORB_SHADE, fill=False)
    c.circle(sx, sy, r, C_ORB_BASE, fill=True)
    c.circle(sx, sy, r - 1, C_ORB_BRIGHT, fill=True)
    c.set(sx - 1, sy - 1, C_ORB_CORE)
    c.set(sx, sy - 1, C_ORB_CORE)
    c.set(sx - 1, sy, C_ORB_CORE)

def draw_female_head_and_face(c, hx, hy, expr='normal', mouth='smirk', dir_look=1):
    # Pure human girl head: NO HORNS, human cute ears, silver/white hair
    # Back hair base mass
    c.rect(hx - 9, hy - 4, 18, 16, C_HAIR_DEEP)
    c.rect(hx - 8, hy - 3, 16, 17, C_HAIR_SHADE)
    c.rect(hx - 10, hy + 2, 4, 15, C_HAIR_SHADE)
    c.rect(hx + 7, hy + 2, 4, 15, C_HAIR_SHADE)
    
    # Bunny-ear headband or cute hair accessory (like image 4 headband)
    c.rect(hx - 6, hy - 8, 2, 5, C_SUIT_BASE)
    c.set(hx - 6, hy - 9, C_SUIT_HILIGHT)
    c.set(hx - 5, hy - 8, C_BOWTIE)
    c.rect(hx + 4, hy - 8, 2, 5, C_SUIT_BASE)
    c.set(hx + 5, hy - 9, C_SUIT_HILIGHT)
    c.set(hx + 4, hy - 8, C_BOWTIE)

    # Face base
    c.rect(hx - 6, hy - 1, 13, 11, C_SKIN_BASE)
    c.rect(hx - 5, hy + 10, 11, 3, C_SKIN_BASE)
    c.rect(hx - 3, hy + 13, 7, 2, C_SKIN_BASE)
    c.rect(hx - 1, hy + 15, 3, 1, C_SKIN_BASE) # chin tip

    # Jaw shading
    c.line(hx - 5, hy + 11, hx - 3, hy + 13, C_SKIN_SHADE)
    c.line(hx + 4, hy + 11, hx + 2, hy + 13, C_SKIN_SHADE)
    c.line(hx - 3, hy + 14, hx + 2, hy + 14, C_SKIN_SHADE)
    c.rect(hx - 1, hy + 15, 3, 1, C_SKIN_DEEP)

    # Human ears with golden droplet earrings
    c.rect(hx - 7, hy + 4, 2, 4, C_SKIN_BASE)
    c.set(hx - 7, hy + 6, C_SKIN_SHADE)
    c.set(hx - 7, hy + 8, C_GOLD_BASE) # earring
    c.rect(hx + 6, hy + 4, 2, 4, C_SKIN_BASE)
    c.set(hx + 6, hy + 6, C_SKIN_SHADE)
    c.set(hx + 6, hy + 8, C_GOLD_BASE)

    # Cute bangs & hair framing face (silvery white with gloss)
    c.rect(hx - 7, hy - 4, 15, 4, C_HAIR_BASE)
    c.rect(hx - 6, hy - 5, 13, 2, C_HAIR_SHINE)
    # Bang strands
    c.rect(hx - 6, hy, 3, 6, C_HAIR_BASE)
    c.set(hx - 5, hy + 6, C_HAIR_SHADE)
    c.rect(hx - 2, hy, 4, 5, C_HAIR_BASE)
    c.set(hx - 1, hy + 5, C_HAIR_SHADE)
    c.rect(hx + 3, hy, 4, 7, C_HAIR_BASE)
    c.set(hx + 4, hy + 7, C_HAIR_SHADE)
    # Side locks
    c.rect(hx - 8, hy + 1, 2, 14, C_HAIR_BASE)
    c.set(hx - 8, hy + 15, C_HAIR_SHADE)
    c.rect(hx + 6, hy + 1, 2, 14, C_HAIR_BASE)
    c.set(hx + 6, hy + 15, C_HAIR_SHADE)

    # Eyes: big, captivating sorceress eyes
    # Left eye
    c.rect(hx - 5, hy + 4, 3, 4, C_EYE_WHITE)
    c.rect(hx - 4, hy + 5, 2, 3, C_EYE_IRIS)
    c.set(hx - 4, hy + 6, C_EYE_PUPIL)
    c.set(hx - 5, hy + 4, C_EYE_HILIGHT)
    c.line(hx - 5, hy + 3, hx - 2, hy + 3, C_OUTLINE) # eyelashes
    # Right eye
    c.rect(hx + 1, hy + 4, 3, 4, C_EYE_WHITE)
    c.rect(hx + 2, hy + 5, 2, 3, C_EYE_IRIS)
    c.set(hx + 2, hy + 6, C_EYE_PUPIL)
    c.set(hx + 1, hy + 4, C_EYE_HILIGHT)
    c.line(hx + 1, hy + 3, hx + 4, hy + 3, C_OUTLINE)

    # Cheeks / Blush
    c.set(hx - 4, hy + 8, C_BLUSH)
    c.set(hx - 5, hy + 8, C_BLUSH)
    c.set(hx + 3, hy + 8, C_BLUSH)
    c.set(hx + 4, hy + 8, C_BLUSH)

    # Small cute nose
    c.set(hx, hy + 8, C_SKIN_SHADE)

    # Mouth
    if mouth == 'smirk':
        c.set(hx, hy + 11, C_BOWTIE)
        c.set(hx + 1, hy + 10, C_BOWTIE_HILIGHT)
    elif mouth == 'open':
        c.rect(hx - 1, hy + 10, 3, 2, C_BOWTIE)
        c.set(hx, hy + 11, C_SKIN_DEEP)
    elif mouth == 'smile':
        c.line(hx - 1, hy + 11, hx + 2, hy + 11, C_BOWTIE)
        c.set(hx - 1, hy + 10, C_BOWTIE_HILIGHT)
        c.set(hx + 2, hy + 10, C_BOWTIE_HILIGHT)
    else:
        c.rect(hx, hy + 11, 2, 1, C_BOWTIE)

def draw_flowing_hair_back(c, hx, hy, flow_x=0, flow_y=0, billow=0):
    # Long gorgeous silver locks cascading behind back
    for i in range(15, 44):
        t = (i - 15) / 29.0
        curve_l = int(-9 - t*4 + flow_x * t*1.6 + math.sin(t*3 + billow)*2)
        curve_r = int(9 + t*4 + flow_x * t*1.6 + math.sin(t*3 + billow)*2)
        y = hy + i + int(flow_y * t)
        c.line(hx + curve_l, y, hx + curve_r, y, C_HAIR_SHADE)
        c.line(hx + curve_l + 1, y, hx + curve_r - 1, y, C_HAIR_BASE)
        c.set(hx + curve_l + 2, y, C_HAIR_SHINE)
        c.set(hx + curve_r - 2, y, C_HAIR_DEEP)
    c.set(hx - 12 + int(flow_x), hy + 44, C_HAIR_DEEP)
    c.set(hx + 12 + int(flow_x), hy + 44, C_HAIR_DEEP)

def draw_hourglass_body(c, tx, ty, breath=0, leg_pose='idle', leg_arg=1):
    # Proportions:
    # Bust: ~100 (wide, voluptuous 16-17px wide across breasts, deep visible cleavage, exposed bust)
    # Waist: ~60 (slender, 8-9px wide corseted midriff)
    # Hips: ~90 (gracefully curves out to 15-16px wide, shapely high-cut bodysuit)
    
    # 1. Neck with Collar & Bowtie (inspired by image 4)
    c.rect(tx - 2, ty, 5, 4, C_SKIN_BASE)
    # White collar
    c.rect(tx - 3, ty + 2, 7, 2, C_COLLAR)
    c.set(tx - 3, ty + 3, C_COLLAR_SHADE)
    c.set(tx + 3, ty + 3, C_COLLAR_SHADE)
    # Red ribbon / bowtie at throat
    c.rect(tx - 1, ty + 3, 3, 2, C_BOWTIE)
    c.set(tx, ty + 3, C_BOWTIE_HILIGHT)
    c.set(tx - 2, ty + 4, C_BOWTIE)
    c.set(tx + 2, ty + 4, C_BOWTIE)

    # 2. Bare Shoulders & Upper Chest (Hở vòng 1 - exposed bust)
    # Wide feminine shoulders
    c.rect(tx - 8, ty + 4, 17, 3, C_SKIN_BASE)
    c.set(tx - 8, ty + 4, C_SKIN_HILIGHT)
    c.set(tx + 8, ty + 4, C_SKIN_HILIGHT)
    # Delicate collarbones
    c.set(tx - 4, ty + 5, C_SKIN_SHADE)
    c.set(tx - 3, ty + 5, C_SKIN_SHADE)
    c.set(tx + 3, ty + 5, C_SKIN_SHADE)
    c.set(tx + 4, ty + 5, C_SKIN_SHADE)

    # 3. VÒNG 1 (~100) - Large, voluptuous, beautifully rounded bust
    # Bust extends from y = ty + 7 to ty + 15
    # Width is 17px (-8 to +8)
    b_y = ty + 7 + int(breath)
    
    # Bare upper breasts (skin) with deep cleavage crevice
    # Left breast upper dome
    c.rect(tx - 8, b_y, 7, 3, C_SKIN_BASE)
    c.set(tx - 6, b_y, C_SKIN_HILIGHT)
    c.set(tx - 5, b_y + 1, C_SKIN_HILIGHT)
    # Right breast upper dome
    c.rect(tx + 1, b_y, 7, 3, C_SKIN_BASE)
    c.set(tx + 5, b_y, C_SKIN_HILIGHT)
    c.set(tx + 4, b_y + 1, C_SKIN_HILIGHT)
    
    # Deep cleavage shadow down center
    c.line(tx, b_y, tx, b_y + 4, C_SKIN_DEEP)
    c.set(tx, b_y + 2, C_SKIN_CREVICE)
    c.set(tx, b_y + 3, C_SKIN_CREVICE)
    
    # Tight corset cups embracing the lower & side curves of bust (Image 4 sweetheart neckline)
    # Sweetheart neckline curves dipping down in center
    c.rect(tx - 8, b_y + 3, 2, 4, C_SUIT_BASE) # left cup outer edge
    c.rect(tx + 7, b_y + 3, 2, 4, C_SUIT_BASE) # right cup outer edge
    c.rect(tx - 7, b_y + 4, 6, 3, C_SUIT_BASE) # left cup bottom
    c.rect(tx + 1, b_y + 4, 6, 3, C_SUIT_BASE) # right cup bottom
    
    # Highlights & corset sheen on breast curves
    c.set(tx - 5, b_y + 5, C_SUIT_SHEEN)
    c.set(tx - 4, b_y + 5, C_SUIT_HILIGHT)
    c.set(tx + 4, b_y + 5, C_SUIT_SHEEN)
    c.set(tx + 3, b_y + 5, C_SUIT_HILIGHT)
    # Golden corset rim accent
    c.set(tx - 8, b_y + 3, C_GOLD_BASE)
    c.set(tx + 8, b_y + 3, C_GOLD_BASE)
    c.set(tx, b_y + 4, C_GOLD_BASE)

    # 4. VÒNG 2 (~60) - Slender, tight hourglass waistline
    # Tapers sharply down from width 17 to width 9 (-4 to +4) at waist
    w_y = b_y + 7
    # Midriff transition
    c.rect(tx - 6, w_y, 13, 2, C_SUIT_BASE)
    c.line(tx - 6, w_y, tx - 6, w_y + 1, C_SUIT_SHADE)
    c.line(tx + 6, w_y, tx + 6, w_y + 1, C_SUIT_SHADE)
    # Narrow waist proper (width = 9px)
    c.rect(tx - 4, w_y + 2, 9, 3, C_SUIT_BASE)
    c.line(tx - 4, w_y + 2, tx - 4, w_y + 4, C_SUIT_SHADE)
    c.line(tx + 4, w_y + 2, tx + 4, w_y + 4, C_SUIT_SHADE)
    # Vertical corset boning lines for slender slimming effect
    c.line(tx - 2, w_y, tx - 2, w_y + 4, C_SUIT_HILIGHT)
    c.line(tx + 2, w_y, tx + 2, w_y + 4, C_SUIT_HILIGHT)
    c.line(tx, w_y + 1, tx, w_y + 4, C_SUIT_SHEEN)

    # 5. VÒNG 3 (~90) - Curvaceous hips widening out (width = 15-16px)
    h_y = w_y + 5
    # High-cut bodysuit hip flair
    c.rect(tx - 6, h_y, 13, 2, C_SUIT_BASE)
    c.rect(tx - 7, h_y + 2, 15, 3, C_SUIT_BASE)
    # High-leg cut line showing side hips/thigh skin before stockings
    c.set(tx - 7, h_y + 3, C_SKIN_BASE)
    c.set(tx - 7, h_y + 4, C_SKIN_SHADE)
    c.set(tx + 7, h_y + 3, C_SKIN_BASE)
    c.set(tx + 7, h_y + 4, C_SKIN_SHADE)
    # Gloss sheen on hips
    c.set(tx - 5, h_y + 2, C_SUIT_HILIGHT)
    c.set(tx + 5, h_y + 2, C_SUIT_HILIGHT)

    # 6. Legs / Stockings / Heeled Boots
    ly = h_y + 5
    if leg_pose == 'idle':
        # Graceful feminine stance, legs together with slight knee angle
        # Thighs in sheer stockings
        c.rect(tx - 6, ly, 5, 8, C_STOCKING)
        c.rect(tx + 1, ly, 5, 8, C_STOCKING)
        c.line(tx - 6, ly, tx - 6, ly + 7, C_STOCKING_SHADE)
        c.line(tx + 5, ly, tx + 5, ly + 7, C_STOCKING_SHADE)
        # Garter bands at top of stockings
        c.line(tx - 6, ly, tx - 2, ly, C_SUIT_BASE)
        c.set(tx - 4, ly - 1, C_GOLD_BASE)
        c.line(tx + 1, ly, tx + 5, ly, C_SUIT_BASE)
        c.set(tx + 3, ly - 1, C_GOLD_BASE)
        
        # Knee line
        c.set(tx - 4, ly + 8, C_SKIN_SHADE)
        c.set(tx + 3, ly + 8, C_SKIN_SHADE)

        # High-heeled sleek sorceress boots
        c.rect(tx - 5, ly + 9, 4, 11, C_BOOT_BASE)
        c.line(tx - 5, ly + 9, tx - 5, ly + 18, C_BOOT_SHADE)
        c.set(tx - 3, ly + 10, C_BOOT_HILIGHT)
        c.rect(tx - 6, ly + 19, 5, 2, C_BOOT_BASE) # foot
        c.set(tx - 6, ly + 20, C_GOLD_BASE) # heel

        c.rect(tx + 1, ly + 9, 4, 11, C_BOOT_BASE)
        c.line(tx + 4, ly + 9, tx + 4, ly + 18, C_BOOT_SHADE)
        c.set(tx + 2, ly + 10, C_BOOT_HILIGHT)
        c.rect(tx + 1, ly + 19, 5, 2, C_BOOT_BASE)
        c.set(tx + 1, ly + 20, C_GOLD_BASE)

    elif leg_pose == 'run':
        # Running strides for move_01 to move_04
        fn = leg_arg
        if fn == 1:
            # Left leg back, right leg forward
            c.line(tx - 4, ly, tx - 9, ly + 8, C_STOCKING)
            c.line(tx - 9, ly + 8, tx - 13, ly + 14, C_BOOT_BASE)
            c.rect(tx - 15, ly + 13, 4, 2, C_BOOT_BASE)
            c.line(tx + 2, ly, tx + 6, ly + 8, C_STOCKING)
            c.line(tx + 6, ly + 8, tx + 8, ly + 18, C_BOOT_BASE)
            c.rect(tx + 7, ly + 18, 5, 2, C_BOOT_BASE)
        elif fn == 2:
            c.line(tx - 3, ly, tx - 3, ly + 8, C_STOCKING)
            c.line(tx - 3, ly + 8, tx - 3, ly + 17, C_BOOT_BASE)
            c.rect(tx - 4, ly + 17, 4, 2, C_BOOT_BASE)
            c.line(tx + 2, ly, tx + 4, ly + 7, C_STOCKING)
            c.line(tx + 4, ly + 7, tx - 4, ly + 13, C_BOOT_BASE)
            c.rect(tx - 6, ly + 13, 3, 2, C_BOOT_BASE)
        elif fn == 3:
            c.line(tx + 3, ly, tx - 8, ly + 8, C_STOCKING)
            c.line(tx - 8, ly + 8, tx - 14, ly + 14, C_BOOT_BASE)
            c.rect(tx - 16, ly + 13, 4, 2, C_BOOT_BASE)
            c.line(tx - 2, ly, tx + 5, ly + 8, C_STOCKING)
            c.line(tx + 5, ly + 8, tx + 7, ly + 18, C_BOOT_BASE)
            c.rect(tx + 6, ly + 18, 5, 2, C_BOOT_BASE)
        else: # fn == 4
            c.line(tx - 2, ly, tx - 1, ly + 8, C_STOCKING)
            c.line(tx - 1, ly + 8, tx + 2, ly + 17, C_BOOT_BASE)
            c.rect(tx + 1, ly + 17, 4, 2, C_BOOT_BASE)
            c.line(tx + 3, ly, tx + 6, ly + 7, C_STOCKING)
            c.line(tx + 6, ly + 7, tx - 2, ly + 14, C_BOOT_BASE)
            c.rect(tx - 4, ly + 14, 3, 2, C_BOOT_BASE)
            
    elif leg_pose == 'jump':
        # Legs tucked back gracefully
        c.line(tx - 4, ly, tx - 8, ly + 6, C_STOCKING)
        c.line(tx - 8, ly + 6, tx - 11, ly + 12, C_BOOT_BASE)
        c.rect(tx - 13, ly + 12, 3, 2, C_BOOT_BASE)
        c.line(tx + 2, ly, tx - 2, ly + 7, C_STOCKING)
        c.line(tx - 2, ly + 7, tx - 5, ly + 14, C_BOOT_BASE)
        c.rect(tx - 7, ly + 14, 3, 2, C_BOOT_BASE)

    elif leg_pose == 'fall':
        # Legs extended downward trailing in air
        c.line(tx - 4, ly, tx - 5, ly + 8, C_STOCKING)
        c.line(tx - 5, ly + 8, tx - 6, ly + 17, C_BOOT_BASE)
        c.rect(tx - 7, ly + 17, 3, 3, C_BOOT_BASE)
        c.line(tx + 3, ly, tx + 4, ly + 8, C_STOCKING)
        c.line(tx + 4, ly + 8, tx + 5, ly + 18, C_BOOT_BASE)
        c.rect(tx + 4, ly + 18, 3, 3, C_BOOT_BASE)

    elif leg_pose == 'kneel':
        # Defeat kneeling pose
        c.rect(tx - 8, ly, 7, 5, C_STOCKING)
        c.rect(tx - 12, ly + 4, 12, 4, C_BOOT_BASE)
        c.rect(tx + 1, ly, 6, 6, C_STOCKING)
        c.rect(tx + 4, ly + 5, 8, 4, C_BOOT_BASE)

print("Hourglass body & female summoner modules defined successfully.")
