import numpy as np
import cv2
from kivy.lang import Builder
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from GUI.pose_estimation import pose_estimation
from kivymd.uix.button import MDRaisedButton
import pandas as pd
from datetime import datetime

class GUI(MDApp):
    def build(self):
        self.title = "Aplikasi Deteksi Olahraga"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('GUI/tampilan.kv')

    def on_start(self):
        Clock.schedule_once(self.change_to_main, 3)

    def change_to_main(self, dt):
        self.root.current = 'main'
    
    def button_pressed(self, button_text, screen_name):
        print(f"Button {button_text} pressed, changing screen to {screen_name}")
        self.root.current = screen_name
        self.root.ids.pose_estimation_layout.update_button_text(button_text)

class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.is_paused = False
        self.countfrom = 0
        self.iscount = False
        self.image_widget = Image()
        self.add_widget(self.image_widget)
        self.pose_estimator = pose_estimation()  # Gunakan instance PoseEstimation yang sudah dibuat
        self.button_text = None
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None))


        # Tambahkan tombol pause
        self.pause_button = MDRaisedButton(
            text='Pause',
            size_hint=(0.1, None),
            md_bg_color=(0.2, 0.4, 0.6, 1),
            radius=[20, 20, 20, 20]
        )
        self.pause_button.bind(on_release=self.toggle_pause)
        button_layout.add_widget(self.pause_button)

        # Tambahkan tombol untuk menampilkan/menyembunyikan counter
        self.toggle_counter_button = MDRaisedButton(
            text='Start',
            size_hint=(0.1, None),
            md_bg_color=(0.2, 0.4, 0.6, 1),
            radius=[20, 20, 20, 20]
        )
        self.toggle_counter_button.bind(on_release=self.toggle_counter)
        button_layout.add_widget(self.toggle_counter_button)

        # Tambahkan button_layout ke MyBoxLayout
        self.add_widget(button_layout)


    def toggle_pause(self, instance):
        self.is_paused = not self.is_paused
        self.pause_button.text = 'Resume' if self.is_paused else 'Pause'

    def update_button_text(self, button_text):
        self.button_text = button_text
        self.arr = pd.DataFrame()

    def toggle_counter(self, instance):
        self.iscount = not self.iscount
        if(self.countfrom is not 0 and self.iscount == False):
            newrow = pd.DataFrame([{self.button_text:self.countfrom}])
            self.arr = pd.concat([self.arr,newrow], ignore_index=False)
            self.arr.to_csv(str(datetime.now().strftime("%Y-%m-%d"))+'.csv',index = False)
        self.countfrom = 0
        self.toggle_counter_button.text = 'Start' if not self.iscount else 'Stop'


    def update_frame(self, dt):
        if not self.is_paused:
            frame,self.countfrom = self.pose_estimator.detect_face_and_predict(self.button_text,self.countfrom,self.iscount)
            frame = cv2.flip(frame, 0)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(frame_rgb.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            self.image_widget.texture = texture
        else:
            self.image_widget.text = "Video is paused"
        

    def on_stop(self):
        self.pose_estimator.release()
    
