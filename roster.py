#roster management by G_bby
import os, io, json, datetime
ROSTERFILE = "roster.json"

roster = []

def getRoster():
    try:
        with io.open(ROSTERFILE, 'r') as roster_file:
            roster = json.load(roster_file)
    except Exception as e:
        return []
    return roster

def updateRank(userid, rank):
    try:
        with io.open(ROSTERFILE, 'r') as roster_file:
            roster = json.load(roster_file)
    except Exception as e:
        return -1

    found = False
    for person in roster:
        if person.get('userid') == userid:
            person['rank'] = rank
            found = True

    if not found:
        roster.append({'userid':userid, 'name':userid, 'rank':rank, 'youtube':"update your youtube link with $youtube", 'time': datetime.datetime.now().isoformat()})

    try:
        with io.open(ROSTERFILE, 'w') as roster_file:
            json.dump(roster, roster_file, ensure_ascii=False)
    except Exception as e:
        return -2

    return 1

def remove(userid):
    roster = []
    remaining = []

    try:
        with io.open(ROSTERFILE, 'r') as roster_file:
            roster = json.load(roster_file)
    except Exception as e:
        return -1

    for person in roster:
        if person.get('userid') != userid:
            remaining.append(person)

    try:
        with io.open(ROSTERFILE, 'w') as roster_file:
            json.dump(remaining, roster_file, ensure_ascii=False)
    except Exception as e:
        return -2


def updateYouTube(userid, youtube):
    if youtube.__contains__("youtube.com") or youtube.__contains__("youtu.be") or youtube.__contains__("yt.be"):
        try:
            with io.open(ROSTERFILE, 'r') as roster_file:
                roster = json.load(roster_file)
        except Exception as e:
            return -1 #error reading roster file

        found = False
        for person in roster:
            if person.get('userid') == userid:
                person['youtube'] = youtube
                found = True

        if not found:
            return -3 #user not found

        try:
            with io.open(ROSTERFILE, 'w') as roster_file:
                json.dump(roster, roster_file, ensure_ascii=False)
        except Exception as e:
            return -2 #error writing to roster file

        return 1 #success

    else:
        return -4 #not a youtube link

def updateName(userid, name):
    # read roster database
    try:
        with io.open(ROSTERFILE, 'r') as roster_file:
            roster = json.load(roster_file)
    except Exception as e:
        return -1  # error reading roster file

    # updates name
    user = {'userid': 'NOT_FOUND', 'name': 'NOT_SET', 'rank': 'NOT_FOUND', 'youtube': "", 'time': ""}
    exists = 0
    for person in roster:
        if userid == person.get('userid'):
            person['name'] = name
            user = person

    # updates database
    try:
        with io.open(ROSTERFILE, 'w') as roster_file:
            json.dump(roster, roster_file, ensure_ascii=False)
    except Exception as e:
        print("error writing to roster file")

    return user

def getName(userid):
    # read roster database
    try:
        with io.open(ROSTERFILE, 'r') as roster_file:
            roster = json.load(roster_file)
    except Exception as e:
        print("error reading roster file")


    for person in roster:
        if userid == person.get('userid'):
            return person['name']

    return "NOT-FOUND"

def nameTaken(name):
    exit_code = 0

    # read roster database
    try:
        with io.open(ROSTERFILE, 'r') as roster_file:
            roster = json.load(roster_file)
            #checks if name in use
            for person in roster:
                if name.lower() == person.get('name').lower():
                    return 1
            return 0
    except Exception as e:
        return -1


    return exit_code
