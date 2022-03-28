FROM animcogn/face_recognition:cpu-latest

WORKDIR /home/face_recognition
COPY /app .

RUN pip3 install -r requirements.txt

COPY src /src

ENTRYPOINT python3 face_recognition_server.py