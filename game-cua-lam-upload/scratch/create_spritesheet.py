import os, sys, struct, zlib

def parse_png(path):
    with open(path, 'rb') as f: data = f.read()
    idx = 8
    ihdr, idat = None, b''
    while idx < len(data):
        length, ctype = struct.unpack('>I4s', data[idx:idx+8])
        if ctype == b'IHDR': ihdr = data[idx+8:idx+8+length]
        elif ctype == b'IDAT': idat += data[idx+8:idx+8+length]
        idx += 12 + length
    w, h = struct.unpack('>II', ihdr[:8])
    raw = zlib.decompress(idat)
    pixels = []
    rb = 1 + w * 4
    for y in range(h):
        row = raw[y*rb+1:(y+1)*rb]
        pixels.append([row[x*4:(x+1)*4] for x in range(w)])
    return w, h, pixels

def write_png(path, w, h, pixels):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        for x in range(w):
            raw.extend(pixels[y][x])
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)
    def chunk(tag, data):
        ch = tag + data
        crc = zlib.crc32(ch) & 0xffffffff
        return struct.pack('>I', len(data)) + ch + struct.pack('>I', crc)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', ihdr)
    png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)

frames_list = [
    'idle_01.png', 'idle_02.png', 'move_01.png', 'move_02.png', 'move_03.png',
    'move_04.png', 'jump_01.png', 'fall_01.png', 'attack_01.png', 'attack_02.png',
    'attack_03.png', 'skill_01.png', 'skill_02.png', 'skill_03.png', 'finisher_01.png',
    'finisher_02.png', 'finisher_03.png', 'dash_01.png', 'dash_02.png', 'defeat_01.png'
]

cols, rows = 5, 4
frame_w, frame_h = 256, 288
sheet_w = cols * frame_w
sheet_h = rows * frame_h

# Create transparent canvas with subtle checkerboard or dark arena background
# Let's use a stylish dark indigo arena background (#101424) so transparent sprites pop clearly!
bg_color = (16, 20, 36, 255)
bg_grid = (22, 28, 48, 255)
sheet_pixels = []
for y in range(sheet_h):
    row = []
    for x in range(sheet_w):
        # subtle 16px tile pattern
        c = bg_grid if ((x//16 + y//16) % 2 == 0) else bg_color
        row.append(c)
    sheet_pixels.append(row)

for idx, fn in enumerate(frames_list):
    col = idx % cols
    row = idx // cols
    ox = col * frame_w
    oy = row * frame_h
    fp = os.path.join('game-assets/characters/3', fn)
    fw, fh, fpx = parse_png(fp)
    for y in range(frame_h):
        for x in range(frame_w):
            p = fpx[y][x]
            if p[3] > 0:
                # alpha blend
                a = p[3] / 255.0
                bg = sheet_pixels[oy + y][ox + x]
                inv = 1.0 - a
                r = int(p[0] * a + bg[0] * inv)
                g = int(p[1] * a + bg[1] * inv)
                b = int(p[2] * a + bg[2] * inv)
                sheet_pixels[oy + y][ox + x] = (r, g, b, 255)

# Save to artifacts directory and game-assets
art_dir = r'C:\Users\ADMIN\.gemini\antigravity\brain\704b332d-44e7-4fab-a752-6a15e1db316e'
os.makedirs(art_dir, exist_ok=True)
art_path = os.path.join(art_dir, 'summoner_spritesheet.png')
write_png(art_path, sheet_w, sheet_h, sheet_pixels)
write_png('game-assets/characters/3/summoner_spritesheet.png', sheet_w, sheet_h, sheet_pixels)

print(f'Saved spritesheet ({sheet_w}x{sheet_h}) to {art_path}')
