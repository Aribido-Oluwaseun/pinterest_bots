from constant import *

def get_fields(_first=False, _last=False, _id=False, _url=False, _image=False,
                _type=False, _bio=False, _username=False, _note=False,
                _created_at=False, _count=False, _name=False,
                _description=False, _creator=False, _link=False,
                _board=False, _color=False, _media=False,
                _attribution=False, _metadata=False,
                _user_all=False, _board_all=False, _pin_all=False):
    field = []
    field_string = ""
    if _id or _user_all or _board_all or _pin_all:
        field.append(ID)
    if _username or _user_all:
        field.append(USERNAME)
    if _first or _user_all:
        field.append(FIRST)
    if _last or _user_all:
        field.append(LAST)
    if _bio or _user_all:
        field.append(BIO)
    if _created_at or _user_all or _board_all or _pin_all:
        field.append(CREATED)
    if _count or _user_all or _board_all or _pin_all:
        field.append(COUNT)
    if _image or _user_all or _board_all or _pin_all:
        field.append(IMAGE)
    if _url or _board_all or _pin_all:
        field.append(URL)
    if _type:
        field.append(ACC_TYPE)
    if _note or _pin_all:
        field.append(NOTE)
    if _name or _board_all:
        field.append(NAME)
    if _description or _board_all:
        field.append(DESCRIPTION)
    if _creator or _board_all or _pin_all:
        field.append(CREATOR)
    if _link or _pin_all:
        field.append(LINK)
    if _board or _pin_all:
        field.append("board")
    if _color or _pin_all:
        field.append(COLOR)
    if _media or _pin_all:
        field.append(MEDIA)
    if _attribution or _pin_all:
        field.append(ATTRIBUTION)
    if _metadata or _pin_all:
        field.append(METADATA)

    size = len(field)
    if size == 0:
        return None

    for i in range(size - 1):
        field_string += field[i] + ","
    field_string += field[-1]
    return field_string

def get_board_name(username, board_name):
    return "{}/{}".format(username,board_name)
