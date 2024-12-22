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
- OSM scraper contains two version where version_2 is the final output.
- but our whole experiment is carried out using version_1


**API**:<br>
- The folder name API contains the file used for building our API. 
- HOW TO RUN IT?
- It has been written inside the code file

**Docker**:<br>
- The folder contains the information how to run multiple jupyter notebook script every 24 hours automatically and mongoDB too.
- HOW TO RUN IT?
- It has been written inside the file named Docker.yml which is inside folder called Docker_for_multiple_script

  **Kiel_events_scraper**:<br>
- The folder contains two subfolders that has Kiel_events_api call and Kiel_events_scraper.
- The kiel_events_api call folder has notebooks to acquire kiel events via api.
- The Kiel_events_scraper has notebooks of various versions.The most latest version has the latest updates.
- 
    **Streamlit_user interface**:<br>
-The folder has notebook to run streamlit app .
-It has app4.py that has program to run the streamlit app.
- It has main.py that runs API in the backend.
- It has datahandlers_v5 that focuses on data integration.
