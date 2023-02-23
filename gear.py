import math
import io

def gear(
        # gear parameters
        cogs = 20,
        spokes = 4,

        #style
        style = 'stroke:#000;stroke-width:2;fill:#ddd',
        
        # geometry parameters
        margin = 0,
        cog_width = 15,
        cog_depth = 12,
        axis_radius = 15,
        inner_radius = 35,
        rim_size = 15,
        spoke_width = 20,
        min_spoke_length = 20,

        # output and debug parameters
        file_name = None,
        draw_grid = False
    ):

    R = cog_width * cogs / math.pi
    Rs = R - cog_depth
    mid = math.ceil((R+margin)/10)*10
    Rrim = Rs - rim_size
    Rin = inner_radius

    def arc_xy(a, r):
        x = mid+r*math.sin(math.radians(a))
        y = mid-r*math.cos(math.radians(a))
        return x, y

    sb = list()

    sb.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{mid*2:.0f}" height="{mid*2:.0f}">')
    sb.append(f'<!-- Notches={cogs}, Radius={R:.2f} -->')

    if draw_grid:
        sb.append('<g style="stroke:#ddd;fill:none">')
        for x in range (20, mid*2, 20):
            sb.append(f'<line x1="{x:.0f}" y1="0" x2="{x:.0f}" y2="{mid*2:.0f}" />')
            sb.append(f'<line x1="0" y1="{x:.0f}" x2="{mid*2:.0f}" y2="{x:.0f}" />')
        sb.append('</g>')

    sb.append(f'<path style="{style}" d="')

    x0, y0 = arc_xy(0, Rs)
    sb.append(f'M {x0} {y0}')
    da = 360 / cogs
    a0 = 0
    for i in range(0, cogs):
        p = [
            arc_xy(a0+da*0.3, Rs),
            arc_xy(a0+da*0.5, R),
            arc_xy(a0+da*0.8, R),
            arc_xy(a0+da, Rs)
        ]
        sb.append(f' A {Rs:.2f} {Rs:.2f} 0 0 1 {p[0][0]:.2f} {p[0][1]:.2f}')
        sb.append(f' L {p[1][0]:.2f} {p[1][1]:.2f}')
        sb.append(f' A {R:.2f} {R:.2f} 0 0 1 {p[2][0]:.2f} {p[2][1]:.2f}')
        if i==cogs-1:
            sb.append(' Z')
        else:
            sb.append(f' L {p[3][0]:.2f} {p[3][1]:.2f}')
        a0 += da

    sb.append(f' M {mid} {mid - axis_radius}')
    sb.append(f' A {axis_radius} {axis_radius} 0 0 0 {mid} {mid + axis_radius}')
    sb.append(f' A {axis_radius} {axis_radius} 0 0 0 {mid} {mid - axis_radius}')

    if spokes>1 and Rin+min_spoke_length<=Rrim:
        da = 360 / spokes
        wa_rim = math.degrees(math.asin(spoke_width * 0.5 / Rrim))
        wa_in = math.degrees(math.asin(spoke_width * 0.5 / Rin))
        if wa_in*2<da:
            a0 = 0
            for i in range(0, spokes):
                p = [
                    arc_xy(a0+wa_in, Rin),
                    arc_xy(a0+da-wa_in, Rin),
                    arc_xy(a0+da-wa_rim, Rrim),
                    arc_xy(a0+wa_rim, Rrim),
                ]
                sb.append(f' M {p[0][0]:.2f} {p[0][1]:.2f}')
                sb.append(f' A {Rin:.2f} {Rin:.2f} 0 0 1 {p[1][0]:.2f} {p[1][1]:.2f}')
                sb.append(f' L {p[2][0]:.2f} {p[2][1]:.2f}')
                sb.append(f' A {Rrim:.2f} {Rrim:.2f} 0 0 0 {p[3][0]:.2f} {p[3][1]:.2f}')
                sb.append(f' Z')
                a0 += da

    sb.append('"/>')
    sb.append('</svg>')

    out = ''.join(sb)
    if file_name:
        with io.open(file_name, 'wt') as f:
            f.write(out)
    return out
