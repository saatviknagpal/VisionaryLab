import cv2, time, os, tensorflow as tf
import numpy as np

from tensorflow.python.keras.utils.data_utils import get_file


np.random.seed(123)

class Detector:
    def __init__(self):
        pass

    def readClasses(self, classesFilePath):
        with open(classesFilePath, 'r') as f:
            self.classList = f.read().splitlines()
        
        #Colors list
        self.colorList = np.random.uniform(0, 255, size=(len(self.classList), 3))

        print(len(self.colorList), len(self.classList))


    def downloadModel(self, modelUrl):
        fileName = os.path.basename(modelUrl)

        self.modelName=fileName[:fileName.index('.')]

        self.cacheDir = "./pretrained_models"

        os.makedirs(self.cacheDir, exist_ok=True)

        get_file(fname=fileName, origin=modelUrl, cache_dir=self.cacheDir, cache_subdir="checkpoints", extract=True)

        print("Model downloaded and extracted to:", self.cacheDir)

    def loadModel(self):
        print("Loading model...")
        tf.keras.backend.clear_session()
        self.model = tf.saved_model.load(os.path.join(self.cacheDir, "checkpoints", self.modelName, "saved_model"))
        print("Model loaded")

    def createBoundingBox(self, image):
        inputTensor = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
        inputTensor = tf.convert_to_tensor(inputTensor, dtype=tf.uint8)

        inputTensor = inputTensor[tf.newaxis, ...]

        detections = self.model(inputTensor)

        bboxs = detections['detection_boxes'][0].numpy()
        classIndexes = detections['detection_classes'][0].numpy().astype(np.int32)
        classScores = detections['detection_scores'][0].numpy()

        imH, imW, imC = image.shape

        bboxIdx = tf.image.non_max_suppression(bboxs, classScores, max_output_size=50, iou_threshold=0.5 ,score_threshold=0.5)

        if len(bboxIdx) != 0:
            for i in bboxIdx:
                bbox = tuple(bboxs[i].tolist())
                classConfidence = round(100*classScores[i])
                classIndex = classIndexes[i]

                classLabelText = self.classList[classIndex]
                classColor = self.colorList[classIndex]

                displayText = "{}: {}%".format(classLabelText, classConfidence)

                ymin, xmin, ymax, xmax = bbox
                xmin = int(xmin * imW)
                ymin = int(ymin * imH)
                xmax = int(xmax * imW)
                ymax = int(ymax * imH)

                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), classColor, 1)

                cv2.putText(image, displayText, (xmin, ymin-10), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)

                lineWidth = min(int((xmax-xmin) * 0.2), int((ymax-ymin) * 0.2))

                cv2.line(image, (xmin, ymin), (xmin + lineWidth, ymin), classColor, 5)
                cv2.line(image, (xmin, ymax), (xmin + lineWidth, ymax), classColor, 5)
                cv2.line(image, (xmax, ymin), (xmax - lineWidth, ymin), classColor, 5)
                cv2.line(image, (xmax, ymax), (xmax - lineWidth, ymax), classColor, 5)
                
        return image


                

    def predictImage(self, imagePath):
        image = cv2.imread(imagePath)

        bboxImage = self.createBoundingBox(image)
        
        cv2.imwrite(self.modelName + ".jpg", bboxImage)
        cv2.imshow("Result", bboxImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def predictVideo(self, videoPath, threshold = 0.5):
        cap = cv2.VideoCapture(videoPath)

        if(cap.isOpened() == False):
            print("Error opening video file")
            return
        
        (success, image) = cap.read()

        startTime = 0

        while(success):
            currentTime = time.time()
            fps = 1/(currentTime - startTime)

            startTime= currentTime

            bboxImage = self.createBoundingBox(image)

            cv2.putText(bboxImage, "FPS: " + str(int(fps)), (20,70), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)

            cv2.imshow("Result", bboxImage)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            (success, image) = cap.read()

        cv2.destroyAllWindows()

