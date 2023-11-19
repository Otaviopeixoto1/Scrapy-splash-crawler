# Scrapy-Splash crawler

A web crawler made using the scrapy python library (https://scrapy.org/) together with the Splash lightweight web browser (https://splash.readthedocs.io/en/stable/) to extract data from the ANVISA medical leaflet repository: https://consultas.anvisa.gov.br/#/bulario/


All the leaflets are queried and extracted by looping over all letters of the alphabet and inserting into the url: https://consultas.anvisa.gov.br/#/bulario/q/?nomeProduto={letter}&categoriasRegulatorias=1,2,3,4,5,6,10,7,8 

This results in a query for all leaflets with names that start with {letter}


# Run

- Splash was configured to run on a custom docker container. First, build the docker image from my docker file:

```
sudo docker build -t mysplash - < Dockerfile
```

- On linux, on the root directory of the project, run this command to start the container:

```
sudo docker run -it -p 8050:8050 -v "$(pwd)"/dockerfolder:/home mysplash --disable-private-mode --max-timeout 36000 --disable-lua-sandbox
```

- On windows its better to use the full path of the dockerfolder:

```
sudo docker run -it -p 8050:8050 -v /{PATH WHERE CLONED REPO IS CONTAINED}/scrapy-splash-crawler/dockerfolder:/home mysplash --disable-private-mode --max-timeout 36000 --disable-lua-sandbox
```

- Then, just run the crawler by using:

```
cd medicamento
scrapy crawl miner
```

- The downloaded leaflets will be stored inside the dockerfolder in the path: dockerfolder/leaflet-{starting letter}


# Pipeline
![Alt text](samples/pipeline.jpg?raw=true "pipeline")


# Status
Currently, the code in this project is functional, however, many leaflet samples were acquired and the project was finished.
