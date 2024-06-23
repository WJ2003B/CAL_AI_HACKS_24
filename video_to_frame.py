import cv2
import os

def capture_photos(video_source=0, interval=2, output_folder='output', file_name='captured_frame.jpg'):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video source
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        raise ValueError("Error: Could not open video source.")

    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    if frame_rate == 0:  # Handle case when frame_rate is 0 (FPS cannot be determined)
        frame_rate = 30  # Default to 30 FPS

    print(f"Frame Rate: {frame_rate} FPS")

    # Calculate the interval in frames
    interval_frames = int(frame_rate * interval)

    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % interval_frames == 0:
            file_path = os.path.join(output_folder, file_name)
            cv2.imwrite(file_path, frame)
            print(f"Saved frame at {file_path}")

        frame_count += 1

        # Display the frame (Optional)
        cv2.imshow('Frame', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    # Specify the video source (0 for default webcam, or a file path for a video file)
    video_source = 0  # Use 0 for webcam or provide the file path for a video file

    # Specify the output folder and file name
    output_folder = './output'
    file_name = 'captured_frame.jpg'

    # Capture photos from the video source
    capture_photos(video_source=video_source, interval=2, output_folder=output_folder, file_name=file_name)
