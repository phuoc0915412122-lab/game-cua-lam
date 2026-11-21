import os, sys, math
sys.path.append(os.path.abspath('game-cua-lam/game-cua-lam-upload/scratch'))
from pixel_canvas import PixelCanvas

# Gothic Vampire Dark Throne Palette (matching Reference Image 4)
C_OUTLINE      = '#07050b'
C_STONE_DEEP   = '#12101a'
C_STONE_DARK   = '#1d1a28'
C_STONE_MID    = '#2e2a3d'
C_STONE_LIGHT  = '#4a455e'
C_STONE_SPEC   = '#756f8f'
C_STONE_GLINT  = '#aba5c4'

C_VELVET_DEEP  = '#2b060d'
C_VELVET_DARK  = '#4d0b18'
C_VELVET_MID   = '#751326'
C_VELVET_BASE  = '#9e1c34'
C_VELVET_HI    = '#c9304c'
C_VELVET_SPEC  = '#e85a74'

C_ORB_DEEP     = '#4a040e'
C_ORB_BASE     = '#a80c24'
C_ORB_BRIGHT   = '#ff2a4b'
C_ORB_CORE     = '#ff8fa0'

def draw_spire(c, cx, base_y, width, height):
    """Draws a sharp Gothic cathedral spire with vertical fluting and metallic highlights."""
    top_y = base_y - height
    hw = width / 2.0
    # Main tapered cone
    poly = [
        (cx - hw, base_y),
        (cx - hw * 0.65, base_y - height * 0.45),
        (cx, top_y),
        (cx + hw * 0.65, base_y - height * 0.45),
        (cx + hw, base_y)
    ]
    c.polygon(poly, C_STONE_DARK, outline_col=C_OUTLINE)
    # Right side highlight facet
    hi_poly = [
        (cx, top_y + 2),
        (cx + hw * 0.45, base_y - height * 0.45),
        (cx + hw * 0.75, base_y - 1),
        (cx + 1, base_y - 1)
    ]
    c.polygon(hi_poly, C_STONE_MID)
    # Center ridge & finial
    c.line(cx, top_y, cx, base_y - 2, C_STONE_LIGHT)
    c.line(cx, top_y, cx, top_y + int(height * 0.35), C_STONE_SPEC)
    c.circle(cx, top_y + 2, 1.4, C_STONE_GLINT, fill=True)
    # Horizontal gothic collar rings
    for f in (0.35, 0.72):
        ry = base_y - height * f
        rw = hw * (1.0 - f * 0.72) + 1.5
        c.line(cx - rw, ry, cx + rw, ry, C_STONE_LIGHT, thickness=2)
        c.line(cx - rw, ry - 1, cx + rw, ry - 1, C_STONE_SPEC)

def draw_dark_throne():
    c = PixelCanvas(192, 160)
    cx = 96

    # 1. Stepped Gothic Obsidian Dais / Base (y = 136..156)
    dais_layers = [
        (149, 86, 8, C_STONE_DEEP, C_STONE_MID),
        (143, 80, 7, C_STONE_DARK, C_STONE_LIGHT),
        (137, 74, 7, C_STONE_MID,  C_STONE_SPEC),
    ]
    for dy, hw, h, col, rim in dais_layers:
        c.rect(cx - hw, dy, hw * 2, h, col)
        c.line(cx - hw, dy, cx + hw, dy, rim)
        c.line(cx - hw, dy + h, cx + hw, dy + h, C_OUTLINE)
        # Vertical stone ribs on dais
        for rx in range(-hw + 8, hw, 12):
            c.line(cx + rx, dy + 1, cx + rx, dy + h - 1, C_STONE_DEEP)

    # 2. Outer Twin Gothic Side Towers (left & right wings, symmetric around cx)
    for side in (-1, 1):
        tx = cx + side * 62
        # Main tower pillar
        c.rect(tx - 16, 70, 32, 70, C_STONE_DARK)
        c.rect(tx - 14, 72, 28, 66, C_STONE_MID)
        # Vertical fluted gothic columns
        for off in (-11, -5, 5, 11):
            c.line(tx + off, 72, tx + off, 138, C_STONE_DEEP, thickness=2)
            c.line(tx + off + 1, 72, tx + off + 1, 138, C_STONE_LIGHT)

        # Flared Gothic Gargoyle/Winged Canopy over the side tower
        wing_poly = [
            (tx - side * 24, 62),
            (tx + side * 26, 56),
            (tx + side * 16, 82),
            (tx - side * 14, 82)
        ]
        c.polygon(wing_poly, C_STONE_DARK, outline_col=C_OUTLINE)
        c.line(tx - side * 22, 63, tx + side * 24, 57, C_STONE_SPEC, thickness=2)

        # Glowing Crimson Energy Alcove / Vampire Crystal inside each wing!
        ox = tx + side * 2
        oy = 71
        c.circle(ox, oy, 10.5, C_OUTLINE, fill=True)
        c.circle(ox, oy, 9.0, C_ORB_DEEP, fill=True)
        c.circle(ox, oy, 7.0, C_ORB_BASE, fill=True)
        c.circle(ox, oy, 4.5, C_ORB_BRIGHT, fill=True)
        c.circle(ox - 1, oy - 1, 2.0, C_ORB_CORE, fill=True)
        # Intricate black gothic web/lattice across crimson orb
        c.line(ox - 8, oy - 3, ox + 8, oy + 4, C_OUTLINE)
        c.line(ox - 6, oy + 6, ox + 7, oy - 5, C_OUTLINE)
        c.circle(ox, oy, 9.5, C_STONE_LIGHT, fill=False)

        # Outer Tower Spires (tall main spire + 2 smaller flanking pinnacles)
        draw_spire(c, tx, 59, 18, 34)
        draw_spire(c, tx - side * 13, 62, 9, 18)
        draw_spire(c, tx + side * 13, 60, 8, 16)

    # 3. Tall Inner Cathedral Pillars flanking the Throne Backrest
    for side in (-1, 1):
        px = cx + side * 38
        c.rect(px - 8, 44, 16, 94, C_STONE_DARK)
        c.rect(px - 6, 46, 12, 90, C_STONE_MID)
        c.line(px - 2, 46, px - 2, 136, C_STONE_LIGHT)
        c.line(px + 3, 46, px + 3, 136, C_STONE_DEEP)
        # Tall slender spire atop inner pillar
        draw_spire(c, px, 46, 13, 28)

    # 4. Grand Central Gothic Pointed Arch & Cathedral Crown (cx = 96, y = 10..110)
    arch_outer = [
        (cx - 38, 110),
        (cx - 36, 62),
        (cx - 24, 38),
        (cx,      18),
        (cx + 24, 38),
        (cx + 36, 62),
        (cx + 38, 110)
    ]
    c.polygon(arch_outer, C_STONE_DARK, outline_col=C_OUTLINE)
    # Metallic silver-grey arch ribbing
    for i in range(len(arch_outer) - 1):
        p0, p1 = arch_outer[i], arch_outer[i + 1]
        c.line(p0[0], p0[1], p1[0], p1[1], C_STONE_LIGHT, thickness=2)

    # Central Sovereign Spire & Flanking Mini-Spires
    draw_spire(c, cx, 24, 15, 22)
    draw_spire(c, cx - 14, 35, 7, 14)
    draw_spire(c, cx + 14, 35, 7, 14)
    draw_spire(c, cx - 22, 43, 6, 11)
    draw_spire(c, cx + 22, 43, 6, 11)

    # Crimson Cathedral Alcove behind backrest inside the pointed arch
    alcove_poly = [
        (cx - 28, 100),
        (cx - 26, 64),
        (cx - 16, 46),
        (cx,      31),
        (cx + 16, 46),
        (cx + 26, 64),
        (cx + 28, 100)
    ]
    c.polygon(alcove_poly, C_VELVET_DEEP, outline_col=C_OUTLINE)
    c.polygon([
        (cx - 21, 96), (cx - 19, 64), (cx, 38), (cx + 19, 64), (cx + 21, 96)
    ], C_VELVET_DARK)
    # Gothic pointed tracery filigree over crimson alcove
    c.line(cx, 31, cx - 22, 66, C_STONE_LIGHT, thickness=2)
    c.line(cx, 31, cx + 22, 66, C_STONE_LIGHT, thickness=2)
    c.line(cx, 44, cx - 16, 70, C_STONE_MID)
    c.line(cx, 44, cx + 16, 70, C_STONE_MID)
    c.circle(cx, 54, 4, C_STONE_SPEC, fill=False)

    # 5. Luxurious Tufted Crimson Velvet Backrest (cx = 96, y = 66..118)
    c.ellipse(cx, 92, 23, 28, C_OUTLINE, fill=True)
    c.ellipse(cx, 92, 21, 26, C_VELVET_DARK, fill=True)
    c.ellipse(cx, 91, 19, 24, C_VELVET_MID, fill=True)
    c.ellipse(cx - 2, 88, 15, 20, C_VELVET_BASE, fill=True)
    # Quilted diamond tufting pattern + plush sheen
    for dy in range(-18, 22, 9):
        for dx in range(-14, 18, 10):
            bx = cx + dx + (5 if (dy // 9) % 2 else 0)
            by = 92 + dy
            if ((bx - cx) / 18.0)**2 + ((by - 92) / 23.0)**2 < 0.85:
                # Diamond crease lines
                c.line(bx - 5, by, bx, by - 4, C_VELVET_DEEP)
                c.line(bx, by - 4, bx + 5, by, C_VELVET_DEEP)
                c.line(bx - 4, by + 1, bx, by + 4, C_VELVET_HI)
                # Tufted button dimple
                c.circle(bx, by, 1.2, C_VELVET_DEEP, fill=True)
                c.set(bx - 1, by - 1, C_VELVET_SPEC)

    # Ornate Gothic Stone Frame hugging the backrest
    c.ellipse(cx, 92, 23, 28, C_STONE_LIGHT, fill=False)
    c.ellipse(cx, 92, 24, 29, C_STONE_DARK, fill=False)

    # 6. Plush Crimson Seat Cushion (y = 114..128)
    seat_poly = [
        (cx - 34, 115),
        (cx + 34, 115),
        (cx + 38, 125),
        (cx - 38, 125)
    ]
    c.polygon(seat_poly, C_VELVET_BASE, outline_col=C_OUTLINE)
    c.line(cx - 32, 117, cx + 32, 117, C_VELVET_HI, thickness=2)
    c.line(cx - 24, 117, cx + 24, 117, C_VELVET_SPEC)
    c.line(cx - 36, 123, cx + 36, 123, C_VELVET_DEEP, thickness=2)

    # 7. Curved Crimson Armrests + Carved Gothic Obsidian Arm Posts
    for side in (-1, 1):
        ax = cx + side * 38
        # Plush padded crimson armrest top
        c.ellipse(ax, 109, 14, 7, C_OUTLINE, fill=True)
        c.ellipse(ax, 109, 12, 5.5, C_VELVET_BASE, fill=True)
        c.ellipse(ax - side * 2, 107, 9, 3, C_VELVET_HI, fill=True)
        c.line(ax - 6, 106, ax + 6, 106, C_VELVET_SPEC)

        # Front carved obsidian gothic armrest scroll pillar
        post_poly = [
            (ax - 9, 109),
            (ax + 9, 109),
            (ax + 11, 138),
            (ax - 11, 138)
        ]
        c.polygon(post_poly, C_STONE_DARK, outline_col=C_OUTLINE)
        c.rect(ax - 7, 112, 14, 24, C_STONE_MID)
        # Carved gothic spiral/skull filigree
        c.circle(ax, 116, 5, C_STONE_LIGHT, fill=False)
        c.circle(ax, 116, 2.5, C_STONE_SPEC, fill=True)
        c.line(ax - 4, 122, ax - 4, 135, C_STONE_LIGHT)
        c.line(ax + 4, 122, ax + 4, 135, C_STONE_LIGHT)
        c.line(ax, 123, ax, 135, C_STONE_DEEP)

    # 8. Ornate Carved Throne Front Apron / Crest below seat (y = 125..138)
    c.rect(cx - 34, 125, 68, 13, C_STONE_DARK)
    c.line(cx - 34, 126, cx + 34, 126, C_STONE_SPEC)
    c.line(cx - 34, 137, cx + 34, 137, C_OUTLINE)
    # Central gothic medallion on apron
    c.ellipse(cx, 131, 6, 5, C_STONE_LIGHT, fill=True)
    c.ellipse(cx, 131, 3.5, 3, C_ORB_BASE, fill=True)
    c.set(cx - 1, 130, C_ORB_CORE)
    # Symmetrical scroll carvings on apron
    for side in (-1, 1):
        c.line(cx + side * 8, 131, cx + side * 26, 129, C_STONE_LIGHT)
        c.line(cx + side * 8, 133, cx + side * 24, 134, C_STONE_SPEC)

    out_path = os.path.abspath('game-cua-lam/game-cua-lam-upload/game-assets/effects/dark_king/dark_throne.png')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'wb') as f:
        f.write(c.to_png_bytes(1))
    print(f"Saved Gothic Dark Throne pixel art to {out_path}")

if __name__ == '__main__':
    draw_dark_throne()
