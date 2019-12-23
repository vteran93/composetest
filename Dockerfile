FROM ubuntu:18.04
WORKDIR /code
ENV FLASK_APP microblog.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apt-get update && apt-get -y install gcc musl-dev linux-headers-generic python-pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN chmod u+x ./entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]