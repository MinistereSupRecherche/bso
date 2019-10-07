# Open Access Monitoring for France

A complete description of the methodology and results can be found in the article <https://hal.archives-ouvertes.fr/hal-02141819>

The results presented in the article can be reproduced with the notebook `French Open Access Monitor` in the notebooks folder.

## Setup
 - Install docker and docker-compose and launch the daemon `systemctl start docker`

 - Install a MongoDB instance (that can be on another machine). Modify `/etc/mongo.conf` and ensure you bind IP 0.0.0.0 or some specific IPs you'll use and start the service and launch the daemon.

 - Replace the IPs in the `.env` file with the MongoDB IP and your local IP.

 - If you are behind a proxy, first build the app:

```
sudo docker-compose build --build-arg HTTP_PROXY=http://PROXY:PORT
```

 - Launch the app:
```
sudo docker-compose up
```

## API doc (swagger)
The swagger is available at `http://0.0.0.0:5000/publications/analyzers/doc`

## Database

The app uses two collections, `unpaywall_dump`and `notices_publications`

 - `unpaywall_dump` can be fed with the script `scripts/load_unpaywall_data.py`. It will download the Unpaywall DB snapshot, filter it by year, and load it into mongo through the app API.

 - `notices_publications` should be fed with the scraped html of the DOI redirect pages `http://doi.org/...`. As an example, the script `scripts/load_publication_html.py` loads an example json element.

## Processing the data to build and update the publications database

The script `script/process_publications.py` processes all the publications in the `unpaywall_dump` collection, determines if it has a french affiliation using the HAL api and the info in the `notices_publications` collection, and finally loads the `publications` collection.
