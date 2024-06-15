import tkinter as tk
from tkinter import messagebox
import psutil
import os
import pwd

def get_current_user():
    return pwd.getpwuid(os.geteuid()).pw_name

def get_process_importance(proc_info, current_user):
    try:
        if proc_info['username'] == 'root':
            return 'high'
        elif proc_info['username'] == current_user:
            return 'medium'
        else:
            return 'low'
    except KeyError:
        return 'low'

class ProcessMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Process Monitor")
        self.geometry("600x500")
        self.current_user = get_current_user()
        
        self.search_var = tk.StringVar()
        self.search_bar = tk.Entry(self, textvariable=self.search_var)
        self.search_bar.pack(pady=5)
        self.search_bar.bind('<Return>', self.search_processes)
        
        self.refresh_button = tk.Button(self, text="Refresh", command=self.refresh_processes)
        self.refresh_button.pack(pady=5)
        
        self.canvas = tk.Canvas(self)
        self.scroll_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.frame = tk.Frame(self.canvas)
        
        self.scroll_frame = self.canvas.create_window((0, 0), window=self.frame, anchor='nw')
        
        self.frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.frame_width)
        
        self.canvas.config(yscrollcommand=self.scroll_y.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")
        
        self.category_frames = {
            'high': None,
            'medium': None,
            'low': None
        }
        self.refresh_processes()

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def frame_width(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.scroll_frame, width = canvas_width)

    def refresh_processes(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        categories = {'high': [], 'medium': [], 'low': []}
        
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                proc_info = proc.info
                importance = get_process_importance(proc_info, self.current_user)
                categories[importance].append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        self.create_category("High Importance", "red", categories['high'])
        self.create_category("Medium Importance", "yellow", categories['medium'])
        self.create_category("Low Importance", "green", categories['low'])

    def create_category(self, name, color, processes):
        if not processes:
            return

        button = tk.Button(self.frame, text=name, bg=color, command=lambda: self.toggle_category(name))
        button.pack(fill=tk.X, padx=5, pady=2)
        
        frame = tk.Frame(self.frame)
        frame.pack(fill=tk.X)
        
        self.category_frames[name] = frame

        for proc_info in processes:
            self.add_process(proc_info, frame, color)
        
        frame.pack_forget()

    def toggle_category(self, name):
        frame = self.category_frames[name]
        if frame.winfo_ismapped():
            frame.pack_forget()
        else:
            frame.pack(fill=tk.X)

    def add_process(self, proc_info, parent_frame, color):
        proc_frame = tk.Frame(parent_frame, bg=color)
        proc_frame.pack(fill=tk.X, padx=5, pady=2)

        proc_label = tk.Label(proc_frame, text=f"{proc_info['name']} (PID: {proc_info['pid']})", bg=color)
        proc_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        kill_button = tk.Button(proc_frame, text="Kill", command=lambda pid=proc_info['pid']: self.kill_process(pid))
        kill_button.pack(side=tk.RIGHT)

    def kill_process(self, pid):
        try:
            p = psutil.Process(pid)
            p.terminate()
            p.wait(timeout=3)
            messagebox.showinfo("Success", f"Process {pid} terminated successfully.")
            self.refresh_processes()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as e:
            messagebox.showerror("Error", f"Failed to terminate process {pid}: {str(e)}")

    def search_processes(self, event=None):
        search_term = self.search_var.get().lower()
        if not search_term:
            self.refresh_processes()
            return
        
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        matching_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                proc_info = proc.info
                if search_term in proc_info['name'].lower():
                    matching_processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        self.create_category("Search Results", "blue", matching_processes)

if __name__ == "__main__":
    app = ProcessMonitor()
    app.mainloop()
