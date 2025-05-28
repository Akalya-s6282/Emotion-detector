import cv2
import mediapipe as mp
from calculate import eye_aspect_ratio
def blink():
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)


    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]
    cam = cv2.VideoCapture(0)
    # Get the default frame width and height
    w = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object

    while True:
        ret, frame = cam.read()
        # Display the captured frame
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_eye = [(int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)) for i in LEFT_EYE]
                right_eye = [(int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)) for i in RIGHT_EYE]

                left_ear = eye_aspect_ratio(left_eye)
                right_ear = eye_aspect_ratio(right_eye)
                ear = (left_ear + right_ear) / 2.0

                # Draw eye points
                for (x, y) in left_eye + right_eye:
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

                    # Blink detection
                if ear < 0.22:
                    cv2.putText(frame, "BLINK", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                    return (1)
                    
                else:
                    return(0)
        cv2.imshow('Camera', frame)
        # Press 'q' to exit the loop
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows