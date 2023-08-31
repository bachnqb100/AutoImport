import tkinter as tk
import time

class ClickPosition:
    def __init__(self, callback):
        self.root = tk.Tk()
        self.root.title("Mouse Click Icon")
        self.callback = callback
        # Set the app to full screen
        self.root.attributes("-fullscreen", True)

        self.root.wait_visibility(self.root)
        self.root.attributes("-alpha", 0.05)

        self.canvas = tk.Canvas(self.root, background="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.pos = 0
        self.canvas.bind("<Button-1>", self.create_icon)
        print("Position: ", self.pos)

    def create_icon(self, event):
        x, y = event.x, event.y
        icon_size = 30
        self.canvas.create_oval(x, y, x + icon_size, y + icon_size, fill="blue")
        self.pos = [x, y]
        self.callback(self.pos)
        time.sleep(0.5)
        self.stop()

    def run(self):
        self.root.mainloop()

    def stop(self):
        print("Position when stop: ", self.pos)
        self.root.destroy()

class AddAction:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Add Action")
        self.root.geometry("300x500")

        self.label = tk.Label(self.root, text="Press a button")
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.root.grid_columnconfigure(0, weight=1)

        self.button1 = tk.Button(self.root, text="Click", command=self.button1_clicked, bg="yellow")
        self.button1.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.button2 = tk.Button(self.root, text="Input", command=self.button2_clicked, bg="gray")
        self.button2.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.button3 = tk.Button(self.root, text="Debug position click", command=self.button3_clicked, bg="gray")
        self.button3.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.position =0

    def button1_clicked(self):
        self.label.config(text="Add click action")
        self.minimize_window()
        self.click_action = ClickPosition(self.update_position)
        self.click_action.run()
        self.click_action.stop()


    def update_position(self, position):
        self.position = position
        self.deminimize_window()
        self.label.config(text="Add click at position: " + self.position.__str__())


    def button3_clicked(self):
        self.label.config(text="Add click at position: " + self.position.__str__())

    def minimize_window(self):
        self.root.iconify()

    def deminimize_window(self):
        self.root.deiconify()
    def debug(self, x):
        self.label.config(text=x)

    def button2_clicked(self):
        self.label.config(text="Add input action")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AddAction()
    app.run()
