import tkinter as tk
from tkinter import ttk

class MainApp:
    def __init__(self):

        self.app = tk.Tk()
        self.app.title("Auto Import Data")
        self.app.geometry("600x200")

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

        self.browse_button = tk.Button(self.app, text="Setup File", command=self.setup_file, bg="gray", font=button_font)
        self.browse_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.save_button1 = tk.Button(self.app, text="Setup Action", command=self.setup_action, bg="gray", font=button_font)
        self.save_button1.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.save_button2 = tk.Button(self.app, text="Start Import", command=self.start_import, bg="green", font=button_font)
        self.save_button2.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    def setup_file(self):
        # Define the behavior of the "Setup File" button.
        pass

    def setup_action(self):
        # Define the behavior of the "Setup Action" button(s).
        pass

    def start_import(self):
        # Define the behavior of the "Setup Action" button(s).
        pass

# Create an instance of the MainApp class
app = MainApp()

# Start the tkinter main loop
app.app.mainloop()
