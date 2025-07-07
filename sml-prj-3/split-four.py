import cv2
import os


def split_four(folder):
    """
    指定したフォルダ内のすべての画像に対して処理を行う
    """
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".png"):
                path = os.path.join(root, file)
                split(path)


def split(img_path, save_dir="splitted_data"):
    """
    画像を四つに分割して保存する
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    h = h // 2
    w = w // 2
    img1 = img[:h, :w]
    img2 = img[:h, w:]
    img3 = img[h:, :w]
    img4 = img[h:, w:]
    cv2.imwrite(
        os.path.join(save_dir, os.path.basename(img_path)).replace(".png", "_1.png"),
        img1,
    )
    cv2.imwrite(
        os.path.join(save_dir, os.path.basename(img_path)).replace(".png", "_2.png"),
        img2,
    )
    cv2.imwrite(
        os.path.join(save_dir, os.path.basename(img_path)).replace(".png", "_3.png"),
        img3,
    )
    cv2.imwrite(
        os.path.join(save_dir, os.path.basename(img_path)).replace(".png", "_4.png"),
        img4,
    )


def convert_label(folder, save_dir="splitted_data"):
    """
    ラベルデータを四つに分割して保存する
    """
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".txt"):
                # ファイル名がclasses.txtの場合はスキップ
                if file == "classes.txt":
                    continue
                path = os.path.join(root, file)
                with open(path) as f:
                    data = f.readlines()
                data = [d.split() for d in data]
                data = [list(map(float, d)) for d in data]
                for d in data:
                    class_id, x_center, y_center, width, height = d
                    if x_center < 0.5 and y_center < 0.5:
                        div = 1
                    elif x_center >= 0.5 and y_center < 0.5:
                        div = 2
                    elif x_center < 0.5 and y_center >= 0.5:
                        div = 3
                    else:
                        div = 4

                    if div == 1:
                        x_center *= 2
                        y_center *= 2
                    elif div == 2:
                        x_center = 2 * (x_center - 0.5)
                        y_center *= 2
                    elif div == 3:
                        x_center *= 2
                        y_center = 2 * (y_center - 0.5)
                    else:
                        x_center = 2 * (x_center - 0.5)
                        y_center = 2 * (y_center - 0.5)

                    width *= 2
                    height *= 2

                    with open(
                        os.path.join(save_dir, os.path.basename(path)).replace(
                            ".txt", f"_{div}.txt"
                        ),
                        "a",
                    ) as f:
                        f.write(
                            f"{int(class_id)} {x_center} {y_center} {width} {height}\n"
                        )


split_four("data_dir")
convert_label("data_dir")
