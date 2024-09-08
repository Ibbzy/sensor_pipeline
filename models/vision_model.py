from google.cloud import vision
import io


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

