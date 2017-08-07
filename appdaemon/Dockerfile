FROM %%BASE_IMAGE%%

ENV LANG C.UTF-8

RUN apk add --no-cache jq git python3 \ 
	&& python3 -m ensurepip \ 
	&& rm -r /usr/lib/python*/ensurepip \
	&& pip3 install --upgrade pip setuptools \ 
	&& if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi \ 
	&& pip install git+https://github.com/home-assistant/appdaemon.git@master

COPY appdaemon-example.yaml /etc/
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]