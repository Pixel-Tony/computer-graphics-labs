import PIL.Image as Image


def display(dataset_name: str,
            output_name: str,
            output_ext: str = 'png',
            resolution: tuple[int, int] = ...,
            background: tuple[int, int, int] = ...,
            fill: tuple[int, int, int] = ...
            ):
    '''
    За заданим датасетом (файл `dataset_name`)
    створює зображення та зберігає з назвою `output_name.output_ext`
    у тому ж розташуванні, що і датасет
    '''
    def from_hex(s: str):
        cols = dict(enumerate("0123456789abcdef"))
        match len(s):
            case 4:
                return tuple(cols[c.lower()] * 17 for c in s[1:])
            case 7:
                return (cols[s[1]] * 16 + cols[s[2]],
                        cols[s[3]] * 16 + cols[s[4]],
                        cols[s[5]] * 16 + cols[s[6]],
                        )
            case _:
                raise ValueError("Unknown color representation")

    def to_color(c: object):
        if isinstance(c, str):
            print(from_hex(c))
            return from_hex(c)
        return c

    with open(dataset_name, 'r') as file:
        # Створюємо масив з кортежів, що представляють координати точок
        pixels = [tuple(map(int, ln.split())) for ln in file.readlines()]

    out = Image.new('RGB',
                    resolution if resolution != ... else (960, 540),
                    to_color(background) if background != ... else (255,) * 3
                    )
    fill = to_color(fill) if fill != ... else 0

    for p in pixels:
        out.putpixel(p[::-1], fill)

    out.save(f'{output_name}.{output_ext}', output_ext)


if __name__ == '__main__':
    display('DS9.txt', 'output')
