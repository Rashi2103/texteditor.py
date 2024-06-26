import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

class TextEditor:
    def __init__(self, window):
        self.window = window
        self.text_edit = tk.Text(window, font="TimesNewRoman 12")
        self.text_edit.grid(row=0, column=1)
        self.file_stack = []
        self.undo_stack = []
        self.redo_stack = []
        self.search_dict = {}

        frame = tk.Frame(window, relief=tk.RAISED, bd=2)
        save_button = tk.Button(frame, text="Save", command=self.save_file)
        open_button = tk.Button(frame, text="Open", command=self.open_file)
        undo_button = tk.Button(frame, text="Undo", command=self.undo)
        redo_button = tk.Button(frame, text="Redo", command=self.redo)
        word_count_button = tk.Button(frame, text="Word Count", command=self.word_count)
        search_button = tk.Button(frame, text="Search", command=self.search_text)

        save_button.grid(row=0, column=0, padx=7, pady=7, sticky='ew')
        open_button.grid(row=1, column=0, padx=7, sticky='ew')
        undo_button.grid(row=2, column=0, padx=7, sticky='ew')
        redo_button.grid(row=3, column=0, padx=7, sticky='ew')
        word_count_button.grid(row=4, column=0, padx=7, sticky='ew')
        search_button.grid(row=5, column=0, padx=7, sticky='ew')
        frame.grid(row=0, column=0, sticky='ns')

        self.search_label = tk.Label(window, text="Search:")
        self.search_label.grid(row=1, column=0, padx=7, sticky='w')

        self.search_entry = tk.Entry(window, width=20)
        self.search_entry.grid(row=1, column=0, padx=7, sticky='ew')

        window.bind("<Control-s>", self.save_file_event)
        window.bind("<Control-o>", self.open_file_event)
        window.bind("<Control-z>", self.undo_event)
        window.bind("<Control-y>", self.redo_event)

    def open_file(self, event=None):
        filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])

        if not filepath:
            return
        self.text_edit.delete(1.0, tk.END)
        with open(filepath, "r") as f:
            content = f.read()
            self.text_edit.insert(tk.END, content)
        self.window.title(f"Open File: {filepath}")
        self.file_stack.append(filepath)
        self.undo_stack.append(self.text_edit.get(1.0, tk.END))
        self.redo_stack.clear()

    def save_file(self, event=None):
        if not self.file_stack:
            filepath = asksaveasfilename(filetypes=[("text files", "*.txt")])
        else:
            filepath = self.file_stack[-1]

        if not filepath:
            return

        with open(filepath, "w") as f:
            content = self.text_edit.get(1.0, tk.END)
            f.write(content)
        self.window.title(f"Open File: {filepath}")
        self.undo_stack.append(self.text_edit.get(1.0, tk.END))
        self.redo_stack.clear()

    def undo(self, event=None):
        if self.undo_stack:
            self.redo_stack.append(self.text_edit.get(1.0, tk.END))
            self.text_edit.delete(1.0, tk.END)
            self.text_edit.insert(tk.END, self.undo_stack.pop())

    def redo(self, event=None):
        if self.redo_stack:
            self.undo_stack.append(self.text_edit.get(1.0, tk.END))
            self.text_edit.delete(1.0, tk.END)
            self.text_edit.insert(tk.END, self.redo_stack.pop())

    def word_count(self):
        content = self.text_edit.get(1.0, tk.END)
        words = content.split()
        word_count = len(words)
        print(f"Word count: {word_count}")

    def search_text(self):
        search_term = self.search_entry.get()
        content = self.text_edit.get(1.0, tk.END)
        words = content.split()
        indices = [i for i, word in enumerate(words) if search_term.lower() in word.lower()]
        if indices:
            print(f"Found '{search_term}' at indices: {indices}")
        else:
            print(f"'{search_term}' not found")

    def save_file_event(self, event):
        self.save_file()

    def open_file_event(self, event):
        self.open_file()

    def undo_event(self, event):
        self.undo()

    def redo_event(self, event):
       self.redo()

def main():
    window = tk.Tk()
    window.title("Text Editor")
    text_editor = TextEditor(window)
    window.mainloop()

if __name__ == "__main__":
    main()
