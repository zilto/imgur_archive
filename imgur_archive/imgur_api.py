import os
import json
import requests

from config import AUTH, STORAGE_DIRPATH, LOGS_FILEPATH


def _get_album_list(filename):
    filepath = os.path.join(STORAGE_DIRPATH, filename)
    with open(filepath, "r") as f:
        return f.read().splitlines()


def _create_dir(path, dir_name):
    # creates output folder if it does not exist
    path = os.path.join(path, dir_name)
    try:
        os.makedirs(path)
    except:
        pass
    return path


def _request_response(request, url):
    "Compose response"
    response = {}
    response['url'] = url
    response['status'] = request.status_code
    if request.status_code == 200:
        response['response'] = request.json()
    else:
        response['response'] = request
    return response


def get_album(album_id):
    url = f"https://api.imgur.com/3/album/{album_id}"
    headers = {"authorization": f"Bearer {AUTH['access_token']}"}
    request = requests.get(url, headers=headers, timeout=1)
    response = _request_response(request, url)
    album_data = response["response"]["data"]
    return album_data


def save_album(album_data):
    album_path = _create_dir(STORAGE_DIRPATH, album_data["id"])
    
    save_album_metadata(album_path, album_data)
    save_album_script(album_path, album_data)
    save_album_media(album_path, album_data)
    save_album_text(album_path, album_data)


def save_album_script(album_path, album_data):
    script = {count:media["id"] for count, media in enumerate(album_data["images"])}
    
    script_filepath = os.path.join(album_path, f"script_{album_data['id']}.json")
    with open(script_filepath, "w") as f:
        f.write(json.dumps(script))


def save_album_metadata(album_path, album_data):
    metadata_tags = ["id", "datetime", "title", "description"]
    metadata = {k:album_data[k] for k in metadata_tags}
    metadata["n_media"] = len(album_data["images"])
    
    local_logs_filepath = os.path.join(album_path, f"metadata_{album_data['id']}.json")
    with open(local_logs_filepath, "w") as f:
        f.write(json.dumps(metadata))
    
    with open(LOGS_FILEPATH, "a") as f:
        f.write("\n")
        f.write(json.dumps(metadata))


def save_album_media(album_path, album_data):
    def _save_media(album_path, media_data):
        _format = {
            "image/jpeg": "jpg",
            "image/png": "png",
            "image/gif": "mp4",
            "video/mp4": "mp4"
        }
        
        extension = _format[media_data["type"]]
        if extension == "mp4":
            media_stream = requests.get(media_data["mp4"], stream=True, timeout=1)
        else:
            media_stream = requests.get(media_data["link"], stream=True)
            
        filename = f"/{media_data['id']}.{extension}"
        filepath = album_path + filename
        with open(filepath, "wb") as f:
            for chunk in media_stream.iter_content(chunk_size=1024):
                f.write(chunk)
    
    for media_data in album_data["images"]:
        _save_media(album_path, media_data)
            

def save_album_text(album_path, album_data):
    descriptions_dict = {media["id"]:media["description"] for media in album_data["images"]}
    descriptions_filepath = os.path.join(album_path, f"descriptions_{album_data['id']}.json")
    with open(descriptions_filepath, "a") as f:
        f.write(json.dumps(descriptions_dict))
        

def main():
    ids = _get_album_list("links.txt")
    for i in ids:
        album_data = get_album(i)
        save_album(album_data)
    

if __name__ == "__main__":
    main()