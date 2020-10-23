FROM python:3-onbuild

RUN pip install -r requirements.txt
COPY . /usr/src/app
CMD ["python3", "app.py"]
