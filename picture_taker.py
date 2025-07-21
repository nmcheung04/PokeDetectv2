import cv2
import os
import re

SAVE_DIR = 'card_pictures'

def create_save_directory(folder):
    '''
    Creates save directory for images
    '''
    os.makedirs(folder, exist_ok=True)

def get_next_image_number(folder):
    '''
    Obtain next image number based on last image number in folder
    '''
    image_files = os.listdir(folder)
    numbers = []
    pattern = re.compile(r'^card_(\d+)\.png$')
    for filename in image_files:
        match = pattern.match(filename)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers) + 1 if numbers else 0

def initialize_camera():
    '''
    Camera startup
    '''
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Error: Cannot open webcam")
    return cap

def capture_images(cap, folder, start_counter):
    '''
    Capture and save image in specified directory
    '''
    img_counter = start_counter
    print("Press 's' to save an image, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame")
            break

        cv2.imshow("Webcam - Press 's' to save", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            img_name = f"card_{img_counter}.png"
            img_path = os.path.join(folder, img_name)
            cv2.imwrite(img_path, frame)
            print(f"Saved {img_path}")
            img_counter += 1

        elif key == ord('q'):
            print("Quitting.")
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    create_save_directory(SAVE_DIR)
    start_counter = get_next_image_number(SAVE_DIR)
    cap = initialize_camera()
    capture_images(cap, SAVE_DIR, start_counter)

if __name__ == "__main__":
    main()
