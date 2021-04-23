#I kind of just realized that discord uses two formats for tag strings <@uuid> and <@!uuid>
#this script fixes all old databases by removing "!" from tags

import os, shutil, io, json, roster, trials, member_plus

def fixuid(userid):
    return userid.replace('!', '')


#backup old databases
def backup():
    try:
        shutil.copyfile(member_plus.MEMBERPLUSFILE, member_plus.MEMBERPLUSFILE + ".old")
        shutil.copyfile(trials.TRIALFILE, trials.TRIALFILE + ".old")
        shutil.copyfile(roster.ROSTERFILE, roster.ROSTERFILE + ".old")
        print("return 1")
        return 1
    except Exception as e:
        return -1


def updateuesrid():

    #fix member+ database
    memberpluses = []
    try:
        with io.open(member_plus.MEMBERPLUSFILE, 'r') as plus_file:
            memberpluses = json.load(plus_file)
    except Exception as e:
        print(e)
        return -1

    for dictionary in memberpluses:
        dictionary['userid'] = fixuid(dictionary.get('userid'))

    try:
        with io.open(member_plus.MEMBERPLUSFILE, 'w') as plus_file:
            json.dump(memberpluses, plus_file, ensure_ascii=False)
    except Exception as e:
        print(e)
        return -1


    #fix trials database
    trials_list = []
    try:
        with io.open(trials.TRIALFILE, 'r') as trials_file:
            trials_list = json.load(trials_file)
    except Exception as e:
        print(e)
        return -1

    # renews trial
    for dictionary in trials_list:
        dictionary['userid'] = fixuid(dictionary.get('userid'))

    # updates database
    try:
        with io.open(trials.TRIALFILE, 'w') as trials_file:
            json.dump(trials_list, trials_file, ensure_ascii=False)
    except Exception as e:
        print(e)
        return -1

    #fix roster database
    roster_list = []
    try:
        with io.open(roster.ROSTERFILE, 'r') as roster_file:
            roster_list = json.load(roster_file)
    except Exception as e:
        print(e)
        return -1

    for dictionary in roster_list:
        print(fixuid(dictionary.get('userid')))
        dictionary['userid'] = fixuid(dictionary.get('userid'))
        print(dictionary['userid'])

    try:
        with io.open(roster.ROSTERFILE, 'w') as roster_file:
            json.dump(roster_list, roster_file, ensure_ascii=False)
    except Exception as e:
        print(e)
        return -1

if backup() == -1:
    print("Backup failed, exiting...")
    exit()
else:
    updateuesrid()

