import cv2
from imutils import face_utils

cam = cv2.VideoCapture(0)

# Get the default frame width and height
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object

while True:
    ret, frame = cam.read()
    # Display the captured frame
    cv2.imshow('Camera', frame)
    (L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']
    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows