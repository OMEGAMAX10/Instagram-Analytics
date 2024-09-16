import os
import json


def get_personal_info(data_folder):
    personal_info = json.load(open(os.path.join(data_folder, 'personal_information', 'personal_information', 'personal_information.json')))['profile_user'][0]
    username = personal_info["string_map_data"]['Username']["value"]
    full_name = personal_info["string_map_data"]['Name']["value"]
    profile_picture_uri = os.path.join(data_folder, personal_info['media_map_data']['Profile Photo']["uri"])
    return username, full_name, profile_picture_uri