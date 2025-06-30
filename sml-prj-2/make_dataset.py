import os
from PIL import Image

import gen_maze


def create_unique_maze_directory(base_path="./data/maze"):
    """
    一意の迷路ディレクトリを作成する。
    既存のディレクトリがある場合は、連番を付けて新しいディレクトリを作成する。
    """
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    i = 1
    while os.path.exists(f"{base_path}/maze{i}"):
        i += 1
    new_path = f"{base_path}/maze{i}"
    os.makedirs(new_path)
    return new_path


def make_dataset(num_data, size, px_size=32):
    """
    指定された数の迷路データセットを生成し、一意のディレクトリに保存する。
    """
    # 保存先ディレクトリの作成
    save_dir = create_unique_maze_directory()

    for i in range(num_data):
        # 迷路の生成
        maze = gen_maze.GenerateMaze(size, size)
        maze.set_start_goal()
        maze_data = (
            maze.get_maze()
        )  # 迷路データ (0: 通路, 1: 壁, 2: スタート, 3: ゴール)

        # 画像の生成
        # 通路: 白, 壁: 黒, スタート: 赤, ゴール: 青
        # 一マス32x32で描画
        image = Image.new(
            "RGB",
            ((size) * px_size, (size) * px_size),
            (255, 255, 255),
        )
        for y in range(size):
            for x in range(size):
                if maze_data[y][x] == 1:
                    color = (0, 0, 0)
                elif maze_data[y][x] == 2:
                    color = (255, 0, 0)
                elif maze_data[y][x] == 3:
                    color = (0, 0, 255)
                image.paste(
                    color,
                    (
                        (x) * px_size,
                        (y) * px_size,
                        (x + 1) * px_size,
                        (y + 1) * px_size,
                    ),
                )
        # すべての偶数行、偶数列に対して連続するwallを長方形として保存
        labels = []
        start_idx = (-1, -1)
        count = 0
        for y in range(size):
            for x in range(size):
                if y % 2 == 0:
                    if maze_data[y][x] == 1:
                        if start_idx == (-1, -1):
                            start_idx = (y, x)
                            count += 1
                        elif start_idx != (-1, -1):
                            count += 1
                    else:
                        if start_idx != (-1, -1):
                            if count > 1:
                                class_id = 0
                                x_center = (start_idx[1] + count / 2) / (size)
                                y_center = (start_idx[0] + 0.5) / (size)
                                width = count / (size)
                                height = 1 / (size)
                                labels.append(
                                    f"{class_id} {x_center} {y_center} {width} {height}"
                                )
                        start_idx = (-1, -1)
                        count = 0
                    if x == size - 1:
                        if start_idx != (-1, -1):
                            if count > 1:
                                class_id = 0
                                x_center = (start_idx[1] + count / 2) / (size)
                                y_center = (start_idx[0] + 0.5) / (size)
                                width = count / (size)
                                height = 1 / (size)
                                labels.append(
                                    f"{class_id} {x_center} {y_center} {width} {height}"
                                )
                        start_idx = (-1, -1)
                        count = 0

        for x in range(size):
            for y in range(size):
                if x % 2 == 0:
                    if maze_data[y][x] == 1:
                        if start_idx == (-1, -1):
                            start_idx = (y, x)
                            count += 1
                        elif start_idx != (-1, -1):
                            count += 1
                    else:
                        if start_idx != (-1, -1):
                            if count > 1:
                                class_id = 0
                                x_center = (start_idx[1] + 0.5) / (size)
                                y_center = (start_idx[0] + count / 2) / (size)
                                width = 1 / (size)
                                height = count / (size)
                                labels.append(
                                    f"{class_id} {x_center} {y_center} {width} {height}"
                                )
                        start_idx = (-1, -1)
                        count = 0
                if y == size - 1:
                    if start_idx != (-1, -1):
                        if count > 1:
                            class_id = 0
                            x_center = (start_idx[1] + 0.5) / (size)
                            y_center = (start_idx[0] + count / 2) / (size)
                            width = 1 / (size)
                            height = count / (size)
                            labels.append(
                                f"{class_id} {x_center} {y_center} {width} {height}"
                            )
                    start_idx = (-1, -1)
                    count = 0

        # スタートとゴールのラベルを追加
        start_y, start_x = maze.get_start()
        goal_y, goal_x = maze.get_goal()
        labels.append(
            f"1 {(start_x + 0.5) / size} {(start_y + 0.5) / size} {1 / size} {1 / size}"
        )
        labels.append(
            f"2 {(goal_x + 0.5) / size} {(goal_y + 0.5) / size} {1 / size} {1 / size}"
        )

        # 重複排除
        labels = list(set(labels))

        # 画像とラベルとクラスファイルの保存
        # 二桁の数字になるようにフォーマット
        id = str(i).zfill(2)
        image.save(f"{save_dir}/maze_{id}.png")
        with open(f"{save_dir}/maze_{id}.txt", "w") as f:
            f.write("\n".join(labels))
        with open(f"{save_dir}/classes.txt", "w") as f:
            f.write("wall\nstart\ngoal\n")


def check_value(user):
    """
    幅と高さが5以上の奇数であるかをチェックする
    """
    if user < 5 or user % 2 == 0:
        return False
    return True


def get_user_input(prompt):
    """
    幅と高さの入力を受け付ける
    """
    while True:
        try:
            value = int(input(prompt))
            if check_value(value):
                return value
            else:
                print("幅と高さは5以上の奇数である必要があります。\n")
        except ValueError:
            print("有効な数字を入力して下さい。\n")


def main():
    print("迷路データセットを生成します")
    print("迷路のサイズとして、5以上の奇数を入力して下さい")
    size = get_user_input("Size = ")
    print("データの数を入力して下さい")
    num_data = int(input("Num data = "))
    make_dataset(num_data, size)


if __name__ == "__main__":
    main()
