import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
import random
import time
from PIL import Image, ImageTk
import threading

class ImageShuffler:
    def __init__(self, root):
        self.root = root
        self.root.title("Выбиратор случайных изображений")
        self.root.geometry("320x120")

        self.select_folder_button = tk.Button(root, text="Выбрать папку", command=self.select_folder)
        self.select_folder_button.pack(pady=10)

        self.image_label = tk.Label(root)
        self.image_label.pack()

    def load_image(self, image_path):
        """Загружает изображение с использованием Pillow и преобразует в массив NumPy для OpenCV."""
        try:
            img = Image.open(image_path)
            img = img.convert("RGB")
            return np.array(img)
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")
            return None

    def display_image(self, image):
        """Отображает изображение в окне Tkinter."""
        img = Image.fromarray(image)
        img = img.resize((300, 300))  # Изменяем размер для отображения
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def shuffle_display_images(self, images):
        """Случайно выбирает и отображает изображения с интервалом в 1 секунду."""
        while True:  # Бесконечный цикл
            img_path = random.choice(images)
            image = self.load_image(img_path)
            if image is not None:
                self.display_image(image)
            time.sleep(1)

    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Выберите папку")

        if folder_path:
            images = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

            if images:
                threading.Thread(target=self.shuffle_display_images, args=(images,), daemon=True).start()
            else:
                print("В выбранной папке нет изображений.")

# Создание графического интерфейса
root = tk.Tk()
app = ImageShuffler(root)

# Запустить основной цикл интерфейса
root.mainloop()
