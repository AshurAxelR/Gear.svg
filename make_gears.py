import io
from gear import gear

style = 'stroke:#999;stroke-width:3;fill:#f5f5f5'

gears = [
    12, 15, 18, 20,
    { 'cogs':22, 'spokes':4, 'inner_radius':40 },
    { 'cogs':26, 'spokes':5, 'inner_radius':45, 'rim_size':20 },
    { 'cogs':28, 'spokes':6, 'inner_radius':45, 'rim_size':20 },
    { 'cogs':32, 'spokes':6, 'inner_radius':50, 'rim_size':20 },
    { 'cogs':36, 'spokes':8, 'inner_radius':55, 'rim_size':22, 'spoke_width':22 }
]

sb = list()
for g in gears:
    if type(g)==int:
        g = { 'cogs':g }
    f = f"gear{g['cogs']}.svg"
    gear(file_name=f'out/{f}', style=style, **g)
    sb.append(f'<img src="{f}" />')

with io.open('out/preview.html', 'wt') as f:
    f.write(''.join(sb))

