import tkinter as tk
from tkinter import scrolledtext

class ChatPanel:
    def __init__(self, on_send_callback):
        self.on_send_callback = on_send_callback
        self.root = tk.Tk()
        self.root.title("Jarvis Chat Panel")
        self.root.geometry("520x440")
        self.root.minsize(400, 300)

        self.status_var = tk.StringVar(value="Idle")
        self.status_label = tk.Label(self.root, textvariable=self.status_var, anchor='w', fg='blue', font=("Segoe UI", 9, "italic"))
        self.status_label.pack(fill=tk.X, padx=10, pady=(8,0))

        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', font=("Segoe UI", 11), bg="#f8f8f8", fg="#222")
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        entry_frame = tk.Frame(self.root)
        entry_frame.pack(fill=tk.X, padx=10, pady=(0,10))

        self.entry = tk.Entry(entry_frame, font=("Segoe UI", 11), bg="white", fg="#222", insertbackground="#222")
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind('<Return>', self.send_message)
        self.entry.focus_set()

        self.send_button = tk.Button(entry_frame, text="Send", command=self.send_message, font=("Segoe UI", 10))
        self.send_button.pack(side=tk.LEFT, padx=(5,0))

        self.clear_button = tk.Button(self.root, text="Clear Chat", command=self.clear_chat, font=("Segoe UI", 9))
        self.clear_button.pack(pady=(0,10), anchor='e', padx=10)

    def send_message(self, event=None):
        user_message = self.entry.get().strip()
        if user_message:
            self.display_message("You", user_message)
            self.entry.delete(0, tk.END)
            self.entry.focus_set()
            try:
                self.on_send_callback(user_message)
            except Exception as e:
                self.display_message("System", f"Error sending message: {e}")

    def display_message(self, sender, message):
        self.chat_area.config(state='normal')
        if sender == "You":
            self.chat_area.insert(tk.END, f"You: {message}\n", "user")
        elif sender == "Jarvis":
            self.chat_area.insert(tk.END, f"Jarvis: {message}\n", "jarvis")
        else:
            self.chat_area.insert(tk.END, f"{sender}: {message}\n", "system")
        self.chat_area.tag_config("user", foreground="#007acc", font=("Segoe UI", 11, "bold"))
        self.chat_area.tag_config("jarvis", foreground="#008000", font=("Segoe UI", 11, "bold"))
        self.chat_area.tag_config("system", foreground="#b00", font=("Segoe UI", 10, "italic"))
        self.chat_area.see(tk.END)
        self.chat_area.config(state='disabled')

    def clear_chat(self):
        self.chat_area.config(state='normal')
        self.chat_area.delete(1.0, tk.END)
        self.chat_area.config(state='disabled')

    def set_status(self, status):
        self.status_var.set(status)

    def run(self):
        self.entry.focus_set()
        self.root.mainloop()
