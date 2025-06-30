from PIL import Image
from bfs_slove import bfs_solve


def find_start_goal(maze):
    for i, row in enumerate(maze):
        if 2 in row:
            start = (i, row.index(2))
        if 3 in row:
            goal = (i, row.index(3))
    return start, goal


def main():
    with open("analyzed_maze.txt", "r") as f:
        maze = f.readlines()

    maze = [list(map(int, maze.strip().split())) for maze in maze]

    size = len(maze)
    start, goal = find_start_goal(maze)

    ans = bfs_solve(maze, start, goal, size)

    px_size = 32
    image = Image.new("RGB", (size * px_size, size * px_size), (255, 255, 255))
    for y_idx, raw in enumerate(maze):
        for x_idx, item in enumerate(raw):
            if item == 0:
                color = (255, 255, 255)
            elif item == 1:
                color = (0, 0, 0)
            elif item == 2:
                color = (255, 0, 0)
            elif item == 3:
                color = (0, 0, 255)
            if (y_idx, x_idx) in ans[1:-1]:
                color = (0, 255, 0)
            x = x_idx * px_size
            y = y_idx * px_size
            image.paste(color, (x, y, x + px_size, y + px_size))

    image.save("solved_maze.png")


if __name__ == "__main__":
    main()
