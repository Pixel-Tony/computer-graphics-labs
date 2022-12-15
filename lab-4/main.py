import os.path as path
import random as r
import PIL.Image as img
import PIL.ImageDraw as draw

IMG_WIDTH = 960
IMG_HEIGHT = 540


class Voronoi:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def _random_color(self) -> tuple[int, int, int]:
        return tuple(r.randint(25, 250) for _ in range(3))

    def _read_dots(self, dataset_path: str):
        with open(dataset_path, 'r') as file:
            self.dots = {
                (*map(int, line.split()),)
                [::-1] for line in file.readlines()
            }

    def _get_regions(self):
        def region_from(dot: tuple[int, int]):
            if dot not in dots:
                return
            region = []
            x, y = dot
            s = [(x, x, y, 1), (x, x, y - 1, -1)]
            while s:
                x1, x2, y, dy = s.pop()
                x = x1
                if (x, y) in dots:
                    while (d := (x - 1, y)) in dots:
                        region.append(d)
                        dots.remove(d)
                        x -= 1
                if x < x1:
                    s.append((x, x1 - 1, y - dy, -dy))
                while x1 <= x2:
                    while (d := (x1, y)) in dots:
                        region.append(d)
                        dots.remove(d)
                        x1 += 1
                        s.append((x, x1 - 1, y + dy, dy))
                        if x1 - 1 > x2:
                            s.append((x2 + 1, x1 - 1, y - dy, -dy))
                    x1 += 1
                    while x1 < x2 and ((x1, y) not in dots):
                        x1 += 1
                    x = x1
            return region

        dots = self.dots.copy()
        regions = []
        while dots:
            dots.add(dot := dots.pop())
            regions.append(region_from(dot))
        return [*map(lambda rg: (*map(self._int_avg, zip(*rg)),), regions)]

    def _int_avg(self, arr):
        return int(sum(arr) / len(arr))

    def _store_regions(self, regions, filename_out: str):
        with open(filename_out, 'w') as file:
            file.write(
                '|'.join(f"{p[0]} {p[1]}" for p in regions)
            )

    def _draw_regions(self, regions, result_path: str):
        def dist_sqr(p1, p2):
            return abs(p1[0] - p2[0]) ** 2 + abs(p1[1] - p2[1]) ** 2

        image = img.new('RGBA', (960, 540), (255, 255, 255))
        cols = {p: self._random_color() for p in regions}
        d = draw.ImageDraw(image)

        image.putdata([
            cols[min(((p, dist_sqr((x, y), p)) for p in regions),
                     key=lambda a: a[1]
                     )[0]]
            for y in range(self.height)
            for x in range(self.width)
        ])

        for p in regions:
            d.ellipse(((p[0] - 2, p[1] - 2), (p[0] + 2, p[1] + 2)), 0, 0, 1)

        for p in self.dots:
            color = tuple(max(a - 25, 0) for a in image.getpixel(p))
            image.putpixel(p, color)
        image.save(result_path)

    def draw(self, dataset_path: str, store_path: str, result_path: str):
        self._read_dots(dataset_path)

        if path.exists(store_path):
            with open(store_path, 'r') as file:
                regions = [
                    (*map(int, reg.split()),)
                    for reg in file.read().split('|')
                ]
        else:
            regions = self._get_regions()
            self._store_regions(regions, store_path)
        self._draw_regions(regions, result_path)


if __name__ == '__main__':
    Voronoi(IMG_WIDTH, IMG_HEIGHT).draw(
        dataset_path='../DS9.txt',
        store_path='store.txt',
        result_path='result/output.png'
    )
