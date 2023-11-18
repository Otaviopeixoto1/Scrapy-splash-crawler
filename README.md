# Scrapy-Splash crawler

A web crawler made using the scrapy python library (https://scrapy.org/) together with the Splash lightweight web browser (https://splash.readthedocs.io/en/stable/) to extract data from the ANVISA medical leaflet repository: https://consultas.anvisa.gov.br/#/bulario/


All the leaflets are queried and extracted by looping over all letters of the alphabet and inserting into the url: https://consultas.anvisa.gov.br/#/bulario/q/?nomeProduto={letter}&categoriasRegulatorias=1,2,3,4,5,6,10,7,8 


# Run

build the docker image from my docker file:

sudo docker build -t mysplash - < Dockerfile

splash was configured to run on a docker container using the command: 

sudo docker run -it -p 8050:8050 -v /home/otavio/python_projects/boitata/crawlers/scrapy-splash-crawler/dockerfolder:/home mysplash --disable-private-mode --max-timeout 36000 --disable-lua-sandbox

Then just run the crawler by using:

cd medicamento
scrapy crawl miner


# Pipeline
![Alt text](samples/pipeline.jpg?raw=true "pipeline")


# Status
Currently, the code in this project is not functional due to changes that happend to the web site, however, many leaflet samples were acquired and the project was finished successfully
