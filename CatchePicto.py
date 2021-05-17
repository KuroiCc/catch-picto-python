# coding: utf-8
import tkinter as tk
import tkinter.font as font
import random
import math

root = tk.Tk()
root.title(u"Cathe Picto")
root.geometry("1200x900")

screen_width = 1200
screen_height = 900

canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="white")


class Human():
    def __init__(self, pic_path):
        self.image = tk.PhotoImage(file=pic_path, master=root)  # 表示画像の設定 "humanpicto.gif"

    def update(self):
        canvas.create_image(self.x, self.y, image=self.image, anchor=tk.NW)  # 設定画像の表示


class Catcher(Human):
    def __init__(self):
        self.x = screen_width // 2  # x座標をwindowの中心とする．
        self.y = screen_height // 2  # y座標をwindowの中心とする．
        super().__init__("catch-picto-python/catcher.gif")


class Runner(Human):
    def __init__(self):
        self.x = int(random.random() * (screen_width - 200)) + 100  # x座標の初期値を100からwindowサイズのx座標-100までにする．
        self.y = int(random.random() * (screen_height - 200)) + 100  # y座標の初期値を100からwindowサイズのx座標-100までにする．
        super().__init__("catch-picto-python/humanpicto.gif")

    def update(self, dx, dy):
        # 左右の壁に近いほど画面内に戻そうとする
        if self.x > screen_width * 0.9:
            self.dx_avoid_wall = math.log(self.x - 0.9 * screen_width + 1, 0.5)
        elif self.x < screen_width * 0.1:
            self.dx_avoid_wall = math.log(0.1 * screen_width - self.x + 1, 2)
        else:
            self.dx_avoid_wall = 0

        # 上下の壁に近いほど画面内に戻そうとする
        if self.y > screen_height * 0.9:
            self.dy_avoid_wall = math.log(self.y - 0.9 * screen_height + 1, 0.5)
        elif self.y < screen_height * 0.1:
            self.dy_avoid_wall = math.log(0.1 * screen_height - self.y + 1, 2)
        else:
            self.dy_avoid_wall = 0

        self.x = self.x + self.dx_avoid_wall + dx
        self.y = self.y + self.dy_avoid_wall + dy
        super().update()


catcher = Catcher()
runner = Runner()


def mouse_move_func(event):  # マウスが移動したときの処理
    catcher.x = event.x  # マウス座標をプレイヤーピクトグラムの座標に設定する
    catcher.y = event.y


root.bind(
    "<Motion>",  # 受付けるイベント（Motion: マウス移動）　
    mouse_move_func  # そのイベント時に実行する関数
)


def update():
    canvas.delete("all")  # canvas をまっさらにする．

    catcher.update()

    # catherとrunnerの距離を計算
    distance_x = catcher.x - runner.x
    distance_y = catcher.y - runner.y
    distance = distance_x**2 + distance_y**2

    # 距離が近いほどcatherからrunnerが早く逃げる
    dx = -distance_x / (distance ** 1.5) * 100000
    dy = -distance_y / (distance ** 1.5) * 100000
    if abs(dx) < 0.9:
        dx = 0
    if abs(dy) < 0.9:
        dy = 0

    runner.update(dx, dy)

    font1 = font.Font(family='Helvetica', size=50, weight='bold')  # 文字列のフォントを設定
    label = tk.Label(root, text="catch me", fg="black", bg="white", font=font1)  # 文字列を設定
    label.place(x=500, y=0)  # 場所を指定
    root.after(20, update)  # 20msec 後にupdateを呼出す


update()  # 起動時に一度実行する．
canvas.pack()  # 画面上に canvasオブジェクトを配置
root.mainloop()  # main プログラムの実行
