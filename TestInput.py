import tkinter as tk

def button1_clicked():
    label.config(text="Button 1 Clicked")

def button2_clicked():
    label.config(text="Button 2 Clicked")

# Create the main window
root = tk.Tk()
root.title("Button App")

# Create buttons
button1 = tk.Button(root, text="Button 1", command=button1_clicked)
button2 = tk.Button(root, text="Button 2", command=button2_clicked)



# Arrange widgets using grid layout
button1.grid(row=0, column=0, padx=10, pady=10)
button2.grid(row=0, column=1, padx=10, pady=10)
label.grid(row=1, columnspan=2)

# Start the main event loop
root.mainloop()
