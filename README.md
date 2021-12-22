# Imgur-archive
Imgur-archive is lightweight python script interacting with the official Imgur API to download and archive albums. It automatically handles medias of type .png, .jpeg, .gif, and .mp4, and stores the description and metadata of the album. This is a simple and efficient tool to build datasets from Imgur media.

## Installation
1. Clone the repository
2. Create your account for the Imgur API
3. Create a file ``.api_secrets.json`` with your Imgur API credentials following the template (.TEMPLATE_api_secrets.json)
4. Create a new directory with a ``links.txt`` file inside
5. Set the variable ``STORAGE_DIRPATH`` in config.py to this directory
6. You should be good to go!

## How to use it
1. Open ``links.txt``
2. Copy the Imgur *album id* from the url of the albums into the file
![imgur_url](/docs/url.png)
![links_txt](/docs/link_txt.png)
3. Save and close it
4. Run the command "``python imgur_api.py``" from the terminal
5. A folder for each album should have been created
An output example can be found in ``/docs/demo_output``

## Manage your archives
- Each folder is named by its unique Imgur *album id*, and each media by its Imgur *media id*.
- Each folder contains 3 additional files: ``metadata_ID.json``, ``script_ID.json``, ``descriptions_ID.json`` with the *album id* appended
- ``metadata_ID.json`` is a dictionary containing the *id*, *publication date*, *title*, *description*, and *number of media files* of the album.`
![metadata](/docs/metadata.png)
- ``script_ID.json`` is a dictionary with incremental values as keys and *media id* as values
![script](/docs/script.png)
- ``descriptions_ID.json`` is a dictionary with the *media id* as key and its description as value. Note: Imgur always displays the description under the media.
![description](/docs/description.png)
- In the main directory, the file ``scraping_logs.json`` contains a metadata dictionary for each album downloaded. When the script is ran, entries are appended.
![logs](/docs/logs.png)

``scraping_logs.json`` contains the catalog of albums downloaded. It can be consulted to avoid downloading duplicates, and being able to cross-reference Imgur album id and title. For each album folder, ``script_ID.json`` is the reference to rebuild the album in the correct order, and fetch descriptions from ``descriptions_ID.json``. With this architecture, album folders are portable because they contain everything needed to rebuild them.

## Motivation
Initially, I built this tool to save recipes and guides hosted on Imgur and posted on Reddit. In my design, it was important to include both the images and text descriptions from Imgur, and preserve the right order of content. I first created a relational database to store this information (see album_model.py), but then realized a modular structure with self-contained data folders was more portable and appropriate. This lead to the current scheme used.

## What I learned
- REST API (imgur API, python requests)
- writing streams to files