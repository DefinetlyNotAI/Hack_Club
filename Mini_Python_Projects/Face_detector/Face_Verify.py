import os
import tempfile
import cv2
import face_recognition
import numpy as np  # Import numpy for array operations
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


def capture_and_save_temp_face():
    """
    Captures and saves a temporary face image from the default video capture device.

    Parameters:
    None

    Returns:
    str: The path to the temporary face image file, or None if image capture fails.
    """
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    colorlog.debug("Video capture initialized.")
    ret, frame = cap.read()
    colorlog.debug(f"Frame captured: {ret}")
    if ret:
        # Save the captured image to a temporary file
        _, temp_file_path = tempfile.mkstemp(suffix=".jpg")
        colorlog.debug(f"Temporary file path: {temp_file_path}")
        cv2.imwrite(temp_file_path, frame)

        colorlog.debug("Image saved to temporary file.")
        return temp_file_path
    else:
        colorlog.error("Failed to capture image.")
        return None


# Function to compare the captured face with known faces
def compare_faces_with_temp(captured_image_path, known_faces_dir):
    """
    Function to compare the captured face with known faces

    Parameters:
    captured_image_path (str): The file path of the captured image
    known_faces_dir (str): The directory containing the known faces

    Returns:
    True if the captured face is found in the known faces, False otherwise
    None if an error occurs
    """
    colorlog.debug("Loading captured image...")
    try:
        captured_image = face_recognition.load_image_file(captured_image_path)
        captured_face_encoding = face_recognition.face_encodings(captured_image)[0]

        captured_face_encoding_np = np.array(captured_face_encoding)
        known_face_encodings = []
        known_face_names = []
    except IndexError:
        colorlog.warning("No faces found in captured image.")
        return None
    except Exception as e:
        colorlog.error(f"Error loading captured image: {e}")
        return None
    colorlog.info("Loading known faces...")
    try:
        for filename in os.listdir(known_faces_dir):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                known_image_path = os.path.join(known_faces_dir, filename)
                known_image = face_recognition.load_image_file(known_image_path)
                known_face_encoding = face_recognition.face_encodings(known_image)[0]
                known_face_encodings.append(np.array(known_face_encoding))
                known_face_names.append(filename)
    except Exception as e:
        colorlog.error(f"Error loading known faces: {e}")
        return None

    colorlog.debug("Comparing faces...")
    try:
        threshold = 0.3  # Adjust this value based on testing
        matches = face_recognition.compare_faces(
            known_face_encodings, captured_face_encoding_np, tolerance=threshold
        )
        if True in matches:
            colorlog.debug("Calculating facial distances...")
            face_distances = face_recognition.face_distance(
                known_face_encodings, captured_face_encoding_np
            )

            # Find the index of the best match
            min_index = np.argmin(face_distances)

            # Calculate and report individual similarity scores for each known face
            for i in range(len(known_face_names)):
                # Calculate the similarity score for the current known face
                current_similarity_score = 1 / (
                    face_distances[i] + 1
                )  # Inverting the distance to get a similarity score

                colorlog.debug(
                    f"{known_face_names[i]} has a similarity score of {current_similarity_score * 100:.2f}%"
                )

            # Report the best match with its similarity score
            colorlog.info(
                f"The best match ({known_face_names[min_index]}) has a similarity score of {current_similarity_score * 100:.2f}%"
            )
            return True
        else:
            colorlog.warning("No match found.")
            return False
    except Exception as e:
        colorlog.error(f"Error comparing faces: {e}")
        return None


if __name__ == "__main__":
    if not os.path.exists("known_faces"):
        os.makedirs("known_faces")
    colorlog.info("Starting face verification...")
    temp_captured_image_path = capture_and_save_temp_face()
    if temp_captured_image_path is not None:
        compare_faces_with_temp(temp_captured_image_path, "known_faces")
