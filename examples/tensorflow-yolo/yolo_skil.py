from skil import Model, Deployment
from skil.utils.yolo import annotate_image
import cv2

model = Model('yolo_v2.pb', name='yolo-tf', model_id='yolo-3493723')

deployment = Deployment(skil_server, 'yolo')
service = model.deploy(deployment, input_names=['input'], output_names=['output'], scale=2)

cap = cv2.VideoCapture(0)
while(True):
    _, image = cap.read()
    detection = service.detect_objects(image)
    image = annotate_image(image, detection)
    cv2.imshow('video', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break