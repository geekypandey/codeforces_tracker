from collections import defaultdict
import operator
import requests
import string
import bs4 as bs
import codeforces_api

from flask import Flask, render_template


app = Flask(__name__)
cf = codeforces_api.CodeforcesApi()


@app.route('/')
def index():
    username = 'geekypandey'
    contests = list(x for x in cf.contest_list() if x.phase=='FINISHED')
    contests.sort(key=lambda x: x.start_time_seconds, reverse=True)
    # contests = [1, 2, 3]
    url = 'https://codeforces.com/contest/'
    user_submissions = cf.user_status(username)
    # grab all the user submissions, loop through them and store them as a map
    u_d = dict()

    for sub in user_submissions:
        p_type = sub.author.participant_type
        key = str(sub.contest_id) + sub.problem.index
        if key not in u_d:
            if sub.verdict == 'OK' and p_type == 'CONTESTANT':
                u_d[key] = 'SC'
            elif sub.verdict == 'OK':
                u_d[key] = 'SP'
            else:
                u_d[key] = 'WA'
        else:
            if u_d[key] == 'SP' and p_type == 'CONTESTANT' and sub.verdict == 'OK':
                u_d[key] = 'SC'
    print(len(u_d))

    problems = cf.problemset_problems()['problems']
    contest_size = defaultdict(int)

    for problem in problems:
        contest_size[problem.contest_id] += 1

    response = []
    for idx, contest in enumerate(contests):
        r = [contest.name, contest.id]
        d = {}
        no_of_problems = contest_size[contest.id]
        for c in string.ascii_uppercase[:no_of_problems]:
            key = str(contest.id) + c
            if key in u_d:
                d[c] = u_d[key]
            else:
                d[c] = ''
        r.append(d)
        response.append(r)
    return render_template('index.html', contests=response)
