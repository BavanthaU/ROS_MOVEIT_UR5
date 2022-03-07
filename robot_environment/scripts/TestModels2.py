
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os
import cv2

# dimensions of our images
img_width, img_height = 100, 100

model = load_model('hand_gestures_500.h5')

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# predicting images
img = image.load_img("zero.png", target_size=(img_width, img_height))
#apply morphology
classes = model.predict(np.expand_dims(img, axis=0))
print(classes)

print("hand is showing " ,np.argmax(classes[0]))


