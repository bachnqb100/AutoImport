import tkinter as tk


class ClickPosition:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mouse Click Icon")

        # Set the app to full screen
        self.root.attributes("-fullscreen", True)

        self.root.wait_visibility(self.root)
        self.root.attributes("-alpha", 0.05)

        self.canvas = tk.Canvas(self.root, background="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.create_icon)

    def create_icon(self, event):
        x, y = event.x, event.y
        icon_size = 30
        self.canvas.create_oval(x, y, x + icon_size, y + icon_size, fill="blue")
        self.pos = [x, y]
        print(self.pos)
        self.stop()
    def run(self):
        self.root.mainloop()

    def stop(self):
        self.root.destroy()

if __name__ == "__main__":

    #main
    app = ClickPosition()
    app.run()
