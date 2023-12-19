import face_recognition
import cv2

# Load sample images and encode known faces
known_face_encodings = []
known_face_names = []

# Encode known faces
image1 = face_recognition.load_image_file("model/data/daniele_positive/2023-11-14 20:11:59.jpeg")
face_encoding1 = face_recognition.face_encodings(image1)[0]
known_face_encodings.append(face_encoding1)
known_face_names.append("Daniele")

image2 = face_recognition.load_image_file("model/data/klara_positive/2023-11-30 10:49:51.jpeg")
face_encoding2 = face_recognition.face_encodings(image2)[0]
known_face_encodings.append(face_encoding2)
known_face_names.append("Klara")

# Initialize variables
face_locations = []
face_encodings = []
face_names = []

# Open video capture
video_capture = cv2.VideoCapture(0)

while True:
    # Read video frame
    ret, frame = video_capture.read()

    # Resize frame for faster processing (optional)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (OpenCV default) to RGB color
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and their encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # Compare face encoding with known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # If a match is found, use the known face name
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        face_names.append(name)

    # Display results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since we scaled them down
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with the name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Face Recognition', frame)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
video_capture.release()
cv2.destroyAllWindows()