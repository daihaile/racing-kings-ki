#!/usr/bin/env python

FROM python:3

#this is where you install your python dependencies
RUN pip install simplejson
RUN pip install datetime
RUN pip install requests
RUN pip install python-dateutil
RUN pip install sseclient
RUN pip install tqdm

WORKDIR /app
COPY /app /app
RUN chmod 755 /app

ENTRYPOINT ["python3", "Main.py"]

