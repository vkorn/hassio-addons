FROM %%BASE_IMAGE%%

ENV LANG C.UTF-8

RUN apk add --no-cache jq nodejs nodejs-npm git python make g++ \ 
	&& mkdir repo \
	&& cd repo \
	&& git init . \
	&& git remote add -f origin https://github.com/vkorn/hassio-addons \
	&& git config core.sparseCheckout true \
	&& echo "hass/config-watcher/" >> .git/info/sparse-checkout \
	&& git pull origin master \
	&& cp -r hass/config-watcher / \
	&& cd .. \
	&& rm -rf repo \
	&& npm config set unsafe-perm true \
	&& npm install -g forever \
	&& cd /config-watcher \ 
	&& npm install . \
	&& npm config set unsafe-perm false \ 
	&& apk del python make g++
	
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]