import skil
import cv2

model = skil.Model('yolo.pb', model_id='yolo_42', name='yolo')
service = model.deploy(skil.Deployment(), input_names=['input'], output_names=['output'])

image = cv2.imread("say_yolo_again.jpg")
detection = service.detect_objects(image)
image = skil.utils.yolo.annotate_image(image, detection)
cv2.imwrite('annotated.jpg', image)
