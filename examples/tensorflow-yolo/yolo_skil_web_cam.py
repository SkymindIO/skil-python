import skil
import cv2

skil_server = skil.Skil()
model = skil.Model('yolo_v2.pb', name='yolo-tf', model_id='yolo-3493723')
deployment = skil.Deployment(skil_server, 'yolo')
service = model.deploy(deployment, input_names=['input'], output_names=['output'], scale=2)

cap = cv2.VideoCapture(0)
while True:
   _, image = cap.read()
   detection = service.detect_objects(image)
   image = skil.utils.yolo.annotate_image(image, detection)
   cv2.imshow('yolo', image)
