import struct, zlib

def create_png_chunk(chunk_type, data):
    chunk_len = struct.pack('>I', len(data))
    chunk_crc = struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff)
    return chunk_len + chunk_type + data + chunk_crc

def make_icon():
    width, height = 256, 256
    signature = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    ihdr = create_png_chunk(b'IHDR', ihdr_data)

    raw = bytearray()
    for y in range(height):
        raw.append(0)  # filter byte
        for x in range(width):
            cx, cy = width//2, height//2
            dx, dy = x - cx, y - cy
            d2 = dx*dx + dy*dy
            if d2 < 80*80:
                raw.extend([12, 22, 16, 255])
            elif d2 < 95*95:
                raw.extend([61, 220, 132, 255])
            elif d2 < 100*100:
                raw.extend([61, 220, 132, 255])
            elif d2 < 110*110:
                raw.extend([61, 220, 132, 180])
            else:
                raw.extend([12, 22, 16, 255])

    # Add "SL" text pixel art
    letters = {
        'S': [[1,1,1,1,1],[1,0,0,0,0],[0,1,1,1,1],[0,0,0,0,1],[1,1,1,1,1]],
        'L': [[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]]
    }
    for ly, row in enumerate(letters['S']):
        for lx, on in enumerate(row):
            if on:
                for dy in range(8):
                    for dx in range(8):
                        idx = ((110 + ly*8 + dy)*256 + (100 + lx*8 + dx)) * 4
                        raw[idx:idx+4] = bytes([61, 220, 132, 255])
    for ly, row in enumerate(letters['L']):
        for lx, on in enumerate(row):
            if on:
                for dy in range(8):
                    for dx in range(8):
                        idx = ((110 + ly*8 + dy)*256 + (150 + lx*8 + dx)) * 4
                        raw[idx:idx+4] = bytes([61, 220, 132, 255])

    compressed = zlib.compress(bytes(raw), 9)
    idat = create_png_chunk(b'IDAT', compressed)
    iend = create_png_chunk(b'IEND', b'')
    png_data = signature + ihdr + idat + iend

    with open(r'C:\Users\bruno\Desktop\StatsLive_App\resources\icon.ico', 'wb') as f:
        f.write(struct.pack('<HHH', 0, 1, 1))
        f.write(struct.pack('<BB', 0, 0))
        f.write(struct.pack('<BB', 0, 0))
        f.write(struct.pack('<HH', 1, 32))
        f.write(struct.pack('<I', len(png_data)))
        f.write(struct.pack('<I', 22))
        f.write(png_data)

    with open(r'C:\Users\bruno\Desktop\StatsLive_App\resources\icon.png', 'wb') as pf:
        pf.write(png_data)

    print(f'Done! icon.ico ({len(png_data)} bytes) + icon.png')

make_icon()