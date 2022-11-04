import json


def get_not_following_me_back(followers_list, following_list, print_output=True):
    followers_list_usernames = [follower['value'] for follower in followers_list]
    dont_follow_me = [unfollower for unfollower in following_list if unfollower['value'] not in followers_list_usernames]
    if print_output:
        print("\nThese people don't follow you back:")
        for unfollower in dont_follow_me:
            print(json.dumps(unfollower, indent=2))
    return dont_follow_me


def get_i_dont_follow_back(followers_list, following_list, print_output=True):
    following_list_usernames = [following['value'] for following in following_list]
    i_dont_follow = [unfollowed for unfollowed in followers_list if unfollowed['value'] not in following_list_usernames]
    if print_output:
        print("\nThese people you don't follow back:")
        for unfollowed in i_dont_follow:
            print(json.dumps(unfollowed, indent=2))
    return i_dont_follow


def get_mutual_followers(followers_list, following_list, print_output=True):
    followers_list_usernames = [follower['value'] for follower in followers_list]
    mutual_followers = [mutual for mutual in following_list if mutual['value'] in followers_list_usernames]
    if print_output:
        print("\nThese people follow you back:")
        for mutual in mutual_followers:
            print(json.dumps(mutual, indent=2))
    return mutual_followers


def search_followers(followers_list, search_term):
    search_term = search_term.lower()
    search_results = [follower for follower in followers_list if search_term in follower['value'].lower()]
    print("\nSearch results for '{}':".format(search_term))
    for result in search_results:
        print(json.dumps(result, indent=2))
    return search_results


followers_list = json.load(open('data/followers_and_following/followers.json'))
followers_list = [follower['string_list_data'][0] for follower in followers_list["relationships_followers"]]
followers_list = [{key: val for key, val in follower.items() if key != 'timestamp'} for follower in followers_list]

following_list = json.load(open('data/followers_and_following/following.json'))
following_list = [following['string_list_data'][0] for following in following_list["relationships_following"]]
following_list = [{key: val for key, val in following.items() if key != 'timestamp'} for following in following_list]

print("Get followers info")
print(f"Number of followers: {len(followers_list)}")
print(f"Number of following: {len(following_list)}")
print("1. Get people who don't follow you back")
print("2. Get people you don't follow back")
print("3. Get mutual followers")
print("4. Search followers")
print("5. Search following")
print("q. Quit")
option = 0
while option != 'q':
    option = input("Choose an option: ")
    if option == '1':
        dont_follow_me = get_not_following_me_back(followers_list, following_list)
        print(f"Number of people who don't follow you back: {len(dont_follow_me)}")
    elif option == '2':
        i_dont_follow = get_i_dont_follow_back(followers_list, following_list)
        print(f"Number of people you don't follow back: {len(i_dont_follow)}")
    elif option == '3':
        mutual_followers = get_mutual_followers(followers_list, following_list)
        print(f"Number of mutual followers: {len(mutual_followers)}")
    elif option == '4':
        search_term = input("Enter search term: ")
        search_results = search_followers(followers_list, search_term)
        print(f"Number of search results: {len(search_results)}")
    elif option == '5':
        search_term = input("Enter search term: ")
        search_results = search_followers(following_list, search_term)
        print(f"Number of search results: {len(search_results)}")
    elif option == 'q':
        print("Bye!")
    else:
        print("Invalid option")
