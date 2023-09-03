import tkinter as tk
from tkinter import messagebox


class ActionRecordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Action Record App")

        # Initialize the list to store actions
        self.actions = []

        # Create a label
        label = tk.Label(root, text="Enter an action:")
        label.pack(pady=10)

        # Create an entry widget
        self.action_entry = tk.Entry(root)
        self.action_entry.pack()

        # Create a button to add actions
        add_button = tk.Button(root, text="Add Action", command=self.add_action)
        add_button.pack(pady=5)

        # Create a listbox to display actions
        self.action_listbox = tk.Listbox(root)
        self.action_listbox.pack(padx=10, pady=10)

        # Create a button to clear actions
        clear_button = tk.Button(root, text="Clear Actions", command=self.clear_actions)
        clear_button.pack(pady=5)

    def add_action(self):
        action_text = self.action_entry.get()
        if action_text:
            self.actions.append(action_text)
            self.action_listbox.insert(tk.END, action_text)
            self.action_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter an action.")

    def clear_actions(self):
        self.actions = []
        self.action_listbox.delete(0, tk.END)


def main():
    root = tk.Tk()
    app = ActionRecordApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
