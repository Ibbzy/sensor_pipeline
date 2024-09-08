from google.cloud import vision
import cv2
import io
import os

DETECT_LABELS = os.getenv("UPLOAD_FILES_TO_GCS", "False").lower() == "true"
BLUR_ALL_IMAGES = os.getenv("BLUR_ALL_IMAGES", "True").lower() == "true"

def detect_labels(image_path):
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    label_annotations = response.label_annotations
    labels = [label.description for label in label_annotations]

    return labels

def blur_labels(image_path, labels, target_labels):
    
    # Apply blurring based on labels (example: faces)
    if '*' in target_labels or any(label.description in target_labels for label in labels):
        
        # read and apply a Gaussian blur to the image and save it
        image = cv2.imread(image_path)
        image = cv2.GaussianBlur(image, (99, 99), 30)
        cv2.imwrite(image_path, image)

    return None

def process_image(image_path, target_labels=None):
    labels = detect_labels(image_path) if DETECT_LABELS else []
    target_labels = ["*"] if BLUR_ALL_IMAGES else (target_labels or [])
    
    blur_labels(image_path, labels, target_labels)

    return image_path, labels