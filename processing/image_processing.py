import cv2
import os
from models.vision_model import VisionModel

DETECT_LABELS = os.getenv("UPLOAD_FILES_TO_GCS", "False").lower() == "true"
BLUR_ALL_IMAGES = os.getenv("BLUR_ALL_IMAGES", "True").lower() == "true"
TARGET_LABELS = os.getenv("TARGET_LABELS", "Face,Beard,Human").split(",")

class ImageProcessingPipeline:
    def __init__(self):
        self.model = VisionModel()

    def blur_image(self, image_path):

        image = cv2.imread(image_path)
        image = cv2.GaussianBlur(image, (99, 99), 30)
        cv2.imwrite(image_path, image)


    def process(self, image_path):
        labels = self.model.detect_labels(image_path) if DETECT_LABELS else []
        if BLUR_ALL_IMAGES or any(label.description in TARGET_LABELS for label in labels):
            self.blur_image(image_path)
        
        return image_path, labels
