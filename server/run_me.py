from Detector import *

modelUrl="http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_320x320_coco17_tpu-8.tar.gz"

# http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_320x320_coco17_tpu-8.tar.gz

classFile= "coco.names.txt"
detector = Detector()
imagePath = "test/10.jpg"
videoPath = 0

detector.readClasses(classFile)
detector.downloadModel(modelUrl)
detector.loadModel()
# detector.predictImage(imagePath)
detector.predictVideo(videoPath)

