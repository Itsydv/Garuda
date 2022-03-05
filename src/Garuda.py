import json
import sys
import os
import codecs

from instagram_private_api import Client as AppClient
from instagram_private_api import ClientCookieExpiredError, ClientLoginRequiredError, ClientError

from src import printcolors as pc
from src import config


class Garuda:
    api = None
    user_id = None
    target_id = None
    is_private = True
    following = False
    cli_mode = False
    target = ""

    def __init__(self, target, is_cli, clear_cookies):
        u = config.getUsername()
        p = config.getPassword()
        self.clear_cookies(clear_cookies)
        self.cli_mode = is_cli
        if not is_cli:
            print("\nAttempt to login...")
        self.login(u, p)
        self.setTarget(target)

    def clear_cookies(self, clear_cookies):
        if clear_cookies:
            self.clear_cache()

    def setTarget(self, target):
        self.target = target.lower()
        user = self.get_user(target.lower())
        self.target_id = user['id']
        self.is_private = user['is_private']
        self.following = self.check_following()
        self.__printTargetBanner__()

    def __printTargetBanner__(self):
        pc.printout("\nLogged as ", pc.GREEN)
        pc.printout(self.api.username, pc.CYAN)
        pc.printout(". Target: ", pc.GREEN)
        pc.printout(str(self.target), pc.CYAN)
        pc.printout(" [" + str(self.target_id) + "]")
        if self.is_private:
            pc.printout(" [PRIVATE PROFILE]", pc.BLUE)
        if self.following:
            pc.printout(" [FOLLOWING]", pc.GREEN)
        else:
            pc.printout(" [NOT FOLLOWING]", pc.RED)

        print("\n")

    def change_target(self):
        pc.printout("Insert new target username: ", pc.YELLOW)
        line = input()
        self.setTarget(line)
        return

    def get_followers(self):
        if self.check_private_profile():
            return

        pc.printout(f"Searching for {self.target}'s followers...\n")

        _followers = []
        followers = []

        rank_token = AppClient.generate_uuid()
        data = self.api.user_followers(
            str(self.target_id), rank_token=rank_token)

        _followers.extend(data.get('users', []))

        next_max_id = data.get('next_max_id')
        while next_max_id:
            sys.stdout.write("Catched %i followers\n" % len(_followers))
            sys.stdout.flush()
            results = self.api.user_followers(
                str(self.target_id), rank_token=rank_token, max_id=next_max_id)
            _followers.extend(results.get('users', []))
            next_max_id = results.get('next_max_id')

        for user in _followers:
            u = {
                'id': user['pk'],
                'username': user['username'],
                'full_name': user['full_name']
            }
            followers.append(u)

        # json_data = {}
        # followings_list = []

        # for node in followers:
        #     if self.jsonDump:
        #         follow = {
        #             'id': node['id'],
        #             'username': node['username'],
        #             'full_name': node['full_name']
        #         }
        #         followings_list.append(follow)

        # if self.jsonDump:
        #     json_data['followers'] = followers
        #     json_file_name = self.output_dir + "/" + self.target + "_followers.json"
        #     with open(json_file_name, 'w') as f:
        #         json.dump(json_data, f)

        return followers

    def get_followings(self):
        if self.check_private_profile():
            return

        pc.printout(f"Searching for {self.target}'s followings...\n")

        _followings = []
        followings = []

        rank_token = AppClient.generate_uuid()
        data = self.api.user_following(
            str(self.target_id), rank_token=rank_token)

        _followings.extend(data.get('users', []))

        next_max_id = data.get('next_max_id')
        while next_max_id:
            sys.stdout.write("Catched %i followings\n" % len(_followings))
            sys.stdout.flush()
            results = self.api.user_following(
                str(self.target_id), rank_token=rank_token, max_id=next_max_id)
            _followings.extend(results.get('users', []))
            next_max_id = results.get('next_max_id')

        for user in _followings:
            u = {
                'id': user['pk'],
                'username': user['username'],
                'full_name': user['full_name']
            }
            followings.append(u)

        # json_data = {}
        # followings_list = []

        # for node in followings:
        #     if self.jsonDump:
        #         follow = {
        #             'id': node['id'],
        #             'username': node['username'],
        #             'full_name': node['full_name']
        #         }
        #         followings_list.append(follow)

        # if self.jsonDump:
        #     json_data['followings'] = followings_list
        #     json_file_name = self.output_dir + "/" + self.target + "_followings.json"
        #     with open(json_file_name, 'w') as f:
        #         json.dump(json_data, f)

        return followings

    def check_not_following(self):
        response = self.getListOfNotFollowing()

        pc.printout(f"\nTotal results: {len(response)}\n", pc.BLUE)

        for username in response:
            pc.printout(" " + username + " \n", pc.GREEN)

    def getListOf(self, content):
        contentList = []
        if content == "followers":
            content_data = self.get_followers()
        else:
            content_data = self.get_followings()
        for user in content_data:
            contentList.append(user.get("username"))
        return sorted(contentList)

    def getListOfNotFollowing(self):
        followers_target = self.getListOf("followers")
        followings_target = self.getListOf("followings")
        return list(set(followings_target) - set(followers_target))

    def get_user(self, username):
        try:
            content = self.api.username_info(username)
            user = dict()
            user['id'] = content['user']['pk']
            user['is_private'] = content['user']['is_private']

            return user
        except ClientError as e:
            pc.printout('ClientError {0!s} (Code: {1:d}, Response: {2!s})\n'.format(
                e.msg, e.code, e.error_response), pc.RED)
            error = json.loads(e.error_response)
            if 'message' in error:
                print(error['message'])
            if 'error_title' in error:
                print(error['error_title'])
            if 'challenge' in error:
                print("Please follow this link to complete the challenge: " +
                      error['challenge']['url'])
            sys.exit(2)

    def login(self, u, p):
        try:
            settings_file = "config/settings.json"
            if not os.path.isfile(settings_file):
                # settings file does not exist
                print(f'Unable to find file: {settings_file!s}')

                # login new
                self.api = AppClient(auto_patch=True, authenticate=True, username=u, password=p,
                                     on_login=lambda x: self.onlogin_callback(x, settings_file))

            else:
                with open(settings_file) as file_data:
                    cached_settings = json.load(
                        file_data, object_hook=self.from_json)
                # print('Reusing settings: {0!s}'.format(settings_file))

                # reuse auth settings
                self.api = AppClient(
                    username=u, password=p,
                    settings=cached_settings,
                    on_login=lambda x: self.onlogin_callback(x, settings_file))

        except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
            print(f'ClientCookieExpiredError/ClientLoginRequiredError: {e!s}')

            # Login expired
            # Do relogin but use default ua, keys and such
            self.api = AppClient(auto_patch=True, authenticate=True, username=u, password=p,
                                 on_login=lambda x: self.onlogin_callback(x, settings_file))

        except ClientError as e:
            pc.printout('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(
                e.msg, e.code, e.error_response), pc.RED)
            error = json.loads(e.error_response)
            pc.printout(error['message'], pc.RED)
            pc.printout(": ", pc.RED)
            pc.printout(e.msg, pc.RED)
            pc.printout("\n")
            if 'challenge' in error:
                print("Please follow this link to complete the challenge: " +
                      error['challenge']['url'])
            exit(9)

    def to_json(self, python_object):
        if isinstance(python_object, bytes):
            return {'__class__': 'bytes',
                    '__value__': codecs.encode(python_object, 'base64').decode()}
        raise TypeError(repr(python_object) + ' is not JSON serializable')

    def from_json(self, json_object):
        if '__class__' in json_object and json_object['__class__'] == 'bytes':
            return codecs.decode(json_object['__value__'].encode(), 'base64')
        return json_object

    def onlogin_callback(self, api, new_settings_file):
        cache_settings = api.settings
        with open(new_settings_file, 'w') as outfile:
            json.dump(cache_settings, outfile, default=self.to_json)

    def check_following(self):
        if str(self.target_id) == self.api.authenticated_user_id:
            return True
        endpoint = 'users/{user_id!s}/full_detail_info/'.format(
            **{'user_id': self.target_id})
        return self.api._call_api(endpoint)['user_detail']['user']['friendship_status']['following']

    def check_private_profile(self):
        if self.is_private and not self.following:
            pc.printout(
                "Impossible to execute command: user has private profile\n", pc.RED)
            send = input("Do you want send a follow request? [Y/N]: ")
            if send.lower() == "y":
                self.api.friendships_create(self.target_id)
                print(
                    "Sent a follow request to target. Use this command after target accepting the request.")
            return True
        return False

    def clear_cache(self):
        try:
            f = open("config/settings.json", 'w')
            f.write("{}")
            pc.printout("Cache Cleared.\n", pc.GREEN)
        except FileNotFoundError:
            pc.printout("Settings.json don't exist.\n", pc.RED)
        finally:
            f.close()
