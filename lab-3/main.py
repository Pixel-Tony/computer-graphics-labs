import PIL.Image as img
import PIL.ImageDraw as Draw


def convex_hull(dataset_src: str, dataset_hull_name: str, output_name: str):
    def counter_clockwise(pts: list[tuple[int, int]]) -> bool:
        '''Чи утворюють точки поворот проти годинникової стрілки'''
        a, b, c = pts
        if a[0] == b[0]:
            if b[1] > a[1]:
                return c[0] <= a[0]
            return c[0] >= a[0]

        q = (b[1] - a[1]) / (b[0] - a[0])
        return ((b[0] > a[0])*2 - 1)*(q*(c[0] - a[0]) + a[1] - c[1]) <= 0

    def draw_n_save(points):
        with open(dataset_hull_name, 'w') as file:
            file.writelines(' '.join(map(str, p)) + '\n' for p in points)

        image = img.new('RGB', (960, 540), (255,) * 3)
        for i in range(len(points) - 1):
            Draw.Draw(image).line(
                (points[i], points[i + 1]),
                fill=(50, 150, 255),
                width=1
            )
            image.putpixel(points[i], 0)
        image.putpixel(points[-1], 0)
        image.save(output_name)

    with open(dataset_src, 'r') as file:
        points = [
            tuple(map(int, line.split()))[::-1]
            for line in file.readlines()
        ]

    length = len(points)
    if length == 2:
        return draw_n_save(points)

    points.sort()

    upper_hull, lower_hull = [], []

    for i in range(length):
        while len(lower_hull) >= 2 \
                and not counter_clockwise(lower_hull[-2:] + [points[i]]):
            lower_hull.pop()
        lower_hull.append(points[i])
    lower_hull.pop()

    for i in range(length - 1, -1, -1):
        while len(upper_hull) >= 2 \
                and not counter_clockwise(upper_hull[-2:] + [points[i]]):
            upper_hull.pop()
        upper_hull.append(points[i])
    upper_hull.pop()

    return draw_n_save(upper_hull + lower_hull)


if __name__ == '__main__':
    path = '\\'.join(__file__.split('\\')[:-1])
    convex_hull(
        f'{path}\\..\\DS9.txt',
        f'{path}\\..\\DS9_convex_hull.txt',
        f'{path}\\result\\output.png'
    )
