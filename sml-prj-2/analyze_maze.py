from PIL import Image, ImageDraw
import numpy as np

with open("maze_00.txt", "r") as f:
    detected_maze = f.readlines()

detected_maze = [m.split() for m in detected_maze]
detected_maze = [list(map(float, m)) for m in detected_maze]

min_width = min([label[3] for label in detected_maze])
size = int(1 / min_width)
px_size = 32
image = Image.new("RGB", (size * px_size, size * px_size), (255, 255, 255))
draw = ImageDraw.Draw(image)

analyzed_maze = np.zeros((size, size))

for label in detected_maze:
    class_id, x_center, y_center, width, height = label
    if class_id == 0:
        color = (0, 0, 0)
    elif class_id == 1:
        color = (255, 0, 0)
    elif class_id == 2:
        color = (0, 0, 255)

    x = (x_center - width / 2) * size * px_size
    y = (y_center - height / 2) * size * px_size
    w = width * size * px_size
    h = height * size * px_size

    x1 = (x + px_size / 2) // px_size
    y1 = (y + px_size / 2) // px_size
    x2 = (x + w + px_size / 2) // px_size
    y2 = (y + h + px_size / 2) // px_size
    print(x1, y1, x2, y2)

    draw.rectangle([x1 * px_size, y1 * px_size, x2 * px_size, y2 * px_size], fill=color)

    for i in range(int(y1), int(y2)):
        for j in range(int(x1), int(x2)):
            analyzed_maze[i][j] = int(class_id) + 1

image.show()

with open("analyzed_maze.txt", "w") as f:
    for y in range(size):
        for x in range(size):
            f.write(str(int(analyzed_maze[y][x])) + " ")
        f.write("\n")
