import sys, os, math, json, base64
sys.path.append(os.path.abspath('scratch'))
from pixel_canvas import PixelCanvas
from design_new_summoner import (
    draw_staff, draw_female_head_and_face, draw_flowing_hair_back, draw_hourglass_body,
    C_OUTLINE, C_SKIN_BASE, C_SKIN_SHADE, C_SKIN_DEEP, C_SKIN_HILIGHT,
    C_HAIR_BASE, C_HAIR_SHADE, C_HAIR_DEEP, C_HAIR_SHINE,
    C_COLLAR, C_BOWTIE, C_BOWTIE_HILIGHT,
    C_SUIT_BASE, C_SUIT_SHADE, C_SUIT_HILIGHT, C_SUIT_SHEEN,
    C_STOCKING, C_BOOT_BASE, C_BOOT_SHADE, C_BOOT_HILIGHT,
    C_GOLD_BASE, C_GOLD_SHADE, C_GOLD_HILIGHT,
    C_ORB_CORE, C_ORB_BRIGHT, C_ORB_BASE, C_ORB_SHADE, C_ORB_GLOW,
    C_MAGIC_CYAN, C_MAGIC_PINK
)

def create_idle_frame(frame_num):
    c = PixelCanvas(64, 72)
    hx = 32
    hy = 14 if frame_num == 1 else 15
    bob = 0 if frame_num == 1 else 1

    # Back hair
    draw_flowing_hair_back(c, hx, hy, flow_x=0 if frame_num == 1 else 1, billow=frame_num * 1.5)

    # Left arm (hand resting on curvaceous hip)
    c.line(hx - 8, hy + 18, hx - 11, hy + 26, C_SKIN_BASE)
    c.line(hx - 11, hy + 26, hx - 9, hy + 33, C_SKIN_BASE)
    c.rect(hx - 10, hy + 32, 2, 2, C_SKIN_BASE)

    # Hourglass body with V1=100 (exposed bust), V2=60 (narrow waist), V3=90 (curvy hips)
    draw_hourglass_body(c, hx, hy + 15, breath=bob, leg_pose='idle')

    # Head and face
    draw_female_head_and_face(c, hx, hy, expr='normal', mouth='smirk')

    # Right arm holding staff
    arm_sway = 0 if frame_num == 1 else 1
    c.line(hx + 7, hy + 18, hx + 11 + arm_sway, hy + 25, C_SKIN_BASE)
    c.line(hx + 11 + arm_sway, hy + 25, hx + 14 + arm_sway, hy + 31, C_SKIN_BASE)
    c.rect(hx + 13 + arm_sway, hy + 30, 3, 3, C_SKIN_BASE)

    # Staff
    staff_x = hx + 15 + arm_sway
    staff_y = hy + 8 + bob
    draw_staff(c, staff_x, staff_y, angle_deg=0, length=46, orb_pulse=1 if frame_num == 1 else 1.5, cast_glow=True)

    # Magical sparkles orbiting orb
    if frame_num == 1:
        c.set(staff_x - 5, staff_y - 2, C_MAGIC_CYAN)
        c.set(staff_x + 5, staff_y + 3, C_MAGIC_PINK)
        c.set(staff_x + 3, staff_y - 4, C_ORB_CORE)
    else:
        c.set(staff_x + 5, staff_y - 3, C_MAGIC_CYAN)
        c.set(staff_x - 4, staff_y + 4, C_MAGIC_PINK)
        c.set(staff_x - 2, staff_y - 5, C_ORB_CORE)

    return c

def create_move_frame(frame_num):
    c = PixelCanvas(64, 72)
    hx = 30 + (1 if frame_num in [2, 4] else 0)
    hy = 14 + (0 if frame_num in [1, 3] else -1)

    # Flowing hair flying back
    draw_flowing_hair_back(c, hx, hy, flow_x=-7, billow=frame_num * 1.6)

    # Hourglass body with running legs
    draw_hourglass_body(c, hx, hy + 15, breath=0, leg_pose='run', leg_arg=frame_num)

    # Left arm swinging
    if frame_num in [1, 2]:
        c.line(hx - 7, hy + 18, hx - 12, hy + 24, C_SKIN_BASE)
        c.line(hx - 12, hy + 24, hx - 14, hy + 30, C_SKIN_BASE)
    else:
        c.line(hx - 7, hy + 18, hx - 4, hy + 24, C_SKIN_BASE)
        c.line(hx - 4, hy + 24, hx - 2, hy + 30, C_SKIN_BASE)

    # Head and face
    draw_female_head_and_face(c, hx, hy, expr='focused', mouth='smirk')

    # Right arm holding staff forward
    staff_sway = 2 if frame_num in [1, 3] else -1
    c.line(hx + 7, hy + 18, hx + 13 + staff_sway, hy + 24, C_SKIN_BASE)
    c.line(hx + 13 + staff_sway, hy + 24, hx + 16 + staff_sway, hy + 29, C_SKIN_BASE)
    c.rect(hx + 15 + staff_sway, hy + 28, 3, 3, C_SKIN_BASE)

    # Staff angled forward slightly
    staff_x = hx + 17 + staff_sway
    staff_y = hy + 7
    draw_staff(c, staff_x, staff_y, angle_deg=-10, length=45, orb_pulse=1, cast_glow=True)

    # Wind / speed particles
    c.set(hx - 15, hy + 28, C_MAGIC_CYAN)
    c.set(hx - 18, hy + 34, C_MAGIC_PINK)

    return c

def create_jump_frame():
    c = PixelCanvas(64, 72)
    hx = 32
    hy = 10

    # Hair billowing upward & back
    draw_flowing_hair_back(c, hx, hy, flow_x=-4, flow_y=-3, billow=3.5)

    # Hourglass body with tucked legs
    draw_hourglass_body(c, hx, hy + 15, breath=0, leg_pose='jump')

    # Arms raised dynamically
    c.line(hx - 8, hy + 18, hx - 14, hy + 13, C_SKIN_BASE)
    c.line(hx - 14, hy + 13, hx - 17, hy + 8, C_SKIN_BASE)

    draw_female_head_and_face(c, hx, hy, expr='excited', mouth='smile')

    # Right arm raising staff
    c.line(hx + 7, hy + 18, hx + 13, hy + 14, C_SKIN_BASE)
    c.line(hx + 13, hy + 14, hx + 17, hy + 10, C_SKIN_BASE)
    c.rect(hx + 16, hy + 9, 3, 3, C_SKIN_BASE)

    staff_x = hx + 18
    staff_y = hy + 1
    draw_staff(c, staff_x, staff_y, angle_deg=-25, length=44, orb_pulse=2, cast_glow=True)

    # Air ascending particles
    c.set(hx - 5, hy + 58, C_MAGIC_CYAN)
    c.set(hx + 8, hy + 56, C_MAGIC_PINK)
    c.set(hx + 2, hy + 62, C_ORB_CORE)

    return c

def create_fall_frame():
    c = PixelCanvas(64, 72)
    hx = 32
    hy = 12

    # Hair floating upward heavily
    draw_flowing_hair_back(c, hx, hy, flow_x=2, flow_y=-6, billow=5.0)

    # Hourglass body with legs trailing down
    draw_hourglass_body(c, hx, hy + 15, breath=0, leg_pose='fall')

    # Left arm floating out
    c.line(hx - 8, hy + 18, hx - 14, hy + 22, C_SKIN_BASE)
    c.line(hx - 14, hy + 22, hx - 18, hy + 26, C_SKIN_BASE)

    draw_female_head_and_face(c, hx, hy, expr='focused', mouth='normal')

    # Right arm holding staff pointing downward
    c.line(hx + 7, hy + 18, hx + 12, hy + 24, C_SKIN_BASE)
    c.line(hx + 12, hy + 24, hx + 15, hy + 30, C_SKIN_BASE)
    c.rect(hx + 14, hy + 29, 3, 3, C_SKIN_BASE)

    staff_x = hx + 16
    staff_y = hy + 8
    draw_staff(c, staff_x, staff_y, angle_deg=15, length=44, orb_pulse=1, cast_glow=True)

    return c

def create_attack_frame(frame_num):
    c = PixelCanvas(64, 72)
    
    if frame_num == 1: # Wind up
        hx = 28
        hy = 14
        draw_flowing_hair_back(c, hx, hy, flow_x=-5, billow=1.0)
        draw_hourglass_body(c, hx, hy + 15, breath=0, leg_pose='idle')
        draw_female_head_and_face(c, hx, hy, expr='focused', mouth='smirk')
        
        # Pull staff back
        c.line(hx + 7, hy + 18, hx + 3, hy + 23, C_SKIN_BASE)
        c.line(hx + 3, hy + 23, hx - 2, hy + 27, C_SKIN_BASE)
        draw_staff(c, hx - 8, hy + 2, angle_deg=-30, length=44, orb_pulse=2, cast_glow=True)
        # Charging sparks
        c.circle(hx - 8, hy + 2, 6, C_ORB_GLOW, fill=False)

    elif frame_num == 2: # Staff swing / thrust forward
        hx = 33
        hy = 15
        draw_flowing_hair_back(c, hx, hy, flow_x=-8, billow=2.5)
        draw_hourglass_body(c, hx, hy + 15, breath=0, leg_pose='run', leg_arg=1)
        draw_female_head_and_face(c, hx, hy, expr='fierce', mouth='open')
        
        # Arm thrust forward horizontally
        c.line(hx + 7, hy + 18, hx + 16, hy + 20, C_SKIN_BASE)
        c.line(hx + 16, hy + 20, hx + 24, hy + 21, C_SKIN_BASE)
        c.rect(hx + 23, hy + 20, 3, 3, C_SKIN_BASE)
        
        # Staff thrust horizontal
        draw_staff(c, hx + 26, hy + 21, angle_deg=80, length=44, orb_pulse=3, cast_glow=True)
        # Swing arc
        c.line(hx + 10, hy + 5, hx + 32, hy + 18, C_MAGIC_CYAN)
        c.line(hx + 12, hy + 6, hx + 34, hy + 19, C_MAGIC_PINK)

    else: # frame_num == 3: Projectile burst forward
        hx = 30
        hy = 15
        draw_flowing_hair_back(c, hx, hy, flow_x=-6, billow=3.5)
        draw_hourglass_body(c, hx, hy + 15, breath=0, leg_pose='run', leg_arg=2)
        draw_female_head_and_face(c, hx, hy, expr='smug', mouth='smirk')
        
        c.line(hx + 7, hy + 18, hx + 18, hy + 22, C_SKIN_BASE)
        c.rect(hx + 17, hy + 21, 3, 3, C_SKIN_BASE)
        draw_staff(c, hx + 22, hy + 16, angle_deg=65, length=42, orb_pulse=2, cast_glow=True)
        
        # Summoned projectile bursting forward
        proj_x = 52
        proj_y = 30
        c.circle(proj_x, proj_y, 7, C_ORB_GLOW, fill=False)
        c.circle(proj_x, proj_y, 5, C_ORB_BASE, fill=True)
        c.circle(proj_x, proj_y, 3, C_MAGIC_CYAN, fill=True)
        c.circle(proj_x, proj_y, 1, C_ORB_CORE, fill=True)
        # Trail
        c.line(proj_x - 10, proj_y, proj_x - 4, proj_y, C_MAGIC_PINK)
        c.line(proj_x - 8, proj_y - 3, proj_x - 3, proj_y - 1, C_MAGIC_CYAN)
        c.line(proj_x - 8, proj_y + 3, proj_x - 3, proj_y + 1, C_MAGIC_CYAN)

    return c

def create_skill_frame(frame_num):
    c = PixelCanvas(64, 72)
    hx = 32
    hy = 14

    # Magic summon circle beneath feet
    ring_y = 66
    c.line(hx - 20, ring_y, hx + 20, ring_y, C_MAGIC_CYAN)
    c.line(hx - 16, ring_y - 1, hx + 16, ring_y - 1, C_MAGIC_PINK)
    c.line(hx - 16, ring_y + 1, hx + 16, ring_y + 1, C_MAGIC_PINK)
    c.set(hx - 12, ring_y, C_ORB_CORE)
    c.set(hx + 12, ring_y, C_ORB_CORE)

    if frame_num == 1:
        # Raising staff overhead with both hands
        draw_flowing_hair_back(c, hx, hy, flow_x=0, flow_y=-3, billow=2.0)
        draw_hourglass_body(c, hx, hy + 15, breath=1, leg_pose='idle')
        draw_female_head_and_face(c, hx, hy, expr='focused', mouth='open')

        # Both arms up
        c.line(hx - 7, hy + 18, hx - 1, hy + 10, C_SKIN_BASE)
        c.line(hx + 7, hy + 18, hx + 3, hy + 10, C_SKIN_BASE)
        c.rect(hx, hy + 8, 3, 3, C_SKIN_BASE)

        # Staff raised high vertically
        draw_staff(c, hx + 1, hy - 4, angle_deg=0, length=44, orb_pulse=2.5, cast_glow=True)

    elif frame_num == 2:
        # Arcane energy surge from orb
        draw_flowing_hair_back(c, hx, hy, flow_x=3, flow_y=-5, billow=4.0)
        draw_hourglass_body(c, hx, hy + 15, breath=1, leg_pose='idle')
        draw_female_head_and_face(c, hx, hy, expr='fierce', mouth='open')

        c.line(hx - 7, hy + 18, hx - 2, hy + 9, C_SKIN_BASE)
        c.line(hx + 7, hy + 18, hx + 4, hy + 9, C_SKIN_BASE)
        draw_staff(c, hx + 1, hy - 6, angle_deg=0, length=44, orb_pulse=4, cast_glow=True)

        # Summoning glyph rays radiating
        for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
            rad = math.radians(angle)
            gx = int(hx + 1 + math.cos(rad) * 11)
            gy = int(hy - 6 + math.sin(rad) * 11)
            c.set(gx, gy, C_MAGIC_CYAN)

    else: # frame_num == 3: Spirit beast wings/avatar burst
        draw_flowing_hair_back(c, hx, hy, flow_x=-4, billow=4.5)
        draw_hourglass_body(c, hx, hy + 15, breath=0, leg_pose='run', leg_arg=1)
        draw_female_head_and_face(c, hx, hy, expr='excited', mouth='smirk')

        # Staff pointed forward unleashing the summon
        c.line(hx + 7, hy + 18, hx + 18, hy + 20, C_SKIN_BASE)
        draw_staff(c, hx + 22, hy + 14, angle_deg=45, length=44, orb_pulse=3, cast_glow=True)

        # Ethereal summon wings in background
        c.line(hx - 16, hy + 5, hx - 6, hy + 14, C_MAGIC_PINK)
        c.line(hx - 22, hy - 2, hx - 14, hy + 6, C_MAGIC_CYAN)
        c.line(hx + 6, hy + 14, hx + 20, hy + 4, C_MAGIC_PINK)
        c.line(hx + 12, hy + 5, hx + 26, hy - 3, C_MAGIC_CYAN)

    return c

def create_finisher_frame(frame_num):
    c = PixelCanvas(64, 72)
    hx = 32
    hy = 14

    # Grand summoning circle
    c.circle(hx, 40, 28, C_ORB_GLOW, fill=False)
    c.circle(hx, 40, 26, (112, 243, 255, 60), fill=False)

    if frame_num == 1:
        # Majestic focus pose
        draw_flowing_hair_back(c, hx, hy, flow_x=0, flow_y=-4, billow=3.0)
        draw_hourglass_body(c, hx, hy + 15, breath=1, leg_pose='idle')
        draw_female_head_and_face(c, hx, hy, expr='fierce', mouth='open')

        # Staff held aloft
        c.line(hx - 7, hy + 18, hx, hy + 10, C_SKIN_BASE)
        c.line(hx + 7, hy + 18, hx + 3, hy + 10, C_SKIN_BASE)
        draw_staff(c, hx + 1, hy - 5, angle_deg=0, length=44, orb_pulse=3, cast_glow=True)

        # Arcane runes floating
        c.rect(hx - 18, hy + 10, 3, 3, C_MAGIC_CYAN)
        c.rect(hx + 16, hy + 10, 3, 3, C_MAGIC_PINK)
        c.rect(hx - 12, hy + 30, 2, 2, C_GOLD_BASE)
        c.rect(hx + 12, hy + 30, 2, 2, C_GOLD_BASE)

    elif frame_num == 2:
        # Blinding celestial pillar of light
        draw_flowing_hair_back(c, hx, hy, flow_x=2, flow_y=-8, billow=6.0)
        # Vertical light beam down center
        for y in range(0, 72):
            c.set(hx - 2, y, (255, 255, 255, 120))
            c.set(hx - 1, y, (240, 147, 251, 180))
            c.set(hx, y, (255, 255, 255, 255))
            c.set(hx + 1, y, (240, 147, 251, 180))
            c.set(hx + 2, y, (255, 255, 255, 120))

        draw_hourglass_body(c, hx, hy + 15, breath=1, leg_pose='idle')
        draw_female_head_and_face(c, hx, hy, expr='excited', mouth='smile')
        draw_staff(c, hx + 1, hy - 7, angle_deg=0, length=44, orb_pulse=5, cast_glow=True)

    else: # frame_num == 3: Full-screen summoner cataclysm shockwave
        draw_flowing_hair_back(c, hx, hy, flow_x=-6, billow=5.0)
        draw_hourglass_body(c, hx, hy + 15, breath=0, leg_pose='run', leg_arg=1)
        draw_female_head_and_face(c, hx, hy, expr='smug', mouth='smirk')

        c.line(hx + 7, hy + 18, hx + 20, hy + 21, C_SKIN_BASE)
        draw_staff(c, hx + 24, hy + 14, angle_deg=50, length=44, orb_pulse=4, cast_glow=True)

        # Shockwave blast rings filling right side
        for rad_r in [12, 20, 28]:
            c.circle(hx + 30, 36, rad_r, (255, 113, 206, 110), fill=False)
            c.circle(hx + 30, 36, rad_r - 2, (112, 243, 255, 130), fill=False)

    return c

def create_dash_frame(frame_num):
    c = PixelCanvas(64, 72)
    hx = 34 if frame_num == 1 else 37
    hy = 17

    # Heavy horizontal hair stream
    for i in range(15, 38):
        t = (i - 15) / 23.0
        y = hy + i - int(t * 12)
        xl = int(hx - 10 - t * 20)
        xr = int(hx + 2 - t * 14)
        c.line(xl, y, xr, y, C_HAIR_SHADE)
        c.line(xl + 1, y, xr - 1, y, C_HAIR_BASE)

    # Low aerodynamic hourglass dash pose
    draw_hourglass_body(c, hx, hy + 13, breath=0, leg_pose='run', leg_arg=2 if frame_num == 1 else 4)
    draw_female_head_and_face(c, hx, hy, expr='focused', mouth='smirk')

    # Staff tucked forward horizontally
    c.line(hx + 7, hy + 16, hx + 18, hy + 19, C_SKIN_BASE)
    draw_staff(c, hx + 24, hy + 18, angle_deg=85, length=44, orb_pulse=2, cast_glow=True)

    # Speed streaks behind tight bodysuit
    for sy in [28, 34, 42, 48, 54]:
        c.line(hx - 28, sy, hx - 12, sy, C_MAGIC_CYAN)
        c.line(hx - 22, sy + 1, hx - 8, sy + 1, C_MAGIC_PINK)

    return c

def create_defeat_frame():
    c = PixelCanvas(64, 72)
    hx = 30
    hy = 24

    # Hair draped down sorrowfully over shoulders
    for i in range(12, 38):
        t = (i - 12) / 26.0
        y = hy + i
        c.line(hx - 10, y, hx - 5, y, C_HAIR_BASE)
        c.line(hx + 5, y, hx + 10, y, C_HAIR_BASE)

    # Kneeling body
    draw_hourglass_body(c, hx, hy + 14, breath=0, leg_pose='kneel')

    # Head bowed down
    draw_female_head_and_face(c, hx, hy, expr='sad', mouth='normal')

    # Arms drooping down
    c.line(hx - 7, hy + 17, hx - 9, hy + 30, C_SKIN_BASE)
    c.line(hx + 7, hy + 17, hx + 9, hy + 30, C_SKIN_BASE)

    # Staff lying on the ground beside her
    draw_staff(c, hx + 22, hy + 38, angle_deg=100, length=42, orb_pulse=0.5, cast_glow=False)

    return c

print("All frame generation functions created successfully.")
