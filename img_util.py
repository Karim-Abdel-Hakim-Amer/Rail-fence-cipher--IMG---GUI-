import cv2

def load_image(path):
    img = cv2.imread(path)
    if img is None:
        raise ValueError("Failed to load image")
    return img

def save_image(path, img):
    if img is None:
        raise ValueError("No image to save")
    cv2.imwrite(path, img)
