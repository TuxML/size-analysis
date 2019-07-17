FROM frolvlad/alpine-python-machinelearning
COPY . /app
ADD http://37.187.140.181/tuxml_dataset/all_size_withyes.pkl /app
WORKDIR /app
ENTRYPOINT ["python","-u","./index.py"]