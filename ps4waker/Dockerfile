FROM %%BASE_IMAGE%%

ENV LANG C.UTF-8

RUN apk add --no-cache jq nodejs nodejs-npm git \ 
	&& npm install -g mustache \
	&& mkdir repo \
	&& cd repo \
	&& git init . \
	&& git remote add -f origin https://github.com/vkorn/hassio-addons \
	&& git config core.sparseCheckout true \
	&& echo "hass/ps4-hass-waker/" >> .git/info/sparse-checkout \
	&& git pull origin master \
	&& cd hass/ps4-hass-waker \
	&& npm install -g . \
	&& cd ../../../ \
	&& rm -rf repo

COPY template.json /templates/
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]