import cv2
import mediapipe as mp
from calculate import eye_aspect_ratio
import time
from PIL import Image
import base64
from io import BytesIO
from collections import deque

def blink(blink_queue, frame_callback):
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    cam = cv2.VideoCapture(0)
    w = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # left_ear_buffer = deque(maxlen=3)
    # right_ear_buffer = deque(maxlen=3)

    last_blink_time = 0
    # last_left_time = 0
    # last_right_time = 0
    COOLDOWN = 1.2  # seconds

    last_action = ""

    while True:
        ret, frame = cam.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_eye = [(int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)) for i in LEFT_EYE]
                right_eye = [(int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)) for i in RIGHT_EYE]

                avg_left_ear = eye_aspect_ratio(left_eye)
                avg_right_ear = eye_aspect_ratio(right_eye)

               

                now = time.time()

                # Blink detection with priority
                if avg_left_ear < 0.21 and avg_right_ear < 0.21:
                    if now - last_blink_time > COOLDOWN:
                        print("Blink")
                        blink_queue.put("BLINK")
                        last_blink_time = now
                        last_action = "Both Blink"

                elif avg_left_ear < 0.23 and avg_right_ear > 0.23:
                    if now - last_blink_time > COOLDOWN:
                        print("Left Blink")
                        blink_queue.put("LEFT")
                        last_blink_time = now
                        last_action = "Left Eye Blink"

                elif avg_right_ear < 0.24 and avg_left_ear > 0.25:
                    if now - last_blink_time > COOLDOWN:
                        print("Right Blink")
                        blink_queue.put("RIGHT")
                        last_blink_time = now
                        last_action = "Right Eye Blink"

                # Draw eye landmarks
                for (x, y) in left_eye + right_eye:
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)


                # Draw EAR values
                cv2.putText(frame, f"L: {avg_left_ear:.2f} R: {avg_right_ear:.2f}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.putText(frame, f"Detected: {last_action}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

                # Optional: zoom into eyes
                eye_x = [pt[0] for pt in left_eye + right_eye]
                eye_y = [pt[1] for pt in left_eye + right_eye]
                x1, x2 = max(min(eye_x) - 40, 0), min(max(eye_x) + 40, w)
                y1, y2 = max(min(eye_y) - 40, 0), min(max(eye_y) + 40, h)
                frame = frame[y1:y2, x1:x2]

        # Resize and send frame
        frame_resized = cv2.resize(frame, (400, 300))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        frame_callback(img_str)

        time.sleep(0.05)

    cam.release()
    cv2.destroyAllWindows()
