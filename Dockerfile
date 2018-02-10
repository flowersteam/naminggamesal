FROM python:3
ENV PYTHONUNBUFFERED 1
ADD requirements.txt /
RUN apt-get update && apt-get install --yes --force-yes apt-utils build-essential python-dev liblzo2-dev liblzma-dev libsqlite3-dev python3-tk tmux
RUN pip install numpy matplotlib scipy psycopg2 codecov coverage jupyter
RUN pip install -r requirements.txt
RUN python3 -m ipykernel install

RUN mkdir /naminggamesal
WORKDIR /naminggamesal
