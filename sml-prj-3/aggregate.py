import numpy as np


class Mahjong:
    def __init__(self, data):
        self.data = data
        self.tiles = np.zeros((6, 37), int)
        self.called_tiles = np.empty((3, 0, 2), int)
        self.out_tiles = []
        self.is_safe = np.full((3, 37), True, bool)
        self.my_tiles = np.empty((0, 4), int)  # 自分の牌
        self.my_hand = np.empty(0, int)  # 手牌
        self.my_called = []  # 鳴いた牌の集合: (牌の集合, 0: チー, 1: ボン, 2: カン)

    def aggregate(self):
        """
        それぞれのプレイヤーがそれぞれの牌を何枚捨てているかと、
        それぞれのプレイヤーが鳴いているかを集計する
        自身の手牌と鳴き牌を取得する
        """
        self.data = [d.split() for d in self.data]
        self.data = [list(map(float, d)) for d in self.data]

        # player... 0: 自家, 1: 下家, 2: 対面, 3: 上家, 4: 鳴き牌, 5: ドラ表示牌
        for d in self.data:
            class_id, x_center, y_center, width, height = d
            class_id = int(class_id)
            player = 0
            if x_center > 0.13 and y_center > 0.5:
                player = 0
                if y_center > 0.75:
                    self.my_tiles = np.append(
                        self.my_tiles,
                        np.array([[class_id, x_center, width, height]]),
                        axis=0,
                    )
                    continue
            elif x_center > 0.6 and y_center <= 0.5:
                player = 1
                if x_center > 0.78 and y_center < 0.75:
                    np.append(self.called_tiles[0], [[class_id, y_center]], axis=0)
                    if class_id == 37:
                        continue
                    player = 4
            elif 0.16 <= x_center <= 0.6 and y_center < 0.255:
                player = 2
                if x_center < 0.7 and y_center < 0.1:
                    np.append(self.called_tiles[1], [[class_id, x_center]], axis=0)
                    if class_id == 37:
                        continue
                    player = 4
            elif (0.16 <= x_center < 0.4 and y_center <= 0.5) or (
                x_center <= 0.13 and y_center >= 0.255
            ):
                player = 3
                if x_center <= 0.13 and y_center >= 0.255:
                    np.append(self.called_tiles[2], [[class_id, y_center]], axis=0)
                    if class_id == 37:
                        continue
                    player = 4
            elif 0.02 < x_center < 0.16 and 0.05 < y_center < 0.12:
                if class_id == 37:
                    continue
                player = 5

            self.tiles[player][class_id] += 1

        # 他家の鳴き牌の暗槓を処理
        for tiles in self.called_tiles:
            tiles = tiles[np.argsort(tiles[:, 1])]
            for i in range(len(tiles)):
                if tiles[i][0] == 37:
                    self.tiles[4][int(tiles[i + 1][0])] += 2
                    i += 3

        self.my_tiles = self.my_tiles[np.argsort(self.my_tiles[:, 1])]
        idx = 0
        space = 0
        for i in range(1, len(self.my_tiles)):
            if self.my_tiles[i][1] - self.my_tiles[i - 1][1] > space:
                idx = i
                space = self.my_tiles[i][1] - self.my_tiles[i - 1][1]
        self.my_hand = self.my_tiles[:idx, 0]
        my_called_tiles = np.array(
            [
                self.my_tiles[idx:, 0],
                self.my_tiles[idx:, 2]
                > self.my_tiles[idx:, 3],  # 幅が高さより大きい -> 倒れている
            ]
        ).T
        back_num = np.count_nonzero(my_called_tiles[:, 0] == 37)  # 裏返っている牌の数
        concealed_kong_num = back_num / 2  # 暗カンの数

        # 赤ドラ用の処理
        np.where(my_called_tiles[:, 0] == 9, 4, my_called_tiles[:, 0])
        np.where(my_called_tiles[:, 0] == 19, 14, my_called_tiles[:, 0])
        np.where(my_called_tiles[:, 0] == 29, 24, my_called_tiles[:, 0])

        current_idx = 0
        while concealed_kong_num > 0:
            if my_called_tiles[current_idx, 0] == 37:
                self.my_called.append(
                    (my_called_tiles[current_idx : current_idx + 4, 0], 2)
                )
                self.tiles[4][int(my_called_tiles[current_idx + 1, 0])] += 2
                np.delete(my_called_tiles, slice(current_idx, current_idx + 4), axis=0)
                concealed_kong_num -= 1
                current_idx += 4
            else:
                current_idx += 1

        current_idx = 0
        while current_idx < len(my_called_tiles):
            current_block = my_called_tiles[current_idx : current_idx + 3, :]
            current_block = current_block[np.argsort(current_block[:, 0])]
            next_block = my_called_tiles[current_idx + 3 : current_idx + 6, :]
            current_tapped_num = np.count_nonzero(current_block[:, 1])
            next_tapped_num = np.count_nonzero(next_block[:, 1])
            if current_tapped_num == 1:
                if (
                    current_block[0, 0]
                    == current_block[1, 0] - 1
                    == current_block[2, 0] - 2
                ):
                    self.my_called.append((current_block[:, 0], 0))
                    current_idx += 3
                else:
                    if current_idx + 6 < len(my_called_tiles):
                        if next_tapped_num == 0:
                            next_tile = my_called_tiles[current_idx + 3, :]
                            if next_tile[0] == current_block[0, 0]:
                                self.my_called.append(
                                    my_called_tiles[current_idx : current_idx + 4, 0], 2
                                )
                                current_idx += 4
                            else:
                                self.my_called.append((current_block[:, 0], 1))
                                current_idx += 3
                        else:
                            self.my_called.append((current_block[:, 0], 1))
                            current_idx += 3
                    else:
                        self.my_called.append((current_block[:, 0], 1))
                        current_idx += 3
            else:
                self.my_called.append(
                    (my_called_tiles[current_idx : current_idx + 4, 0], 2)
                )
                current_idx += 4

    def get_out_tiles(self):
        """
        四枚見えている牌を返す
        """
        for i in range(37):
            count = 0
            for j in range(6):
                count += self.tiles[j][i]
                if i < 30:  # 赤ドラ用の処理
                    if i % 10 == 4:
                        count += self.tiles[j][i + 5]
                    if i % 10 == 9:
                        count += self.tiles[j][i - 5]
            count += self.my_tiles[:, 0].tolist().count(i)
            if count == 4:
                self.out_tiles.append(i)

        return self.out_tiles

    def get_is_safe(self):
        """
        それぞれのプレイヤーに対して、それぞれの牌が安全かどうかを返す
        """
        for i in range(37):
            for j in range(3):
                if self.tiles[j + 1][i] == 0:  # 捨てていないか
                    self.is_safe[j][i] = False

        return self.is_safe

    def get_dora(self):
        """
        ドラの配列を返す
        """
        dora = []
        for i in range(37):
            if self.tiles[5][i] > 0:
                if i < 30:  # 数字牌
                    temp = i // 10
                    if i % 10 == 9:  # 赤ドラ
                        dora.append([temp * 10 + 4, self.tiles[5][i]])
                    else:
                        dora.append([temp * 10 + (i + 1) % 10, self.tiles[5][i]])
                elif i < 34:  # 風牌
                    dora.append([30 + (i - 30 + 1) % 4, self.tiles[5][i]])
                else:  # 三元牌
                    dora.append([34 + (i - 34 + 1) % 3, self.tiles[5][i]])

        return dora


if __name__ == "__main__":
    data_file = "ma-jann\DN2024-07-19 171503.txt"
    with open(data_file) as f:
        data = f.readlines()
    mahjong = Mahjong(data)
    mahjong.aggregate()
    out_tiles = mahjong.get_out_tiles()
    is_safe = mahjong.get_is_safe()

    with open("classes.txt") as f:
        classes = f.readlines()
    classes = [c.strip() for c in classes]

    print("\n--------------------------------------------------\n")

    print("それぞれのプレイヤーの捨て牌は以下の通りです\n")
    for i in range(4):
        tiles = mahjong.tiles[i]
        if i == 0:
            print("自家", end=": ")
        elif i == 1:
            print("下家", end=": ")
        elif i == 2:
            print("対面", end=": ")
        else:
            print("上家", end=": ")
        for j, tile in enumerate(tiles):
            if tile > 0:
                print(classes[j], tile, end=", ")
        print()

    print("\n--------------------------------------------------\n")

    print("他家に鳴かれた牌は以下の通りです\n")
    tiles = mahjong.tiles[4]
    for i, tile in enumerate(tiles):
        if tile > 0:
            print(classes[i], tile, end=", ")
    print()

    print("\n--------------------------------------------------\n")

    print("ドラ表示牌は以下の通りです\n")
    tiles = mahjong.tiles[5]
    for i, tile in enumerate(tiles):
        if tile > 0:
            print(classes[i], tile, end=", ")
    print()

    print("\n--------------------------------------------------\n")

    print("ドラは以下の通りです\n")
    dora = mahjong.get_dora()
    for tile in dora:
        print(classes[int(tile[0])], tile[1], end=", ")
    print()

    print("\n--------------------------------------------------\n")

    print("四枚見えている牌は以下の通りです\n")
    for tile in out_tiles:
        print(classes[tile], end=", ")
    if len(out_tiles) == 0:
        print("なし", end="")
    print()

    print("\n--------------------------------------------------\n")

    print("自家の手牌は以下の通りです\n")
    for tile in mahjong.my_hand:
        print(classes[int(tile)], end=", ")
    print()

    print("\n--------------------------------------------------\n")

    print("自家が鳴いた牌は以下の通りです\n")
    for called in mahjong.my_called:
        if called[1] == 0:
            print("チー", end=": ")
        elif called[1] == 1:
            print("ポン", end=": ")
        else:
            print("カン", end=": ")
        print("[", end="")
        for tile in called[0]:
            print(classes[int(tile)], end=", ")
        print("]", end=", ")
    print()

    print("\n--------------------------------------------------\n")

    print("それぞれのプレイヤーに対する安牌は以下の通りです\n")
    for i in range(3):
        if i == 0:
            print("下家", end=": ")
        elif i == 1:
            print("対面", end=": ")
        else:
            print("上家", end=": ")
        for tile in mahjong.my_hand:
            if is_safe[i][int(tile)]:
                print(classes[int(tile)], end=", ")
        print()

    print("\n--------------------------------------------------\n")
