FROM joyzoursky/python-chromedriver:latest
COPY . /srv/zstu

WORKDIR /srv/zstu
RUN apt-get update \
    && apt-get install -y jq cron \
    && apt autoremove -y \
    && apt-get clean \
    && pip3 install --upgrade pip \
    && pip3 install -r requirements.txt \
    && cp run.sh /bin/report

WORKDIR /srv/zstu   
CMD [ "/bin/bash", "run.sh" ]