import matplotlib.pyplot as plt
import numpy as np


def draw():
    grid = np.zeros((size, size))

    for x, y in visited:
        grid[y][x] = 1

    plt.clf()
    plt.imshow(grid, cmap="Blues", vmin=0, vmax=1)
    plt.pause(0.1)


def bubble(x, y):
    current = {(x, y)}

    while current:
        next_layer = set()

        for x, y in current:
            if (x, y) in visited:
                continue

            if x < 0 or y < 0 or x >= size or y >= size:
                continue

            visited.add((x, y))

            next_layer.add((x+1, y))
            next_layer.add((x-1, y))
            next_layer.add((x, y+1))
            next_layer.add((x, y-1))

        draw()

        current = next_layer


visited = set()
size = 21

plt.ion()
plt.figure()

bubble(size//2, size//2-5)

plt.ioff()
plt.show()