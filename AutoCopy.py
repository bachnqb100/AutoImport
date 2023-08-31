import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import time
import pyautogui
class FilePathApp:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("File Path Input")

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.app, textvariable=self.entry_var, width=80)
        self.entry.grid(row=0, column=0, padx=1, pady=10)

        self.browse_button = tk.Button(self.app, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=1, padx=1, pady=10)

        self.save_button = tk.Button(self.app, text="Confirm", command=self.save_file_path_and_close)
        self.save_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.entry_var.set(file_path)

    def save_file_path_and_close(self):
        cached_path = self.entry_var.get()
        if cached_path:
            self.path = cached_path
            self.app.destroy()

    def run(self):
        self.app.mainloop()

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

        self.canvas.bind("<Button-1>", self.create_icon)
        self.pos = [0,0]

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

    def get_pos(self, position):
        position = self.pos

    def stop(self):
        self.root.destroy()

class ActionRecorder:
    def __init__(self):
        self.actions = []

    def record_click(self, x, y):
        self.actions.append(("click", x, y))

    def record_key(self, key):
        self.actions.append(("key", key))

    def perform_actions(self):
        for action in self.actions:
            if action[0] == "click":
                pyautogui.click(action[1], action[2])
            elif action[0] == "key":
                pyautogui.write(action[1])
            time.sleep(0.5)

    def modify_action(self, action_type, *args):
        for index, action in enumerate(self.actions):
            if action[0] == action_type:
                if 0 <= index < len(self.actions):
                    self.actions[index] = (action_type,) + args

class AddAction:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Add Action")
        self.root.geometry("300x150")

        self.label = tk.Label(self.root, text="Press a button")
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.root.grid_columnconfigure(0, weight=1)

        self.button1 = tk.Button(self.root, text="Click", command=self.button1_clicked, bg="yellow")
        self.button1.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.button2 = tk.Button(self.root, text="Input", command=self.button2_clicked, bg="gray")
        self.button2.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.position = 0


    def button1_clicked(self):
        self.label.config(text="Add click action")
        click_action = ClickPosition(self.update_position)
        click_action.run()
        click_action.stop()


    def update_position(self, pos):
        self.position = pos
        self.label.config(text="Add click at position: " + self.position.__str__())

    def button2_clicked(self):
        self.label.config(text="Add input action")

    def run(self):
        self.root.mainloop()

class MainApp:
    def __init__(self):

        self.app = tk.Tk()
        self.app.title("Auto Import Data")
        self.app.geometry("600x300")

        # Set up custom title font using ttk.Style
        title_font = ("Roboto", 16, "bold")
        style = ttk.Style()
        style.configure("Title.TLabel", font=title_font)

        # Set up application icon
        icon_path = "zoro.ico"
        self.app.iconbitmap(icon_path)

        # Set column weights to make buttons expand horizontally
        button_font = ("Roboto", 15)
        self.app.grid_columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.app, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0, padx=1, pady=10, sticky="ew")

        self.browse_button = tk.Button(self.app, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=1, padx=1, pady=10, sticky="ew")

        self.browse_button = tk.Button(self.app, text="Setup File", command=self.setup_file, bg="gray", font=button_font)
        self.browse_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.save_button1 = tk.Button(self.app, text="Setup Action", command=self.setup_action, bg="gray", font=button_font)
        self.save_button1.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.save_button2 = tk.Button(self.app, text="Start Import", command=self.start_import, bg="green", font=button_font)
        self.save_button2.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.log_text = tk.Text(self.app, wrap="word", height=10, width=50)  # Set the height and width
        self.log_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.entry_var.set(file_path)
            self.log("Browse file successfully!!!")
            self.log("Click \"Setup File\"...")

    def setup_file(self):
        cached_path = self.entry_var.get()
        if cached_path:
            self.path = cached_path
            self.log("Setup file successfully!!!")

    def setup_action(self):
        add_action = AddAction()
        add_action.run()

    def start_import(self):
        # Define the behavior of the "Setup Action" button(s).
        pass

    def run(self):
        self.app.mainloop()


if __name__ == "__main__":

    #main
    app = MainApp()
    app.run()

    #get path
    # file_path_app = FilePathApp()
    # file_path_app.run()
    # file_path = file_path_app.path

    #gen actions record


    # with open(file_path, 'r') as file:
    #     for line in file:
    #         print(line.strip())
