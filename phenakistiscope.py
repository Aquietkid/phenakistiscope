import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

class RotatingImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Rotator")

        self.canvas = tk.Canvas(root, width=400, height=400, bg="gray")
        self.canvas.pack()

        controls = tk.Frame(root)
        controls.pack(pady=10)

        tk.Label(controls, text="Speed (°/sec)").grid(row=0, column=0, padx=5)
        self.speed_var = tk.DoubleVar(value=180)
        tk.Spinbox(controls, from_=-10000, to=10000, increment=10,
                   textvariable=self.speed_var, width=8).grid(row=0, column=1, padx=5)

        tk.Label(controls, text="Interval (ms)").grid(row=0, column=2, padx=5)
        self.interval_var = tk.DoubleVar(value=0)
        tk.Spinbox(controls, from_=0, to=100000, increment=50,
                   textvariable=self.interval_var, width=8).grid(row=0, column=3, padx=5)

        ttk.Button(controls, text="Load Image", command=self.load_image).grid(row=0, column=4, padx=5)
        ttk.Button(controls, text="Start", command=self.start_rotation).grid(row=0, column=5, padx=5)
        ttk.Button(controls, text="Stop", command=self.stop_rotation).grid(row=0, column=6, padx=5)

        self.running = False
        self.angle = 0

    def load_image(self):
        path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff"),
                ("All files", "*.*")
            ]
        )
        if not path:
            return
        self.original_img = Image.open(path)
        self.display_image(self.original_img)

    def display_image(self, img):
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.image = img_tk
        self.canvas.create_image(200, 200, image=img_tk)

    def rotate(self):
        if not self.running:
            return
        speed = self.speed_var.get()
        interval = self.interval_var.get()
        dt = 0.016 if interval == 0 else interval / 1000.0
        self.angle = (self.angle + speed * dt) % 360
        rotated = self.original_img.rotate(self.angle, resample=Image.BICUBIC)
        self.display_image(rotated)
        delay = 1 if interval == 0 else int(interval)
        self.root.after(delay, self.rotate)

    def start_rotation(self):
        if not hasattr(self, 'original_img'):
            return
        self.running = True
        self.rotate()

    def stop_rotation(self):
        self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = RotatingImageApp(root)
    root.mainloop()
