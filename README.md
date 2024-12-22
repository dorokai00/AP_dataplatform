# SH_data_platform


**Avg rent estimator**:<br>
This folder contains the notebook which first collects and parses the zip codes of SH. Then it geocodes them for the lat, lon coordinates. Then it gets the average rent estimates. Also a list of locations which werent found is included.

**Connecting_dbs**:<br>
This folder contains the versions running up to final datahandler/outputmanager set-up. I didnt delete them because the way I understood it you might want them, but they are definitely not like needed I'd say.
Then there is the final version containing only the classes, as well as one with the experiments of functionality and outputs.

**Data**:<br>
contains notebook to read in collection + the collections. 

**Digitize_the_planet**:<br>
Contains a notebook with API calls and geoboundaries of SH.

**Docker_exp_setup**:<br>
Contains a small trial set up of docker for YP with Sumans yaml file + dependencies.

**geoboundaries**:<br>
Data of and method for getting SH boundaries.

**vector store**:<br>
Contains a notebook with Qdrant experimentation, which I didnt use in the end.
And the creating and filling of ChromaDB vector store from MongoDB textual data in another notebook.

**YP scraper**:<br>
Contains developmental and final versions of YP scraper.
- one for Kiel only
- one where if the process breaks down, its easy to restart 
- one to just run completely if everything goes well

**OSM DATA**:<br>

