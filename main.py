from GUI.GUI import SportsDetectionApp
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    app = SportsDetectionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
