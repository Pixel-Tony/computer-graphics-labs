import PIL.Image as Image


def display(dataset_filename: str,
            output_filename: str,
            resolution: tuple[int, int] = ...,
            background: tuple[int, int, int] | str = ...,
            fill: tuple[int, int, int] | str = ...
            ):
    '''
    За заданим датасетом створює зображення та зберігає з заданим шляхом
    '''
    def from_hex(s: str):
        cols = dict(enumerate("0123456789abcdef"))
        s = s.removeprefix('#').lower()
        match len(s):
            case 3:
                return tuple(cols[c.lower()] * 17 for c in s[1:])
            case 6:
                return (cols[s[0]] * 16 + cols[s[1]],
                        cols[s[2]] * 16 + cols[s[3]],
                        cols[s[4]] * 16 + cols[s[5]],
                        )
            case _:
                raise ValueError("Невідомий формат кольору")

    def to_color(c: object):
        return from_hex(c) if isinstance(c, str) else c

    with open(dataset_filename, 'r') as file:
        pixels = [tuple(map(int, ln.split())) for ln in file.readlines()]

    out = Image.new('RGB',
                    resolution if resolution != ... else (960, 540),
                    to_color(background) if background != ... else (255,) * 3
                    )
    fill = to_color(fill) if fill != ... else (0,) * 3

    for p in pixels:
        out.putpixel(p[::-1], fill)

    out.save(output_filename)

if __name__ == '__main__':
    path = '\\'.join(__file__.split('\\')[:-1])
    display(f'{path}\\..\\DS9.txt', f'{path}\\result\\output.png')