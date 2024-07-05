import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        self.image_window = None
        self.panel = None

        self.create_widgets()

        self.image = None
        self.cap = None
        self.previewing = False

        self.root.bind('<Configure>', self.resize_canvas)

    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        btn_load = tk.Button(top_frame, text="Выбрать фото с компьютера", command=self.load_image)
        btn_load.grid(row=0, column=0, padx=5, pady=5)

        btn_open_webcam = tk.Button(top_frame, text="Открыть веб-камеру", command=self.open_webcam)
        btn_open_webcam.grid(row=0, column=1, padx=5, pady=5)

        btn_capture = tk.Button(top_frame, text="Сделать снимок", command=self.capture_image)
        btn_capture.grid(row=0, column=2, padx=5, pady=5)

        btn_close_webcam = tk.Button(top_frame, text="Закрыть веб-камеру", command=self.close_webcam)
        btn_close_webcam.grid(row=0, column=3, padx=5, pady=5)

        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        bottom_frame = tk.Frame(self.root)
        bottom_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)
        bottom_frame.columnconfigure(2, weight=1)
        bottom_frame.columnconfigure(3, weight=1)

        channel_frame = tk.LabelFrame(bottom_frame, text="Выбор цветового канала", padx=10, pady=10)
        channel_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.channel_var = tk.StringVar(value="All")
        tk.Radiobutton(channel_frame, text="Все каналы", variable=self.channel_var, value="All", command=self.show_channel).pack(anchor=tk.W)
        tk.Radiobutton(channel_frame, text="Красный", variable=self.channel_var, value="R", command=self.show_channel).pack(anchor=tk.W)
        tk.Radiobutton(channel_frame, text="Зелёный", variable=self.channel_var, value="G", command=self.show_channel).pack(anchor=tk.W)
        tk.Radiobutton(channel_frame, text="Синий", variable=self.channel_var, value="B", command=self.show_channel).pack(anchor=tk.W)

        resize_frame = tk.LabelFrame(bottom_frame, text="Изменить размер изображения", padx=10, pady=10)
        resize_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(resize_frame, text="Высота:").grid(row=0, column=0)
        self.height_entry = tk.Entry(resize_frame, width=5)
        self.height_entry.grid(row=0, column=1)

        tk.Label(resize_frame, text="Ширина:").grid(row=1, column=0)
        self.width_entry = tk.Entry(resize_frame, width=5)
        self.width_entry.grid(row=1, column=1)

        btn_resize = tk.Button(resize_frame, text="Изменить размер", command=self.resize_image)
        btn_resize.grid(row=2, column=0, columnspan=2, pady=5)

        rectangle_frame = tk.LabelFrame(bottom_frame, text="Нарисовать синий прямоугольник", padx=10, pady=10)
        rectangle_frame.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        tk.Label(rectangle_frame, text="Координаты левой верхней вершины").grid(row=0, column=0, columnspan=2)
        tk.Label(rectangle_frame, text="X:").grid(row=1, column=0)
        self.x1_entry = tk.Entry(rectangle_frame, width=5)
        self.x1_entry.grid(row=1, column=1)

        tk.Label(rectangle_frame, text="Y:").grid(row=2, column=0)
        self.y1_entry = tk.Entry(rectangle_frame, width=5)
        self.y1_entry.grid(row=2, column=1)

        tk.Label(rectangle_frame, text="Координаты правой нижней вершины").grid(row=3, column=0, columnspan=2)
        tk.Label(rectangle_frame, text="X:").grid(row=4, column=0)
        self.x2_entry = tk.Entry(rectangle_frame, width=5)
        self.x2_entry.grid(row=4, column=1)

        tk.Label(rectangle_frame, text="Y:").grid(row=5, column=0)
        self.y2_entry = tk.Entry(rectangle_frame, width=5)
        self.y2_entry.grid(row=5, column=1)

        btn_rectangle = tk.Button(rectangle_frame, text="Нарисовать", command=self.draw_rectangle)
        btn_rectangle.grid(row=6, column=0, columnspan=2, pady=5)

        brightness_frame = tk.LabelFrame(bottom_frame, text="Понизить яркость изображения", padx=10, pady=10)
        brightness_frame.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        tk.Label(brightness_frame, text="Значение уменьшения яркости:").grid(row=0, column=0)
        self.brightness_entry = tk.Entry(brightness_frame, width=5)
        self.brightness_entry.grid(row=0, column=1)

        btn_brightness = tk.Button(brightness_frame, text="Понизить яркость", command=self.decrease_brightness)
        btn_brightness.grid(row=0, column=2, padx=5, pady=5)

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
        if not file_path:
            return

        try:
            self.image = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            if self.image is None:
                raise ValueError("Could not open or find the image")
            self.show_image(self.image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {e}")

    def open_webcam(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Failed to open webcam")
            return
        self.previewing = True
        self.preview_webcam()

    def close_webcam(self):
        if self.cap:
            self.cap.release()
            self.cap = None
        self.previewing = False

    def preview_webcam(self):
        if not self.previewing:
            return

        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture image from webcam")
            return

        self.show_image(frame)
        self.root.after(10, self.preview_webcam)

    def capture_image(self):
        if not self.cap or not self.cap.isOpened():
            messagebox.showerror("Error", "Webcam is not opened")
            return

        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture image")
            return

        self.image = frame
        self.close_webcam()
        self.show_image(self.image)

    def show_image(self, image):
        self.current_image = image
        self.update_canvas()

    def update_canvas(self):
        if self.current_image is None:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        image_height, image_width = self.current_image.shape[:2]
        image_ratio = image_width / image_height

        if canvas_width / canvas_height > image_ratio:
            display_width = int(canvas_height * image_ratio)
            display_height = canvas_height
        else:
            display_width = canvas_width
            display_height = int(canvas_width / image_ratio)

        resized_image = cv2.resize(self.current_image, (display_width, display_height))
        b, g, r = cv2.split(resized_image)
        img = cv2.merge((r, g, b))
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)

        self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
        self.canvas.image = imgtk

    def show_channel(self):
        if self.image is None:
            return

        channel = self.channel_var.get()
        if channel == "All":
            self.show_image(self.image)
        else:
            channel_index = {"R": 2, "G": 1, "B": 0}[channel]
            channel_image = np.zeros_like(self.image)
            channel_image[:, :, channel_index] = self.image[:, :, channel_index]
            self.show_image(channel_image)

    def resize_image(self):
        if self.image is None:
            return

        try:
            new_height = int(self.height_entry.get())
            new_width = int(self.width_entry.get())
            resized_image = cv2.resize(self.image, (new_width, new_height))
            self.image = resized_image
            self.show_image(self.image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to resize image: {e}")

    def draw_rectangle(self):
        if self.image is None:
            return

        try:
            x1 = int(self.x1_entry.get())
            y1 = int(self.y1_entry.get())
            x2 = int(self.x2_entry.get())
            y2 = int(self.y2_entry.get())
            cv2.rectangle(self.image, (x1, y1), (x2, y2), (255, 0, 0), 2)
            self.show_image(self.image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to draw rectangle: {e}")

    def decrease_brightness(self):
        if self.image is None:
            messagebox.showerror("Error", "No image loaded")
            return

        try:
            decrease_value = int(self.brightness_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid brightness value")
            return

        # Вычисляем коэффициент уменьшения яркости
        brightness_ratio = 1 - (decrease_value / 255.0)

        # Уменьшаем яркость изображения
        self.image = np.clip(self.image * brightness_ratio, 0, 255).astype(np.uint8)
        self.show_image(self.image)

    def resize_canvas(self, event):
        self.update_canvas()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
