import numpy as np
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
from datetime import datetime
import threading
from GUI.pose_estimation import pose_estimation

class SportsDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Deteksi Olahraga")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.is_paused = False
        self.countfrom = 0
        self.iscount = False
        self.button_text = None
        self.arr = pd.DataFrame()
        self.pose_estimator = pose_estimation()
        self.running = True
        
        # Show splash screen
        self.show_splash()
        
    def show_splash(self):
        """Tampilan splash screen selama 3 detik"""
        splash_frame = tk.Frame(self.root, bg='#2196F3')
        splash_frame.pack(fill='both', expand=True)
        
        title = tk.Label(
            splash_frame, 
            text="Aplikasi Deteksi Olahraga", 
            font=('Arial', 32, 'bold'),
            bg='#2196F3',
            fg='white'
        )
        title.pack(expand=True)
        
        # Otomatis pindah ke menu utama setelah 3 detik
        self.root.after(3000, lambda: self.show_main_menu(splash_frame))
        
    def show_main_menu(self, previous_frame):
        """Menu utama untuk memilih jenis olahraga"""
        previous_frame.destroy()
        
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        title = tk.Label(
            main_frame, 
            text="Pilih Jenis Olahraga", 
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0'
        )
        title.pack(pady=30)
        
        # Contoh tombol olahraga - sesuaikan dengan kebutuhan
        sports = ['Push Up', 'Sit Up', 'Squat', 'Plank']
        
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(expand=True)
        
        for sport in sports:
            btn = tk.Button(
                button_frame,
                text=sport,
                font=('Arial', 16),
                bg='#2196F3',
                fg='white',
                activebackground='#1976D2',
                activeforeground='white',
                width=15,
                height=2,
                cursor='hand2',
                command=lambda s=sport, f=main_frame: self.start_detection(s, f)
            )
            btn.pack(pady=10)
    
    def start_detection(self, sport_name, previous_frame):
        """Mulai deteksi pose dengan webcam"""
        previous_frame.destroy()
        
        self.button_text = sport_name
        self.arr = pd.DataFrame()
        
        # Main detection frame
        detection_frame = tk.Frame(self.root, bg='#f0f0f0')
        detection_frame.pack(fill='both', expand=True)
        
        # Header
        header = tk.Label(
            detection_frame,
            text=f"Deteksi: {sport_name}",
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0'
        )
        header.pack(pady=10)
        
        # Video display
        self.video_label = tk.Label(detection_frame, bg='black')
        self.video_label.pack(pady=10)
        
        # Counter display
        self.counter_label = tk.Label(
            detection_frame,
            text=f"Counter: {self.countfrom}",
            font=('Arial', 18),
            bg='#f0f0f0'
        )
        self.counter_label.pack(pady=5)
        
        # Control buttons
        control_frame = tk.Frame(detection_frame, bg='#f0f0f0')
        control_frame.pack(pady=10)
        
        self.pause_button = tk.Button(
            control_frame,
            text='Pause',
            font=('Arial', 12),
            bg='#FF9800',
            fg='white',
            width=10,
            command=self.toggle_pause
        )
        self.pause_button.pack(side='left', padx=5)
        
        self.start_button = tk.Button(
            control_frame,
            text='Start',
            font=('Arial', 12),
            bg='#4CAF50',
            fg='white',
            width=10,
            command=self.toggle_counter
        )
        self.start_button.pack(side='left', padx=5)
        
        back_button = tk.Button(
            control_frame,
            text='Kembali',
            font=('Arial', 12),
            bg='#F44336',
            fg='white',
            width=10,
            command=lambda: self.go_back(detection_frame)
        )
        back_button.pack(side='left', padx=5)
        
        # Start video update loop
        self.update_video()
    
    def toggle_pause(self):
        """Toggle pause/resume video"""
        self.is_paused = not self.is_paused
        self.pause_button.config(text='Resume' if self.is_paused else 'Pause')
    
    def toggle_counter(self):
        """Toggle start/stop counter"""
        self.iscount = not self.iscount
        
        if self.countfrom != 0 and not self.iscount:
            # Simpan data ke CSV
            newrow = pd.DataFrame([{self.button_text: self.countfrom}])
            self.arr = pd.concat([self.arr, newrow], ignore_index=False)
            filename = f"{datetime.now().strftime('%Y-%m-%d')}.csv"
            self.arr.to_csv(filename, index=False)
            print(f"Data disimpan ke {filename}")
        
        self.countfrom = 0 if not self.iscount else self.countfrom
        self.start_button.config(text='Stop' if self.iscount else 'Start')
        
    def update_video(self):
        """Update video frame"""
        if not self.is_paused and self.running:
            frame, self.countfrom = self.pose_estimator.detect_face_and_predict(
                self.button_text, 
                self.countfrom, 
                self.iscount
            )
            
            # Convert frame untuk Tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))
            
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            
            # Update counter display
            self.counter_label.config(text=f"Counter: {self.countfrom}")
        
        # Schedule next update (30 FPS)
        if self.running:
            self.root.after(33, self.update_video)
    
    def go_back(self, current_frame):
        """Kembali ke menu utama"""
        current_frame.destroy()
        self.is_paused = False
        self.countfrom = 0
        self.iscount = False
        self.show_main_menu(tk.Frame(self.root))
        
    def on_closing(self):
        """Cleanup saat aplikasi ditutup"""
        self.running = False
        self.pose_estimator.release()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = SportsDetectionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
