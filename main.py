import pafy
import cv2
import imutils
import numpy as np
import argparse
import signal
import sys
import time

NMS_THRESHOLD=0.3
MIN_CONFIDENCE=0.2
path = 'output.txt'
f = open(path, 'a')
def signal_handler(signum, frame):
    print("******************************************************************")
    f.write("******************************************************************\n")
    print('caught ctrl+c signal...')
    f.write('caught ctrl+c signal...\n')
    if signum == signal.SIGINT.value:
        print("******************************************************************")
        f.write("******************************************************************\n")
        print("Remaining frames : {0}".format(one_hour_frames))
        f.write("Remaining frames : {0}\n".format(one_hour_frames))
        print("Remaining times : {0} minutes {1} seconds".format(round((one_hour_frames/fps)/60,2),round((one_hour_frames/fps)%60,2)))
        f.write("Remaining times : {0} minutes {1} seconds\n".format(round((one_hour_frames/fps)/60,2),round((one_hour_frames/fps)%60,2)))
        print("Remaining people appear frames : {0}".format(total_people_appears_in_one_hour_frame))
        f.write("Remaining people appear frames : {0}\n".format(total_people_appears_in_one_hour_frame))
        print("Remaining people appear times : {0} minutes {1} seconds".format(round((total_people_appears_in_one_hour_frame/fps)/60,2),round((total_people_appears_in_one_hour_frame/fps)%60,2)))
        f.write("Remaining people appear times : {0} minutes {1} seconds\n".format(round((total_people_appears_in_one_hour_frame/fps)/60,2),round((total_people_appears_in_one_hour_frame/fps)%60,2)))
        print("Remaining weighted frames in one hour: {0}".format(total_people_in_one_hour))
        f.write("Remaining weighted frames in one hour: {0}\n".format(total_people_in_one_hour))
        print("Remaining weighted times in one hour : {0} hours {1} minutes {2} seconds".format(round(total_people_in_one_hour/fps/3600,2),round(((total_people_in_one_hour/fps)%3600)/60,2),round((total_people_in_one_hour/fps)%60,2)))
        f.write("Remaining weighted times in one hour : {0} hours {1} minutes {2} seconds\n".format(round(total_people_in_one_hour/fps/3600,2),round(((total_people_in_one_hour/fps)%3600)/60,2),round((total_people_in_one_hour/fps)%60,2)))
        print("Remaining appears people : {0}".format(total_people_in_one_hour))
        f.write("Remaining appears people : {0}\n".format(total_people_in_one_hour))
        print("Remaining average people : {0}".format(round(total_people_in_one_hour/one_hour_frames,2)))
        f.write("Remaining average people : {0}\n".format(round(total_people_in_one_hour/one_hour_frames,2)))
        print("******************************************************************")
        f.write("******************************************************************\n")
        print("Total frames : {0}".format(total_frames))
        f.write("Total frames : {0}\n".format(total_frames))
        print("Total times : {0} hours {1} minutes {2} seconds".format(round(total_frames/fps/3600,2),round(((total_frames/fps)%3600)/60,2),round((total_frames/fps)%60,2)))
        f.write("Total times : {0} hours {1} minutes {2} seconds\n".format(round(total_frames/fps/3600,2),round(((total_frames/fps)%3600)/60,2),round((total_frames/fps)%60,2)))
        print("Total people appears frames : {0}".format(total_people_appears_frame))
        f.write("Total people appears frames : {0}\n".format(total_people_appears_frame))
        print("Total people appears times :{0} hours {1} minutes {2} seconds".format(round(total_people_appears_frame/fps/3600,2),round(((total_people_appears_frame/fps)%3600)/60,2),round((total_people_appears_frame/fps)%60,2)))
        f.write("Total people appears times : {0} hours {1} minutes {2} seconds\n".format(round(total_people_appears_frame/fps/3600,2),round(((total_people_appears_frame/fps)%3600)/60,2),round((total_people_appears_frame/fps)%60,2)))
        print("Total weighted frames : {0}".format(total_people))
        f.write("Total weighted frames : {0}\n".format(total_people))
        print("Total weighted times : {0} hours {1} minutes {2} seconds".format(round(total_people/fps/3600,2),round(((total_people/fps)%3600)/60,2),round((total_people/fps)%60,2)))
        f.write("Total weighted times : {0} hours {1} minutes {2} seconds\n".format(round(total_people/fps/3600,2),round(((total_people/fps)%3600)/60,2),round((total_people/fps)%60,2)))
        print("******************************************************************")
        f.write("******************************************************************\n")
        print("Average people in this video : {0}".format(round(total_people/total_frames,2)))
        f.write("Average people in this video : {0}\n".format(round(total_people/total_frames,2)))
        f.write('==================================================================\n')
    sys.exit(1)


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
    global total_frames
    global total_people_appears_frame
    global one_hour_frames
    global total_people_appears_in_one_hour_frame
    global total_people
    global total_people_in_one_hour
    total_frames = 0
    total_people_appears_frame = 0
    one_hour_frames = 0
    total_people_appears_in_one_hour_frame = 0
    total_people = 0
    total_people_in_one_hour = 0
    weighted_frames_in_one_hour = 0
    weighted_frames_in_total = 0
    video = cv2.VideoCapture(path)
    check, frame = video.read()
    if check == False:
        print('Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided).')
        return

    print('Detecting people...')

    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    f.write("******************************************************************\n")
    print("******************************************************************")
    if int(major_ver)  < 3 :
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
        f.write("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}\n".format(fps))
    else :
        fps = video.get(cv2.CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
        f.write("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}\n".format(fps))
 
    # With webcam get(CV_CAP_PROP_FPS) does not work.
    # Let's see for ourselves.


    while video.isOpened():
        #check is True if reading was successful 
        check, frame =  video.read()
        total_frames = total_frames + 1
        one_hour_frames = one_hour_frames + 1
        person = 0
        if check:
            frame = imutils.resize(frame , width=min(800,frame.shape[1]))
            results = pedestrian_detection(frame, model, layer_name,personidz=LABELS.index("person"))
            
            for res in results:
                cv2.rectangle(frame, (res[1][0],res[1][1]), (res[1][2],res[1][3]), (0, 255, 0), 2)
                person += 1
            cv2.putText(frame, f'Total Persons : {person}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
            cv2.imshow("Detection",frame)
            if person > 0:
                total_people_appears_frame = total_people_appears_frame + 1
                total_people_appears_in_one_hour_frame = total_people_appears_in_one_hour_frame + 1
                total_people = total_people + person
                total_people_in_one_hour = total_people_in_one_hour + person
            if writer is not None:
                writer.write(frame)
            if one_hour_frames/fps >= 3600:
                print("******************************************************************")
                f.write("******************************************************************\n")
                print("Total frames in one hour: {0}".format(one_hour_frames))
                f.write("Total frames in one hour: {0}\n".format(one_hour_frames))
                print("Total times in one hour: {0} hours {1} minutes {2} seconds".format(round(one_hour_frames/fps/3600,2),round(((one_hour_frames/fps)%3600)/60,2),round((one_hour_frames/fps)%60,2)))
                f.write("Total times in one hour: {0} hours {1} minutes {2} seconds\n".format(round(one_hour_frames/fps/3600,2),round(((one_hour_frames/fps)%3600)/60,2),round((one_hour_frames/fps)%60,2)))
                print("Total people appears in frames during one hours : {0}".format(total_people_appears_in_one_hour_frame))
                f.write("Total people appears in frames during one hours : {0}\n".format(total_people_appears_in_one_hour_frame))
                print("Total people appears in times during one hours : {0} hours {1} minutes {2} seconds".format(round(total_people_appears_in_one_hour_frame/fps/3600,2),round(((total_people_appears_in_one_hour_frame/fps)%3600)/60,2),round((total_people_appears_in_one_hour_frame/fps)%60,2)))
                f.write("Total people appears in times during one hours : {0} hours {1} minutes {2} seconds\n".format(round(total_people_appears_in_one_hour_frame/fps/3600,2),round(((total_people_appears_in_one_hour_frame/fps)%3600)/60,2),round((total_people_appears_in_one_hour_frame/fps)%60,2)))
                print("Weighted frames in one hour: {0}".format(total_people_in_one_hour))
                f.write("Weighted frames in one hour: {0}\n".format(total_people_in_one_hour))
                print("Weighted times in one hour : {0} hours {1} minutes {2} seconds".format(round(total_people_in_one_hour/fps/3600,2),round(((total_people_in_one_hour/fps)%3600)/60,2),round((total_people_in_one_hour/fps)%60,2)))
                f.write("Weighted times in one hour : {0} hours {1} minutes {2} seconds\n".format(round(total_people_in_one_hour/fps/3600,2),round(((total_people_in_one_hour/fps)%3600)/60,2),round((total_people_in_one_hour/fps)%60,2)))
                print("Total people appears in one hour: {0}".format(total_people_in_one_hour))
                f.write("Total people appears in one hour: {0}\n".format(total_people_in_one_hour))
                print("Average people in one hour : {0}".format(round(total_people_in_one_hour/one_hour_frames),2))
                f.write("Average people in one hour : {0}\n".format(round(total_people_in_one_hour/one_hour_frames),2))
                print("******************************************************************")
                f.write("******************************************************************\n")
                one_hour_frames = 0
                total_people_appears_in_one_hour_frame = 0
                total_people_in_one_hour =0
            key = cv2.waitKey(1)
            if key== ord('q'):
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()
    print("******************************************************************")
    f.write("******************************************************************\n")
    print("Remaining frames : {0}".format(one_hour_frames))
    f.write("Remaining frames : {0}\n".format(one_hour_frames))
    print("Remaining times : {0} minutes {1} seconds".format(round((one_hour_frames/fps)/60,2),round((one_hour_frames/fps)%60,2)))
    f.write("Remaining times : {0} minutes {1} seconds\n".format(round((one_hour_frames/fps)/60,2),round((one_hour_frames/fps)%60,2)))
    print("Remaining people appear frames : {0}".format(total_people_appears_in_one_hour_frame))
    f.write("Remaining people appear frames : {0}\n".format(total_people_appears_in_one_hour_frame))
    print("Remaining people appear times : {0} minutes {1} seconds".format(round((total_people_appears_in_one_hour_frame/fps)/60,2),round((total_people_appears_in_one_hour_frame/fps)%60,2)))
    f.write("Remaining people appear times : {0} minutes {1} seconds\n".format(round((total_people_appears_in_one_hour_frame/fps)/60,2),round((total_people_appears_in_one_hour_frame/fps)%60,2)))
    print("Remaining weighted frames in one hour: {0}".format(total_people_in_one_hour))
    f.write("Remaining weighted frames in one hour: {0}\n".format(total_people_in_one_hour))
    print("Remaining weighted times in one hour : {0} hours {1} minutes {2} seconds".format(round(total_people_in_one_hour/fps/3600,2),round(((total_people_in_one_hour/fps)%3600)/60,2),round((total_people_in_one_hour/fps)%60,2)))
    f.write("Remaining weighted times in one hour : {0} hours {1} minutes {2} seconds\n".format(round(total_people_in_one_hour/fps/3600,2),round(((total_people_in_one_hour/fps)%3600)/60,2),round((total_people_in_one_hour/fps)%60,2)))
    print("Remaining appears people : {0}".format(total_people_in_one_hour))
    f.write("Remaining appears people : {0}\n".format(total_people_in_one_hour))
    print("Remaining average people : {0}".format(round(total_people_in_one_hour/one_hour_frames,2)))
    f.write("Remaining average people : {0}\n".format(round(total_people_in_one_hour/one_hour_frames,2)))
    print("******************************************************************")
    f.write("******************************************************************\n")
    print("Total frames : {0}".format(total_frames))
    f.write("Total frames : {0}\n".format(total_frames))
    print("Total times : {0} hours {1} minutes {2} seconds".format(round(total_frames/fps/3600,2),round(((total_frames/fps)%3600)/60,2),round((total_frames/fps)%60,2)))
    f.write("Total times : {0} hours {1} minutes {2} seconds\n".format(round(total_frames/fps/3600,2),round(((total_frames/fps)%3600)/60,2),round((total_frames/fps)%60,2)))
    print("Total people appears frames : {0}".format(total_people_appears_frame))
    f.write("Total people appears frames : {0}\n".format(total_people_appears_frame))
    print("Total people appears times :{0} hours {1} minutes {2} seconds".format(round(total_people_appears_frame/fps/3600,2),round(((total_people_appears_frame/fps)%3600)/60,2),round((total_people_appears_frame/fps)%60,2)))
    f.write("Total people appears times : {0} hours {1} minutes {2} seconds\n".format(round(total_people_appears_frame/fps/3600,2),round(((total_people_appears_frame/fps)%3600)/60,2),round((total_people_appears_frame/fps)%60,2)))
    print("Total weighted frames : {0}".format(total_people))
    f.write("Total weighted frames : {0}\n".format(total_people))
    print("Total weighted times : {0} hours {1} minutes {2} seconds".format(round(total_people/fps/3600,2),round(((total_people/fps)%3600)/60,2),round((total_people/fps)%60,2)))
    f.write("Total weighted times : {0} hours {1} minutes {2} seconds\n".format(round(total_people/fps/3600,2),round(((total_people/fps)%3600)/60,2),round((total_people/fps)%60,2)))
    print("******************************************************************")
    f.write("******************************************************************\n")
    print("Average people in this video : {0}".format(round(total_people/total_frames,2)))
    f.write("Average people in this video : {0}\n".format(round(total_people/total_frames,2)))
    f.write('==================================================================\n')


def detectByPathStreamLive(path, writer):
    global total_frames
    global total_people_appears_frame
    global one_hour_frames
    global total_people_appears_in_one_hour_frame
    global fps
    global total_people
    global total_people_in_one_hour
    total_frames = 0
    total_people_appears_frame = 0
    one_hour_frames = 0
    total_people_appears_in_one_hour_frame = 0
    total_people = 0
    total_people_in_one_hour = 0
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
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    print("******************************************************************")
    if int(major_ver)  < 3 :
        fps = capture.get(cv2.cv.CV_CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
        f.write("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}\n".format(fps))
    else :
        fps = capture.get(cv2.CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
        f.write("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}\n".format(fps))
 
    # With webcam get(CV_CAP_PROP_FPS) does not work.
    # Let's see for ourselves.


    while capture.isOpened():
        #check is True if reading was successful 
        check, frame =  capture.read()
        total_frames = total_frames + 1
        one_hour_frames = one_hour_frames + 1
        person = 0
        if check:
            frame = imutils.resize(frame , width=min(800,frame.shape[1]))
            results = pedestrian_detection(frame, model, layer_name,personidz=LABELS.index("person"))
            
            for res in results:
                cv2.rectangle(frame, (res[1][0],res[1][1]), (res[1][2],res[1][3]), (0, 255, 0), 2)
                person += 1
            cv2.putText(frame, f'Total Persons : {person}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
            cv2.imshow("Detection",frame)
            if person > 0:
                total_people_appears_frame = total_people_appears_frame + 1
                total_people_appears_in_one_hour_frame = total_people_appears_in_one_hour_frame + 1
                total_people = total_people + person
                total_people_in_one_hour = total_people_in_one_hour + person
            if writer is not None:
                writer.write(frame)
            if one_hour_frames/fps >= 3600:
                print("******************************************************************")
                f.write("******************************************************************\n")
                print("Total frames in one hour: {0}".format(one_hour_frames))
                f.write("Total frames in one hour: {0}\n".format(one_hour_frames))
                print("Total times in one hour: {0} hours {1} minutes {2} seconds".format(round(one_hour_frames/fps/3600,2),round(((one_hour_frames/fps)%3600)/60,2),round((one_hour_frames/fps)%60,2)))
                f.write("Total times in one hour: {0} hours {1} minutes {2} seconds\n".format(round(one_hour_frames/fps/3600,2),round(((one_hour_frames/fps)%3600)/60,2),round((one_hour_frames/fps)%60,2)))
                print("Total people appears in frames during one hours : {0}".format(total_people_appears_in_one_hour_frame))
                f.write("Total people appears in frames during one hours : {0}\n".format(total_people_appears_in_one_hour_frame))
                print("Total people appears in times during one hours : {0} hours {1} minutes {2} seconds".format(round(total_people_appears_in_one_hour_frame/fps/3600,2),round(((total_people_appears_in_one_hour_frame/fps)%3600)/60,2),round((total_people_appears_in_one_hour_frame/fps)%60,2)))
                f.write("Total people appears in times during one hours : {0} hours {1} minutes {2} seconds\n".format(round(total_people_appears_in_one_hour_frame/fps/3600,2),round(((total_people_appears_in_one_hour_frame/fps)%3600)/60,2),round((total_people_appears_in_one_hour_frame/fps)%60,2)))
                print("Weighted frames in one hour: {0}".format(total_people_in_one_hour))
                f.write("Weighted frames in one hour: {0}\n".format(total_people_in_one_hour))
                print("Weighted times in one hour : {0} hours {1} minutes {2} seconds".format(round(total_people_in_one_hour/fps/3600,2),round(((total_people_in_one_hour/fps)%3600)/60,2),round((total_people_in_one_hour/fps)%60,2)))
                f.write("Weighted times in one hour : {0} hours {1} minutes {2} seconds\n".format(round(total_people_in_one_hour/fps/3600,2),round(((total_people_in_one_hour/fps)%3600)/60,2),round((total_people_in_one_hour/fps)%60,2)))
                print("Total people appears in one hour: {0}".format(total_people_in_one_hour))
                f.write("Total people appears in one hour: {0}\n".format(total_people_in_one_hour))
                print("Average people in one hour : {0}".format(round(total_people_in_one_hour/one_hour_frames),2))
                f.write("Average people in one hour : {0}\n".format(round(total_people_in_one_hour/one_hour_frames),2))
                print("******************************************************************")
                f.write("******************************************************************\n")
                one_hour_frames = 0
                total_people_appears_in_one_hour_frame = 0
                total_people_in_one_hour = 0
            key = cv2.waitKey(1)

            if key== ord('q'):
                break
        else:
            break
    capture.release()
    cv2.destroyAllWindows()
    print("******************************************************************")
    f.write("******************************************************************\n")
    print("Remaining frames : {0}".format(one_hour_frames))
    f.write("Remaining frames : {0}\n".format(one_hour_frames))
    print("Remaining times : {0} minutes {1} seconds".format(round((one_hour_frames/fps)/60,2),round((one_hour_frames/fps)%60,2)))
    f.write("Remaining times : {0} minutes {1} seconds\n".format(round((one_hour_frames/fps)/60,2),round((one_hour_frames/fps)%60,2)))
    print("Remaining people appear frames : {0}".format(total_people_appears_in_one_hour_frame))
    f.write("Remaining people appear frames : {0}\n".format(total_people_appears_in_one_hour_frame))
    print("Remaining people appear times : {0} minutes {1} seconds".format(round((total_people_appears_in_one_hour_frame/fps)/60,2),round((total_people_appears_in_one_hour_frame/fps)%60,2)))
    f.write("Remaining people appear times : {0} minutes {1} seconds\n".format(round((total_people_appears_in_one_hour_frame/fps)/60,2),round((total_people_appears_in_one_hour_frame/fps)%60,2)))
    print("Remaining weighted frames in one hour: {0}".format(total_people_in_one_hour))
    f.write("Remaining weighted frames in one hour: {0}\n".format(total_people_in_one_hour))
    print("Remaining weighted times in one hour : {0} hours {1} minutes {2} seconds".format(round(total_people_in_one_hour/fps/3600,2),round(((total_people_in_one_hour/fps)%3600)/60,2),round((total_people_in_one_hour/fps)%60,2)))
    f.write("Remaining weighted times in one hour : {0} hours {1} minutes {2} seconds\n".format(round(total_people_in_one_hour/fps/3600,2),round(((total_people_in_one_hour/fps)%3600)/60,2),round((total_people_in_one_hour/fps)%60,2)))
    print("Remaining appears people : {0}".format(total_people_in_one_hour))
    f.write("Remaining appears people : {0}\n".format(total_people_in_one_hour))
    print("Remaining average people : {0}".format(round(total_people_in_one_hour/one_hour_frames,2)))
    f.write("Remaining average people : {0}\n".format(round(total_people_in_one_hour/one_hour_frames,2)))
    print("******************************************************************")
    f.write("******************************************************************\n")
    print("Total frames : {0}".format(total_frames))
    f.write("Total frames : {0}\n".format(total_frames))
    print("Total times : {0} hours {1} minutes {2} seconds".format(round(total_frames/fps/3600,2),round(((total_frames/fps)%3600)/60,2),round((total_frames/fps)%60,2)))
    f.write("Total times : {0} hours {1} minutes {2} seconds\n".format(round(total_frames/fps/3600,2),round(((total_frames/fps)%3600)/60,2),round((total_frames/fps)%60,2)))
    print("Total people appears frames : {0}".format(total_people_appears_frame))
    f.write("Total people appears frames : {0}\n".format(total_people_appears_frame))
    print("Total people appears times :{0} hours {1} minutes {2} seconds".format(round(total_people_appears_frame/fps/3600,2),round(((total_people_appears_frame/fps)%3600)/60,2),round((total_people_appears_frame/fps)%60,2)))
    f.write("Total people appears times : {0} hours {1} minutes {2} seconds\n".format(round(total_people_appears_frame/fps/3600,2),round(((total_people_appears_frame/fps)%3600)/60,2),round((total_people_appears_frame/fps)%60,2)))
    print("Total weighted frames : {0}".format(total_people))
    f.write("Total weighted frames : {0}\n".format(total_people))
    print("Total weighted times : {0} hours {1} minutes {2} seconds".format(round(total_people/fps/3600,2),round(((total_people/fps)%3600)/60,2),round((total_people/fps)%60,2)))
    f.write("Total weighted times : {0} hours {1} minutes {2} seconds\n".format(round(total_people/fps/3600,2),round(((total_people/fps)%3600)/60,2),round((total_people/fps)%60,2)))
    print("******************************************************************")
    f.write("******************************************************************\n")
    print("Average people in this video : {0}".format(round(total_people/total_frames,2)))
    f.write("Average people in this video : {0}\n".format(round(total_people/total_frames,2)))
    f.write('==================================================================\n')



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
        print('[INFO] Opening video from path : {0}.'.format(video_path))
        f.write('\n')
        f.write('==================================================================\n')
        f.write('[INFO] Opening video from path : {0}.\n'.format(video_path))
        f.write("******************************************************************\n")
        detectByPathVideo(video_path, writer)
    elif image_path is not None:
        print('[INFO] Opening Image from path.')
        detectByPathImage(image_path, args['output'])
    elif stream_path is not None:
        print('[INFO] Opening Live stream from path : {0}.'.format(stream_path))
        f.write('\n')
        f.write('==================================================================\n')
        f.write('[INFO] Opening Live stream from path : {0}.\n'.format(stream_path))
        f.write("******************************************************************\n")
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

signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":

    labelsPath = "./model/coco.names"
    LABELS = open(labelsPath).read().strip().split("\n")

    weights_path = "./model/yolov4-tiny.weights"
    config_path = "./model/yolov4-tiny.cfg"

    model = cv2.dnn.readNetFromDarknet(config_path, weights_path)
    layer_name = model.getLayerNames()
    layer_name = [layer_name[i-1] for i in model.getUnconnectedOutLayers()]

    args = argsParser()
    humanDetector(args)
