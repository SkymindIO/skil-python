try:
    import cv2
except ImportError:
    cv2 = None


def annotate_image(image, detection):
    """ Annotate images with object detection results

    # Arguments:
        image: numpy array representing the image used for detection
        detection: `DetectionResult` result from SKIL on the same image

    # Return value:
        annotated image as numpy array
    """
    if cv2 is None:
        raise Exception("OpenCV is not installed.")
    objects = detection.get('objects')
    if objects:
        for detect in objects:
            confs = detect.get('confidences')
            max_conf = max(confs)
            max_index = confs.index(max_conf)
            classes = detect.get('predictedClasses')
            max_class = classes[max_index]
            h = detect.get('height')
            w = detect.get('width')
            center_x = detect.get('centerX')
            center_y = detect.get('centerY')
            lower = (int(center_x - w/2), int(center_y - h/2))
            upper = (int(center_x + w/2), int(center_y + h/2))
            im = cv2.rectangle(image, lower, upper, (255, 0, 0), 3)
            cv2.putText(image, max_class + " " + str(max_conf),
                        upper, cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
    return image
