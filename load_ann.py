import timeit
start = timeit.default_timer()
import face_recognition
from annoy import AnnoyIndex
import numpy as np
embedding_size = 128  # FaceNet output size
t = AnnoyIndex(embedding_size, 'euclidean')
t.load('all_hyper1.ann')
#Person list
def readFile(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return words

known_face_names = readFile('hyper_id1.txt')
img = face_recognition.load_image_file('encode/6/6.jpg', mode='RGB')
face_locations = face_recognition.face_locations(img)
face_encodings = face_recognition.face_encodings(img, face_locations)
matches_id, dis = t.get_nns_by_vector(face_encodings[0], 1, include_distances=True)
matches_id = matches_id[0]
print(str(known_face_names[matches_id]) + '   Distance: ' +str(dis[0]))

print('Time: ', timeit.default_timer()-start)
