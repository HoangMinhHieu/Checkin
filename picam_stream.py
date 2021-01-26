import timeit
start = timeit.default_timer()

import face_recognition
import picamera
from annoy import AnnoyIndex
import numpy as np
import math

camera = picamera.PiCamera()
camera.resolution = (320, 240)
rgb_small_frame = np.empty((240, 320, 3), dtype=np.uint8)

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
kt = True

stop = timeit.default_timer()
print('Startup time : ' + str(stop-start))
while kt==True:
    print("Capturing image...")
    camera.start_preview()
    camera.capture(rgb_small_frame, format="rgb")

    # Only process every other frame of video to save time
    if process_this_frame:

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        # Choose the face with largest area if there are more than 1
        # More than 1 face
        if (len(face_locations) > 0):
            dists = []
            # largest_face_location = []
            print("Number of Faces: {}".format(len(face_locations)))
            for i in range(len(face_locations)):
                p = face_locations[i]
                # dist = sqrt((p[2] - p[0]) ** 2 + (p[3] - p[1]) ** 2)
                dist = math.hypot(p[2] - p[0], p[3] - p[1])
                dists.append(dist)
            largest_face_id = np.argmax(dists)

            face_encodings = face_recognition.face_encodings(rgb_small_frame, [face_locations[largest_face_id]])

            face_locations = [face_locations[largest_face_id]]

            face_encoding = face_encodings[0]
            # index vector  annoy
            matches_id = u.get_nns_by_vector(face_encoding, 1)[0]
            # print("Merry Christmas! " + str(matches_id))

            # vector ra index
            known_face_encoding = np.array(u.get_item_vector(matches_id))
            # print(known_face_encoding)
            # Create arrays of known face encodings and their names
            known_face_encodings = []
            known_face_encodings.append(known_face_encoding)
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.37)
            name = "Stranger!"
            #
            # # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                # first_match_index = matches.index(True)
                name = known_face_names[matches_id]
                print("Person ID: {}".format(name))
                if name=='33':
                    kt = False
            else:
                print(name)
    process_this_frame = not process_this_frame

if kt == False:
    camera.close()


