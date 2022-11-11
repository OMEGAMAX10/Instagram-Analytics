import os
import json


def get_followers_list(data_folder):
    followers_list = json.load(open(os.path.join(data_folder, 'followers_and_following', 'followers.json')))
    followers_list = [follower['string_list_data'][0] for follower in followers_list["relationships_followers"]]
    followers_list = [{key: val for key, val in follower.items() if key != 'timestamp'} for follower in followers_list]
    return followers_list


def get_followings_list(data_folder):
    followings_list = json.load(open(os.path.join(data_folder, 'followers_and_following', 'following.json')))
    followings_list = [following['string_list_data'][0] for following in followings_list["relationships_following"]]
    followings_list = [{key: val for key, val in following.items() if key != 'timestamp'} for following in followings_list]
    return followings_list


def get_not_following_me_back(followers_list, following_list):
    followers_list_usernames = [follower['value'] for follower in followers_list]
    dont_follow_me = [unfollower for unfollower in following_list if unfollower['value'] not in followers_list_usernames]
    return dont_follow_me


def get_i_dont_follow_back(followers_list, following_list):
    following_list_usernames = [following['value'] for following in following_list]
    i_dont_follow = [unfollowed for unfollowed in followers_list if unfollowed['value'] not in following_list_usernames]
    return i_dont_follow


def get_mutual_followers(followers_list, following_list):
    followers_list_usernames = [follower['value'] for follower in followers_list]
    mutual_followers = [mutual for mutual in following_list if mutual['value'] in followers_list_usernames]
    return mutual_followers


def search_accounts(search_term, account_list):
    return [account for account in account_list if search_term.lower() in account['value'].lower()]
