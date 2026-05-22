with open(r'C:\Users\bruno\.mavis\stat-lab\estatisticas.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('icon-192.svg')
print('Found at:', idx)
if idx >= 0:
    print(repr(content[idx-100:idx+200]))