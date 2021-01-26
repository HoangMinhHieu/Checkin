def notification(string):
    with open('/home/pi/checkFace/data.txt', 'w') as log:
        log.write('{}'.format(string))
notification('Warming up...')

import timeit
start = timeit.default_timer()
import time 
import face_recognition
import picamera
from annoy import AnnoyIndex
import numpy as np
import math

open('/home/pi/checkFace/data.txt', 'w').close()
camera = picamera.PiCamera()
camera.resolution = (128, 128)
# camera.exposure_compensation = 2
#camera.meter_mode = 'backlit'
#camera.framerate = 30
# camera.saturation = 55
camera.brightness = 60
rgb_small_frame = np.empty((128, 128, 3), dtype=np.uint8)

# Load Annoy tree
f = 128
u = AnnoyIndex(f, 'euclidean')
u.load('all_hyper1.ann')

# Person ID list
def readFile(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return words

known_face_names = readFile('hyper_id1.txt')

# Initialize some variables
face_locations = []
face_encodings = []
process_this_frame = True


stop = timeit.default_timer()
print('Startup time : ' + str(stop-start))
print("Capturing image...")

def face_rec(rgb_small_frame):
    #print('Capturing image..', round(1.0/time.time()- start_time, 1))
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    # Choose the face with largest area if there are more than 1
    # More than 1 face
    if (len(face_locations) > 0):
        dists = []
        # largest_face_location = []
        print("Found {} Face(s). {}fps".format(len(face_locations),round(1.0/(time.time() -start_time), 1)))
        for i in range(len(face_locations)):
            p = face_locations[i]
            dist = math.hypot(p[2] - p[0], p[3] - p[1])
            dists.append(dist)
        largest_face_id = np.argmax(dists)

        face_encodings = face_recognition.face_encodings(rgb_small_frame, [face_locations[largest_face_id]])

        face_locations = [face_locations[largest_face_id]]

        face_encoding = face_encodings[0]
        # index vector  annoy
        matches_id, dis = u.get_nns_by_vector(face_encoding, 1, include_distances = True)
        matches_id = matches_id[0]
        dis = dis[0]

        name = "0"
        # # If a match was found in known_face_encodings, just use the first one.
        if (dis<0.4):
            # first_match_index = matches.index(True)
            name = known_face_names[matches_id]
            print("PERSON ID: {} {}".format(name,round(dis,3)))
            return int(name)
        else:
            print(name, round(dis,3))
            return int(name)
    else:
        
        return -1
           
#start preview
camera.start_preview(fullscreen=False,window=(50,175,300,300))
#camera.start_preview(fullscreen=False,window=(37,205,450,330))
n = 0
while True:
    start_time = time.time()
    # freetime = value/fps then stop the camera
#     if (n == 5):
#         print("Camera Closed")
#         camera.close()
    camera.capture(rgb_small_frame, format="rgb")

    # Only process every other frame of video to save time
    if process_this_frame:
        id = face_rec(rgb_small_frame)
        if (id > 0):
            notification('\n' + 'ID: ' + str(id) + '\n' + '\n' + 'Checkin time:  ' + str(time.ctime()))
            with open('/home/pi/checkFace/attendance.txt', 'a') as f:
                f.write('ID: '+str(id)+' - Checkin time: '+ str(time.ctime())+'\n')
        if (id == 0):
            notification('Unknow')

    print('FPS:',round(1.0/(time.time() -start_time), 1))
    process_this_frame = not process_this_frame




