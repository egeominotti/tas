FROM nikolaik/python-nodejs:latest

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends python3-pip \
                                         python3-dev \
                                         libpq-dev \
                                         postgresql \
                                         postgresql-contrib \
                                         gdal-bin \
                                         postgis \
                                         nodejs \
                                         libpq-dev \
                                         musl-dev \
                                         gcc \
                                         wget \
                                         curl \
                                         git

RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.1/zsh-in-docker.sh)" -- \
    -t https://github.com/denysdovhan/spaceship-prompt \
    -a 'SPACESHIP_PROMPT_ADD_NEWLINE="false"' \
    -a 'SPACESHIP_PROMPT_SEPARATE_LINE="false"' \
    -p git \
    -p ssh-agent \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions

RUN mkdir /tas
WORKDIR /tas
COPY entrypoint.sh /tas/
COPY requirements.txt /tas/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /tas/
ENTRYPOINT ["/tas/entrypoint.sh"]

