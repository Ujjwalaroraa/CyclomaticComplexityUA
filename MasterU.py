mport requests

from flask import Flask
from flask_restful import Resource, Api, request
from threading import Lock
from collections import deque
from time import time


app = Flask(__name__)
api = Api(app)

JOB_QUEUE = deque()
JOB_QUEUE_LOCK = Lock()
CC = 0
CC_COUNT = 0
CC_LOCK = Lock()
COMMIT_LIST_URL = 'https://api.github.com/repos/Manik459/Chat_SocketP/commits'
FILES_LIST_URL = 'https://api.github.com/repos/Manik459/Chat_SocketP/git/trees/{}'
TOTAL_COMMITS = 0
TOTAL_WORKERS = 0
TOTAL_WORKERS_LOCK = Lock()


class Master(Resource):
    '''
    Master issues Workers with commit SHA's for a given repo
    and accepts the average CC of a commit from Workers
    '''

    def get(self):
        global JOB_QUEUE
        global JOB_QUEUE_LOCK

        with JOB_QUEUE_LOCK:
            try:
                return {'sha': JOB_QUEUE.popleft()}

            except IndexError:
                return '', 204

    def put(self):
        global CC
        global CC_COUNT
        global CC_LOCK
        global TOTAL_COMMITS

        new_cc = float(request.form['cc'])
        with CC_LOCK:
            CC += new_cc
            CC_COUNT += 1
            if CC_COUNT == TOTAL_COMMITS:
                shutdown_server()
                return '', 503

        return '', 204


class NodeSetup(Resource):
    ''' Issues newly instantiated Workers with a URL to access commits '''

    def get(self):
        global TOTAL_WORKERS
        global TOTAL_WORKERS_LOCK
        global FILES_LIST_URL

        print('New node joined')
        with TOTAL_WORKERS_LOCK:
            TOTAL_WORKERS += 1
        return {'url': FILES_LIST_URL}


def get_commits():
    '''
    Retrieves SHA's for every commit in my Internet Apps Chat Server repository that has 56 commits
    and 7 python files, and fills the Job Queue
    '''
    global COMMIT_LIST_URL
    global JOB_QUEUE

    with open('github-token', 'r') as f:
        token = f.read().split()[0]
        payload = {'access_token': token}

    resp = requests.get(COMMIT_LIST_URL, params=payload)

    # Repositories with more than 30 commits are pagianated
    # and require additional requests
    while 'next' in resp.links:
        for item in resp.json():
            JOB_QUEUE.append(item['sha'])

        resp = requests.get(resp.links['next']['url'], params=payload)

    print(resp.json())
    for item in resp.json():
        JOB_QUEUE.append(item['sha'])


def calc_avg_cc():
    ''' Calculate and print the average cyclomatic complexity for the repository '''
    global CC

    print('-----AVG CC: {0:0.2f}-----'.format(CC / CC_COUNT))


def shutdown_server():
    ''' Snippet from flask-restful docs to shutdown a flask server '''

    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


api.add_resource(Master, '/')
api.add_resource(NodeSetup, '/init')

if __name__ == '__main__':
    get_commits()
    TOTAL_COMMITS = len(JOB_QUEUE)
    start = time()
    app.run(host='0.0.0.0', port=4000, debug=False)
    end = time()
    delta = end - start
    print('Workers used: {}'.format(TOTAL_WORKERS))
    print('Time elapsed: {0:0.2f}s'.format(delta))
    print('\n-----Shutting Down Server-----')
    calc_avg_cc()
    with open('results.txt', 'a') as results:
        results.write('Workers: {}\nTime: {}\n'.format(TOTAL_WORKERS, delta))
