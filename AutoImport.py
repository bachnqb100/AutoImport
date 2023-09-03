import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import time
import pyautogui
import keyboard

QUIT_KEY = "esc"


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

class MainApp:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Auto Import Data")
        self.app.geometry("800x500")

        # Create a frame to hold the left column widgets
        left_frame = tk.Frame(self.app)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Set up row and column weights to make widgets expand
        left_frame.grid_columnconfigure(0, weight=1)

        # Create a frame to hold the right column widgets (Listbox)
        right_frame = tk.Frame(self.app)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Create a frame to hold the Text widget at the bottom
        text_frame = tk.Frame(self.app)
        text_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Set up custom title font using ttk.Style
        title_font = ("Roboto", 16, "bold")
        style = ttk.Style()
        style.configure("Title.TLabel", font=title_font)

        # Set up application icon
        icon_path = "zoro.ico"
        self.app.iconbitmap(icon_path)

        # Configure column and row weights for left_frame, right_frame, and text_frame
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_rowconfigure(1, weight=1)

        # Left Column Widgets
        button_font = ("Roboto", 15)

        self.label_count = tk.Label(left_frame, text="Loop Count:", anchor="w", height=1)
        self.label_count.grid(row=0, column=0, padx=1, pady=1, sticky="ew")

        self.count_entry_var = tk.StringVar()
        self.count_entry = tk.Entry(left_frame, textvariable=self.count_entry_var)
        self.count_entry.grid(row=1, column=0, padx=1, pady=10, sticky="ew")

        self.label_input = tk.Label(left_frame, text="Input File Data:", anchor="w", height=1)
        self.label_input.grid(row=2, column=0, padx=1, pady=1, sticky="ew")

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(left_frame, textvariable=self.entry_var)
        self.entry.grid(row=3, column=0, padx=1, pady=1, sticky="ew")

        self.browse_button = tk.Button(left_frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=3, column=1, padx=1, pady=10, sticky="ew")

        self.setup_action_button = tk.Button(left_frame, text="Add Input", command=self.add_input, bg="yellow", font=button_font)
        self.setup_action_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.setup_file_button = tk.Button(left_frame, text="Add Click", command=self.add_click, bg="yellow", font=button_font)
        self.setup_file_button.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        self.start_import_button = tk.Button(left_frame, text="Start Import", command=self.execute_actions, bg="green", font=button_font)
        self.start_import_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        # Right Column (Listbox)
        self.list_box = tk.Listbox(right_frame)
        self.list_box.pack(fill="both", expand=True)

        # Text widget at the bottom
        self.log_text = tk.Text(text_frame, wrap="word", height=10, width=50)
        self.log_text.pack(fill="both", expand=True)\

        # Init record actions
        self.actions = []
        self.path = " "
        self.count_voucher = 0

        self.has_path = False

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.entry_var.set(file_path)
            self.has_path = True
            self.log("Browse file successfully!!!")
        else:
            self.has_path = False
            self.log("No path input, value input is value in the text box???")

    def add_file(self):
        cached_path = self.entry_var.get()
        if cached_path:
            self.path = cached_path
            self.log("Setup file successfully!!!")

    def add_click(self):
        self.log("Add click action...")
        self.app.iconify()
        click_action = ClickPosition(self.update_position)
        click_action.run()
        click_action.stop()

    def update_position(self, pos):
        position = pos
        self.app.deiconify()
        self.add_position(pos[0], pos[1])
        self.insert_message("Click at position: " + position.__str__())
        self.log("Add click at position: " + position.__str__())

    # Region executed add action and run
    def add_position(self, x, y):
        self.actions.append(("click", x, y))

    def add_string(self, value):
        self.actions.append(("string", value))

    def perform_actions(self):
        for action in self.actions:
            if action[0] == "click":
                pyautogui.click(action[1], action[2])
            elif action[0] == "string":
                pyautogui.write(action[1])
            time.sleep(0.01)

    def execute_actions(self):
        self.log("Execute actions...")
        self.app.iconify()
        if (self.has_path):
            with open(self.path, 'r') as file:
                # Iterate through each line in the file
                for line in file:
                    # Process the line here
                    self.log("Add voucher: " + line.strip())
                    self.modify_string_value_in_action_string("string", line.strip())
                    self.perform_actions()
                    time.sleep(0.5)
        else:
            count_input = int(self.count_entry_var.get())
            self.log("Add voucher: " + self.path.__str__())
            for i in range(count_input):
                self.perform_actions()
                time.sleep(0.5)

        self.app.deiconify()
    def modify_string_value_in_action_string(self, action_type, *args):
        for index, action in enumerate(self.actions):
            if action[0] == action_type:
                if 0 <= index < len(self.actions):
                    self.actions[index] = (action_type,) + args

    def add_input(self):
        self.count_voucher = 0
        if (self.has_path):
            self.add_file()
            self.add_string("test")
            self.insert_message("Add string input into textbox!!!")
            self.log("Count voucher:...")
            with open(self.path, 'r') as file:
                # Iterate through each line in the file
                for line in file:
                    # Process the line here
                    self.count_voucher = self.count_voucher + 1
                    self.log(line.strip())
            self.log("Total voucher: " + self.count_voucher.__str__())
        else:
            cached_path = self.entry_var.get()
            self.path = cached_path
            self.log("No input path???")
            self.add_string(self.path)
            self.insert_message("Add string input into textbox but default???")
            self.log("If continuing, the value in textbox will fill!!!")


    def log_message(self, message):
        print(message)
        self.log(message)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def insert_message(self, message):
        self.list_box.insert(tk.END, message)

    def run(self):
        self.app.mainloop()

    def stop(self):
        self.app.destroy()


if __name__ == "__main__":
    app = MainApp()
    app.run()

    keyboard.add_hotkey(QUIT_KEY, app.stop)


