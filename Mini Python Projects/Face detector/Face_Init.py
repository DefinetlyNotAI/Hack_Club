import os
import cv2
import dlib
from imutils import face_utils
import colorlog

# Configure colorlog for logging messages with colors
logger = colorlog.getLogger()
# Change to INFO if needed
logger.setLevel(colorlog.DEBUG)

handler = colorlog.StreamHandler()
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red",
    },
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Load the detector and predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("sp68fl.dat")


def detect_and_draw_landmarks(image, loop):
    colorlog.debug(f"Starting loop {loop}...")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    colorlog.debug("Converted image to grayscale")
    rects = detector(gray, 1)
    colorlog.debug(f"Detected {len(rects)} faces")

    try:
        for (i, rect) in enumerate(rects):
            colorlog.debug(f"Processing face {i + 1}")
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            colorlog.debug("Extracted facial landmarks")

            # Calculate the size of the face region as a proxy for certainty
            face_size = max(rect.width(), rect.height())
            colorlog.debug(f"Face size: {face_size}")

            # Arbitrary threshold for high certainty
            if face_size > 300:
                # Green for high certainty
                color = (0, 255, 0)
                colorlog.debug("High certainty with plotting")
            # Arbitrary threshold for medium certainty
            elif 180 < face_size <= 300:
                # Yellow for medium certainty
                color = (0, 255, 255)
                colorlog.debug("Medium certainty with plotting")
            else:
                # Red for low certainty
                color = (0, 0, 255)
                colorlog.debug("Low certainty with plotting")

            # Extract facial landmarks
            colorlog.debug("Extracting facial landmarks")
            left_eye = shape[36:42]
            right_eye = shape[42:48]
            nose = shape[30:36]
            mouth = shape[48:68]

            # Draw dots on facial landmarks for display
            colorlog.debug("Plotting dots onto facial landmarks")
            for point in left_eye:
                cv2.circle(image, tuple(point), 2, color, -1)
            for point in right_eye:
                cv2.circle(image, tuple(point), 2, color, -1)
            for point in nose:
                cv2.circle(image, tuple(point), 2, color, -1)
            for point in mouth:
                cv2.circle(image, tuple(point), 2, color, -1)
    except Exception as e:
        colorlog.error(f"Error processing face: {e}")

    colorlog.debug(f"Finished detection and plotting - LOOP {loop}")
    return image.copy()


def capture():
    loop = 0
    colorlog.info("Starting video capture...")
    try:
        while True:
            loop += 1
            ret, frame = cap.read()
            if not ret:
                colorlog.error("Can't receive frame (stream end?). Exiting ...")
                break

            # Create a copy of the frame for displaying with dots
            display_frame = detect_and_draw_landmarks(frame.copy(), loop)

            # Display the frame with dots
            cv2.imshow('Face Detection', display_frame)

            key = cv2.waitKey(1) & 0xFF
            colorlog.info("Press 'c' to save the image.")
            if key == ord('c'):  # Press 'c' to continue/save the image
                files = os.listdir('known_faces')
                number = sum([1 for f in files if os.path.isfile(os.path.join('known_faces', f))])
                # Save the original frame without modifications
                cv2.imwrite(f'known_faces/face_{number}.jpg', frame)
                colorlog.info("Image saved.")

                break

        # Add debug print statements for easy debugging
        colorlog.info("Video capture completed.")
        colorlog.debug(f"Loop number: {loop}")
        colorlog.debug(f"Key pressed: {chr(key)}")
    except Exception as e:
        colorlog.error(f"An error occurred: {e}")


# Initialize the camera
try:
    if not os.path.exists('known_faces'):
        os.makedirs('known_faces')
    cap = cv2.VideoCapture(0)
    capture()
    cap.release()
    cv2.destroyAllWindows()
    colorlog.info("Program completed.")
except Exception as e:
    colorlog.error(f"An error occurred: {e}")
