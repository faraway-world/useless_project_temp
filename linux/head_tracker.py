import os
import threading
import time
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HeadTracker(threading.Thread):
    def __init__(self, volume_callback, model_path="face_landmarker.task"):
        super().__init__(daemon=True)
        self.volume_callback = volume_callback
        self.model_path = model_path
        self.running = True

    def run(self):
        if not os.path.exists(self.model_path):
            print(f"Error: {self.model_path} not found. Head tracking disabled.")
            return

        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_faces=1
        )

        cap = cv2.VideoCapture(0)
        
        with vision.FaceLandmarker.create_from_options(options) as landmarker:
            while self.running and cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    time.sleep(0.01)
                    continue

                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
                
                timestamp = int(time.perf_counter() * 1000)
                result = landmarker.detect_for_video(mp_image, timestamp)

                if result.face_landmarks:
                    landmarks = result.face_landmarks[0]
                    nose_x = landmarks[1].x
                    left_x = landmarks[234].x
                    right_x = landmarks[454].x

                    total_width = right_x - left_x
                    if total_width > 0:
                        yaw = (nose_x - left_x) / total_width
                        
                        if yaw > 0.60:
                            self.volume_callback(0.02)
                        elif yaw < 0.40:
                            self.volume_callback(-0.02)

                time.sleep(0.05)

        cap.release()

    def stop(self):
        self.running = False