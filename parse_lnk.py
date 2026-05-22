import struct

lnk = open(r'C:\Users\bruno\Desktop\Tactical Lab.lnk', 'rb').read()
print(f"File size: {len(lnk)} bytes")
print(f"Magic: {lnk[:4].hex()}")

# ShellIDList offset at 0x4c
pos = 0x4c
count = struct.unpack('<H', lnk[pos:pos+2])[0]
print(f"Shell items count: {count}")
pos += 2

for i in range(count):
    size = struct.unpack('<H', lnk[pos:pos+2])[0]
    data = lnk[pos+2:pos+size]
    item_type = data[0] if len(data) > 0 else 0
    print(f"  Item {i}: type=0x{item_type:02x}, size={size}")
    # Try to decode text from known item types
    if len(data) > 2:
        try:
            text = data[2:].decode('utf-16-le', errors='replace').rstrip('\x00')
            if text:
                print(f"    Text: {text}")
        except:
            pass
    pos += size

# Show extra data sections
print(f"\nData after shell items (offset {hex(pos)}):")
extra = lnk[pos:]
for i in range(0, min(len(extra), 600), 32):
    hex_str = ' '.join(f'{b:02x}' for b in extra[i:i+32])
    ascii_str = ''.join(chr(b) if 32<=b<127 else '.' for b in extra[i:i+32])
    print(f"  {pos+i:04x}: {hex_str}  {ascii_str}")

# Look for URL patterns
content = lnk.decode('latin-1')
for marker in ['http', 'chrome', 'profile', 'vercel', 'localhost']:
    idx = content.find(marker, 200)  # skip header
    if idx >= 0:
        print(f"\nFound '{marker}' at offset {idx}: {repr(content[idx-10:idx+100])}")