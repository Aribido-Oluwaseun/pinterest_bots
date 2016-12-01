from pinterest_api import Pinterest
from bot_accounts import Account
import requests as req
import argparse

class BotError(Exception):
    "Define Bot Exceptions"


class Bot(object):
    """To Do
    make this class print information for all number of bots used
    For now, print info for the first user only for a start
    """

    def __init__(self, number_of_bots=None, bot_token=None):
        if not number_of_bots:
            raise BotError("Enter at least 1 bot account")

        self.selected_token = None
        self.number_of_bots = number_of_bots
        self.all_accounts = Account().get_accounts()

        if int(self.number_of_bots) > len(self.all_accounts):
            raise BotError("Number of Bots Accounts defined (%s) is less than "
                        "number requested (%s)" % (len(self.all_accounts)))
        self.all_usernames = [users for users in self.all_accounts]

        if bot_token is not None:
            self.selected_token = [bot_token]
        else:
            self.selected_token = [self.all_accounts[usernames] for usernames
                                   in self.all_usernames]

    def initialize_bots(self):
        return [Pinterest(token) for token in self.selected_token]

class Run(object):

    def _parse_cmdline(self):
        parser = argparse.ArgumentParser(description='Interactive cmd line '
                                                     'for Pinterest')
        parser.add_argument('-n', '--number-of-bots', required=True, default=False,
                            dest='number_of_bots', help='number of bots to '
                                                        'spin')
        parser.add_argument('-B', '--specify-board-name', default=False,
                            dest='specify_board_name', help='enter a board name'
                                                       'e.g: to post a pin on')
        parser.add_argument('-N', '--note', dest='note', help='note to '
                                                              'include with a post')
        parser.add_argument('-a', '--api-key', default=False,
                            dest='api_key', help='Specify API Key')
        parser.add_argument('-f', '--follow', default=False, dest='follow',
                            help='Specify user to follow')
        parser.add_argument('-o', '--get-followers', default=False,
                            dest='get_followers', help='get all followers')
        parser.add_argument('-u', '--un-follow', default=False,
                            dest='un_follow', help='un-follow a user')
        parser.add_argument('-U','--user', default=False,
                            dest='user', help='specify a specific user to '
                                                           'take action with')
        parser.add_argument('-b', '--board', default=False, dest='follow_board',
                            help='follow a board')
        parser.add_argument('-g', '--get-pin', default=False, dest='get_pin',
                            help='get pin')
        parser.add_argument('-p', '--post-pin', default=False, dest='post_pin',
                            help='post a pin')
        parser.add_argument('-r', '--remove-pin', default=False,
                            dest='remove_pin', help='remove a pin')
        parser.add_argument('-O', '--get-other-user-pins', default=False,
							dest='get_other_user_pins', help='get total pins'
                                                            'for another user')
        return parser.parse_args()

    def _call_function(self, parser):

        self.number_of_bots = parser.number_of_bots
        if not parser.api_key:
            self._api_key = None
        else:
            self._api_key = parser.api_key

        if not parser.follow:
            self._follow = None
        else:
            self._follow = parser.follow

        if not parser.note:
            self._note = None
        else:
            self._note = parser.note

        if not parser.specify_board_name:
            self._board_name = None
        else:
            self._board_name = parser.specify_board_name

        if not parser.get_followers:
            self._get_followers = None
        else:
            self._get_followers = parser.get_followers

        if not parser.un_follow:
            self._un_follow = None
        else:
            self._un_follow = parser.un_follow

        if not parser.user:
            self._user = None
        else:
            self._user = parser.user

        if not parser.follow_board:
            self._follow_board = None
        else:
            self._follow_board = parser.follow_board

        if not parser.get_pin:
            self._get_pin = None
        else:
            self._get_pin = parser.get_pin

        if not parser.post_pin:
            self._post_pin = None
        else:
            self._post_pin = parser.post_pin

        if not parser.remove_pin:
            self._remove_pin = None
        else:
            self._remove_pin = parser.remove_pin

        if not parser.get_other_user_pins:
            self._get_other_user_pins = None
        else:
            self._get_other_user_pins = parser.get_other_user_pins



    def execute(self):
        parser = self._parse_cmdline()
        self._call_function(parser)
        if self._api_key:
            bot = Bot(self.number_of_bots, self._api_key)
        else:
            bot = Bot(self.number_of_bots)
        pinterest = bot.initialize_bots()[0] # returns a number of pinterest
        # objects for now, we use only one of them
        # To Do: Make all bot accounts usable at the same time

        if self._follow:
            follow = pinterest.follow_user(self._follow)
            print "\nAttempting to follow %s..." % (self._follow)
            print follow.content

        if self._get_followers:
            followers = pinterest.get_user_follower(self._get_followers)
            print "\n%s has the following followers ..." % (self._get_followers)
            print followers.content

        if self._un_follow:
            unfollow = pinterest.unfollow_user(self._un_follow)
            print "\nAttempting to unfollow %s..." % (self._un_follow)
            print unfollow.content

        if self._follow_board:
            if self._user is not None:
                follow_board = pinterest.follow_board(self._user,
                                                      self._follow_board)
                print "\n Attempting to follow user %s on board: %s" % (
                    self._user, self._follow_board)
                print follow_board.content
            else:
                raise BotError("Error attempting to follow a board while "
                               "board owner is not specified")
		
        if self._get_other_user_pins:
            other_people_follower = pinterest.get_other_user_pins(
                str(self._get_other_user_pins))
            print "/nAttempting to fetch follower information for %s" % (
                self._get_other_user_pins)
            print other_people_follower.content

        if self._get_pin:
            pin = pinterest.get_pin(self._get_pin)
            print "/nAttempting to get pin: %s" % (self._get_pin)
            print pin.content

        if self._post_pin:
            if not (self._user and self._board_name and self._note):
                raise BotError("\nEnter -U to specify username for board "
                                 "owner, -B to specify the board name and -N "
                               "to enter a note" )
            else:
                pin = pinterest.post_pin(self._user, self._board_name,
                                         self._note, image_url=self._post_pin)
                print pin.content


def main():
    run = Run()
    run.execute()

if __name__ == "__main__":
    main()