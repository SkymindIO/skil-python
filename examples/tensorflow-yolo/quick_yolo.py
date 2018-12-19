import skil
import cv2

model = skil.Model('yolo_v2.pb')
service = model.deploy(skil.Deployment(), input_names=['input'], output_names=['output'])

image = cv2.imread("say_yolo_again.jpg", mode='RGB')
detection = service.detect_objects(image)
image = skil.utils.yolo.annotate_image(image, detection)
cv2.imshow('yolo', image)
