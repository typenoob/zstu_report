FROM joyzoursky/python-chromedriver:latest
ADD ./crontask /etc/cron.d/crontask
COPY . /srv/zstu

WORKDIR /srv/zstu
RUN apt-get update \
    && apt-get install -y jq cron \
    && apt autoremove -y \
    && apt-get clean \
    && pip3 install --upgrade pip \
    && pip3 install -r requirements.txt \
    && chmod 0644 /etc/cron.d/crontask \
    && echo "#!/bin/sh\n" > /home/boot.sh \
    && echo "service cron restart" >> /home/boot.sh \
    && echo "\n" >> /home/boot.sh \
    && echo "crontab /etc/cron.d/crontask" >> /home/boot.sh \
    && echo "\n" >> /home/boot.sh \
    && echo "flask run --host=0.0.0.0" >> /home/boot.sh \
    && echo "\n" >> /home/boot.sh \
    && echo "/bin/bash" >> /home/boot.sh \
    && cp run.sh /bin/report

WORKDIR /srv/zstu   
CMD [ "/bin/bash", "/home/boot.sh" ]
