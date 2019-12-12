FROM ubuntu:18.04
# Replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update --fix-missing \
	&& apt-get install -y curl build-essential libssl-dev apt-transport-https \
	software-properties-common python3 python3-dev python3-pip python3-venv \
	monit && useradd -ms /bin/bash lunchbuddy

# Set home and app dir shortcuts
RUN mkdir /home/lunchbuddy/app
ENV HOME /home/lunchbuddy
ENV APP $HOME/app
# Move files to proper location
COPY ./backend $APP/backend
COPY ./frontend $APP/frontend
COPY ./*.sh $APP/
COPY ./monitrc $APP/
RUN chmod 700 ${APP}/monitrc && chown -R lunchbuddy:lunchbuddy $APP

# Switch to app user
USER lunchbuddy
WORKDIR $APP

# Set node version
ENV NVM_DIR /home/lunchbuddy/.nvm
ENV NODE_VERSION 12.10.0
ENV HOME /home/lunchbuddy

# Install nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.1/install.sh | bash \
	&& source $NVM_DIR/nvm.sh \
	&& nvm install $NODE_VERSION \
	&& nvm alias default $NODE_VERSION \
	&& nvm use default

# Set path
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $HOME/.yarn/bin:$HOME/.config/yarn/global/node_modules/.bin:$NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# Install yarn
# Environment file for deployment
RUN curl -o- -L https://yarnpkg.com/install.sh | bash \
	&& echo "PORT=3000" >> ./frontend/.env

# Install python and node packages
RUN ./install.sh

# Run tests
RUN ./test.sh

# Frontend port, monit port
EXPOSE 3000 2812

# Run monit
ENTRYPOINT [ "monit", "-c", "./monitrc" ]
