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
    response = []
    for idx, contest in enumerate(contests):
        submissions = cf.contest_status(contest.id, username)
        res = requests.get(url + str(contest.id))
        soup = bs.BeautifulSoup(res.text, 'html.parser')
        no_of_problems = len(soup.find('table', {'class': 'problems'}).find_all('tr')) - 1
        r = [contest.name, contest.id]
        d = {}
        for c in string.ascii_uppercase[:no_of_problems]:
            d[c] = ''
        print(len(submissions))
        for sub in submissions:
            idx = sub.problem.index
            p_type = sub.author.participant_type
            if d[idx] == 'SC': continue
            elif d[idx] == 'SP' and p_type == 'CONTESTANT' and sub.verdict == 'OK':
                d[idx] = 'SC'
            elif d[idx] == 'WA' or d[idx] == '':
                if sub.verdict == 'OK':
                    if p_type == 'CONTESTANT':
                        d[idx] = 'SC'
                    else:
                        d[idx] = 'SP'
                else:
                    d[idx] = 'WA'
        r.append(d)
        response.append(r)
        if idx == 10:
            break
    return render_template('index.html', contests=response)
