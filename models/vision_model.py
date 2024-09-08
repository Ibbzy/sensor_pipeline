from google.cloud import vision
import io
import cv2

class VisionModel:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def detect_labels(self, image_path):
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = self.client.label_detection(image=image)
        label_annotations = response.label_annotations
        labels = [label.description for label in label_annotations]

        return labels

    
    def blur_labels(self, image_path, labels, target_labels):
    
        # Apply blurring based on labels (example: faces)
        if '*' in target_labels or any(label.description in target_labels for label in labels):
            
            # read and apply a Gaussian blur to the image and save it
            image = cv2.imread(image_path)
            image = cv2.GaussianBlur(image, (99, 99), 30)
            cv2.imwrite(image_path, image)

        return None