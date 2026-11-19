import os, sys, math
sys.path.append(os.path.abspath('scratch'))
from pixel_canvas import PixelCanvas
from design_128_summoner import (
    draw_staff_128, draw_head_128, draw_white_cape_128, draw_beauty_queen_body_128,
    draw_toned_leg_128, draw_toned_arm_128,
    C_OUTLINE, C_SKIN_BASE, C_SKIN_SHADE, C_SKIN_DEEP, C_SKIN_HILIGHT,
    C_HAIR_BASE, C_HAIR_SHADE, C_HAIR_DEEP, C_HAIR_SHINE,
    C_CAPE_WHITE, C_CAPE_BASE, C_CAPE_SHADE, C_CAPE_DEEP,
    C_RUBY_BASE, C_RUBY_HILIGHT, C_RUBY_SHADE,
    C_SUIT_BASE, C_SUIT_SHADE, C_SUIT_HILIGHT, C_SUIT_SHEEN,
    C_GOLD_BASE, C_GOLD_SHADE, C_GOLD_HILIGHT,
    C_STOCKING_BASE, C_STOCKING_SHADE, C_STOCKING_LIGHT,
    C_BOOT_BASE, C_BOOT_SHADE, C_BOOT_HILIGHT,
    C_ORB_CORE, C_ORB_BRIGHT, C_ORB_BASE, C_ORB_SHADE, C_ORB_GLOW,
    C_MAGIC_CYAN, C_MAGIC_PINK
)

def create_idle_frame_128(frame_num):
    c = PixelCanvas(128, 144)
    hx = 56
    hy = 26 if frame_num == 1 else 28
    bob = 0 if frame_num == 1 else 2
    tx = hx
    ty = hy + 28

    # White cape billowing behind
    draw_white_cape_128(c, tx, ty, billow_dx=0 if frame_num == 1 else -4)

    # Back toned leg (left leg, supporting stance)
    draw_toned_leg_128(c, tx - 5, ty + 34, tx - 5, ty + 54, tx - 5, ty + 74, foot_dx=2)

    # Front toned leg (right leg, shapely 3/4 stance, beauty queen 1m67)
    draw_toned_leg_128(c, tx + 7, ty + 34, tx + 9, ty + 54, tx + 9, ty + 74, foot_dx=5)

    # Hourglass body with V1=100 (exposed bust), V2=60, V3=90
    draw_beauty_queen_body_128(c, tx, ty, breath=bob)

    # 3/4 Head & Face
    draw_head_128(c, hx, hy, expr='normal', mouth='smirk')

    # Left toned arm (resting gracefully on hip)
    draw_toned_arm_128(c, tx - 10, ty + 8, tx - 18, ty + 20, tx - 13, ty + 31)

    # Right toned arm (holding staff forward)
    arm_sway = 0 if frame_num == 1 else 2
    draw_toned_arm_128(c, tx + 14, ty + 10, tx + 24 + arm_sway, ty + 20, tx + 31 + arm_sway, ty + 30)

    # Staff with signature ring & glowing orb
    staff_x = tx + 35 + arm_sway
    staff_y = hy + 14 + bob
    draw_staff_128(c, staff_x, staff_y, angle_deg=-2, length=88, orb_pulse=1 if frame_num == 1 else 2, cast_swirl=True)

    return c

def create_move_frame_128(frame_num):
    c = PixelCanvas(128, 144)
    hx = 52 + (2 if frame_num in [2, 4] else 0)
    hy = 26 + (0 if frame_num in [1, 3] else -2)
    tx = hx
    ty = hy + 28

    # Trailing cape
    draw_white_cape_128(c, tx, ty, billow_dx=-20, billow_w=16)

    # 4-stage Running Cycle with long, toned, beauty-queen legs
    ly = ty + 34
    if frame_num == 1:
        # Left leg back, right leg forward
        draw_toned_leg_128(c, tx - 5, ly, tx - 15, ly + 16, tx - 25, ly + 32, foot_dx=-3)
        draw_toned_leg_128(c, tx + 7, ly, tx + 16, ly + 16, tx + 20, ly + 38, foot_dx=5)
    elif frame_num == 2:
        draw_toned_leg_128(c, tx - 5, ly, tx - 4, ly + 16, tx - 4, ly + 38, foot_dx=3)
        draw_toned_leg_128(c, tx + 7, ly, tx + 14, ly + 14, tx - 2, ly + 28, foot_dx=-2)
    elif frame_num == 3:
        draw_toned_leg_128(c, tx - 5, ly, tx + 14, ly + 16, tx + 18, ly + 38, foot_dx=5)
        draw_toned_leg_128(c, tx + 7, ly, tx - 14, ly + 16, tx - 26, ly + 32, foot_dx=-3)
    else:
        draw_toned_leg_128(c, tx - 5, ly, tx - 2, ly + 16, tx + 6, ly + 38, foot_dx=3)
        draw_toned_leg_128(c, tx + 7, ly, tx + 15, ly + 14, tx + 2, ly + 30, foot_dx=0)

    draw_beauty_queen_body_128(c, tx, ty, breath=0)
    draw_head_128(c, hx, hy, expr='focused', mouth='smirk')

    # Left arm swinging
    if frame_num in [1, 2]:
        draw_toned_arm_128(c, tx - 10, ty + 8, tx - 20, ty + 18, tx - 25, ty + 28)
    else:
        draw_toned_arm_128(c, tx - 10, ty + 8, tx - 2, ty + 18, tx + 4, ty + 28)

    # Right arm holding staff forward
    sway = 4 if frame_num in [1, 3] else -2
    draw_toned_arm_128(c, tx + 14, ty + 10, tx + 26 + sway, ty + 18, tx + 34 + sway, ty + 26)

    staff_x = tx + 36 + sway
    staff_y = hy + 12
    draw_staff_128(c, staff_x, staff_y, angle_deg=-12, length=86, orb_pulse=1, cast_swirl=True)

    return c

def create_jump_frame_128():
    c = PixelCanvas(128, 144)
    hx = 56
    hy = 18
    tx = hx
    ty = hy + 28

    # Cape expanding like angel wings (Concept Jump pose!)
    for cy in range(ty, ty + 70):
        t = (cy - ty) / 70.0
        c.line(int(tx - 16 - t * 32), cy, int(tx - 6 - t * 16), cy, C_CAPE_SHADE)
        c.line(int(tx - 14 - t * 32), cy, int(tx - 8 - t * 16), cy, C_CAPE_BASE)
        c.line(int(tx + 20 + t * 12), cy, int(tx + 28 + t * 28), cy, C_CAPE_SHADE)
        c.line(int(tx + 20 + t * 12), cy, int(tx + 26 + t * 28), cy, C_CAPE_BASE)

    # Bent toned legs tucked back gracefully
    draw_toned_leg_128(c, tx - 5, ty + 34, tx - 18, ty + 46, tx - 24, ty + 58, foot_dx=-3)
    draw_toned_leg_128(c, tx + 7, ty + 34, tx - 2, ty + 48, tx - 8, ty + 62, foot_dx=-2)

    draw_beauty_queen_body_128(c, tx, ty, breath=0)
    draw_head_128(c, hx, hy, expr='excited', mouth='smile')

    # Left arm raised joyfully
    draw_toned_arm_128(c, tx - 10, ty + 8, tx - 22, ty - 2, tx - 30, ty - 12)

    # Right arm raising staff high into the air
    draw_toned_arm_128(c, tx + 14, ty + 10, tx + 26, ty - 2, tx + 34, ty - 14)

    draw_staff_128(c, tx + 36, hy - 4, angle_deg=-25, length=86, orb_pulse=3, cast_swirl=True)

    return c

def create_fall_frame_128():
    c = PixelCanvas(128, 144)
    hx = 56
    hy = 22
    tx = hx
    ty = hy + 28

    # Cape floating up
    for cy in range(ty - 8, ty + 56):
        t = (cy - (ty - 8)) / 64.0
        c.line(int(tx - 12 - t * 28), cy, int(tx - 2 - t * 8), cy, C_CAPE_SHADE)
        c.line(int(tx - 10 - t * 28), cy, int(tx - 4 - t * 8), cy, C_CAPE_BASE)

    # Toned legs trailing down
    draw_toned_leg_128(c, tx - 5, ty + 34, tx - 7, ty + 50, tx - 9, ty + 70, foot_dx=3)
    draw_toned_leg_128(c, tx + 7, ty + 34, tx + 9, ty + 50, tx + 11, ty + 72, foot_dx=3)

    draw_beauty_queen_body_128(c, tx, ty, breath=0)
    draw_head_128(c, hx, hy, expr='focused', mouth='normal')

    # Floating arms
    draw_toned_arm_128(c, tx - 10, ty + 8, tx - 22, ty + 16, tx - 28, ty + 26)
    draw_toned_arm_128(c, tx + 14, ty + 10, tx + 24, ty + 20, tx + 30, ty + 32)

    draw_staff_128(c, tx + 32, hy + 16, angle_deg=18, length=86, orb_pulse=1, cast_swirl=True)

    return c

def create_attack_frame_128(frame_num):
    c = PixelCanvas(128, 144)
    hx = 50 if frame_num != 2 else 54
    hy = 28
    tx = hx
    ty = hy + 28

    # Cape
    draw_white_cape_128(c, tx, ty, billow_dx=-24 if frame_num == 2 else -12, billow_w=12)

    # Broad solid combat stance
    draw_toned_leg_128(c, tx - 5, ty + 34, tx - 16, ty + 50, tx - 24, ty + 70, foot_dx=-3)
    draw_toned_leg_128(c, tx + 7, ty + 34, tx + 16, ty + 50, tx + 22, ty + 72, foot_dx=5)

    draw_beauty_queen_body_128(c, tx, ty, breath=0)
    draw_head_128(c, hx, hy, expr='fierce' if frame_num == 2 else 'focused', mouth='open' if frame_num == 2 else 'smirk')

    if frame_num == 1:
        # Pull staff back
        draw_toned_arm_128(c, tx - 10, ty + 8, tx - 18, ty + 18, tx - 22, ty + 28)
        draw_toned_arm_128(c, tx + 14, ty + 10, tx + 6, ty + 18, tx - 4, ty + 26)
        draw_staff_128(c, tx - 14, hy + 4, angle_deg=-35, length=88, orb_pulse=2, cast_swirl=True)

    elif frame_num == 2:
        # Thrust horizontal (Signature ATTACK pose from Concept Sheet!)
        draw_toned_arm_128(c, tx - 10, ty + 8, tx - 4, ty + 20, tx + 2, ty + 30)
        # Thick toned right arm thrusting forward horizontally!
        draw_toned_arm_128(c, tx + 14, ty + 10, tx + 34, ty + 12, tx + 50, ty + 14)

        staff_x = tx + 54
        staff_y = hy + 42
        draw_staff_128(c, staff_x, staff_y, angle_deg=82, length=86, orb_pulse=3, cast_swirl=True)

        # Concentric swirling pastel cyan & pink magic rings from concept sheet
        c.circle(staff_x, staff_y, 16, (112, 243, 255, 180), fill=False)
        c.circle(staff_x, staff_y, 24, (255, 113, 206, 160), fill=False)
        c.circle(staff_x, staff_y, 32, (200, 100, 245, 130), fill=False)

    else:
        # Projectile blast
        draw_toned_arm_128(c, tx + 14, ty + 10, tx + 36, ty + 14, tx + 48, ty + 18)
        draw_staff_128(c, tx + 50, hy + 34, angle_deg=70, length=84, orb_pulse=2, cast_swirl=True)

        proj_x = 108
        proj_y = 60
        c.circle(proj_x, proj_y, 14, C_ORB_GLOW, fill=False)
        c.circle(proj_x, proj_y, 10, C_ORB_BASE, fill=True)
        c.circle(proj_x, proj_y, 6, C_MAGIC_CYAN, fill=True)
        c.circle(proj_x, proj_y, 2, C_ORB_CORE, fill=True)
        c.line(proj_x - 24, proj_y, proj_x - 8, proj_y, C_MAGIC_PINK)
        c.line(proj_x - 20, proj_y - 6, proj_x - 6, proj_y - 2, C_MAGIC_CYAN)
        c.line(proj_x - 20, proj_y + 6, proj_x - 6, proj_y + 2, C_MAGIC_CYAN)

    return c

def create_skill_frame_128(frame_num):
    # Concept Sheet CASTING pose!
    c = PixelCanvas(128, 144)
    hx = 56
    hy = 26
    tx = hx
    ty = hy + 28

    # Glowing Summoning Circle beneath feet (from concept sheet!)
    ground_y = 132
    c.circle(tx, ground_y, 34, (255, 113, 206, 130), fill=False)
    c.line(tx - 38, ground_y, tx + 38, ground_y, C_MAGIC_PINK)
    c.line(tx - 30, ground_y - 2, tx + 30, ground_y - 2, C_MAGIC_CYAN)
    c.line(tx - 30, ground_y + 2, tx + 30, ground_y + 2, C_MAGIC_CYAN)

    # Wide casting stance with both toned legs planted firm
    draw_toned_leg_128(c, tx - 5, ty + 34, tx - 18, ty + 50, tx - 26, ty + 72, foot_dx=-3)
    draw_toned_leg_128(c, tx + 7, ty + 34, tx + 18, ty + 50, tx + 26, ty + 72, foot_dx=5)

    draw_white_cape_128(c, tx, ty, billow_dx=-12, billow_w=8)
    draw_beauty_queen_body_128(c, tx, ty, breath=2)
    draw_head_128(c, hx, hy, expr='fierce' if frame_num == 2 else 'focused', mouth='open' if frame_num == 2 else 'smirk')

    # Left arm casting magic forward
    draw_toned_arm_128(c, tx - 10, ty + 8, tx - 26, ty + 10, tx - 38, ty + 12)

    # Glowing rune circle in front of left palm (Concept Casting!)
    seal_x = tx - 42
    seal_y = ty + 12
    c.circle(seal_x, seal_y, 14, C_MAGIC_PINK, fill=False)
    c.circle(seal_x, seal_y, 10, C_MAGIC_CYAN, fill=False)
    c.circle(seal_x, seal_y, 2, C_ORB_CORE, fill=True)

    # Right arm holding staff aloft
    draw_toned_arm_128(c, tx + 14, ty + 10, tx + 28, ty - 2, tx + 36, ty - 14)
    draw_staff_128(c, tx + 36, hy - 4, angle_deg=-15, length=88, orb_pulse=4 if frame_num == 2 else 2, cast_swirl=True)

    if frame_num == 3:
        # Spirit beast crest
        c.line(tx - 44, hy + 8, tx - 24, hy + 26, C_MAGIC_PINK)
        c.line(tx + 12, hy + 26, tx + 48, hy + 6, C_MAGIC_PINK)

    return c

def create_finisher_frame_128(frame_num):
    c = PixelCanvas(128, 144)
    hx = 56
    hy = 26
    tx = hx
    ty = hy + 28

    c.circle(tx, 80, 56, C_ORB_GLOW, fill=False)

    draw_toned_leg_128(c, tx - 5, ty + 34, tx - 7, ty + 54, tx - 7, ty + 74, foot_dx=2)
    draw_toned_leg_128(c, tx + 7, ty + 34, tx + 9, ty + 54, tx + 9, ty + 74, foot_dx=5)

    draw_white_cape_128(c, tx, ty, billow_dx=0, billow_w=8)
    draw_beauty_queen_body_128(c, tx, ty, breath=2)
    draw_head_128(c, hx, hy, expr='fierce', mouth='open')

    if frame_num == 2:
        # Celestial light pillar
        for y in range(0, 144):
            c.set(tx - 4, y, (255, 255, 255, 120))
            c.set(tx - 2, y, (240, 168, 255, 180))
            c.set(tx, y, (255, 255, 255, 255))
            c.set(tx + 2, y, (240, 168, 255, 180))
            c.set(tx + 4, y, (255, 255, 255, 120))

    draw_toned_arm_128(c, tx - 10, ty + 8, tx - 2, ty - 2, tx + 2, ty - 12)
    draw_toned_arm_128(c, tx + 14, ty + 10, tx + 8, ty - 2, tx + 4, ty - 12)

    draw_staff_128(c, tx + 2, hy - 12, angle_deg=0, length=88, orb_pulse=5 if frame_num == 2 else 3, cast_swirl=True)

    if frame_num == 3:
        for rad_r in [28, 44, 60]:
            c.circle(tx + 50, 72, rad_r, (255, 113, 206, 120), fill=False)

    return c

def create_dash_frame_128(frame_num):
    c = PixelCanvas(128, 144)
    hx = 60 if frame_num == 1 else 66
    hy = 34
    tx = hx
    ty = hy + 26

    draw_white_cape_128(c, tx, ty, billow_dx=-32, billow_w=24)

    ly = ty + 34
    draw_toned_leg_128(c, tx - 5, ly, tx - 14, ly + 12, tx - 26, ly + 28, foot_dx=-2)
    draw_toned_leg_128(c, tx + 7, ly, tx + 12, ly + 12, tx + 6, ly + 32, foot_dx=4)

    draw_beauty_queen_body_128(c, tx, ty, breath=0)
    draw_head_128(c, hx, hy, expr='focused', mouth='smirk')

    draw_toned_arm_128(c, tx + 14, ty + 8, tx + 32, ty + 12, tx + 46, ty + 16)
    draw_staff_128(c, tx + 50, hy + 38, angle_deg=85, length=86, orb_pulse=2, cast_swirl=True)

    for sy in [56, 72, 88, 104]:
        c.line(tx - 60, sy, tx - 28, sy, C_MAGIC_CYAN)

    return c

def create_defeat_frame_128():
    c = PixelCanvas(128, 144)
    hx = 56
    hy = 48
    tx = hx
    ty = hy + 26

    draw_white_cape_128(c, tx, ty, billow_dx=0, billow_w=0)

    # Folded toned legs on ground
    c.circle(tx - 8, ty + 34, 10.0, C_STOCKING_BASE, fill=True)
    c.circle(tx + 8, ty + 34, 10.0, C_STOCKING_BASE, fill=True)
    c.rect(tx - 24, ty + 38, 48, 12, C_BOOT_BASE)

    draw_beauty_queen_body_128(c, tx, ty, breath=0)
    draw_head_128(c, hx, hy, expr='sad', mouth='normal')

    draw_toned_arm_128(c, tx - 10, ty + 8, tx - 16, ty + 22, tx - 18, ty + 36)
    draw_toned_arm_128(c, tx + 14, ty + 10, tx + 18, ty + 22, tx + 20, ty + 36)

    draw_staff_128(c, tx + 44, hy + 76, angle_deg=100, length=84, orb_pulse=0.5, cast_swirl=False)

    return c

print("build_all_frames_128 loaded successfully.")
