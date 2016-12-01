"""
This group of API queries follower data on Pinterest and stores them
"""
from pinterest_api import Pinterest
from bot_accounts import Account
import requests as req
from constant import *
from helper import *
import os

class PinterestUserError(Exception):
    "Define Class Exceptions"

class API(object):
    def __init__(self, _token=None):
        if not _token:
            raise PinterestUserError("Token Not found. Check if account was added!")
        self._token = _token

    def get_my_likes(self):
        request_link = ''.join([PINTEREST_URL,ME, LIKE, '?access_token=',
                        self._token, '&limit=100'])
        return req.get(request_link)

    def get_user_likes(self, username):
        request_link = ''.join([PINTEREST_URL, username,'/', LIKE,
                                '?access_token=',
                        self._token, '&limit=100'])
        return  req.get(request_link)

    def get_current_followers(self, username=None, cursor=None):
        payload = {TOKEN: self._token, CURSOR: cursor}
        request_link = PINTEREST_URL + ME + FOLLOWER
        return req.get(request_link, params=payload)

    def get_user_boards(self, username, cursor=None):
        field = get_fields(_image=True, _attribution=True)
        payload = {TOKEN: self._token, FIELDS: field, CURSOR: cursor}
        request_link = OTHER_USER_URL + USER + username + '/' + PIN
        return req.get(request_link, params=payload)

    def get_any_pin_info(self, pin_id):
        request_link = ''.join([PINTEREST_URL,PIN,pin_id,'/',
                                '?access_token=',self._token,'&limit=100'])
        return req.get(request_link)

    def get_board_pins(self, username, boardname, url=None):
        if url is not None:
            request_link = url
        else:
            request_link = ''.join([PINTEREST_URL, BOARD, username, '/',
                                boardname, '/', PIN, '?access_token=',
                                self._token, '&limit=100'])
        return req.get(request_link)


    def get_my_board(self, cursor=None):
        payload = {TOKEN: self._token, CURSOR: cursor}
        request_link = PINTEREST_URL + ME + FOLLOW + INTEREST
        return req.get(request_link, params=payload)

    def get_user_following(self, cursor=None):
        payload = {TOKEN: self.token, CURSOR: cursor}
        request_link = PINTEREST_URL + ME + FOLLOW + USER
        return req.get(request_link, params=payload)


    # get user to follow a specific board given username and board name
    def follow_board(self, username, board_name):
        board = get_board_name(username, board_name)
        data = {BOARD_DATA: board}
        payload = {TOKEN: self._token}
        request_link = PINTEREST_URL + ME + FOLLOW + BOARD
        return req.post(request_link, params=payload, data=data)

    # get user to follow a specific user given username
    def follow_user(self, username):
        data = {USER_DATA: username}
        payload = {TOKEN: self._token}
        request_link = PINTEREST_URL + ME + FOLLOW + USER
        return req.post(request_link, params=payload, data=data)

    # get user's likes
    def get_my_likes(self, cursor=None):
        field = get_fields()
        payload = {TOKEN: self._token, FIELDS: field, CURSOR: cursor}
        request_link = PINTEREST_URL + ME + LIKE
        return req.get(request_link, params=payload)