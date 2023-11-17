FROM scrapinghub/splash
  
RUN echo 'root:bttminer' | chpasswd
RUN echo 'splash:bttminer' | chpasswd

RUN apt-get update && \
      apt-get -y install sudo
      
RUN adduser splash sudo
