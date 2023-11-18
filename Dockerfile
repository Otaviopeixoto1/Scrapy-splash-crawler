FROM scrapinghub/splash

USER root
RUN echo root:bttminer | chpasswd
RUN echo splash:bttminer | chpasswd

RUN apt-get update && \
      apt-get -y install sudo
      
RUN adduser splash sudo

RUN pip install bs4
RUN pip install selenium
RUN apt-get install -y firefox
#splash:splash
USER splash