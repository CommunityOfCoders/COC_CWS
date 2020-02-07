FROM python:3

ADD dockertry.py /

RUN apt-get update -y && apt-get update && apt install cmake -y && apt install python3-pip -y && pip3 install dlib && pip3 install face_recognition 

CMD [ "python", "dockertry.py"]