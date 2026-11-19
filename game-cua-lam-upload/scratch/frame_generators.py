import sys, os, math, base64
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
from test_body import (
    draw_staff, draw_flowing_hair_back, draw_torso_and_robe, draw_legs_idle
)

def create_idle_frame(frame_num):
    c = PixelCanvas(64, 72)
    hx = 32
    hy = 14 if frame_num == 1 else 15
    bob = 0 if frame_num == 1 else 1

    # Back hair
    draw_flowing_hair_back(c, hx, hy, flow_x=0 if frame_num == 1 else 1, billow=frame_num * 1.5)

    # Left arm (resting on hip)
    c.line(hx - 8, hy + 18, hx - 11, hy + 26, C_SKIN_BASE)
    c.line(hx - 11, hy + 26, hx - 9, hy + 33, C_SKIN_BASE)
    c.rect(hx - 10, hy + 33, 2, 2, C_SKIN_BASE)

    # Torso & robe
    draw_torso_and_robe(c, hx, hy + 15, breath=bob)

    # Legs
    draw_legs_idle(c, hx, hy + 35)

    # Head and face
    draw_head_and_face(c, hx, hy, expr='normal', mouth='smirk')

    # Right arm holding staff
    arm_sway = 0 if frame_num == 1 else 1
    c.line(hx + 7, hy + 18, hx + 11 + arm_sway, hy + 25, C_SKIN_BASE)
    c.line(hx + 11 + arm_sway, hy + 25, hx + 14 + arm_sway, hy + 31, C_SKIN_BASE)
    c.rect(hx + 13 + arm_sway, hy + 30, 3, 3, C_SKIN_BASE)

    # Staff
    staff_x = hx + 15 + arm_sway
    staff_y = hy + 8 + bob
    draw_staff(c, staff_x, staff_y, angle_deg=0, length=46, orb_pulse=1 if frame_num == 1 else 1.5, cast_glow=True)

    # Magic sparkles orbiting orb
    if frame_num == 1:
        c.set(staff_x - 5, staff_y - 2, C_MINT_BRIGHT)
        c.set(staff_x + 5, staff_y + 3, C_MINT_BASE)
        c.set(staff_x + 3, staff_y - 4, C_MINT_CORE)
    else:
        c.set(staff_x + 5, staff_y - 3, C_MINT_BRIGHT)
        c.set(staff_x - 4, staff_y + 4, C_MINT_BASE)
        c.set(staff_x - 2, staff_y - 5, C_MINT_CORE)

    return c

def create_move_frame(frame_num):
    c = PixelCanvas(64, 72)
    hx = 30 + (1 if frame_num in [2, 4] else 0)
    hy = 14 + (0 if frame_num in [1, 3] else -1)
    
    # Back hair flying backward (leftward since character faces right)
    draw_flowing_hair_back(c, hx, hy, flow_x=-7, billow=frame_num * 1.6)

    # Dynamic running legs
    ly = hy + 35
    if frame_num == 1: # Right leg forward, left leg back
        # Left leg (back)
        c.line(hx - 3, ly, hx - 8, ly + 8, C_SKIN_BASE)
        c.line(hx - 8, ly + 8, hx - 12, ly + 14, C_BOOT_BASE)
        c.rect(hx - 14, ly + 14, 4, 2, C_BOOT_BASE) # back foot raised
        # Right leg (forward)
        c.line(hx + 1, ly, hx + 6, ly + 8, C_SKIN_BASE)
        c.line(hx + 6, ly + 8, hx + 8, ly + 18, C_BOOT_BASE)
        c.rect(hx + 7, ly + 18, 5, 2, C_BOOT_BASE) # front foot landing
    elif frame_num == 2: # Passing 1
        # Left leg moving forward
        c.line(hx - 2, ly, hx - 2, ly + 8, C_SKIN_BASE)
        c.line(hx - 2, ly + 8, hx - 2, ly + 17, C_BOOT_BASE)
        c.rect(hx - 3, ly + 17, 4, 2, C_BOOT_BASE)
        # Right leg pushing off
        c.line(hx + 2, ly, hx + 4, ly + 7, C_SKIN_BASE)
        c.line(hx + 4, ly + 7, hx - 4, ly + 13, C_BOOT_BASE)
        c.rect(hx - 6, ly + 13, 3, 2, C_BOOT_BASE)
    elif frame_num == 3: # Left leg forward, right leg back
        # Right leg (back)
        c.line(hx + 1, ly, hx - 7, ly + 8, C_SKIN_BASE)
        c.line(hx - 7, ly + 8, hx - 13, ly + 14, C_BOOT_BASE)
        c.rect(hx - 15, ly + 14, 4, 2, C_BOOT_BASE)
        # Left leg (forward)
        c.line(hx - 2, ly, hx + 5, ly + 8, C_SKIN_BASE)
        c.line(hx + 5, ly + 8, hx + 7, ly + 18, C_BOOT_BASE)
        c.rect(hx + 6, ly + 18, 5, 2, C_BOOT_BASE)
    else: # Passing 2
        # Right leg moving forward
        c.line(hx + 2, ly, hx + 1, ly + 8, C_SKIN_BASE)
        c.line(hx + 1, ly + 8, hx + 1, ly + 17, C_BOOT_BASE)
        c.rect(hx, ly + 17, 4, 2, C_BOOT_BASE)
        # Left leg kicking back
        c.line(hx - 3, ly, hx - 4, ly + 7, C_SKIN_BASE)
        c.line(hx - 4, ly + 7, hx - 6, ly + 13, C_BOOT_BASE)
        c.rect(hx - 8, ly + 13, 3, 2, C_BOOT_BASE)

    # Torso & robe (leaning forward slightly)
    draw_torso_and_robe(c, hx, hy + 15, breath=0)

    # Head and face
    draw_head_and_face(c, hx, hy, expr='normal', mouth='open' if frame_num % 2 == 1 else 'smirk')

    # Arms and staff (staff angled forward dynamically)
    arm_swing = math.sin(frame_num * math.pi / 2.0) * 3
    c.line(hx + 7, hy + 18, hx + 12 + int(arm_swing), hy + 24, C_SKIN_BASE)
    c.line(hx + 12 + int(arm_swing), hy + 24, hx + 16 + int(arm_swing), hy + 29, C_SKIN_BASE)
    c.rect(hx + 15 + int(arm_swing), hy + 28, 3, 3, C_SKIN_BASE)

    # Staff angled forward at 18 degrees
    staff_x = hx + 17 + int(arm_swing)
    staff_y = hy + 11
    draw_staff(c, staff_x, staff_y, angle_deg=-20, length=44, orb_pulse=1, cast_glow=True)

    # Wind / spirit dust trail at feet
    dust_x = hx - 12 - frame_num * 2
    c.set(dust_x, ly + 18, C_MINT_SHADE)
    c.set(dust_x - 2, ly + 17, C_MINT_BASE)
    c.set(dust_x - 3, ly + 19, C_MINT_BRIGHT)

    return c

def create_jump_frame():
    c = PixelCanvas(64, 72)
    hx = 31
    hy = 10 # Lifted high

    # Back hair streaming downward
    draw_flowing_hair_back(c, hx, hy, flow_x=-2, flow_y=4, billow=2)

    # Tucked jumping legs
    ly = hy + 35
    # Both legs bent upward gracefully
    c.line(hx - 3, ly, hx - 6, ly + 6, C_SKIN_BASE)
    c.line(hx - 6, ly + 6, hx - 3, ly + 12, C_BOOT_BASE)
    c.rect(hx - 4, ly + 12, 4, 2, C_BOOT_BASE)

    c.line(hx + 2, ly, hx + 5, ly + 5, C_SKIN_BASE)
    c.line(hx + 5, ly + 5, hx + 2, ly + 11, C_BOOT_BASE)
    c.rect(hx + 1, ly + 11, 4, 2, C_BOOT_BASE)

    # Robe floating with air resistance
    draw_torso_and_robe(c, hx, hy + 15)

    # Head and face looking forward/up
    draw_head_and_face(c, hx, hy, expr='normal', mouth='open')

    # Staff held high aloft
    c.line(hx + 7, hy + 17, hx + 12, hy + 12, C_SKIN_BASE)
    c.line(hx + 12, hy + 12, hx + 16, hy + 8, C_SKIN_BASE)
    c.rect(hx + 15, hy + 7, 3, 3, C_SKIN_BASE)

    draw_staff(c, hx + 18, hy - 4, angle_deg=10, length=46, orb_pulse=1.8, cast_glow=True)

    # Magic wind arcs around feet
    c.circle(hx, ly + 14, 8, C_MINT_BASE, fill=False)

    return c

def create_fall_frame():
    c = PixelCanvas(64, 72)
    hx = 32
    hy = 12

    # Hair billowing upward as summoner falls
    draw_flowing_hair_back(c, hx, hy, flow_x=-3, flow_y=-6, billow=3)

    # Legs extended downward to absorb landing
    ly = hy + 35
    c.line(hx - 3, ly, hx - 5, ly + 8, C_SKIN_BASE)
    c.line(hx - 5, ly + 8, hx - 3, ly + 18, C_BOOT_BASE)
    c.rect(hx - 4, ly + 18, 4, 2, C_BOOT_BASE)

    c.line(hx + 2, ly, hx + 3, ly + 8, C_SKIN_BASE)
    c.line(hx + 3, ly + 8, hx + 4, ly + 17, C_BOOT_BASE)
    c.rect(hx + 3, ly + 17, 4, 2, C_BOOT_BASE)

    # Robe billowing upward
    draw_torso_and_robe(c, hx, hy + 15)

    # Head and face
    draw_head_and_face(c, hx, hy, expr='normal', mouth='smirk')

    # Staff pointed forward-downward
    c.line(hx + 7, hy + 18, hx + 13, hy + 24, C_SKIN_BASE)
    c.line(hx + 13, hy + 24, hx + 16, hy + 30, C_SKIN_BASE)
    c.rect(hx + 15, hy + 29, 3, 3, C_SKIN_BASE)

    draw_staff(c, hx + 18, hy + 18, angle_deg=-30, length=44, orb_pulse=1.2, cast_glow=True)

    # Spirit cushion buffer under feet
    c.rect(hx - 10, ly + 19, 20, 2, C_MINT_SHADE)
    c.rect(hx - 6, ly + 20, 12, 1, C_MINT_BRIGHT)

    return c

def create_attack_frame(frame_num):
    c = PixelCanvas(64, 72)
    
    if frame_num == 1: # Wind-up: pulling staff back, body coiled
        hx = 28
        hy = 15
        draw_flowing_hair_back(c, hx, hy, flow_x=4, billow=1)
        draw_legs_idle(c, hx, hy + 34)
        draw_torso_and_robe(c, hx, hy + 15)
        draw_head_and_face(c, hx, hy, expr='normal', mouth='smirk')
        # Arms pulling staff back
        c.line(hx - 6, hy + 18, hx - 2, hy + 23, C_SKIN_BASE)
        c.line(hx + 6, hy + 18, hx + 2, hy + 23, C_SKIN_BASE)
        c.rect(hx - 1, hy + 22, 4, 3, C_SKIN_BASE)
        # Staff angled back
        draw_staff(c, hx - 12, hy + 2, angle_deg=45, length=44, orb_pulse=1.5, cast_glow=True)
        # Gathering energy sparks
        c.circle(hx - 12, hy + 2, 7, C_MINT_BASE, fill=False)
        c.set(hx - 15, hy, C_MINT_CORE)
        c.set(hx - 9, hy + 5, C_MINT_BRIGHT)

    elif frame_num == 2: # Attack strike: thrusting staff forward, emitting spirit orb projectile!
        hx = 30
        hy = 14
        draw_flowing_hair_back(c, hx, hy, flow_x=-8, billow=2)
        # Deep lunge stance
        ly = hy + 35
        # Back leg
        c.line(hx - 4, ly, hx - 11, ly + 7, C_SKIN_BASE)
        c.line(hx - 11, ly + 7, hx - 15, ly + 18, C_BOOT_BASE)
        c.rect(hx - 17, ly + 18, 5, 2, C_BOOT_BASE)
        # Front leg
        c.line(hx + 2, ly, hx + 8, ly + 8, C_SKIN_BASE)
        c.line(hx + 8, ly + 8, hx + 10, ly + 18, C_BOOT_BASE)
        c.rect(hx + 9, ly + 18, 5, 2, C_BOOT_BASE)

        draw_torso_and_robe(c, hx, hy + 15)
        draw_head_and_face(c, hx, hy, expr='normal', mouth='open')

        # Arms thrust forward
        c.line(hx + 7, hy + 18, hx + 18, hy + 21, C_SKIN_BASE)
        c.line(hx + 6, hy + 20, hx + 15, hy + 23, C_SKIN_BASE)
        c.rect(hx + 17, hy + 20, 3, 3, C_SKIN_BASE)

        # Staff horizontal thrusting forward
        staff_x = hx + 36
        staff_y = hy + 21
        draw_staff(c, staff_x, staff_y, angle_deg=-90, length=44, orb_pulse=2.5, cast_glow=True)

        # Glowing Spirit Orb / Blast burst at tip!
        c.circle(staff_x + 8, staff_y, 7, C_MINT_BRIGHT, fill=True)
        c.circle(staff_x + 8, staff_y, 4, C_MINT_CORE, fill=True)
        c.circle(staff_x + 8, staff_y, 10, C_MINT_BASE, fill=False)
        # Crescent shockwave
        c.line(staff_x + 15, staff_y - 8, staff_x + 18, staff_y, C_MINT_BRIGHT)
        c.line(staff_x + 18, staff_y, staff_x + 15, staff_y + 8, C_MINT_BRIGHT)
        c.set(staff_x + 19, staff_y, C_MINT_CORE)

    else: # Follow-through recovery
        hx = 31
        hy = 14
        draw_flowing_hair_back(c, hx, hy, flow_x=-5, billow=3)
        draw_legs_idle(c, hx, hy + 35)
        draw_torso_and_robe(c, hx, hy + 15)
        draw_head_and_face(c, hx, hy, expr='normal', mouth='smirk')
        # Staff held in dynamic flourish
        c.line(hx + 7, hy + 18, hx + 15, hy + 23, C_SKIN_BASE)
        c.rect(hx + 14, hy + 22, 3, 3, C_SKIN_BASE)
        draw_staff(c, hx + 22, hy + 14, angle_deg=-45, length=46, orb_pulse=1.3, cast_glow=True)
        # Trailing sparkles
        c.set(hx + 28, hy + 10, C_MINT_BRIGHT)
        c.set(hx + 30, hy + 15, C_MINT_BASE)
        c.set(hx + 26, hy + 20, C_MINT_CORE)

    return c

def create_skill_frame(frame_num):
    c = PixelCanvas(64, 72)
    hx = 32
    hy = 14

    if frame_num == 1: # Chanting start: raising staff, eyes shining, magic circle appearing
        draw_flowing_hair_back(c, hx, hy, flow_x=0, billow=2)
        draw_legs_idle(c, hx, hy + 35)
        draw_torso_and_robe(c, hx, hy + 15)
        draw_head_and_face(c, hx, hy, expr='normal', mouth='open')
        # Raising staff with right hand
        c.line(hx + 7, hy + 18, hx + 12, hy + 10, C_SKIN_BASE)
        c.rect(hx + 11, hy + 9, 3, 3, C_SKIN_BASE)
        # Left hand making mystic mudra
        c.line(hx - 8, hy + 18, hx - 12, hy + 24, C_SKIN_BASE)
        c.rect(hx - 13, hy + 24, 3, 2, C_SKIN_BASE)
        # Staff raised high
        draw_staff(c, hx + 14, hy - 6, angle_deg=5, length=48, orb_pulse=2.0, cast_glow=True)
        # Ground glyph runes
        ly = hy + 54
        c.line(hx - 16, ly, hx + 16, ly, C_MINT_SHADE)
        c.line(hx - 12, ly + 1, hx + 12, ly + 1, C_MINT_BASE)

    elif frame_num == 2: # Summon channeling: massive light pillar, dual hands on staff
        draw_flowing_hair_back(c, hx, hy, flow_x=0, flow_y=-4, billow=4)
        draw_legs_idle(c, hx, hy + 35)
        draw_torso_and_robe(c, hx, hy + 15)
        draw_head_and_face(c, hx, hy, expr='normal', mouth='open')
        # Both hands holding staff aloft
        c.line(hx - 7, hy + 18, hx - 2, hy + 8, C_SKIN_BASE)
        c.line(hx + 7, hy + 18, hx + 2, hy + 8, C_SKIN_BASE)
        c.rect(hx - 2, hy + 7, 4, 3, C_SKIN_BASE)
        # Staff upright right above head
        draw_staff(c, hx, hy - 12, angle_deg=0, length=48, orb_pulse=3.0, cast_glow=True)
        # Vertical aura pillar
        c.line(hx - 2, 0, hx - 2, hy - 4, (180, 255, 234, 180))
        c.line(hx + 2, 0, hx + 2, hy - 4, (180, 255, 234, 180))
        c.line(hx, 0, hx, hy - 4, C_MINT_CORE)
        # Full ground summoning ring
        ly = hy + 54
        c.circle(hx, ly, 18, C_MINT_BASE, fill=False)
        c.circle(hx, ly, 14, C_MINT_BRIGHT, fill=False)
        c.rect(hx - 10, ly - 1, 20, 2, C_MINT_CORE)

    else: # Summon release: sacred beast spirit emergence!
        draw_flowing_hair_back(c, hx, hy, flow_x=-4, billow=5)
        # Powerful wide stance
        ly = hy + 35
        c.line(hx - 4, ly, hx - 8, ly + 8, C_SKIN_BASE)
        c.line(hx - 8, ly + 8, hx - 10, ly + 18, C_BOOT_BASE)
        c.rect(hx - 12, ly + 18, 5, 2, C_BOOT_BASE)

        c.line(hx + 2, ly, hx + 7, ly + 8, C_SKIN_BASE)
        c.line(hx + 7, ly + 8, hx + 9, ly + 18, C_BOOT_BASE)
        c.rect(hx + 8, ly + 18, 5, 2, C_BOOT_BASE)

        draw_torso_and_robe(c, hx, hy + 15)
        draw_head_and_face(c, hx, hy, expr='normal', mouth='smirk')

        # Staff angled down-forward releasing beast energy
        c.line(hx + 7, hy + 18, hx + 16, hy + 24, C_SKIN_BASE)
        c.rect(hx + 15, hy + 23, 3, 3, C_SKIN_BASE)
        draw_staff(c, hx + 22, hy + 18, angle_deg=-45, length=46, orb_pulse=2.5, cast_glow=True)

        # Divine White Dragon / Bai Ze spirit silhouette around her!
        # Ethereal dragon head emerging
        dx, dy = hx + 18, hy - 6
        c.rect(dx, dy, 12, 6, (255, 255, 255, 220))
        c.line(dx + 12, dy + 2, dx + 15, dy + 1, C_MINT_BRIGHT) # dragon snout
        c.set(dx + 7, dy + 2, '#48d8b2') # dragon eye
        c.line(dx + 3, dy - 1, dx - 2, dy - 5, C_GOLD_BASE) # dragon horn
        c.circle(hx, hy + 20, 24, (110, 227, 189, 130), fill=False) # divine protective shield

    return c

def create_finisher_frame(frame_num):
    c = PixelCanvas(64, 72)
    hx = 32
    hy = 12 if frame_num == 1 else 13

    if frame_num == 1: # Floating in midair, gathering ultimate beast celestial fire
        draw_flowing_hair_back(c, hx, hy, flow_x=0, flow_y=-6, billow=6)
        # Floating feet
        ly = hy + 35
        c.line(hx - 3, ly, hx - 5, ly + 8, C_SKIN_BASE)
        c.line(hx - 5, ly + 8, hx - 4, ly + 16, C_BOOT_BASE)
        c.rect(hx - 5, ly + 16, 4, 2, C_BOOT_BASE)
        c.line(hx + 2, ly, hx + 4, ly + 8, C_SKIN_BASE)
        c.line(hx + 4, ly + 8, hx + 5, ly + 16, C_BOOT_BASE)
        c.rect(hx + 4, ly + 16, 4, 2, C_BOOT_BASE)

        draw_torso_and_robe(c, hx, hy + 15)
        draw_head_and_face(c, hx, hy, expr='normal', mouth='open')

        # Holding staff horizontally across chest with both hands
        c.line(hx - 8, hy + 18, hx - 2, hy + 20, C_SKIN_BASE)
        c.line(hx + 8, hy + 18, hx + 2, hy + 20, C_SKIN_BASE)
        c.rect(hx - 4, hy + 19, 8, 3, C_SKIN_BASE)
        draw_staff(c, hx + 22, hy + 20, angle_deg=-90, length=44, orb_pulse=3.0, cast_glow=True)

        # Radiating ultimate celestial aura
        c.circle(hx, hy + 18, 22, C_GOLD_BASE, fill=False)
        c.circle(hx, hy + 18, 26, C_MINT_BASE, fill=False)
        # Horns alight with crimson energy
        c.set(hx - 8, hy - 14, '#ff385c')
        c.set(hx + 6, hy - 14, '#ff385c')

    elif frame_num == 2: # Grand slam / unleash: giant dragon beast burst!
        draw_flowing_hair_back(c, hx, hy, flow_x=-8, billow=6)
        # Powerful forward strike
        ly = hy + 35
        c.line(hx - 5, ly, hx - 12, ly + 8, C_SKIN_BASE)
        c.line(hx - 12, ly + 8, hx - 16, ly + 18, C_BOOT_BASE)
        c.rect(hx - 18, ly + 18, 5, 2, C_BOOT_BASE)

        c.line(hx + 2, ly, hx + 8, ly + 8, C_SKIN_BASE)
        c.line(hx + 8, ly + 8, hx + 11, ly + 18, C_BOOT_BASE)
        c.rect(hx + 10, ly + 18, 5, 2, C_BOOT_BASE)

        draw_torso_and_robe(c, hx, hy + 15)
        draw_head_and_face(c, hx, hy, expr='normal', mouth='open')

        # Staff thrust forward
        c.line(hx + 7, hy + 18, hx + 20, hy + 20, C_SKIN_BASE)
        c.rect(hx + 19, hy + 19, 3, 3, C_SKIN_BASE)
        draw_staff(c, hx + 36, hy + 20, angle_deg=-90, length=44, orb_pulse=3.5, cast_glow=True)

        # Giant Dragon Beast Head manifested in glowing energy
        dx = hx + 24
        dy = hy - 2
        # Dragon head
        c.rect(dx, dy - 10, 18, 12, (255, 255, 255, 240))
        c.rect(dx + 18, dy - 8, 8, 8, (255, 255, 255, 240))
        c.line(dx + 26, dy - 7, dx + 31, dy - 5, C_MINT_BRIGHT) # giant snout
        # Horns
        c.line(dx + 12, dy - 10, dx + 6, dy - 18, C_GOLD_BASE)
        c.line(dx + 13, dy - 10, dx + 7, dy - 18, C_GOLD_HILIGHT)
        # Eye
        c.rect(dx + 16, dy - 6, 3, 3, '#ff2255')
        c.set(dx + 17, dy - 5, '#ffffff')
        # Shockwave blast waves
        c.circle(dx + 16, dy, 20, C_MINT_BASE, fill=False)
        c.circle(dx + 16, dy, 24, C_GOLD_BASE, fill=False)

    else: # Ultimate climax: blinding light & swirling celestial spirit particles
        draw_flowing_hair_back(c, hx, hy, flow_x=-6, billow=5)
        draw_legs_idle(c, hx, hy + 35)
        draw_torso_and_robe(c, hx, hy + 15)
        draw_head_and_face(c, hx, hy, expr='winking', mouth='smirk')
        # Staff upright with massive pulsating halo
        c.line(hx + 7, hy + 18, hx + 15, hy + 22, C_SKIN_BASE)
        c.rect(hx + 14, hy + 21, 3, 3, C_SKIN_BASE)
        draw_staff(c, hx + 18, hy + 6, angle_deg=-10, length=46, orb_pulse=3.0, cast_glow=True)
        # Celestial aura rings
        c.circle(hx + 18, hy + 6, 14, C_MINT_BRIGHT, fill=False)
        c.circle(hx + 18, hy + 6, 20, C_GOLD_BASE, fill=False)
        c.circle(hx, hy + 25, 28, (110, 227, 189, 100), fill=False)

    return c

def create_dash_frame(frame_num):
    c = PixelCanvas(64, 72)
    hx = 34 if frame_num == 1 else 38
    hy = 17 # Low crouching forward dive

    # Hair flying straight back
    draw_flowing_hair_back(c, hx, hy, flow_x=-14, billow=frame_num * 3)

    # Low dash legs
    ly = hy + 30
    c.line(hx - 4, ly, hx - 14, ly + 4, C_SKIN_BASE)
    c.line(hx - 14, ly + 4, hx - 22, ly + 14, C_BOOT_BASE)
    c.rect(hx - 24, ly + 14, 5, 2, C_BOOT_BASE)

    c.line(hx + 2, ly, hx + 8, ly + 5, C_SKIN_BASE)
    c.line(hx + 8, ly + 5, hx + 12, ly + 14, C_BOOT_BASE)
    c.rect(hx + 11, ly + 14, 5, 2, C_BOOT_BASE)

    draw_torso_and_robe(c, hx, hy + 12)
    draw_head_and_face(c, hx, hy, expr='normal', mouth='smirk')

    # Holding staff pointing backward like a streamlined spear
    c.line(hx + 6, hy + 16, hx + 2, hy + 20, C_SKIN_BASE)
    c.rect(hx + 1, hy + 19, 3, 3, C_SKIN_BASE)
    draw_staff(c, hx - 6, hy + 20, angle_deg=100, length=42, orb_pulse=1.5, cast_glow=True)

    # Motion blur speedlines & cyan spirit afterimages
    for trail in range(3):
        tx = hx - 12 - trail * 8
        c.line(tx, hy + 8 + trail * 4, tx + 6, hy + 8 + trail * 4, (110, 227, 189, 140 - trail * 40))
        c.line(tx - 4, ly + 6, tx + 2, ly + 6, (110, 227, 189, 120 - trail * 40))

    return c

def create_defeat_frame():
    c = PixelCanvas(64, 72)
    hx = 30
    hy = 32 # Collapsed low onto floor

    # Hair draped over shoulders and resting on ground
    c.rect(hx - 12, hy + 4, 24, 12, C_HAIR_SHADE)
    c.rect(hx - 10, hy + 6, 20, 14, C_HAIR_BASE)

    # Collapsed body / robe
    c.rect(hx - 14, hy + 18, 28, 14, C_ROBE_SHADE)
    c.rect(hx - 12, hy + 19, 24, 11, C_ROBE_BASE)
    c.line(hx - 14, hy + 31, hx + 14, hy + 31, C_GOLD_BASE)

    # Kneeling legs
    c.rect(hx - 16, hy + 26, 8, 6, C_BOOT_BASE)
    c.rect(hx + 8, hy + 26, 8, 6, C_BOOT_BASE)

    # Head bowed, peaceful closed eyes
    draw_head_and_face(c, hx, hy, expr='closed', mouth='normal')

    # One arm touching ground supporting body
    c.line(hx - 8, hy + 16, hx - 14, hy + 26, C_SKIN_BASE)
    c.rect(hx - 15, hy + 25, 3, 2, C_SKIN_BASE)

    # Staff resting horizontally on the floor beside her
    draw_staff(c, hx + 22, hy + 30, angle_deg=-90, length=44, orb_pulse=0.3, cast_glow=False)

    return c

print('Frame generator functions ready.')
