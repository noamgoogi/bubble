import cv2
import numpy as np

cam = cv2.VideoCapture(0)

size = 50
visited = set()
front = set()
active = False

cv2.namedWindow("Bubble", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Bubble", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


def getAvgRGB(frame, x, y, w, h):
    x1 = x * size
    y1 = y * size

    x2 = min(x1 + size, w)
    y2 = min(y1 + size, h)

    region = frame[y1:y2, x1:x2]

    if region.size == 0:
        return (0, 0, 0)

    avg_color = np.mean(region, axis=(0, 1))
    return tuple(map(int, avg_color))


def step_bubble(w, h):
    global front, visited, active

    if not front:
        active = False
        return

    next_front = set()

    for x, y in front:
        if (x, y) in visited:
            continue

        if x < 0 or y < 0 or x >= w // size or y >= h // size:
            continue

        visited.add((x, y))

        for n in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            if n not in visited:
                next_front.add(n)

    front = next_front


def draw(frame, w, h):
    for x, y in front:
        color = getAvgRGB(frame, x, y, w, h)
        cv2.rectangle(frame, (x * size, y * size), (x * size + size, y * size + size), color, -1)


def mouse_event(event, mx, my, flags, param):
    global front, visited, active, w, h

    if event == cv2.EVENT_LBUTTONDOWN:
        if active:
            return

        grid_x = mx // size
        grid_y = my // size

        visited = set()
        front = {(grid_x, grid_y)}
        active = True


cv2.setMouseCallback("Bubble", mouse_event)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    step_bubble(w, h)
    draw(frame, w, h)

    cv2.imshow("Bubble", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()