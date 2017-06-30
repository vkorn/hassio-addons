FROM %%BASE_IMAGE%%

ENV LANG C.UTF-8

RUN apk add --no-cache jq nodejs nodejs-npm \ 
	&& npm install --verbose -g smartthings-mqtt-bridge mustache

COPY template.yml /templates/
COPY run.sh /
RUN chmod a+x /run.sh

# We need to percist state, so using data
ENV CONFIG_DIR=/data

CMD [ "/run.sh" ]