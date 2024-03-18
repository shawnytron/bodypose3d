import cv2
import os
import sys

def record_video(participant_number):
    # Create directories if they don't exist
    if not os.path.exists("media"):
        os.makedirs("media")

    cam0_folder = f"media/cam0_participant_p{participant_number}"
    cam1_folder = f"media/cam1_participant_p{participant_number}"

    if not os.path.exists(cam0_folder):
        os.makedirs(cam0_folder)
    if not os.path.exists(cam1_folder):
        os.makedirs(cam1_folder)

    # Open cameras
    cam0 = cv2.VideoCapture(6)
    cam1 = cv2.VideoCapture(12)

    # Check if cameras are opened successfully
    if not (cam0.isOpened() and cam1.isOpened()):
        print("Error: Couldn't open cameras.")
        return

    # Define video codecs and output video writers
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out0 = cv2.VideoWriter(f"{cam0_folder}/video_cam0.mp4", fourcc, 30.0, (1280, 720))
    out1 = cv2.VideoWriter(f"{cam1_folder}/video_cam1.mp4", fourcc, 30.0, (1280, 720))

    while True:
        # Capture frame from cameras
        ret0, frame0 = cam0.read()
        ret1, frame1 = cam1.read()

        if not (ret0 and ret1):
            print("Error: Couldn't capture frame.")
            break

        # Display frames from cameras
        cv2.imshow('Camera 0', frame0)
        cv2.imshow('Camera 1', frame1)

        # Write frames to video files
        out0.write(frame0)
        out1.write(frame1)

        # Check for the 'Esc' key to stop recording
        if cv2.waitKey(1) == 27:
            break

    # Release resources
    cam0.release()
    cam1.release()
    out0.release()
    out1.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 record.py <participant_number>")
        sys.exit(1)
    
    participant_number = sys.argv[1]
    record_video(participant_number)
