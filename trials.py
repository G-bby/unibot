#trial expiration management by G_bby
import os, io, json, datetime

TRIALTIME = datetime.timedelta(days=30)
TRIALFILE = "trials.json"

trials = []

def newTrial(userid):
    exit_code = 1
    # -2 write error
    # -1 read error
    # 0 trial not found
    # 1 trial renewed

    #read trial database
    try:
        with io.open(TRIALFILE, 'r') as trials_file:
            trials = json.load(trials_file)
    except Exception as e:
        return -1

    #check if trial exists
    trialexists = False
    for dictionary in trials:
        if userid == dictionary.get('userid'):
            trialexists = True

    #adds new trial
    if not trialexists:
        dateoftrial = datetime.datetime.now()
        expiration = datetime.datetime.now() + TRIALTIME

        trials.append({'userid':userid, 'dateoftrial':dateoftrial.isoformat(), 'expiration':expiration.isoformat()})
    else:
        exit_code = 0

    #updates database
    try:
        with io.open(TRIALFILE, 'w') as trials_file:
            json.dump(trials, trials_file, ensure_ascii=False)
    except Exception as e:
        return -2

    return exit_code

def renewTrial(userid):
    exit_code = 1
    # -2 write error
    # -1 read error
    # 0 trial not found
    # 1 trial renewed

    # read trial database
    try:
        with io.open(TRIALFILE, 'r') as trials_file:
            trials = json.load(trials_file)
    except Exception as e:
        return -1

    #renews trial
    trialexists = 0
    for dictionary in trials:
        if userid == dictionary.get('userid'):
            dictionary['dateoftrial'] = datetime.datetime.now().isoformat()
            dictionary['expiration'] = (datetime.datetime.now() + TRIALTIME).isoformat()
            trialexists = 1

    exit_code = trialexists
    #updates database
    try:
        with io.open(TRIALFILE, 'w') as trials_file:
            json.dump(trials, trials_file, ensure_ascii=False)
    except Exception as e:
        return -2
    return exit_code

def getTrial(userid):

    # read trial database
    try:
        with io.open(TRIALFILE, 'r') as trials_file:
            trials = json.load(trials_file)
    except Exception as e:
        print("error reading trial")

    # renews trial
    trial = {"userid": "NOT_FOUND", "dateoftrial": "NOT_FOUND", "expiration": "NOT_FOUND"}
    trialexists = 0
    for dictionary in trials:
        if userid == dictionary.get('userid'):
            trial = dictionary

    # updates database
    try:
        with io.open(TRIALFILE, 'w') as trials_file:
            json.dump(trials, trials_file, ensure_ascii=False)
    except Exception as e:
        print("error writing to trial file")
    return trial

def purgeTrials():
    #list of purged trials
    expired = []

    #list of remaining trials
    remaining = []

    # read trial database
    try:
        with io.open(TRIALFILE, 'r') as trials_file:
            trials = json.load(trials_file)
    except Exception as e:
        print("error reading trial")

    #removes expired trials
    for dictionary in trials:
        if datetime.datetime.now() >= datetime.datetime.strptime(dictionary['expiration'], "%Y-%m-%dT%H:%M:%S.%f"):
            expired.append(dictionary)
        else:
            remaining.append(dictionary)

    # updates database
    try:
        with io.open(TRIALFILE, 'w') as trials_file:
            json.dump(remaining, trials_file, ensure_ascii=False)
    except Exception as e:
        print("error writing to trial file")

    return expired



