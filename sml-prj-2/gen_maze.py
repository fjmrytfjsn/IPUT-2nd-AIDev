import random


class GenerateMaze:
    # widthとheightは共に奇数かつ5以上の整数
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[1 for _ in range(width)] for _ in range(height)]
        self.start = [0, 0]
        self.goal = [0, 0]
        self._dig_walls()

    def _search_directions(self, y, x):
        directions = []
        if x - 2 > 0 and self.maze[y][x - 2] == 1:
            directions.append("L")
        if x + 2 < self.width and self.maze[y][x + 2] == 1:
            directions.append("R")
        if y - 2 > 0 and self.maze[y - 2][x] == 1:
            directions.append("U")
        if y + 2 < self.height and self.maze[y + 2][x] == 1:
            directions.append("D")
        return directions

    def _dig_walls(self):
        start_y = random.choice([i for i in range(1, self.height, 2)])
        start_x = random.choice([i for i in range(1, self.width, 2)])
        self.maze[start_y][start_x] = 0
        stack = [(start_y, start_x)]
        while stack:
            y, x = stack[-1]
            directions = self._search_directions(y, x)
            if directions == []:
                stack.pop()
                continue

            chose = random.choice(directions)
            if chose == "L":
                for i in range(1, 3):
                    self.maze[y][x - i] = 0
                x -= i
            elif chose == "R":
                for i in range(1, 3):
                    self.maze[y][x + i] = 0
                x += i
            elif chose == "U":
                for i in range(1, 3):
                    self.maze[y - i][x] = 0
                y -= i
            elif chose == "D":
                for i in range(1, 3):
                    self.maze[y + i][x] = 0
                y += i
            stack.append((y, x))

    def set_start_goal(self):
        edges = ["top", "bottom", "left", "right"]
        start_edge = random.choice(edges)
        edges.remove(start_edge)
        goal_edge = random.choice(edges)
        if start_edge == "top":
            start_y = 0
            start_x = random.choice([i for i in range(1, self.width, 2)])
        elif start_edge == "bottom":
            start_y = self.height - 1
            start_x = random.choice([i for i in range(1, self.width, 2)])
        elif start_edge == "left":
            start_y = random.choice([i for i in range(1, self.height, 2)])
            start_x = 0
        elif start_edge == "right":
            start_y = random.choice([i for i in range(1, self.height, 2)])
            start_x = self.width - 1

        while True:
            if goal_edge == "top":
                goal_y = 0
                goal_x = random.choice([i for i in range(1, self.width, 2)])
            elif goal_edge == "bottom":
                goal_y = self.height - 1
                goal_x = random.choice([i for i in range(1, self.width, 2)])
            elif goal_edge == "left":
                goal_y = random.choice([i for i in range(1, self.height, 2)])
                goal_x = 0
            elif goal_edge == "right":
                goal_y = random.choice([i for i in range(1, self.height, 2)])
                goal_x = self.width - 1

            if not (abs(start_y - goal_y) == 1 and abs(start_x - goal_x) == 1):
                break

        self.start = (start_y, start_x)
        self.goal = (goal_y, goal_x)
        self.maze[start_y][start_x] = 2
        self.maze[goal_y][goal_x] = 3

    def print_maze(self, print_width=2):
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == 0:
                    print(" " * print_width, end="")
                elif self.maze[y][x] == 1:
                    print("#" * print_width, end="")
                elif self.maze[y][x] == 2:
                    print("S" * print_width, end="")
                elif self.maze[y][x] == 3:
                    print("G" * print_width, end="")
            print()

    def get_start(self):
        return self.start

    def get_goal(self):
        return self.goal

    def get_maze(self):
        return self.maze


if __name__ == "__main__":

    def check_value(user):
        if user < 5 or user % 2 == 0:
            return False
        else:
            return True

    while True:
        print("迷路を出力します")
        print("幅と高さが5以上の奇数を入力")
        try:
            width = int(input("Width = "))
            height = int(input("Height = "))
        except ValueError:
            print("有効な数字を入力して下さい\n")
            continue

        if all([check_value(width), check_value(height)]):
            break

    maze = GenerateMaze(width, height)
    maze.set_start_goal()
    maze.print_maze()
