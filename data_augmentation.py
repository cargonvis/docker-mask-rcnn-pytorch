import os
import cv2
import numpy as np

# Get the current directory
current_dir = os.getcwd()

# Ask the user to input the images folder name
images_folder_name = input("Enter the name of the images folder: ")

# Construct the source directory path
source_dir = os.path.join(current_dir, images_folder_name)

# Function to apply data augmentation techniques and save the augmented images
def apply_data_augmentation(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Apply data augmentation techniques
    # Example techniques: flip, rotate, brightness adjustment, and blur
    augmented_images = [
        np.flip(image, axis=0),                # Flip vertically
        np.flip(image, axis=1),                # Flip horizontally
        cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE),    # Rotate 90 degrees clockwise
        cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE),    # Rotate 90 degrees counterclockwise
        cv2.addWeighted(image, 1.5, np.zeros(image.shape, dtype=np.uint8), 0, 0),   # Increase brightness by 1.5 times
        cv2.addWeighted(image, 0.5, np.zeros(image.shape, dtype=np.uint8), 0, 0),   # Decrease brightness by 0.5 times
        cv2.GaussianBlur(image, (15, 15), 0),     # Apply Gaussian blur with increased kernel size
    ]
    
    # Data augmentation technique names
    technique_names = [
        "flip_vertical",
        "flip_horizontal",
        "rotate_clockwise",
        "rotate_counterclockwise",
        "increase_brightness",
        "decrease_brightness",
        "gaussian_blur",
    ]
    
    # Save the augmented images
    for i, augmented_image in enumerate(augmented_images):
        filename, ext = os.path.splitext(image_path)
        technique_name = technique_names[i]
        save_path = f"{filename}_{technique_name}{ext}"
        cv2.imwrite(save_path, augmented_image)
        print(f"Saved {save_path}")
    
# Iterate over the images in the source directory
for filename in os.listdir(source_dir):
    if filename.endswith(".jpg"):
        image_path = os.path.join(source_dir, filename)
        apply_data_augmentation(image_path)