import cv2

img_path = "画像.png"
img = cv2.imread(img_path)

# 線を引く
# 画像の大きさを1として倍率で指定
x = 0.6
y = 0.5

color = (255, 0, 0)
thickness = 2
x_start = (x, 0)
x_end = (x, 1)
x_start_point = (int(img.shape[1] * x_start[0]), int(img.shape[0] * x_start[1]))
x_end_point = (int(img.shape[1] * x_end[0]), int(img.shape[0] * x_end[1]))
y_start = (0, y)
y_end = (1, y)
y_start_point = (int(img.shape[1] * y_start[0]), int(img.shape[0] * y_start[1]))
y_end_point = (int(img.shape[1] * y_end[0]), int(img.shape[0] * y_end[1]))

img = cv2.line(img, x_start_point, x_end_point, color, thickness)
img = cv2.line(img, y_start_point, y_end_point, color, thickness)

# 画像を表示
# ウインドウサイズを変更可能
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.imshow("image", img)
cv2.waitKey(0)
