from constant import *
from helper import *
import requests as req
from time import time
import datetime
import calendar
from pinterest_user_api import API
import json
import os
from tables import *
import argparse

DATABASE_FILE = 'pinterest7.h5'
TOKEN = 'AeMGKOZMmMuG4f-v7T4sPezjpULfFHTir30Y5TFDaA0cR-AsNQAAAAA'
FILE = 'pinterest_data.xlsx'

class  Error(Exception):
    "Define Common Errors"




class GetData(object):

    def __init__(self):
        """Initializes class attributes."""
        self.api = API(TOKEN)
        self.followers = {}
        self.total_pins = 0
        self.pin_data = {}
        self.count = 0

    def get_my_followers(self):
        """This method gets followers.

        This method calls the get followers api and returns a list of all
        followers: URL, ID, Last name and First name. It then checks the list of
        followers and updates it if new followers were added to the list.

        :return: updated class object followers
        """
        raw = self.api.get_current_followers()
        content = json.loads(raw.content)
        followers = {}
        for i in range(len(content['data'])):
            followers[str(content['data'][i]['url'][26:-1])]= {
                'first_name': content['data'][i]['first_name'],
                'last_name': content['data'][i]['last_name'], 'id':
                    content['data'][i]['id']}
        return followers

    def update_followers(self):
        followers = self.get_current_followers()
        for i in followers:
            if i not in self.followers:
                self.followers.update(followers)
        return self.followers

    def get_follower_boards(self, username):
        """This method gets all boards and their IDs given their username.

        :param username: username of one of the followers
        :return: boards and their id, pin count, repin_count, follower_count,
         owner_url and description
        """
        boards = {}
        raw = self.api.get_user_boards(username)
        cursor = len(username) + 2
        raw_json = json.loads(raw.content)
        pins = len(raw_json['data']['pins'])
        for i in range(pins):
            boards[raw_json['data']['pins'][i]['board']['url'][cursor:-1]] = {
                   'time': raw_json['generated_at'],
                   'id':raw_json['data']['pins'][i]['board']['id'],
                   'pin_count':raw_json['data']['pins'][i]['board'][
                       'pin_count'],
                    'follower_count':raw_json['data']['pins'][i]['board'][
                        'follower_count'],
                    'repin_count':raw_json['data']['pins'][i][
                        'repin_count'],
                    'owner_url': raw_json['data']['pins'][i]['pinner'][
                        'profile_url'],
                    'description': raw_json['data']['pins'][i]['board'][
                        'description']}
        return boards

    def get_board_pins(self, username, boardname, URL=None):
        """
        This method gets all the pins of a board if the boardname is given

        :param username: username of the user
        :param boardname: boardname for a user
        :param URL: next page Url
        :return: data saved from the page
        """
        username = username
        boardname = boardname
        URL = URL
        raw = self.api.get_board_pins(username, boardname, URL)
        pin_data = {}
        raw_json = json.loads(raw.content)
        total_pins = len(raw_json['data'])
        for i in range(total_pins):
            pin_data[raw_json['data'][i]['url'][30:-1]]  = {'note':
                                                                    raw_json[
                                                                'data'][i][
                'note'], 'link':raw_json['data'][i]['link']
                                                            }
        self.pin_data.update(pin_data)
        next_page_url = str(raw_json['page']['next'])

        if next_page_url != 'None':
            self.get_board_pins(username, boardname, URL=next_page_url)
        else:
            return self.pin_data

    def get_pin_data(self, pin_id):
        raw = self.api.get_any_pin_info(pin_id)
        raw_json = json.loads(raw.content)
        formatted_pin_string = [raw_json['data']['id'], raw_json['data'][
            'url'], raw_json['data']['note'], raw_json['data']['link']]
        return formatted_pin_string

    def get_my_boards(self):
        raw = self.api.get_user_interest()
        raw_json = json.loads(raw.content)
        return raw_json

    def get_my_likes(self):
        raw = self.api.get_my_likes()
        raw_json = json.loads(raw.content)
        return raw_json

class PinTable(IsDescription):
    pin_id = StringCol(50)
    url    = StringCol(500)
    note   = StringCol(500)
    link   = StringCol(500)

class BoardProperty(IsDescription):
    description    = StringCol(100)
    follower_count = UInt16Col()
    board_id       = StringCol(100)
    owner_url      = StringCol(100)
    pin_count      = UInt16Col()
    time           = StringCol(50)
    repin_count    = UInt16Col()
    mod_name       = StringCol(50)  # filled with original board name if the
    # board name was modified to fit table storage needs.


class DataBase(object):
    def __init__(self, table_name, data=None):
        self.table_name = table_name
        self.data = data
        self.root_follower = {}
        self.follower_board = {}
        self.board_pin = {}
        self.mod_table_name = None

    def cmdline(self):
        parser = argparse.ArgumentParser(description='CMD for Pytables')
        parser.add_argument('-t', '--table-name', required=True, default=False,
                            dest='table_name', help='insert table name')
        input = parser.parse_args()
        return input.table_name

    def check_table_name(self, table_name):
        if os.path.isfile(table_name):
            raise OSError('database file already exists')
        if not table_name.endswith('.h5'):
            raise NameError('table file name should end with .h5')
        return table_name

    def create_database(self):
        table = self.check_table_name(self.table_name)
        database_file = open_file(table, mode='w',
                                  title='Pinterest Data File')
        for follower in self.data:
            self.root_follower[follower] = database_file.create_group('/',
                                                                   follower,
                                                                      follower)
            for board in self.data[follower]:

                path = ''.join(['/', follower])
                table_property = 'prop_' + board        # Store table properties
                table_name = 'tab_'+board               # store table name
                if '/' in table_name:
                    self.mod_table_name = table_name
                    table_name.replace('/', '_')
                if '/' in table_property:
                    table_property.replace('/', '_')
                self.follower_board[table_property] = database_file.create_table(
                    where=path, name=table_property, description=BoardProperty,
                title=table_property)
                self.follower_board[board] = database_file.create_table(
                    where=path, name=table_name, description=PinTable,
                    title=table_name)
        database_file.close()
        return database_file

    def save_all_data_into_database(self,follower, board, pin):
        table_path = ''.join('/', follower, board)
        database_file = open_file(self.table_name, 'a')
        database_path = database_file.get_node(table_path)
        row = database_path.row
        for _ in len(self.data[follower][board]):
            row['pin_id']  = pin[0]
            row['url']     = pin[1]
            row['note']    = pin[2]
            row['link']    = pin[3]

class RunForever(object):

    def __init__(self):
        """
        Please note that duration should be in minutes
        :param update_step:
        :param duration:
        """
        self.database = None
        self.get_data = GetData()
        current_time = datetime.datetime.utcnow()
        # get stop time in epoch format
        self.end_time =  None

    def crawl_and_save(self):
        board = {}
        self.database = DataBase(table_name=DATABASE_FILE, data=board)
        follower = self.get_data.get_my_followers()
        for each_follower in follower:
            board[each_follower] = self.get_data.get_follower_boards(each_follower)
        self.board = board

        # Create Database and Boards
        database_file = self.database.create_database()

        return database_file
        # if not os.path.isfile(DATABASE_FILE):
        # self.database.create_database()

    def run_forever(self):
        # Get all my followers
        pass
        # Save them to database

def main():
    run = RunForever()
    data = run.crawl_and_save()
    print data

if __name__ == '__main__':
    main()