FROM python:3.9-slim
 
# Install utilities
RUN apt-get -y update; apt-get install -y wget gnupg curl unzip 

# Install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update && apt-get install -y google-chrome-stable 

# Install chromedriver for selinium
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


# Set display port to avoid crash
ENV DISPLAY=:99

ADD ./ /project

# Install python dependencies
RUN python3.9 -m pip install -r /project/requirements.txt

WORKDIR /project/
CMD ["python3.9", "pschecker.py"]