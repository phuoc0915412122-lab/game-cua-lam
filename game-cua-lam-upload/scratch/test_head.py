import sys, os, math
sys.path.append(os.path.abspath('scratch'))
from pixel_canvas import PixelCanvas

# Palette
C_OUTLINE = '#13111c'
C_SKIN_BASE = '#fedecb'
C_SKIN_SHADE = '#ebb196'
C_SKIN_DEEP = '#ca856a'
C_SKIN_HILIGHT = '#fff2eb'
C_BLUSH = '#ff9aa8'

C_EYE_WHITE = '#ffffff'
C_EYE_PUPIL = '#751035'
C_EYE_IRIS = '#f03678'
C_EYE_HILIGHT = '#ffbad2'

C_HORN_BASE = '#d81f3b'
C_HORN_SHADE = '#8a0d20'
C_HORN_DEEP = '#4c0511'
C_HORN_HILIGHT = '#ff7589'

C_HAIR_BASE = '#ea8350'
C_HAIR_SHADE = '#ba572d'
C_HAIR_DEEP = '#7d3319'
C_HAIR_HILIGHT = '#f8b48f'
C_HAIR_SHINE = '#ffe3d1'

C_ROBE_BASE = '#232f4a'
C_ROBE_SHADE = '#161e31'
C_ROBE_DEEP = '#0c101c'
C_ROBE_HILIGHT = '#3e5178'
C_ROBE_WHITE = '#edf3f7'
C_ROBE_WHITE_SHADE = '#b8c7d6'

C_GOLD_BASE = '#f3c445'
C_GOLD_SHADE = '#b1841e'
C_GOLD_HILIGHT = '#fff099'

C_MINT_CORE = '#ffffff'
C_MINT_BRIGHT = '#b4ffea'
C_MINT_BASE = '#6ee3bd'
C_MINT_SHADE = '#33a380'
C_MINT_DEEP = '#165744'

C_BOOT_BASE = '#192033'
C_BOOT_SHADE = '#101422'
C_BOOT_HILIGHT = '#2c3752'

C_STAFF_WOOD = '#7d522c'
C_STAFF_WOOD_DARK = '#4e3015'
C_STAFF_WOOD_LIGHT = '#a87442'

def draw_head_and_face(c, hx, hy, expr='normal', mouth='smirk', dir_look=1):
    # Head & face centered at (hx, hy)
    # hy is top of head ~ 12
    # Horns (behind front hair, above head)
    # Left Horn
    c.rect(hx - 9, hy - 8, 3, 4, C_HORN_SHADE)
    c.rect(hx - 8, hy - 9, 2, 2, C_HORN_HILIGHT)
    c.rect(hx - 10, hy - 7, 2, 4, C_HORN_DEEP)
    c.rect(hx - 8, hy - 11, 2, 3, C_HORN_BASE)
    c.set(hx - 7, hy - 12, C_HORN_HILIGHT)
    c.set(hx - 8, hy - 12, C_HORN_BASE)
    c.set(hx - 8, hy - 13, C_HORN_HILIGHT) # Horn tip

    # Right Horn
    c.rect(hx + 6, hy - 8, 3, 4, C_HORN_SHADE)
    c.rect(hx + 7, hy - 9, 2, 2, C_HORN_HILIGHT)
    c.rect(hx + 8, hy - 7, 2, 4, C_HORN_DEEP)
    c.rect(hx + 6, hy - 11, 2, 3, C_HORN_BASE)
    c.set(hx + 6, hy - 12, C_HORN_HILIGHT)
    c.set(hx + 7, hy - 12, C_HORN_BASE)
    c.set(hx + 6, hy - 13, C_HORN_HILIGHT) # Horn tip

    # Back hair base mass
    c.rect(hx - 10, hy - 3, 20, 16, C_HAIR_DEEP)
    c.rect(hx - 9, hy - 2, 18, 18, C_HAIR_SHADE)
    c.rect(hx - 11, hy + 2, 4, 16, C_HAIR_SHADE)
    c.rect(hx + 7, hy + 2, 4, 16, C_HAIR_SHADE)

    # Face base
    # Head contour
    c.rect(hx - 7, hy - 1, 14, 11, C_SKIN_BASE)
    c.rect(hx - 6, hy + 10, 12, 3, C_SKIN_BASE)
    c.rect(hx - 4, hy + 13, 8, 2, C_SKIN_BASE)
    c.rect(hx - 2, hy + 15, 4, 1, C_SKIN_BASE) # chin tip

    # Jaw shading
    c.line(hx - 6, hy + 11, hx - 4, hy + 13, C_SKIN_SHADE)
    c.line(hx + 5, hy + 11, hx + 3, hy + 13, C_SKIN_SHADE)
    c.line(hx - 4, hy + 14, hx + 3, hy + 14, C_SKIN_SHADE)
    c.rect(hx - 2, hy + 15, 4, 1, C_SKIN_DEEP)

    # Ears (pointed spirit/elf ears like img 2)
    c.rect(hx - 8, hy + 4, 2, 4, C_SKIN_BASE)
    c.set(hx - 9, hy + 3, C_SKIN_BASE)
    c.set(hx - 10, hy + 2, C_SKIN_SHADE) # ear tip left
    c.rect(hx + 6, hy + 4, 2, 4, C_SKIN_BASE)
    c.set(hx + 7, hy + 3, C_SKIN_BASE)
    c.set(hx + 8, hy + 2, C_SKIN_SHADE) # ear tip right

    # Eyes
    if expr == 'closed':
        # Defeat / resting eyes
        c.line(hx - 5, hy + 6, hx - 2, hy + 7, C_OUTLINE)
        c.line(hx + 2, hy + 7, hx + 5, hy + 6, C_OUTLINE)
    elif expr == 'winking':
        c.line(hx - 5, hy + 6, hx - 2, hy + 6, C_OUTLINE)
        # Right eye open
        c.rect(hx + 2, hy + 4, 4, 5, C_EYE_WHITE)
        c.rect(hx + 2, hy + 3, 5, 2, C_OUTLINE) # upper lash
        c.rect(hx + 3, hy + 4, 3, 4, C_EYE_IRIS)
        c.rect(hx + 3, hy + 4, 2, 2, C_EYE_PUPIL)
        c.set(hx + 4, hy + 5, C_EYE_HILIGHT)
        c.set(hx + 3, hy + 7, C_OUTLINE)
    else:
        # Left eye
        c.rect(hx - 6, hy + 4, 4, 5, C_EYE_WHITE)
        c.rect(hx - 6, hy + 3, 5, 2, C_OUTLINE) # thick upper lash
        c.rect(hx - 5, hy + 4, 3, 4, C_EYE_IRIS)
        c.rect(hx - 5, hy + 4, 2, 2, C_EYE_PUPIL)
        c.set(hx - 4, hy + 5, C_EYE_HILIGHT)
        c.set(hx - 5, hy + 7, C_OUTLINE) # lower lash
        # Right eye
        c.rect(hx + 2, hy + 4, 4, 5, C_EYE_WHITE)
        c.rect(hx + 1, hy + 3, 5, 2, C_OUTLINE) # thick upper lash
        c.rect(hx + 2, hy + 4, 3, 4, C_EYE_IRIS)
        c.rect(hx + 2, hy + 4, 2, 2, C_EYE_PUPIL)
        c.set(hx + 3, hy + 5, C_EYE_HILIGHT)
        c.set(hx + 2, hy + 7, C_OUTLINE)

    # Eyebrows
    c.line(hx - 6, hy + 2, hx - 2, hy + 2, C_HAIR_DEEP)
    c.line(hx + 2, hy + 2, hx + 6, hy + 2, C_HAIR_DEEP)

    # Blush (cute anime cheek blush)
    c.rect(hx - 6, hy + 8, 3, 2, C_BLUSH)
    c.rect(hx + 3, hy + 8, 3, 2, C_BLUSH)

    # Nose
    c.set(hx, hy + 9, C_SKIN_DEEP)

    # Mouth
    if mouth == 'smirk': # cute smirk with tiny fang (like Image 1)
        c.rect(hx - 1, hy + 12, 4, 2, C_OUTLINE)
        c.set(hx, hy + 12, C_EYE_WHITE) # cute fang!
        c.set(hx + 1, hy + 13, C_EYE_PUPIL)
    elif mouth == 'open': # shouting / chanting
        c.rect(hx - 1, hy + 11, 4, 3, C_OUTLINE)
        c.rect(hx, hy + 12, 2, 2, C_EYE_PUPIL)
        c.set(hx, hy + 11, C_EYE_WHITE) # top teeth
    elif mouth == 'smile':
        c.line(hx - 2, hy + 12, hx + 2, hy + 12, C_OUTLINE)
        c.set(hx + 2, hy + 11, C_OUTLINE)
    else: # normal / determined
        c.line(hx - 1, hy + 12, hx + 2, hy + 12, C_OUTLINE)

    # Hair bangs & front strands (inspired by Image 1 & Image 3)
    # Ahoge cowlick on top
    c.line(hx, hy - 4, hx + 1, hy - 7, C_HAIR_BASE)
    c.set(hx + 2, hy - 8, C_HAIR_HILIGHT)
    c.set(hx + 3, hy - 8, C_HAIR_BASE)

    # Main forehead bangs
    c.rect(hx - 8, hy - 3, 16, 4, C_HAIR_BASE)
    c.rect(hx - 6, hy - 4, 12, 2, C_HAIR_HILIGHT)
    c.line(hx - 5, hy - 3, hx + 5, hy - 3, C_HAIR_SHINE)

    # Bang strands framing face
    # Left bang
    c.rect(hx - 8, hy + 1, 3, 9, C_HAIR_BASE)
    c.rect(hx - 9, hy + 3, 2, 10, C_HAIR_SHADE)
    c.set(hx - 8, hy + 10, C_HAIR_BASE)
    c.set(hx - 8, hy + 11, C_HAIR_DEEP)
    # Center bang
    c.rect(hx - 2, hy + 1, 3, 5, C_HAIR_BASE)
    c.set(hx - 1, hy + 6, C_HAIR_BASE)
    c.set(hx - 1, hy + 7, C_HAIR_DEEP)
    # Right bang
    c.rect(hx + 5, hy + 1, 3, 9, C_HAIR_BASE)
    c.rect(hx + 7, hy + 3, 2, 10, C_HAIR_SHADE)
    c.set(hx + 6, hy + 10, C_HAIR_BASE)
    c.set(hx + 6, hy + 11, C_HAIR_DEEP)

    # Gold hairpin / ornament on left side (like Image 3 bottom-right)
    c.rect(hx - 7, hy - 1, 2, 3, C_GOLD_BASE)
    c.set(hx - 8, hy, C_GOLD_HILIGHT)
    c.set(hx - 6, hy, C_MINT_BASE) # mint spirit jewel in hair!

print('draw_head_and_face defined.')
