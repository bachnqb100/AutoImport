import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import time
import pyautogui
import keyboard
import os
import pandas as pd


QUIT_KEY = "esc"


def is_valid_file_path(path):
    return os.path.exists(path)


def is_excel_file(file_path):

    if not is_valid_file_path(file_path):
        return False
    # Get the file extension from the path
    file_extension = os.path.splitext(file_path)[1]

    # Check if the file extension is for Excel files
    if file_extension.lower() in (".xlsx", ".xls"):
        return True
    else:
        return False


def get_value_in_line(filename, line_number):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if 1 <= line_number <= len(lines):
                return lines[line_number - 1].strip()  # Subtract 1 to convert to zero-based indexing
            else:
                return "Line number out of range"
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return str(e)

def count_lines(filename):
    try:
        with open(filename, 'r') as file:
            line_count = sum(1 for line in file)
        return line_count
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return str(e)
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
        self.app.geometry("800x750")

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
        #
        # # Set up application icon
        # icon_path = "zoro.ico"
        # self.app.iconbitmap(icon_path)

        # Configure column and row weights for left_frame, right_frame, and text_frame
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_rowconfigure(1, weight=1)

        # Left Column Widgets
        button_font = ("Roboto", 15)

        # seconds per step
        self.label_time_per_step = tk.Label(left_frame, text="Seconds per Step:", anchor="w", height=1)
        self.label_time_per_step.grid(row=0, column=0, padx=1, pady=1, sticky="ew")

        self.time_per_step_entry_var = tk.StringVar()
        self.time_per_step_entry_var.set(str(0.05))

        self.time_per_step_entry = tk.Entry(left_frame, textvariable=self.time_per_step_entry_var)
        self.time_per_step_entry.grid(row=1, column=0, padx=1, pady=1, sticky="ew")

        # seconds per loop
        self.label_time_per_loop = tk.Label(left_frame, text="Seconds per Loop:", anchor="w", height=1)
        self.label_time_per_loop.grid(row=2, column=0, padx=1, pady=1, sticky="ew")

        self.time_per_loop_entry_var = tk.StringVar()
        self.time_per_loop_entry_var.set(str(0.1))

        self.time_per_loop_entry = tk.Entry(left_frame, textvariable=self.time_per_loop_entry_var)
        self.time_per_loop_entry.grid(row=3, column=0, padx=1, pady=1, sticky="ew")

        # count
        self.label_count = tk.Label(left_frame, text="Loop Count:", anchor="w", height=1)
        self.label_count.grid(row=4, column=0, padx=1, pady=1, sticky="ew")

        self.count_entry_var = tk.StringVar()
        self.count_entry = tk.Entry(left_frame, textvariable=self.count_entry_var)
        self.count_entry.grid(row=5, column=0, padx=1, pady=1, sticky="ew")

        # Add click Data
        self.setup_file_button = tk.Button(left_frame, text="Add Click", command=self.add_click, bg="yellow", font=button_font)
        self.setup_file_button.grid(row=6, column=0, padx=1, pady=1, sticky="ew")

        # Add String Data
        # path
        self.label_input = tk.Label(left_frame, text="Input File Data:", anchor="w", height=1)
        self.label_input.grid(row=7, column=0, padx=1, pady=1, sticky="ew")

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(left_frame, textvariable=self.entry_var)
        self.entry.grid(row=8, column=0, padx=1, pady=1, sticky="ew")

        self.browse_button = tk.Button(left_frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=8, column=1, padx=1, pady=1, sticky="ew")

        # excel path
        self.label_excel_input = tk.Label(left_frame, text="Excel File Data:", anchor="w", height=1)
        self.label_excel_input.grid(row=9, column=0, padx=1, pady=1, sticky="ew")

        self.entry_excel_var = tk.StringVar()
        self.entry_excel = tk.Entry(left_frame, textvariable=self.entry_excel_var)
        self.entry_excel.grid(row=10, column=0, padx=1, pady=1, sticky="ew")

        self.browse_excel_button = tk.Button(left_frame, text="Browse", command=self.browse_excel_file)
        self.browse_excel_button.grid(row=10, column=1, padx=1, pady=1, sticky="ew")

        # excel column name
        self.label_excel_column_name = tk.Label(left_frame, text="Excel column name:", anchor="w", height=1)
        self.label_excel_column_name.grid(row=11, column=0, padx=1, pady=1, sticky="ew")

        self.excel_column_name_var = tk.StringVar()
        self.excel_column_name_var.set("Mã Voucher")

        self.excel_column_name_entry = tk.Entry(left_frame, textvariable=self.excel_column_name_var)
        self.excel_column_name_entry.grid(row=12, column=0, padx=1, pady=1, sticky="ew")

        # add input file
        self.setup_action_button = tk.Button(left_frame, text="Add Input", command=self.add_input, bg="yellow", font=button_font)
        self.setup_action_button.grid(row=13, column=0, padx=1, pady=1, sticky="ewn")

        # Add keyboard

        self.label_input_key = tk.Label(left_frame, text="Input Key:", anchor="w", height=1)
        self.label_input_key.grid(row=14, column=0, padx=1, pady=1, sticky="ew")

        self.entry_key_var = tk.StringVar()
        self.entry_key = tk.Entry(left_frame, textvariable=self.entry_key_var)
        self.entry_key.grid(row=15, column=0, padx=1, pady=1, sticky="ew")

        self.setup_key_button = tk.Button(left_frame, text="Add Key", command=self.add_key_input, bg="yellow",
                                             font=button_font)
        self.setup_key_button.grid(row=16, column=0, padx=1, pady=1, sticky="ew")

        # Start import
        self.start_import_button = tk.Button(left_frame, text="Start Import", command=self.execute_actions, bg="green", font=button_font)
        self.start_import_button.grid(row=17, column=0, padx=1, pady=1, sticky="ew")

        # Clear import
        self.clear_import_button = tk.Button(left_frame, text="Clear Import", command=self.clear_actions, bg="red", font=button_font)
        self.clear_import_button.grid(row=18, column=0, padx=1, pady=1, sticky="ew")

        # Right Column (Listbox)
        self.list_box = tk.Listbox(right_frame)
        self.list_box.pack(fill="both", expand=True)

        # Text widget at the bottom
        self.log_text = tk.Text(text_frame, wrap="word", height=10, width=50)
        self.log_text.pack(fill="both", expand=True)

        # Init record actions
        self.actions = []
        self.path = " "
        self.count_voucher = 0
        self.has_path = False
        self.count_voucher_has_path = 0

        self.excel_path = " "

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.entry_var.set(file_path)
            self.log("Browse file successfully!!!")
        else:
            self.log("No path file data input???")

    def browse_excel_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.entry_excel_var.set(file_path)
            self.log("Browse excel file successfully!!!")
        else:
            self.log("No path file excel input???")


    def add_file(self):
        cached_path = self.entry_var.get()
        excel_cached_path = self.entry_excel_var.get()
        if cached_path:
            self.path = cached_path
            self.log("Setup string successfully!!!")

        if excel_cached_path:
            self.excel_path = excel_cached_path
            self.log("Get file data excel successfully!!!")

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

    def add_string(self, has_path, value, excel_path):
        self.actions.append(("string", has_path, value, excel_path))

    def add_key(self, value):
        self.actions.append(("key", value))

    def perform_actions(self, count, interval):
        for action in self.actions:
            if action[0] == "click":
                pyautogui.click(action[1], action[2])
            elif action[0] == "string":
                if not action[1]:
                    pyautogui.write(action[2])
                else:
                    data = get_value_in_line(action[2], count+1)
                    self.log("Input: " + data.__str__())
                    if data.__str__() in action[3]:
                        self.log("Data existed in excel file data, no input again....XXX")
                    else:
                        pyautogui.write(data)
            elif action[0] == "key":
                keyboard.send(action[1])
            time.sleep(interval)

    def execute_actions(self):
        self.log("Check action")
        string_action_number = 0
        for action in self.actions:
            if action[0] == "string":
                break
            string_action_number += 1

        self.log("Execute actions...")
        self.app.iconify()
        time_per_step = float(self.time_per_loop_entry_var.get())
        time_per_loop = float(self.time_per_loop_entry_var.get())
        self.log("Step interval: " + time_per_step.__str__())
        self.log("Loop interval: " + time_per_loop.__str__())

        if self.has_path:
            for i in range(self.count_voucher_has_path):
                self.log("Loop Count: " + i.__str__())
                self.perform_actions(i, time_per_step)
                time.sleep(time_per_loop)
            self.log("Done input from file!!!")
        else:
            count_input = int(self.count_entry_var.get())
            for i in range(count_input):
                self.log("Loop Count: " + i.__str__())
                self.perform_actions(i, time_per_step)
                time.sleep(time_per_loop)
            self.log("Done input " + count_input.__str__() + " times from input text box!!!")
        time.sleep(0.1)
        self.app.deiconify()

    def modify_string_value_in_action_string(self, action_type, *args):
        for index, action in enumerate(self.actions):
            if action[0] == action_type:
                if 0 <= index < len(self.actions):
                    self.actions[index] = (action_type,) + args

    def clear_actions(self):
        self.actions = []
        self.count_voucher_has_path = 0
        self.log("Clear all action...")
        self.list_box.delete(0, tk.END)
        self.has_path = False

    def add_input(self):
        self.add_file()

        excel_data = "NULL"

        if is_excel_file(self.excel_path):
            df = pd.read_excel(self.excel_path)

            excel_data = df[self.excel_column_name_var.get().__str__()].values


        if is_valid_file_path(self.path):
            self.has_path = True
            self.count_voucher_has_path = count_lines(self.path)
            self.add_string(True, self.path, excel_data)
            self.insert_message("Add string input into textbox from file!!!")
            self.log("Total voucher: " + self.count_voucher_has_path.__str__())
        else:
            self.add_string(False, self.path, excel_data)
            self.log("No input path???")
            self.insert_message("Add string input into textbox: " + self.path.__str__())
            self.log("If continuing, the value in textbox will fill!!!")

        # if (self.has_path):
        #     self.add_file()
        #     self.add_string("test")
        #     self.insert_message("Add string input into textbox from file!!!")
        #     self.log("Count voucher:...")
        #     with open(self.path, 'r') as file:
        #         # Iterate through each line in the file
        #         for line in file:
        #             # Process the line here
        #             self.count_voucher = self.count_voucher + 1
        #             self.log(line.strip())
        #     self.log("Total voucher: " + self.count_voucher.__str__())
        # else:
        #     cached_path = self.entry_var.get()
        #     self.path = cached_path
        #     self.log("No input path???")
        #     self.add_string(self.path)
        #     self.insert_message("Add string input into textbox: " + self.path.__str__())
        #     self.log("If continuing, the value in textbox will fill!!!")

    def add_key_input(self):
        self.add_key(self.entry_key_var.get())
        self.insert_message("Press key: " + self.entry_key_var.get())
        self.log("Add key input: " + self.entry_key_var.get())

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
    keyboard.add_hotkey(QUIT_KEY, app.stop)
    app.run()




