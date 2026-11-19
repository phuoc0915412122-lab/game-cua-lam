import os, struct, zlib, math

class PixelCanvas:
    def __init__(self, w=128, h=144):
        self.w = w
        self.h = h
        self.pixels = [[(0, 0, 0, 0) for _ in range(w)] for _ in range(h)]

    @staticmethod
    def parse_color(col):
        if isinstance(col, tuple):
            if len(col) == 3:
                return (int(col[0]), int(col[1]), int(col[2]), 255)
            return (int(col[0]), int(col[1]), int(col[2]), int(col[3]))
        hex_str = col.lstrip('#')
        if len(hex_str) == 3:
            r = int(hex_str[0]*2, 16)
            g = int(hex_str[1]*2, 16)
            b = int(hex_str[2]*2, 16)
            return (r, g, b, 255)
        elif len(hex_str) == 6:
            r = int(hex_str[0:2], 16)
            g = int(hex_str[2:4], 16)
            b = int(hex_str[4:6], 16)
            return (r, g, b, 255)
        elif len(hex_str) == 8:
            r = int(hex_str[0:2], 16)
            g = int(hex_str[2:4], 16)
            b = int(hex_str[4:6], 16)
            a = int(hex_str[6:8], 16)
            return (r, g, b, a)
        return (0, 0, 0, 255)

    def set(self, x, y, col):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.w and 0 <= y < self.h:
            col = self.parse_color(col)
            if col[3] == 255 or self.pixels[y][x][3] == 0:
                self.pixels[y][x] = col
            elif col[3] > 0:
                bg = self.pixels[y][x]
                a = col[3] / 255.0
                inv = 1.0 - a
                r = int(col[0] * a + bg[0] * inv)
                g = int(col[1] * a + bg[1] * inv)
                b = int(col[2] * a + bg[2] * inv)
                out_a = min(255, int(col[3] + bg[3] * inv))
                self.pixels[y][x] = (r, g, b, out_a)

    def get(self, x, y):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.pixels[y][x]
        return (0, 0, 0, 0)

    def rect(self, x, y, w, h, col):
        x0, y0 = int(round(x)), int(round(y))
        x1, y1 = int(round(x + w)), int(round(y + h))
        for cy in range(y0, y1):
            for cx in range(x0, x1):
                self.set(cx, cy, col)

    def line(self, x0, y0, x1, y1, col, thickness=1):
        if thickness <= 1:
            x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            sx = 1 if x0 < x1 else -1
            sy = 1 if y0 < y1 else -1
            err = dx - dy
            x, y = x0, y0
            max_steps = (dx + dy + 2) * 2
            for _ in range(max_steps):
                self.set(x, y, col)
                if x == x1 and y == y1:
                    break
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x += sx
                if e2 < dx:
                    err += dx
                    y += sy
        else:
            r = thickness / 2.0
            self.capsule(x0, y0, x1, y1, r, r, col)

    def circle(self, cx, cy, r, col, fill=True):
        icx, icy = int(round(cx)), int(round(cy))
        ir = int(math.ceil(r)) + 1
        for y in range(icy - ir, icy + ir + 1):
            for x in range(icx - ir, icx + ir + 1):
                d = math.hypot(x - cx, y - cy)
                if fill:
                    if d <= r:
                        self.set(x, y, col)
                else:
                    if abs(d - r) <= 0.65:
                        self.set(x, y, col)

    def ellipse(self, cx, cy, rx, ry, col, fill=True, angle_deg=0):
        if rx <= 0 or ry <= 0:
            return
        rad = math.radians(angle_deg)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        max_r = int(math.ceil(max(rx, ry))) + 2
        icx, icy = int(round(cx)), int(round(cy))
        for y in range(icy - max_r, icy + max_r + 1):
            for x in range(icx - max_r, icx + max_r + 1):
                dx, dy = x - cx, y - cy
                lx = dx * cos_a + dy * sin_a
                ly = -dx * sin_a + dy * cos_a
                val = (lx / rx)**2 + (ly / ry)**2
                if fill:
                    if val <= 1.0:
                        self.set(x, y, col)
                else:
                    if 0.78 <= val <= 1.25:
                        self.set(x, y, col)

    def polygon(self, pts, col, outline_col=None):
        if len(pts) < 3:
            return
        min_y = max(0, int(math.floor(min(p[1] for p in pts))))
        max_y = min(self.h - 1, int(math.ceil(max(p[1] for p in pts))))
        n = len(pts)
        for y in range(min_y, max_y + 1):
            nodes = []
            j = n - 1
            for i in range(n):
                yi, yj = pts[i][1], pts[j][1]
                xi, xj = pts[i][0], pts[j][0]
                if (yi < y <= yj) or (yj < y <= yi):
                    if yj != yi:
                        nodes.append(xi + (y - yi) / (yj - yi) * (xj - xi))
                j = i
            nodes.sort()
            for k in range(0, len(nodes) - 1, 2):
                x_start = max(0, int(math.ceil(nodes[k])))
                x_end = min(self.w - 1, int(math.floor(nodes[k + 1])))
                for x in range(x_start, x_end + 1):
                    self.set(x, y, col)
        if outline_col:
            for i in range(n):
                p0 = pts[i]
                p1 = pts[(i + 1) % n]
                self.line(p0[0], p0[1], p1[0], p1[1], outline_col)

    def capsule(self, x0, y0, x1, y1, r0, r1, base_col, shade_col=None, hi_col=None, outline_col=None):
        dx = x1 - x0
        dy = y1 - y0
        dist = math.hypot(dx, dy)
        steps = max(int(dist * 2.5), 1)
        # First pass: optional outline
        if outline_col:
            for s in range(steps + 1):
                t = s / float(steps)
                cx = x0 + dx * t
                cy = y0 + dy * t
                cr = r0 + (r1 - r0) * t + 1.0
                self.circle(cx, cy, cr, outline_col, fill=True)
        # Second pass: shaded volume
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
                        col = base_col
                        if shade_col and (ix < -cr * 0.25 or iy > cr * 0.45):
                            col = shade_col
                        elif hi_col and (ix > cr * 0.2 and iy < cr * 0.25):
                            col = hi_col
                        self.set(px, py, col)

    def to_png_bytes(self, scale=1):
        out_w = self.w * scale
        out_h = self.h * scale
        raw = bytearray()
        for y in range(out_h):
            raw.append(0)
            src_y = y // scale
            for x in range(out_w):
                src_x = x // scale
                r, g, b, a = self.pixels[src_y][src_x]
                raw.extend((r, g, b, a))

        ihdr = struct.pack('>IIBBBBB', out_w, out_h, 8, 6, 0, 0, 0)
        def chunk(tag, data):
            ch = tag + data
            crc = zlib.crc32(ch) & 0xffffffff
            return struct.pack('>I', len(data)) + ch + struct.pack('>I', crc)

        png = b'\x89PNG\r\n\x1a\n'
        png += chunk(b'IHDR', ihdr)
        png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
        png += chunk(b'IEND', b'')
        return png
