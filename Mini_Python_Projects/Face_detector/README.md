# Facial Landmark Detection and Face Verification System

This project consists of two main components:

1. **Facial Landmark Detection**: Utilizes OpenCV and DLib to detect faces in real-time video feed and draw facial landmarks such as eyes, nose, and mouth.
2. **Face Verification**: Captures a face image and compares it against a database of known faces to verify identity.

## Dependencies

- OpenCV
- DLib
- Face Recognition library
- ColorLog for colored terminal logs
- NumPy

## Getting Started

### Prerequisites

Ensure you have Python installed on your system. This project is tested on Python 3.7+.
Ensure you have the required [dependencies](/requirements.txt) installed.

### Installation

Clone this repository to your local machine.

```bash
git clone https://github.com/DefinetlyNotAI/Hack_Club
cd 'Hack_Club\Mini Python Projects\Face detector\'
```

Create a virtual environment (optional but recommended):
```bash
python -m venv venv
```
```bash
venv\Scripts\activate  # On Windows
```
```bash
source venv/bin/activate  # On Unix or MacOS
```

Finally, install the required packages:
```bash
pip install opencv-python-headless dlib face_recognition colorlog numpy
```

### Usage

#### Facial Landmark Detection and Saving

Run the `Face_init.py` script to start the facial landmark detection process. 
Faces detected in the video stream will have their landmarks drawn in real-time.

```bash
python Face_init.py
```

To save an image of a detected face, press 'c'. The image will be saved in the `known_faces` directory.

#### Face Verification

Run the `Face_Verify.py` script to start the face verification process.
It will capture your face, and the system will attempt to match it 
against known faces stored in the `known_faces` directory.

```bash
python Face_Verify.py
```

### Contributing

Contributions are welcome! Please feel free to submit a pull request.

### License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.
