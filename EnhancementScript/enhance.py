import os
import cv2
import fingerprint_enhancer


def enhance_all_images_in_directory(directory):
    """
    Enhances all images in the given directory and its subdirectories.
    """
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            img_path = os.path.join(subdir, file)
            try:
                img = cv2.imread(img_path, 0)
                enhanced_img = fingerprint_enhancer.enhance_Fingerprint(img)

                # Display the enhanced image
                cv2.imshow('Enhanced Image', enhanced_img)
                # Wait for a key press to move to the next image
                cv2.waitKey(0)

                # Optionally, save the enhanced image
                enhanced_img_path = os.path.join(subdir, f'enhanced_{file}')
                cv2.imwrite(enhanced_img_path, enhanced_img)

            except Exception as e:
                print(f"Error processing {img_path}: {e}")


if __name__ == "__main__":
    directory_path = 'path/to/your/directory'  # Update this path to your directory
    enhance_all_images_in_directory(directory_path)
