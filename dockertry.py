from PIL import Image, ImageDraw
import os
import face_recognition
known_face_encodings = []
known_face_names = []
retrain=1
knownfolderpath=input("knownfolderpath=")
##############can count, identify and locate people in an image
def addtoknown(filename,personname):
    image_of_known = face_recognition.load_image_file(filename)
    known_face_encodings.append( face_recognition.face_encodings(image_of_known)[0] )
    known_face_names.append(personname)

directory = os.fsencode(knownfolderpath)
#retrain=int(input("Do you want to retrain face recognizer?(0/1)"))
if(retrain):
    print("####training face recognizer.........")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".jpg"): 
            name=filename.split('.')[0]
            locn=knownfolderpath+"/"+filename
            print("##########training on ",locn)
            addtoknown(locn,name)    
        else:
            continue
    print("###training finished!")


editedfname=input("test image location=")
facetestimage = face_recognition.load_image_file(editedfname)
face_locations = face_recognition.face_locations(facetestimage)
if(len(face_locations)):
	print(f'There are {len(face_locations)} people in '+editedfname)

face_encodings = face_recognition.face_encodings(facetestimage, face_locations)
pil_image = Image.fromarray(facetestimage)
draw = ImageDraw.Draw(pil_image)
for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = "Unknown Person"
    # If match
    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]
    # Draw box
    draw.rectangle(((left, top), (right, bottom)), outline=(255,255,0))
    # Draw label
    text_width, text_height = draw.textsize(name)
    draw.rectangle(((left,bottom - text_height - 10), (right, bottom)), fill=(255,255,0), outline=(255,255,0))
    draw.text((left + 6, bottom - text_height - 5), name, fill=(0,0,0))
del draw
#pil_image.show()
#print(fname+" has "+peopletotag)
fnameinitials=editedfname.split('.')[0]
pil_image.save(fnameinitials+"pplbox.jpg")
