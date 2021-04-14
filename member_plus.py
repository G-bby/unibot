#memberplus social management by G_bby
import os, io, json, datetime

MEMBERPLUSFILE = "memberpluses.json"

memberpluses = []

def newMemberPlus(userid):
    exit_code = 1
    # -2 write error
    # -1 read error
    # 0 memberplus not found
    # 1 memberplus added

    #read memberplus database
    try:
        with io.open(MEMBERPLUSFILE, 'r') as plus_file:
            memberpluses = json.load(plus_file)
    except Exception as e:
        return -1

    #check if memberplus exists
    plusexists = False
    for dictionary in memberpluses:
        if userid == dictionary.get('userid'):
            plusexists = True

    #adds new memberplus
    if not plusexists:
        dateofplus = datetime.datetime.now()
        memberpluses.append({'userid':userid, 'name': userid, 'dateofplus':dateofplus.isoformat(), 'socials':""})
    else:
        exit_code = 0

    #updates database
    try:
        with io.open(MEMBERPLUSFILE, 'w') as plus_file:
            json.dump(memberpluses, plus_file, ensure_ascii=False)
    except Exception as e:
        return -2

    return exit_code

def getMemberPlus(userid):
    # read memberplus database
    try:
        with io.open(MEMBERPLUSFILE, 'r') as plus_file:
            memberpluses = json.load(plus_file)
    except Exception as e:
        print("error reading member plus")

    # renews memberplus
    memberplus = {"userid": "NOT_FOUND", 'name': "NOT_SET", "dateofplus": "NOT_FOUND", "socials": ""}
    plusexists = 0
    for dictionary in memberpluses:
        if userid == dictionary.get('userid'):
            memberplus = dictionary

    # updates database
    try:
        with io.open(MEMBERPLUSFILE, 'w') as plus_file:
            json.dump(memberpluses, plus_file, ensure_ascii=False)
    except Exception as e:
        print("error writing to member plus file")
    return memberplus

def updateSocials(userid, socials):
    # read memberplus database
    try:
        with io.open(MEMBERPLUSFILE, 'r') as plus_file:
            memberpluses = json.load(plus_file)
    except Exception as e:
        print("error reading member plus file")

    # updates socials
    memberplus = {"userid": "NOT_FOUND", 'name': "NOT_SET", "dateofplus": "NOT_FOUND", "socials": ""}
    plusexists = 0
    for dictionary in memberpluses:
        if userid == dictionary.get('userid'):
            dictionary['socials'] = socials
            memberplus = dictionary

    # updates database
    try:
        with io.open(MEMBERPLUSFILE, 'w') as plus_file:
            json.dump(memberpluses, plus_file, ensure_ascii=False)
    except Exception as e:
        print("error writing to member plus file")

    return memberplus

def updateName(userid, name):
    # read memberplus database
    try:
        with io.open(MEMBERPLUSFILE, 'r') as plus_file:
            memberpluses = json.load(plus_file)
    except Exception as e:
        print("error reading member plus file")

    # updates name
    memberplus = {"userid": "NOT_FOUND", 'name': "NOT_SET", "dateofplus": "NOT_FOUND", "socials": ""}
    plusexists = 0
    for dictionary in memberpluses:
        if userid == dictionary.get('userid'):
            dictionary['name'] = name
            memberplus = dictionary

    # updates database
    try:
        with io.open(MEMBERPLUSFILE, 'w') as plus_file:
            json.dump(memberpluses, plus_file, ensure_ascii=False)
    except Exception as e:
        print("error writing to member plus file")

    return memberplus

def getSocials(name):
    # read memberplus database
    try:
        with io.open(MEMBERPLUSFILE, 'r') as plus_file:
            memberpluses = json.load(plus_file)
    except Exception as e:
        print("error reading member plus file")

    # updates name
    memberplus = {"userid": "NOT_FOUND", 'name': "NOT_SET", "dateofplus": "NOT_FOUND", "socials": ""}
    plusexists = 0
    for dictionary in memberpluses:
        if name.lower() == dictionary.get('name').lower():
            memberplus = dictionary

    # updates database
    try:
        with io.open(MEMBERPLUSFILE, 'w') as plus_file:
            json.dump(memberpluses, plus_file, ensure_ascii=False)
    except Exception as e:
        print("error writing to member plus file")

    return memberplus['socials']

def removeMemberPlus(userid):
    exit_code = 0
    # -2 write error
    # -1 read error
    # 0 memberplus not found
    # 1 memberplus removed

    #list of remaining memberpluses
    remaining = []

    # read memberplus database
    try:
        with io.open(MEMBERPLUSFILE, 'r') as plus_file:
            memberpluses = json.load(plus_file)
    except Exception as e:
        return -1

    #renews memberplus
    for dictionary in memberpluses:
        if userid != dictionary.get('userid'):
            remaing.append(dictionary)
        else:
            exit_code = 1

    #updates database
    try:
        with io.open(MEMBERPLUSFILE, 'w') as plus_file:
            json.dump(remaining, plus_file, ensure_ascii=False)
    except Exception as e:
        return -2
    return exit_code

def nameTaken(name):
    exit_code = 0

    # read memberplus database
    try:
        with io.open(MEMBERPLUSFILE, 'r') as plus_file:
            memberpluses = json.load(plus_file)
            #checks if name in use
            for dictionary in memberpluses:
                if name.lower() == dictionary.get('name').lower():
                    return 1
            return 0
    except Exception as e:
        return -1


    return exit_code
