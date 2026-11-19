import os, sys, math
sys.path.append(os.path.abspath('scratch'))
from pixel_canvas import PixelCanvas

# ==============================================================================
# 👑 DARK KING (VUA BÓNG TỐI) — TRUE NATIVE 128x144 64-BIT PIXEL ART PALETTE
# ==============================================================================
C_OUTLINE       = '#08060c'
C_VOID_BLACK    = '#0d0b14'
C_SUIT_DEEP     = '#14111f'
C_SUIT_BASE     = '#1d192b'
C_SUIT_MID      = '#29233d'
C_SUIT_LIGHT    = '#3a3254'
C_SUIT_SPEC     = '#534778'

C_CAPE_OUTER    = '#120f1c'
C_CAPE_FOLD     = '#1f1a30'
C_CAPE_RIM      = '#342b4f'
C_CAPE_INNER_DP = '#231338'
C_CAPE_INNER    = '#381e59'
C_CAPE_INNER_HI = '#522c80'

C_PURPLE_DARK   = '#3c1769'
C_PURPLE_ROYAL  = '#6228a8'
C_PURPLE_BRIGHT = '#9346f0'
C_PURPLE_GLOW   = '#c17dff'
C_PURPLE_CORE   = '#f2e0ff'

C_CRIMSON_DEEP  = '#6e0d25'
C_CRIMSON_BASE  = '#bd193f'
C_CRIMSON_GLOW  = '#ff4772'

C_GOLD_OUTLINE  = '#472a05'
C_GOLD_DEEP     = '#7d4e0d'
C_GOLD_SHADE    = '#b87918'
C_GOLD_BASE     = '#e8a825'
C_GOLD_BRIGHT   = '#ffd24c'
C_GOLD_SPEC     = '#fff7bd'

C_SKIN_OUTLINE  = '#523428'
C_SKIN_DEEP     = '#b8866f'
C_SKIN_SHADE    = '#deb099'
C_SKIN_BASE     = '#f7d4c1'
C_SKIN_HILIGHT  = '#ffece0'

C_HAIR_OUTLINE  = '#06050a'
C_HAIR_BASE     = '#110f1a'
C_HAIR_MID      = '#1f1b30'
C_HAIR_HILIGHT  = '#383054'
C_HAIR_SPEC     = '#594d82'

C_BLADE_BLACK   = '#09070f'
C_BLADE_CORE    = '#191429'
C_BLADE_EDGE    = '#8e42eb'
C_BLADE_GLOW    = '#d19eff'
C_BLADE_WHITE   = '#ffffff'


def draw_dark_aura_128(c, cx, cy, phase=0.0, intensity=1.0):
    """
    Draws the swirling Dark King shadowy aura ('bá khí hắc ám') with
    organic S-curved shadowy tendrils, purple-black energy flames, and rising embers.
    """
    # Ground shadow vortex beneath feet
    gy = 135
    c.ellipse(cx, gy, int(28 * intensity), 5, (14, 10, 24, 160), fill=True)
    c.ellipse(cx, gy, int(20 * intensity), 3, (56, 24, 96, 185), fill=True)
    c.ellipse(cx, gy, int(31 * intensity), 6, (147, 70, 240, 120), fill=False)

    # Organic S-curved dark flame wisps swirling around torso & cape
    wisp_anchors = [
        (cx - 26, cy + 28, -1.0, 22),
        (cx + 22, cy + 20,  1.0, 20),
        (cx - 18, cy - 4,  -0.8, 18),
        (cx + 18, cy - 12,  0.8, 16),
        (cx - 34, cy + 44, -1.2, 20),
    ]
    for idx, (ax, ay, side, h_len) in enumerate(wisp_anchors):
        if idx >= int(5 * intensity + 0.5):
            break
        p_off = (phase + idx * 0.22) % 1.0
        wy_base = ay - p_off * 14
        # Draw tapered S-curve flame tendril from bottom to tip
        steps = 12
        for s in range(steps):
            t = s / float(steps - 1)
            curve_x = ax + side * math.sin(t * math.pi * 1.4 + phase * math.pi * 2) * 4.5
            curve_y = wy_base - t * h_len
            rad = (1.0 - t) * 2.4 + 0.6
            # Outer dark void smoke
            c.circle(curve_x, curve_y, rad + 1.0, (18, 9, 32, int(130 * (1.0 - t * 0.6))), fill=True)
            # Inner royal purple flame
            c.circle(curve_x, curve_y, rad * 0.65, (125, 50, 215, int(175 * (1.0 - t * 0.5))), fill=True)
            if s in (2, 5):
                c.set(curve_x, curve_y, (193, 125, 255, 210))

    # Crisp pixel embers rising around the Dark King
    ember_offsets = [
        (-22, -24), (20, -28), (-30, 8), (26, 4), (-14, -36), (15, -38), (-38, 26), (28, -14)
    ]
    for idx, (ex, ey) in enumerate(ember_offsets):
        p_shift = int(((phase * 24 + idx * 7) % 18))
        px = int(cx + ex + math.sin(phase * 2 * math.pi + idx) * 3)
        py = int(cy + ey - p_shift)
        col = C_PURPLE_CORE if idx % 3 == 0 else (C_PURPLE_GLOW if idx % 2 == 0 else C_PURPLE_BRIGHT)
        c.set(px, py, col)
        c.set(px, py + 1, (98, 40, 168, 180))


def draw_flowing_royal_cape_128(c, shoulder_x, shoulder_y, waist_x, waist_y,
                                billow_dx=-28, billow_dy=0, spread=1.0, wave_phase=0.0):
    """
    Draws the massive, solid, multi-layered gothic black & royal-purple cloak
    with deep cloth folds, velvet inner lining, and ragged demon-king hems.
    Zero gaps or disconnected lines — rendered with solid overlapping polygons!
    """
    # 5 major cape folds fanning behind the character (to the left: x < shoulder_x)
    base_top_l = (shoulder_x - 14, shoulder_y + 2)
    base_top_r = (shoulder_x + 12, shoulder_y + 4)

    # Calculate bottom hem points with natural wave physics
    hem_y_base = 128 + billow_dy
    hem_pts = []
    num_spikes = 6
    for i in range(num_spikes):
        t = i / float(num_spikes - 1)
        wave_x = math.sin(wave_phase * 2 * math.pi + i * 1.1) * 4.5
        wave_y = math.cos(wave_phase * 2 * math.pi + i * 1.3) * 3.5
        hx = (shoulder_x - 42 * spread + billow_dx) + t * (48 * spread - billow_dx * 0.45) + wave_x
        hy = hem_y_base - (1.0 - t) * 14 + (i % 2) * 8 + wave_y
        hem_pts.append((hx, hy))

    # 1. Inner purple-black velvet lining polygon (visible underneath and between jagged tears)
    lining_poly = [base_top_l, base_top_r, (waist_x + 14, waist_y + 18)]
    for hx, hy in reversed(hem_pts):
        lining_poly.append((hx + 3, hy + 3))
    c.polygon(lining_poly, C_CAPE_INNER_DP, outline_col=C_OUTLINE)

    # Inner purple sheen bands
    for i in range(len(hem_pts) - 1):
        p0 = hem_pts[i]
        p1 = hem_pts[i + 1]
        mid_x = (p0[0] + p1[0]) * 0.5 + 3
        mid_y = (p0[1] + p1[1]) * 0.5 - 6
        c.polygon([
            (shoulder_x - 4, shoulder_y + 14),
            (p0[0] + 2, p0[1] + 2),
            (mid_x, mid_y),
            (p1[0] + 2, p1[1] + 2)
        ], C_CAPE_INNER)

    # 2. Main outer black cloak shell with jagged gothic tails
    outer_poly = [
        (shoulder_x - 15, shoulder_y + 1),
        (shoulder_x + 11, shoulder_y + 3),
        (waist_x + 10, waist_y + 12)
    ]
    # Add jagged peaks and valleys along the bottom hem
    for i in range(len(hem_pts) - 1, -1, -1):
        hx, hy = hem_pts[i]
        outer_poly.append((hx, hy))
        if i > 0:
            nx, ny = hem_pts[i - 1]
            valley_x = (hx + nx) * 0.5 + 4
            valley_y = (hy + ny) * 0.5 - 11
            outer_poly.append((valley_x, valley_y))
    # Back sweep curve from leftmost tail up to shoulder
    left_tip = hem_pts[0]
    outer_poly.append(( (left_tip[0] + shoulder_x - 18) * 0.5 - 6, (left_tip[1] + shoulder_y) * 0.5 ))
    c.polygon(outer_poly, C_CAPE_OUTER, outline_col=C_OUTLINE)

    # 3. Sculpted cloth folds (volumetric shading & rim highlights)
    for i, (hx, hy) in enumerate(hem_pts):
        sx = shoulder_x - 10 + i * 3.5
        sy = shoulder_y + 6 + i * 1.5
        fold_col = C_CAPE_FOLD if i % 2 == 0 else C_SUIT_MID
        c.capsule(sx, sy, hx + 2, hy - 3, 2.5, 1.2, fold_col)
        if i in (0, 2, 4):
            c.line(sx - 1, sy, hx, hy - 2, C_CAPE_RIM)

    # 4. Gold & Purple royal trim along the front sweeping edge of the cloak
    front_tail = hem_pts[-1]
    c.line(shoulder_x + 10, shoulder_y + 6, waist_x + 9, waist_y + 12, C_PURPLE_ROYAL, thickness=2)
    c.line(waist_x + 9, waist_y + 12, front_tail[0], front_tail[1], C_PURPLE_ROYAL, thickness=2)
    c.line(shoulder_x + 11, shoulder_y + 6, waist_x + 10, waist_y + 12, C_GOLD_SHADE)
    c.line(waist_x + 10, waist_y + 12, front_tail[0] + 1, front_tail[1], C_GOLD_BASE)


def draw_boot_leg_128(c, hip_x, hip_y, knee_x, knee_y, ankle_x, ankle_y,
                      foot_dir=1, is_front=True):
    """
    Draws a muscular, well-proportioned human leg in fitted dark combat trousers
    with purple diamond thigh motifs and gold-trimmed gothic armored greaves/boots.
    """
    thigh_base  = C_SUIT_BASE if is_front else C_SUIT_DEEP
    thigh_shade = C_SUIT_DEEP if is_front else C_VOID_BLACK
    thigh_hi    = C_SUIT_LIGHT if is_front else C_SUIT_BASE

    # 1. Muscular Thigh (radius 7.2 -> 5.4, thickness ~14.5px!)
    c.capsule(hip_x, hip_y, knee_x, knee_y, 7.2, 5.4,
              thigh_base, shade_col=thigh_shade, hi_col=thigh_hi, outline_col=C_OUTLINE)

    # Subtle purple diamond/chevron pattern on front thigh (from reference Image 1)
    if is_front:
        mx = (hip_x + knee_x) * 0.5 + 1
        my = (hip_y + knee_y) * 0.5
        c.line(mx, my - 4, mx + 2, my, C_PURPLE_ROYAL)
        c.line(mx + 2, my, mx, my + 4, C_PURPLE_ROYAL)
        c.line(mx, my + 4, mx - 2, my, C_PURPLE_DARK)
        c.line(mx - 2, my, mx, my - 4, C_PURPLE_DARK)
        c.set(mx, my, C_PURPLE_GLOW)

    # 2. Armored Calf / Greave (radius 5.5 -> 4.2)
    boot_base  = C_SUIT_MID if is_front else C_SUIT_DEEP
    boot_shade = C_VOID_BLACK
    boot_hi    = C_SUIT_SPEC if is_front else C_SUIT_MID
    c.capsule(knee_x, knee_y, ankle_x, ankle_y, 5.6, 4.2,
              boot_base, shade_col=boot_shade, hi_col=boot_hi, outline_col=C_OUTLINE)

    # 3. Gothic Pointed Knee Guard (Purple cowl + Gold V-chevron)
    kx, ky = int(round(knee_x)), int(round(knee_y))
    knee_poly = [
        (kx - 5, ky - 2),
        (kx + 6, ky - 2),
        (kx + 5, ky + 4),
        (kx + 1, ky + 7),
        (kx - 4, ky + 4)
    ]
    c.polygon(knee_poly, C_PURPLE_DARK if is_front else C_SUIT_DEEP, outline_col=C_OUTLINE)
    # Gleaming Gold V-trim on knee
    c.line(kx - 4, ky - 1, kx + 1, ky + 4, C_GOLD_BASE)
    c.line(kx + 1, ky + 4, kx + 5, ky - 1, C_GOLD_BRIGHT if is_front else C_GOLD_SHADE)
    if is_front:
        c.set(kx + 1, ky + 4, C_GOLD_SPEC)

    # Horizontal gold ring strap on mid-boot
    sx = (knee_x + ankle_x) * 0.5
    sy = (knee_y + ankle_y) * 0.5 - 1
    c.line(sx - 4, sy, sx + 5, sy, C_GOLD_BASE if is_front else C_GOLD_DEEP)

    # 4. Armored Foot & Gold Pointed Toe Cap (3/4 forward-right angle)
    ax, ay = int(round(ankle_x)), int(round(ankle_y))
    toe_len = 11 if is_front else 9
    foot_poly = [
        (ax - 5, ay - 2),
        (ax + 4, ay - 2),
        (ax + toe_len, ay + 3),
        (ax + toe_len + 1, ay + 6),
        (ax - 5, ay + 6)
    ]
    c.polygon(foot_poly, C_VOID_BLACK if not is_front else C_SUIT_DEEP, outline_col=C_OUTLINE)
    # Gold chevron toe trim (from reference images!)
    c.line(ax + 3, ay + 1, ax + toe_len - 1, ay + 4, C_GOLD_BASE if is_front else C_GOLD_DEEP)
    c.line(ax + toe_len - 1, ay + 4, ax + 4, ay + 5, C_GOLD_BRIGHT if is_front else C_GOLD_SHADE)
    if is_front:
        c.set(ax + toe_len - 1, ay + 4, C_GOLD_SPEC)


def draw_royal_torso_128(c, tx, ty, lean_dx=0):
    """
    Draws the fitted sleek black royal combat coat in a 3/4 forward-right stance:
    - Broad athletic shoulders (~32px), tapering to a trim 20px waist
    - Ribbed chevron chest armor plate
    - Purple inner lapel trims & crimson-purple throat gem
    - Double horizontal gold waist bands + X-crossed gold belts
    - Flared coat-tail panels over the hips
    """
    sx = tx + lean_dx
    sy = ty

    # 1. Flared coat flaps over hips (ty + 22 to ty + 42)
    left_flap = [
        (tx - 9, ty + 22),
        (tx - 1, ty + 22),
        (tx - 4, ty + 40),
        (tx - 16, ty + 38)
    ]
    right_flap = [
        (tx + 1, ty + 22),
        (tx + 11, ty + 22),
        (tx + 17, ty + 38),
        (tx + 6, ty + 40)
    ]
    c.polygon(left_flap, C_SUIT_DEEP, outline_col=C_OUTLINE)
    c.polygon(right_flap, C_SUIT_BASE, outline_col=C_OUTLINE)
    # Gold & purple trim on coat flaps
    c.line(tx - 15, ty + 37, tx - 8, ty + 22, C_PURPLE_ROYAL)
    c.line(tx + 10, ty + 22, tx + 16, ty + 37, C_GOLD_BASE)

    # 2. Main V-Taper Torso Polygon (3/4 angle: center of chest is at tx + 2)
    torso_poly = [
        (sx - 14, sy + 2),   # Left shoulder (back)
        (sx - 6,  sy - 1),   # Left traps
        (sx + 8,  sy - 1),   # Right traps
        (sx + 16, sy + 2),   # Right shoulder (front)
        (tx + 11, ty + 23),  # Right waist
        (tx - 9,  ty + 23)   # Left waist
    ]
    c.polygon(torso_poly, C_SUIT_BASE, outline_col=C_OUTLINE)

    # 3/4 shading on left (back) side of torso, highlight on right (front-facing) pectoral
    back_shade_poly = [
        (sx - 13, sy + 3),
        (sx - 3,  sy + 1),
        (tx - 2,  ty + 22),
        (tx - 8,  ty + 22)
    ]
    c.polygon(back_shade_poly, C_SUIT_DEEP)

    chest_hi_poly = [
        (sx + 3,  sy + 3),
        (sx + 13, sy + 4),
        (tx + 9,  ty + 15),
        (tx + 3,  ty + 15)
    ]
    c.polygon(chest_hi_poly, C_SUIT_MID)

    # 3. Center Ribbed Chevron Breastplate (Shadow's iconic segmented black armor)
    cx = sx + 2
    for i in range(6):
        ry = sy + 4 + i * 3
        w = 6 - int(i * 0.4)
        c.line(cx - w, ry, cx, ry + 2, C_SUIT_LIGHT)
        c.line(cx, ry + 2, cx + w, ry, C_SUIT_SPEC)
        c.line(cx - w, ry + 1, cx, ry + 3, C_OUTLINE)
        c.line(cx, ry + 3, cx + w, ry + 1, C_OUTLINE)

    # 4. Purple Royal Lapels & Gold Collar Clasp
    # Left lapel
    c.line(sx - 6, sy + 2, tx - 3, ty + 18, C_PURPLE_ROYAL, thickness=2)
    c.line(sx - 8, sy + 4, sx - 5, sy + 6, C_GOLD_BASE)
    # Right lapel
    c.line(sx + 9, sy + 2, tx + 6, ty + 18, C_PURPLE_BRIGHT, thickness=2)
    c.line(sx + 10, sy + 4, sx + 7, sy + 6, C_GOLD_BRIGHT)

    # Diamond ruby/amethyst brooch at throat (cx, sy + 2)
    c.polygon([(cx, sy), (cx + 2, sy + 2), (cx, sy + 4), (cx - 2, sy + 2)], C_CRIMSON_BASE)
    c.set(cx, sy + 1, C_CRIMSON_GLOW)
    c.set(cx, sy, C_GOLD_SPEC)

    # 5. Double Gold Waist Bands + X-Crossed Gold Belts (from reference Images 1-3)
    wy = ty + 19
    c.line(tx - 8, wy, tx + 10, wy, C_GOLD_BASE)
    c.line(tx - 8, wy + 2, tx + 10, wy + 2, C_GOLD_BRIGHT)
    # X-crossed diagonal belts over hips
    c.line(tx - 8, wy + 3, tx + 11, wy + 9, C_GOLD_SHADE, thickness=2)
    c.line(tx - 8, wy + 3, tx + 11, wy + 8, C_GOLD_BRIGHT)
    c.line(tx - 9, wy + 9, tx + 10, wy + 3, C_GOLD_SHADE, thickness=2)
    c.line(tx - 9, wy + 8, tx + 10, wy + 3, C_GOLD_BASE)
    # Center belt buckle
    c.rect(tx + 1, wy + 4, 3, 3, C_GOLD_SPEC)


def draw_flared_collar_back_128(c, nx, ny):
    """
    Draws the high, wide-flared dark royal collar (with purple inner lining and
    thick gleaming gold borders) that frames the neck and lower head.
    """
    # Left flared wing (extending back-left)
    left_wing = [
        (nx - 4,  ny + 6),
        (nx - 22, ny - 3),
        (nx - 14, ny - 9),
        (nx - 2,  ny + 1)
    ]
    c.polygon(left_wing, C_CAPE_INNER, outline_col=C_OUTLINE)
    c.line(nx - 4, ny + 6, nx - 22, ny - 3, C_GOLD_BASE, thickness=2)
    c.line(nx - 22, ny - 3, nx - 14, ny - 9, C_GOLD_BRIGHT, thickness=2)
    # Hanging gold tassel cord on left collar tip
    c.line(nx - 19, ny - 1, nx - 24, ny + 1, C_GOLD_SHADE)
    c.rect(nx - 25, ny, 2, 2, C_GOLD_BRIGHT)

    # Right flared wing (extending forward-right)
    right_wing = [
        (nx + 4,  ny + 6),
        (nx + 23, ny - 2),
        (nx + 15, ny - 8),
        (nx + 2,  ny + 1)
    ]
    c.polygon(right_wing, C_CAPE_INNER_HI, outline_col=C_OUTLINE)
    c.line(nx + 4, ny + 6, nx + 23, ny - 2, C_GOLD_BRIGHT, thickness=2)
    c.line(nx + 23, ny - 2, nx + 15, ny - 8, C_GOLD_SPEC)


def draw_head_and_golden_crown_128(c, hx, hy, expr='confident'):
    """
    Draws the handsome young adult human male Dark King head in strict 3/4 side profile
    facing forward-right (+X), with layered anime raven-black hair and an ornate,
    gleaming Golden Crown on his head.
    NEVER looks straight at the viewer/camera!
    """
    # 1. High Neck Collar & Neck Skin
    c.rect(hx - 4, hy + 12, 9, 7, C_SKIN_SHADE)
    c.rect(hx - 2, hy + 12, 6, 6, C_SKIN_BASE)
    # Dark high-neck turtleneck guard
    c.polygon([
        (hx - 5, hy + 15),
        (hx + 6, hy + 15),
        (hx + 7, hy + 20),
        (hx - 6, hy + 20)
    ], C_SUIT_DEEP, outline_col=C_OUTLINE)

    # 2. Back & Side Hair Mass (Raven black anime locks)
    back_hair = [
        (hx - 11, hy - 7),
        (hx + 9,  hy - 8),
        (hx + 12, hy + 1),
        (hx - 9,  hy + 14),
        (hx - 14, hy + 9),
        (hx - 14, hy - 1)
    ]
    c.polygon(back_hair, C_HAIR_BASE, outline_col=C_HAIR_OUTLINE)

    # 3. Sculpted 3/4 Anime Male Face Contour (facing forward-right)
    # Forehead at hy-2, nose bridge projecting to hx+10 at hy+6, sharp jawline to chin at hx+6, hy+13
    face_poly = [
        (hx - 4, hy - 2),
        (hx + 8, hy - 2),
        (hx + 9, hy + 3),
        (hx + 10, hy + 6),  # Nose projection (3/4 profile)
        (hx + 9, hy + 9),
        (hx + 6, hy + 13),  # Sharp handsome chin
        (hx - 1, hy + 12),  # Jawline angle
        (hx - 5, hy + 8)    # Ear / sideburn area
    ]
    c.polygon(face_poly, C_SKIN_BASE)

    # Volumetric facial shading (left side of face & under jaw shaded, cheekbone lit)
    shade_poly = [
        (hx - 5, hy - 1),
        (hx - 1, hy - 1),
        (hx,     hy + 11),
        (hx - 4, hy + 9)
    ]
    c.polygon(shade_poly, C_SKIN_SHADE)
    # Jawline crisp shadow & outline
    c.line(hx - 4, hy + 9, hx - 1, hy + 12, C_SKIN_OUTLINE)
    c.line(hx - 1, hy + 12, hx + 6, hy + 13, C_SKIN_OUTLINE)
    c.line(hx + 6, hy + 13, hx + 9, hy + 9, C_SKIN_OUTLINE)
    c.line(hx + 9, hy + 4, hx + 10, hy + 6, C_SKIN_OUTLINE) # Nose profile bridge
    # Cheekbone & nose bridge highlight
    c.line(hx + 3, hy + 6, hx + 6, hy + 6, C_SKIN_HILIGHT)
    c.set(hx + 9, hy + 5, C_SKIN_HILIGHT)

    # Ear (on left side of 3/4 head, partially framed by hair)
    c.rect(hx - 6, hy + 4, 2, 4, C_SKIN_SHADE)
    c.set(hx - 6, hy + 5, C_SKIN_DEEP)

    # 4. Sharp Anime Eyes Looking Strictly Forward-Right (3/4 perspective!)
    # Near eye (left side of face from viewer, hx+0 to hx+4)
    c.line(hx, hy + 3, hx + 4, hy + 4, C_OUTLINE) # Bold upper eyelashes
    c.line(hx - 1, hy + 2, hx + 4, hy + 3, C_HAIR_BASE) # Sharp eyebrow
    c.rect(hx + 1, hy + 4, 4, 3, '#ffffff') # Sclera
    # Iris positioned on the RIGHT side of the sclera so he looks FORWARD-RIGHT!
    eye_col = C_CRIMSON_GLOW if expr == 'fierce' else C_CRIMSON_BASE
    c.rect(hx + 2, hy + 4, 3, 3, eye_col)
    c.set(hx + 3, hy + 5, C_OUTLINE) # Pupil looking right
    c.set(hx + 2, hy + 4, '#ffffff') # Specular eye catchlight

    # Far eye (foreshortened near right edge of 3/4 face, hx+7 to hx+9)
    c.line(hx + 7, hy + 3, hx + 9, hy + 4, C_OUTLINE)
    c.line(hx + 7, hy + 2, hx + 9, hy + 2, C_HAIR_BASE)
    c.rect(hx + 7, hy + 4, 2, 3, '#ffffff')
    c.rect(hx + 8, hy + 4, 2, 3, eye_col)
    c.set(hx + 8, hy + 4, '#ffffff')

    # Confident smirk / battle expression
    if expr == 'fierce':
        c.rect(hx + 5, hy + 9, 3, 2, C_CRIMSON_DEEP)
        c.set(hx + 6, hy + 9, '#ffffff')
    else:
        c.line(hx + 4, hy + 10, hx + 7, hy + 9, C_SKIN_OUTLINE)

    # 5. Layered Anime Front & Side Bangs (framing face without obscuring eyes)
    # Crown of hair above forehead
    top_hair = [
        (hx - 10, hy - 9),
        (hx + 8,  hy - 9),
        (hx + 11, hy - 2),
        (hx - 11, hy - 2)
    ]
    c.polygon(top_hair, C_HAIR_BASE)
    # Anime hair sheen arc across crown
    c.line(hx - 7, hy - 5, hx + 5, hy - 5, C_HAIR_HILIGHT, thickness=2)
    c.line(hx - 4, hy - 6, hx + 3, hy - 6, C_HAIR_SPEC)

    # Hanging bangs
    # Left sideburn lock
    c.polygon([(hx - 9, hy - 2), (hx - 4, hy - 2), (hx - 5, hy + 10), (hx - 10, hy + 12)], C_HAIR_BASE)
    c.line(hx - 7, hy - 1, hx - 7, hy + 9, C_HAIR_MID)
    # Center-left bang between/above near eye
    c.polygon([(hx - 3, hy - 3), (hx + 1, hy - 3), (hx - 1, hy + 3)], C_HAIR_MID)
    # Center-right bang sweeping between eyes
    c.polygon([(hx + 3, hy - 3), (hx + 7, hy - 3), (hx + 6, hy + 4), (hx + 4, hy + 2)], C_HAIR_BASE)
    c.line(hx + 5, hy - 2, hx + 5, hy + 2, C_HAIR_HILIGHT)
    # Far right temple lock
    c.polygon([(hx + 8, hy - 3), (hx + 11, hy - 1), (hx + 11, hy + 5), (hx + 9, hy + 3)], C_HAIR_BASE)

    # 6. ORNATE GLEAMING GOLDEN CROWN (Vương miện vàng hoàng gia)
    # Fits snugly around the 3/4 head at hy - 7 to hy - 17
    cy = hy - 7
    # Crown golden circlet band (curved for 3/4 perspective)
    band_poly = [
        (hx - 10, cy),
        (hx + 10, cy),
        (hx + 9,  cy + 4),
        (hx - 9,  cy + 4)
    ]
    c.polygon(band_poly, C_GOLD_BASE, outline_col=C_GOLD_OUTLINE)
    c.line(hx - 8, cy + 1, hx + 8, cy + 1, C_GOLD_BRIGHT)
    c.line(hx - 9, cy + 3, hx + 8, cy + 3, C_GOLD_DEEP)

    # 5 Royal Spikes in 3/4 perspective (tallest central peak facing 3/4 forward-right at hx + 3)
    spikes = [
        # (base_left, base_right, tip_x, tip_y, color)
        (hx - 10, hx - 6, hx - 9, cy - 5,  C_GOLD_SHADE),   # Far back-left spike
        (hx - 6,  hx - 1, hx - 4, cy - 8,  C_GOLD_BASE),    # Mid-left spike
        (hx - 1,  hx + 6, hx + 3, cy - 11, C_GOLD_BRIGHT),  # Tallest Sovereign Front-Center Spike!
        (hx + 5,  hx + 9, hx + 8, cy - 8,  C_GOLD_BASE),    # Mid-right spike
        (hx + 8,  hx + 11,hx + 11,cy - 5,  C_GOLD_SHADE),   # Far right spike
    ]
    for b_l, b_r, tx_s, ty_s, s_col in spikes:
        c.polygon([(b_l, cy), (b_r, cy), (tx_s, ty_s)], s_col, outline_col=C_GOLD_OUTLINE)

    # Specular metallic pixel highlights on the crown spikes
    c.line(hx + 2, cy - 1, hx + 3, cy - 10, C_GOLD_SPEC)
    c.set(hx + 3, cy - 11, '#ffffff')
    c.line(hx - 4, cy - 1, hx - 4, cy - 7, C_GOLD_BRIGHT)
    c.set(hx - 4, cy - 8, C_GOLD_SPEC)
    c.line(hx + 7, cy - 1, hx + 8, cy - 7, C_GOLD_SPEC)

    # Jewels embedded in the crown band (Crimson Ruby & Royal Amethyst)
    c.rect(hx + 2, cy + 1, 2, 2, C_CRIMSON_BASE)
    c.set(hx + 2, cy + 1, C_CRIMSON_GLOW)
    c.set(hx - 4, cy + 2, C_PURPLE_BRIGHT)
    c.set(hx + 7, cy + 2, C_PURPLE_BRIGHT)


def draw_arm_and_gauntlet_128(c, sh_x, sh_y, el_x, el_y, wr_x, wr_y,
                              is_front=True, open_hand=False, hand_dir=(1, 0)):
    """
    Draws an athletic human arm with fitted black sleeve, flared purple-and-gold
    royal cuff (from reference Image 1), and black leather gloved hand.
    """
    arm_base  = C_SUIT_BASE if is_front else C_SUIT_DEEP
    arm_shade = C_VOID_BLACK
    arm_hi    = C_SUIT_LIGHT if is_front else C_SUIT_MID

    # Upper arm (bicep/deltoid)
    c.capsule(sh_x, sh_y, el_x, el_y, 5.2, 4.2,
              arm_base, shade_col=arm_shade, hi_col=arm_hi, outline_col=C_OUTLINE)
    # Shoulder gold epaulette accent
    if is_front:
        c.line(sh_x - 3, sh_y - 2, sh_x + 4, sh_y - 1, C_GOLD_BASE)

    # Forearm & Royal Cuff
    c.capsule(el_x, el_y, wr_x, wr_y, 4.3, 4.6,
              C_PURPLE_DARK if is_front else C_SUIT_DEEP,
              shade_col=C_VOID_BLACK,
              hi_col=C_PURPLE_ROYAL if is_front else C_SUIT_MID,
              outline_col=C_OUTLINE)

    # Double gold bracelet rings around forearm cuff (iconic detail in reference images!)
    dx = wr_x - el_x
    dy = wr_y - el_y
    length = max(1.0, math.hypot(dx, dy))
    nx, ny = -dy / length, dx / length
    for t_ring in (0.55, 0.85):
        rx = el_x + dx * t_ring
        ry = el_y + dy * t_ring
        c.line(rx - nx * 4.5, ry - ny * 4.5, rx + nx * 4.5, ry + ny * 4.5,
               C_GOLD_BRIGHT if is_front else C_GOLD_SHADE, thickness=2)

    # Black Gloved Hand
    c.circle(wr_x, wr_y, 3.8, C_VOID_BLACK, fill=True)
    c.circle(wr_x, wr_y, 2.8, C_SUIT_MID if is_front else C_SUIT_DEEP, fill=True)
    if open_hand:
        # Dramatic splayed dark-magic fingers (like Reference Image 1 & 3!)
        hx_d, hy_d = hand_dir
        base_ang = math.atan2(hy_d, hx_d)
        for f_ang in (-0.65, -0.25, 0.15, 0.55):
            ang = base_ang + f_ang
            fx = wr_x + math.cos(ang) * 7.5
            fy = wr_y + math.sin(ang) * 7.5
            c.line(wr_x, wr_y, fx, fy, C_VOID_BLACK, thickness=2)
            c.line(wr_x, wr_y, fx, fy, C_SUIT_LIGHT if is_front else C_SUIT_MID)


def draw_obsidian_sword_128(c, hilt_x, hilt_y, tip_x, tip_y, aura_intensity=1.0):
    """
    Draws the Dark King's long, sleek jet-black Slime Longsword with
    ornate crossguard, purple-violet glowing edges, and dark energy aura.
    """
    dx = tip_x - hilt_x
    dy = tip_y - hilt_y
    length = max(1.0, math.hypot(dx, dy))
    ux, uy = dx / length, dy / length
    nx, ny = -uy, ux

    # 1. Pommel & Grip extending behind hilt_x, hilt_y
    pom_x = hilt_x - ux * 10
    pom_y = hilt_y - uy * 10
    c.line(pom_x, pom_y, hilt_x, hilt_y, C_SUIT_MID, thickness=3)
    c.circle(pom_x, pom_y, 2.5, C_GOLD_BASE, fill=True)
    c.set(pom_x, pom_y, C_GOLD_SPEC)

    # 2. Outer Purple Aura Glow along blade
    if aura_intensity > 0:
        for s in range(4, int(length), 3):
            bx = hilt_x + ux * s
            by = hilt_y + uy * s
            c.circle(bx, by, 3.2 * aura_intensity, (147, 70, 240, 85), fill=True)

    # 3. Sleek Tapered Obsidian Blade Polygon
    guard_x = hilt_x + ux * 3
    guard_y = hilt_y + uy * 3
    blade_poly = [
        (guard_x + nx * 2.4, guard_y + ny * 2.4),
        (tip_x + nx * 0.6,   tip_y + ny * 0.6),
        (tip_x + ux * 3.0,   tip_y + uy * 3.0), # Needle-sharp point
        (tip_x - nx * 0.6,   tip_y - ny * 0.6),
        (guard_x - nx * 2.4, guard_y - ny * 2.4)
    ]
    c.polygon(blade_poly, C_BLADE_BLACK, outline_col=C_BLADE_EDGE)
    # Center metallic ridge highlight
    c.line(guard_x, guard_y, tip_x, tip_y, C_BLADE_GLOW)
    c.line(guard_x + ux * 6, guard_y + uy * 6, tip_x - ux * 6, tip_y - uy * 6, C_BLADE_WHITE)

    # 4. Ornate Gothic Crossguard (black & gold wings)
    g_left_x, g_left_y   = guard_x - nx * 9 - ux * 1, guard_y - ny * 9 - uy * 1
    g_right_x, g_right_y = guard_x + nx * 9 - ux * 1, guard_y + ny * 9 - uy * 1
    c.line(g_left_x, g_left_y, g_right_x, g_right_y, C_BLADE_BLACK, thickness=3)
    c.line(g_left_x + nx * 1, g_left_y + ny * 1, g_right_x - nx * 1, g_right_y - ny * 1, C_GOLD_BASE)
    c.circle(guard_x, guard_y, 2.2, C_PURPLE_GLOW, fill=True)
    c.set(guard_x, guard_y, C_BLADE_WHITE)


def draw_dark_king_pose_128(c, pose_params):
    """
    Master composite renderer for any 128x144 Dark King frame with natural
    human anatomy, 3/4 side-profile angle, secondary cape motion, and VFX.
    """
    tx = pose_params.get('tx', 58)
    ty = pose_params.get('ty', 46)
    lean_dx = pose_params.get('lean_dx', 0)
    aura_phase = pose_params.get('aura_phase', 0.0)
    aura_intensity = pose_params.get('aura_intensity', 1.0)

    # 1. Background Dark Aura & Ground Shadow
    if aura_intensity > 0:
        draw_dark_aura_128(c, tx, ty + 20, phase=aura_phase, intensity=aura_intensity)

    # 2. Flowing Royal Black & Purple Cloak (behind body)
    draw_flowing_royal_cape_128(
        c,
        shoulder_x=tx + lean_dx,
        shoulder_y=ty + 1,
        waist_x=tx,
        waist_y=ty + 22,
        billow_dx=pose_params.get('cape_dx', -26),
        billow_dy=pose_params.get('cape_dy', 0),
        spread=pose_params.get('cape_spread', 1.0),
        wave_phase=pose_params.get('cape_phase', aura_phase)
    )

    # 3. Back Arm (if drawn behind torso)
    back_arm = pose_params.get('back_arm')
    if back_arm and back_arm.get('layer', 'back') == 'back':
        draw_arm_and_gauntlet_128(
            c, back_arm['sh'][0], back_arm['sh'][1],
            back_arm['el'][0], back_arm['el'][1],
            back_arm['wr'][0], back_arm['wr'][1],
            is_front=False,
            open_hand=back_arm.get('open_hand', False),
            hand_dir=back_arm.get('hand_dir', (1, 0))
        )

    # 4. Back Leg & Front Leg
    back_leg = pose_params['back_leg']
    front_leg = pose_params['front_leg']
    draw_boot_leg_128(c, back_leg['hip'][0], back_leg['hip'][1],
                      back_leg['knee'][0], back_leg['knee'][1],
                      back_leg['ankle'][0], back_leg['ankle'][1], is_front=False)
    draw_boot_leg_128(c, front_leg['hip'][0], front_leg['hip'][1],
                      front_leg['knee'][0], front_leg['knee'][1],
                      front_leg['ankle'][0], front_leg['ankle'][1], is_front=True)

    # 5. Royal Combat Torso
    draw_royal_torso_128(c, tx, ty, lean_dx=lean_dx)

    # 6. High Flared Winged Collar
    hx = pose_params.get('hx', tx + lean_dx + 1)
    hy = pose_params.get('hy', ty - 17)
    draw_flared_collar_back_128(c, hx, hy + 13)

    # 7. Handsome 3/4 Anime Head & Gleaming Golden Crown
    draw_head_and_golden_crown_128(c, hx, hy, expr=pose_params.get('expr', 'confident'))

    # 8. Back Arm (if layered in front of torso, e.g. cross-body slash or open-palm cast)
    if back_arm and back_arm.get('layer') == 'front':
        draw_arm_and_gauntlet_128(
            c, back_arm['sh'][0], back_arm['sh'][1],
            back_arm['el'][0], back_arm['el'][1],
            back_arm['wr'][0], back_arm['wr'][1],
            is_front=False,
            open_hand=back_arm.get('open_hand', False),
            hand_dir=back_arm.get('hand_dir', (1, 0))
        )

    # 9. Sword (if layered behind front arm)
    sword = pose_params.get('sword')
    if sword and sword.get('layer', 'front') == 'behind_arm':
        draw_obsidian_sword_128(c, sword['hilt'][0], sword['hilt'][1],
                                sword['tip'][0], sword['tip'][1],
                                aura_intensity=sword.get('aura', 1.0))

    # 10. Front Arm
    front_arm = pose_params['front_arm']
    draw_arm_and_gauntlet_128(
        c, front_arm['sh'][0], front_arm['sh'][1],
        front_arm['el'][0], front_arm['el'][1],
        front_arm['wr'][0], front_arm['wr'][1],
        is_front=True,
        open_hand=front_arm.get('open_hand', False),
        hand_dir=front_arm.get('hand_dir', (1, 0))
    )

    # 11. Sword (if layered in front)
    if sword and sword.get('layer', 'front') == 'front':
        draw_obsidian_sword_128(c, sword['hilt'][0], sword['hilt'][1],
                                sword['tip'][0], sword['tip'][1],
                                aura_intensity=sword.get('aura', 1.0))
