import os
import random
import time
import threading
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageShuffler:
    def __init__(self, root):
        self.root = root
        self.root.title("Выбиратор случайных изображений 2")
        self.root.geometry("820x920")  # Размер для сетки

        # Поле для выбора папки
        self.select_folder_button = tk.Button(root, text="Выбрать папку", command=self.select_folder)
        self.select_folder_button.pack(pady=5)

        # Поле для настройки скорости
        self.speed_label = tk.Label(root, text="Скорость (сек):")
        self.speed_label.pack()
        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_entry = tk.Entry(root, textvariable=self.speed_var, width=5)
        self.speed_entry.pack()

        # Поле для количества изображений в ряду
        self.count_label = tk.Label(root, text="Количество изображений в ряду:")
        self.count_label.pack()
        self.count_var = tk.IntVar(value=5)
        self.count_entry = tk.Entry(root, textvariable=self.count_var, width=5)
        self.count_entry.pack()

        # Поле для количества рядов
        self.rows_label = tk.Label(root, text="Количество рядов:")
        self.rows_label.pack()
        self.rows_var = tk.IntVar(value=3)
        self.rows_entry = tk.Entry(root, textvariable=self.rows_var, width=5)
        self.rows_entry.pack()

        # Область для отображения изображений
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack(pady=10)

        # Кнопки "Запуск" и "Стоп"
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=5)

        self.start_button = tk.Button(self.control_frame, text="Запуск", command=self.start_shuffling)
        self.start_button.pack(side='left', padx=5)

        self.stop_button = tk.Button(self.control_frame, text="Стоп", command=self.stop_shuffling)
        self.stop_button.pack(side='left', padx=5)

        self.images = []
        self.thread = None
        self.running = False

    def load_image(self, image_path):
        """Загружает изображение с использованием Pillow и преобразует в массив NumPy."""
        try:
            img = Image.open(image_path)
            img = img.convert("RGB")
            return np.array(img)
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")
            return None

    def display_images(self, images):
        """Отображает изображения в виде сетки на канвасе, распределяя по рядам."""
        self.canvas.delete("all")
        width, height = 100, 100  # Размер каждого изображения
        spacing = 2  # Расстояние между изображениями

        count_rows = self.rows_var.get()
        total_images = len(images)
        images_per_row = total_images // count_rows
        remainder = total_images % count_rows

        index = 0
        self.canvas.images = []  # Обнуляем список ссылок
        for row in range(count_rows):
            count_in_this_row = images_per_row + (1 if row < remainder else 0)
            for col in range(count_in_this_row):
                if index >= total_images:
                    break
                img = images[index]
                if img is not None:
                    pil_img = Image.fromarray(img)
                    pil_img = pil_img.resize((width, height))
                    img_tk = ImageTk.PhotoImage(pil_img)
                    x = col * (width + spacing)
                    y = row * (height + spacing)
                    self.canvas.create_image(x, y, anchor='nw', image=img_tk)
                    self.canvas.images.append(img_tk)
                index += 1

    def shuffle_display_images(self, images):
        """Обновляет изображения в виде сетки с заданной скоростью."""
        self.running = True
        while self.running:
            total_images = self.count_var.get() * self.rows_var.get()
            selected_images = []
            for _ in range(total_images):
                img_path = random.choice(images)
                image = self.load_image(img_path)
                selected_images.append(image)
            self.display_images(selected_images)
            time.sleep(self.speed_var.get())

    def start_shuffling(self):
        """Запускает поток ретрансляции изображений."""
        if self.thread and self.thread.is_alive():
            self.running = False
            self.thread.join()
        if self.images:
            self.thread = threading.Thread(target=self.shuffle_display_images, args=(self.images,), daemon=True)
            self.thread.start()

    def stop_shuffling(self):
        """Останавливает поток ретрансляции изображений."""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def select_folder(self):
        """Выбор папки и автоматический запуск ретрансляции."""
        folder_path = filedialog.askdirectory(title="Выберите папку")
        if folder_path:
            self.images = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                           if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
            if self.images:
                self.start_shuffling()
            else:
                print("В выбранной папке нет изображений.")

# Создание интерфейса
root = tk.Tk()
app = ImageShuffler(root)

# Запуск интерфейса
root.mainloop()
