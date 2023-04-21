import picamera
from time import sleep
import numpy as np
from tflite_runtime.interpreter import Interpreter
from PIL import Image

interpreter = Interpreter(model_path='mobilenet_v1_1.0_224_quant.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# camera = picamera.PiCamera()
# camera.start_preview()
# sleep(5)
# camera.capture("image.jpg")
# camera.stop_preview()

for i in range(0, 34):
    image = Image.open('img{}.jpg'.format(i))
    image = image.resize((224, 224))
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    image = image.astype(np.uint8)

    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    output = np.squeeze(output)
    predicted_class_index = np.argmax(output)
    confidence = output[predicted_class_index]

    with open('labels.txt', 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    predicted_class = labels[predicted_class_index]
    print("For image name: img{}".format(i))
    print('Predicted Class:', predicted_class)
    print('Confidence:', confidence)
