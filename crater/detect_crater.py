from pycda import CDA,load_image
from pycda.sample_data import get_sample_image
image = load_image('a2.jpeg')
#image.show()
cda = CDA()
detections = cda.predict(image)
detections.head(4)
detections.to_csv('latlon.csv', index=False)
prediction = cda.get_prediction(image)
prediction.set_scale(12.5)
prediction.show()

