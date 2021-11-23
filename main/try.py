import pafy
import cv2
import imutils
import numpy as np
import argparse

NMS_THRESHOLD=0.3
MIN_CONFIDENCE=0.2

def pedestrian_detection(image, model, layer_name, personidz=0):
	(H, W) = image.shape[:2]
	results = []


	blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
		swapRB=True, crop=False)
	model.setInput(blob)
	layerOutputs = model.forward(layer_name)

	boxes = []
	centroids = []
	confidences = []

	for output in layerOutputs:
		for detection in output:

			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			if classID == personidz and confidence > MIN_CONFIDENCE:

				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				boxes.append([x, y, int(width), int(height)])
				centroids.append((centerX, centerY))
				confidences.append(float(confidence))
	# apply non-maxima suppression to suppress weak, overlapping
	# bounding boxes
	idzs = cv2.dnn.NMSBoxes(boxes, confidences, MIN_CONFIDENCE, NMS_THRESHOLD)
	# ensure at least one detection exists
	if len(idzs) > 0:
		# loop over the indexes we are keeping
		for i in idzs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])
			# update our results list to consist of the person
			# prediction probability, bounding box coordinates,
			# and the centroid
			res = (confidences[i], (x, y, x + w, y + h), centroids[i])
			results.append(res)
	# return the list of results
	return results

def detectByPathVideo(path, writer):

    video = cv2.VideoCapture(path)
    check, frame = video.read()
    if check == False:
        print('Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided).')
        return

    print('Detecting people...')
    while video.isOpened():
        #check is True if reading was successful 
        check, frame =  video.read()
        person = 0
        if check:
            frame = imutils.resize(frame , width=min(800,frame.shape[1]))
            results = pedestrian_detection(frame, model, layer_name,personidz=LABELS.index("person"))
            
            for res in results:
                cv2.rectangle(frame, (res[1][0],res[1][1]), (res[1][2],res[1][3]), (0, 255, 0), 2)
                person += 1
            cv2.putText(frame, f'Total Persons : {person}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
            cv2.imshow("Detection",frame)
            if writer is not None:
                writer.write(frame)
            key = cv2.waitKey(1)
            if key== ord('q'):
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()


def detectByPathStreamLive(path, writer):

    url = path
    video = pafy.new(url)
    best = video.getbest(preftype="mp4")
    capture = cv2.VideoCapture(best.url)
    # video = cv2.VideoCapture(path)
    check, frame = capture.read()
    # check, frame = video.read()
    if check == False:
        print('Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided).')
        return

    print('Detecting people...')
    while capture.isOpened():
        #check is True if reading was successful 
        check, frame =  capture.read()
        person = 0
        if check:
            frame = imutils.resize(frame , width=min(800,frame.shape[1]))
            results = pedestrian_detection(frame, model, layer_name,personidz=LABELS.index("person"))
            
            for res in results:
                cv2.rectangle(frame, (res[1][0],res[1][1]), (res[1][2],res[1][3]), (0, 255, 0), 2)
                person += 1
            cv2.putText(frame, f'Total Persons : {person}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
            cv2.imshow("Detection",frame)
            if writer is not None:
                writer.write(frame)
            key = cv2.waitKey(1)
            if key== ord('q'):
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()



def detectByCamera(writer):   
    video = cv2.VideoCapture(0)
    print('Detecting people...')

    while True:
        check, frame = video.read()

        results = pedestrian_detection(frame, model, layer_name,personidz=LABELS.index("person"))
            
        for res in results:
            cv2.rectangle(frame, (res[1][0],res[1][1]), (res[1][2],res[1][3]), (0, 255, 0), 2)
        cv2.imshow("Detection",frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
                break

    video.release()
    cv2.destroyAllWindows()

def detectByPathImage(path, output_path):
    image = cv2.imread(path)

    image = imutils.resize(image, width = min(800, image.shape[1])) 

    results = pedestrian_detection(image, model, layer_name,personidz=LABELS.index("person"))
            
    for res in results:
        cv2.rectangle(image, (res[1][0],res[1][1]), (res[1][2],res[1][3]), (0, 255, 0), 2)
    cv2.imshow("Detection",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def humanDetector(args):
    image_path = args["image"]
    video_path = args['video']
    stream_path = args['stream']
    if str(args["camera"]) == 'true' : camera = True 
    else : camera = False

    writer = None
    if args['output'] is not None and image_path is None:
        writer = cv2.VideoWriter(args['output'],cv2.VideoWriter_fourcc(*'MJPG'), 10, (600,600))

    if camera:
        print('[INFO] Opening Web Cam.')
        detectByCamera(ouput_path,writer)
    elif video_path is not None:
        print('[INFO] Opening Video from path.')
        detectByPathVideo(video_path, writer)
    elif image_path is not None:
        print('[INFO] Opening Image from path.')
        detectByPathImage(image_path, args['output'])
    elif stream_path is not None:
        print('[INFO] Opening Live stream from path.')
        detectByPathStreamLive(stream_path, writer)

def argsParser():
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-v", "--video", default=None, help="path to Video File ")
    arg_parse.add_argument("-s", "--stream", default=None, help="path to Stream File ")
    arg_parse.add_argument("-i", "--image", default=None, help="path to Image File ")
    arg_parse.add_argument("-c", "--camera", default=False, help="Set true if you want to use the camera.")
    arg_parse.add_argument("-o", "--output", type=str, help="path to optional output video file")
    args = vars(arg_parse.parse_args())

    return args

labelsPath = "coco.names"
LABELS = open(labelsPath).read().strip().split("\n")


weights_path = "yolov4-tiny.weights"
config_path = "yolov4-tiny.cfg"

model = cv2.dnn.readNetFromDarknet(config_path, weights_path)
layer_name = model.getLayerNames()
layer_name = [layer_name[i-1] for i in model.getUnconnectedOutLayers()]

if __name__ == "__main__":
    # HOGCV = cv2.HOGDescriptor()
    # HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    args = argsParser()
    humanDetector(args)