FROM python:3.6.6-alpine

RUN apk add --no-cache \
  enchant \
  #tini \
  aspell-en


COPY requirements.txt /
RUN pip install -r /requirements.txt && \
  #todo: download file directly to prevent re-download
  python -c "import nltk; nltk.download('punkt')"

COPY . /app
WORKDIR /app


#ENTRYPOINT ["/sbin/tini", "--", "python", "--", "sotawhat.py"]
ENTRYPOINT ["python", "--", "sotawhat.py"]

