# SPDX-License-Identifier: GPL-2.0-or-later
#
# This file is part of a project licensed under the GNU General Public License, version 2 or later.
# You may redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 2 of the License or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import asyncio
import cv2
import face_recognition
import numpy as np
import os
import pickle
import random
import select
import sys
import threading
import time

from evdev import InputDevice, ecodes
from kasa import Discover
from screeninfo import get_monitors
from tkinter import simpledialog
from tkinter import messagebox

# TAPO Samrt Plug credentials
tapo_plug_1_ip = ''
tapo_user = ''
tapo_pass = ''

# Video device (/dev/videoX)
video_device = 0

# Capture device for touchscreen or mouse events
input_device_file = '/dev/input/event9'

# Path to store training images
dataset_path = 'dataset'

# Number of images to be captured for Raspberry Pi
capture_count = 20

# Number of images to be captured for PC
# capture_count = 50

# Initialize variables for storing known face encodings and their names
known_face_encodings = []
known_face_names = []
known_face_recog_count = {}
event_count = 5

# Exit program on touchscreen release
def event_exit():
    try:
        input_device = InputDevice(input_device_file)
        print(f"Touch the screen to kill program")

        for event in input_device.read_loop():
            if event.type == ecodes.EV_KEY and event.value == 0:
                print(f"Exiting IoT Santa...")
                os._exit(0)
    except Exception as e:
        print(f"Error on touchscreeni: {e}")

# Tapo plug
async def tapo_plug(state):
    dev = await Discover.discover_single(tapo_plug_1_ip, username=tapo_user, password=tapo_pass)
    time.sleep(0.125)
    if state == 'on':
        await dev.turn_on()
    else:
        await dev.turn_off()
    await dev.update()

# Actuate event
def actuate_event(name):
    # Initialize a blank window
    window_name = "Merry Christmas"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    monitors = get_monitors()
    for i, monitor in enumerate(monitors):
        width = monitor.width
        height = monitor.height
    
    # Full screen
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Load the background image
    background = cv2.imread('images/background.jpg')  # Replace with your background image path
    if background is None:
        print("Error: Background image not found!")
        exit()
    background = cv2.resize(background, (width, height))  # Resize to match screen dimensions

    # Colors
    background_color = (0, 0, 255)  # Black
    text_color = (0, 255, 0)      # Green

    # Parameters for the text
    text = "Merry Christmas " + name
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    thickness = 4

    # Initialize animation variables
    x_start = width - 1  # Start position (off-screen)
    y_position = 400  # Vertical position of the text
    frame_height, frame_width = height - 1, width - 1
    speed = 5  # Speed of the text animation
    count = 0

    # Animation variables
    x, y = width // 8, height // 4
    dx, dy = 3, 2  # Change in position
    font_scale_change = 0.01
    color_change_speed = 10

    # Load a random JPEG image
    image = cv2.imread('images/random_image.jpg')  # Replace with your JPEG image path
    if image is None:
        print("Error: Image not found!")
        exit()
    image = cv2.resize(image, (100, 100))  # Resize the image

    # Image appearance variables
    image_position = (random.randint(0, width - 100), random.randint(0, height - 100))
    image_timer = time.time()
    image_interval = 1  # Seconds between new image appearances

    # Generate random initial color
    def random_color():
        return tuple(random.randint(0, 255) for _ in range(3))

    font_color = random_color()

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Turn ON Tapo smart plug
    try:
        asyncio.run(tapo_plug('on'))
    except Exception as e:
        print(f"Unable to communicate with tapo smart plug: {e}");
        exit -1

    while True:
        # Create a blank frame
        frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
        frame[:, :] = background_color

        # Start with the background
        frame = background.copy()

        # Calculate text size and position
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_width = text_size[0]
        text_height = text_size[1]
        text_position = (x_start, y_position + text_height // 2)

        # Draw the text
        cv2.putText(frame, text, text_position, font, font_scale, text_color, thickness)

        # Update the text position
        x_start -= speed
        if x_start < -text_width:  # Reset if the text moves off-screen
            x_start = frame_width

        # Update position
        x += dx
        y += dy

        # Update font scale
        font_scale += font_scale_change
        if font_scale > 2 or font_scale < 0.5:
            font_scale_change = -font_scale_change

        # Update color
        font_color = tuple(
            (c + random.randint(-color_change_speed, color_change_speed)) % 256 for c in font_color
        )

        # Draw text
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = x - text_size[0] // 4
        text_y = y + text_size[1] // 4

        cv2.putText(frame, text, (text_x, text_y), font, font_scale, font_color, thickness)

        # Check boundaries and reverse direction if needed
        if text_x < 0 or text_x + text_size[0] > width:
            dx = -dx
        if text_y - text_size[1] < 0 or text_y > height:
            dy = -dy

        # Display random image at intervals
        if time.time() - image_timer > image_interval:
            image_position = (random.randint(0, width - 100), random.randint(0, height - 100))
            image_timer = time.time()

        # Overlay the image
        x_img, y_img = image_position
        h, w = image.shape[:2]
        frame[y_img:y_img + h, x_img:x_img + w] = image

        # Display the frame
        cv2.imshow(window_name, frame)

        # Exit on 'q' key
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        count += 1
        if count >= 220:
            break

    # Cleanup
    cv2.destroyWindow("Merry Christmas")

    # Turn OFF Tapo smart plug
    try:
        asyncio.run(tapo_plug('off'))
    except Exception as e:
        print(f"Unable to communicate with tapo smart plug: {e}");
        exit -1

# Function to capture and save face images for training
def capture_faces():

    global known_face_encodings, known_face_names

    # Create a directory to store training images if not exist
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    # Initialize the webcam video capture
    video_capture = cv2.VideoCapture(video_device)

    print("Starting face capture. Press 'q' to stop.")
    # face_id = input('Enter the ID for the new face: ')
    face_id = simpledialog.askstring("Registration", "Enter name")
    if face_id is None:
        print(f"No name entered. Exiting...");
        return -1

    count = 0

    while True:
        # Capture a single frame from the video feed
        ret, frame = video_capture.read()

        # Find all face locations and face encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Save the face encoding and label (ID) to the training set
            known_face_encodings.append(face_encoding)
            known_face_names.append(face_id)

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Label the face with the given face ID
            cv2.putText(frame, f'ID: {face_id}', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            # Save the captured face as an image file
            cv2.imwrite(f"{dataset_path}/{face_id}_{count}.jpg", frame[top:bottom, left:right])
            count += 1
        
        # Display the frame with rectangles drawn around faces
        cv2.imshow("Capturing Faces", frame)

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= capture_count:  # You can stop after capturing 50 images
            break

    video_capture.release()
    cv2.destroyAllWindows()

    print("Face capture complete.")

# Function to train faces
def train_faces():
    print("Training faces")
    global known_face_encodings, known_face_names

    # Loop through each image in the directory
    for filename in os.listdir(dataset_path):
        image_path = os.path.join(dataset_path, filename)

        # Check if it's a valid image file
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Load the image file and get face encodings
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            # If no face is found in the image, skip it
            if len(encodings) == 0:
                print(f"No faces found in {filename}, skipping.")
                continue

            # Assume the first face in the image is the one we want to recognize
            known_face_encodings.append(encodings[0])
            fname = os.path.splitext(filename)[0]
            label = fname.split('_')[0]
            known_face_names.append(label)

    # Save the encodings and names to a file using pickle
    with open('face_encodings.pkl', 'wb') as f:
        pickle.dump((known_face_encodings, known_face_names), f)

    print(f"Training completed. {len(known_face_encodings)} faces trained.")
    messagebox.showinfo("Information","Training complete")

# Function to recognize faces in real-time
def recognize_faces():
    print("Starting IoT Santa")

    global known_face_encodings, known_face_names, known_face_recog_count
    global event_count

    # Load the saved encodings and names from the pickle file
    with open('face_encodings.pkl', 'rb') as f:
        known_face_encodings, known_face_names = pickle.load(f)

    # Load the names for counting number of detections
    for name in known_face_names:
        known_face_recog_count[name] = 0

    window_name = 'Santa'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Initialize the webcam video capture
    video_capture = cv2.VideoCapture(video_device)
    
    while True:
        # Capture a single frame from the webcam
        ret, frame = video_capture.read()

        # Find all face locations and face encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Loop through each detected face
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compare the face encoding to the known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match is found, label the face
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                val = known_face_recog_count[name]
                if val >= event_count:
                    for key in known_face_recog_count:
                        known_face_recog_count[key] = 0
                    video_capture.release()
                    actuate_event(name)
                    # reinitialize the webcam video capture
                    video_capture = cv2.VideoCapture(video_device)
                else:
                    known_face_recog_count[name] = val + 1;
            else:
                for key in known_face_recog_count:
                    known_face_recog_count[key] = 0

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow(window_name, frame)

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

# Main menu for the program
def main():

    if len(sys.argv) < 2:
        print("Invalid choice. Please try again.")
        exit(-1)
        
    choice = sys.argv[1]


    if choice == 'capture':
        capture_faces()
    elif choice == 'train':
        train_faces()
    elif choice == 'recog':
        # Start the thread to monitor touchscreen events to kill the program
        exit_thread = threading.Thread(target=event_exit, daemon=True)
        exit_thread.start()
        recognize_faces()
    else:
        print("Invalid choice. Please try again.")
        exit(-1)

if __name__ == "__main__":
    main()

