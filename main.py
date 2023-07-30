import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import glob
import os

# 获取data目录下的所有.png文件
images = glob.glob('data/*.png')

# 确保有足够的图片
if len(images) < 16:
    raise ValueError("你需要至少16张不同的图片。")

# 获取所有文件名（不包括扩展名）
image_names = [os.path.splitext(os.path.basename(img_path))[0] for img_path in images]

correct_image_included = True

# 初始化分数和尝试次数为0
score = 0
attempts = 0


def check_image(name, img_path, no_correct_image=False):
    global score, attempts
    correct_name = os.path.splitext(os.path.basename(img_path))[0] if img_path else None
    attempts += 1
    if no_correct_image and not correct_image_included:
        # messagebox.showinfo("结果", "正确！")
        score += 1
    elif not no_correct_image and name == correct_name:
        # messagebox.showinfo("结果", "正确！")
        score += 1
    else:
        messagebox.showinfo("结果", "错误！")
    show_random()


def show_random():
    global correct_image_included
    name = random.choice(image_names)
    correct_image_included = random.random() > 0.2
    correct_image = os.path.join('data', f'{name}.png') if correct_image_included else None
    remaining_images = [img for img in images if img != correct_image] if correct_image else images[:]

    if correct_image_included:
        selected_images = random.sample(remaining_images, 15) + [correct_image]
    else:
        selected_images = random.sample(remaining_images, 16)

    random.shuffle(selected_images)

    # 清除现有的图像和标签
    for widget in root.winfo_children():
        widget.destroy()

    # 显示名称
    label = tk.Label(root, text=str(name), font=("Helvetica", 32))
    label.grid(row=0, column=0, columnspan=4, padx=10, pady=30)

    # 显示图片
    for i, img_path in enumerate(selected_images):
        img = Image.open(img_path)
        img = img.resize((100, 100))  # 重新调整大小
        photo = ImageTk.PhotoImage(img)
        button = tk.Button(root, image=photo, command=lambda img_path=img_path: check_image(name, img_path))
        button.image = photo  # 让python保留对photo的引用
        button.grid(row=i // 4 + 1, column=i % 4, padx=10, pady=10)

    # 添加一个表示“正确答案不在这十六张图片中”的按钮
    button = tk.Button(root, text="正确答案不在这十六张图片中", command=lambda: check_image(name, None, True))
    button.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    # 显示分数
    score_label = tk.Label(root, text="分数: " + str(score), font=("Helvetica", 24))
    score_label.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

    # 显示正确率
    accuracy_label = tk.Label(root, text="正确率: " + "{:.2%}".format(score / attempts) if attempts else "N/A",
                              font=("Helvetica", 24))
    accuracy_label.grid(row=7, column=0, columnspan=4, padx=10, pady=10)


root = tk.Tk()
root.title("layu")
show_random()
root.mainloop()
