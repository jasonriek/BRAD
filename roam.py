import json
import sys

from logger import Logger
from roam_calls import *


rout = Logger()

def main(feed=None):
    try:
        if feed:
            feed = json.load(feed)
        else:
            feed = {'test': 'This is test data!'}
        start.run(inputs=feed, logger=rout)

    except Exception:
        print(traceback.format_exc())
    rout.show()
    rout.writeToFile()
    sys.stdout.flush()


if __name__ == '__main__':
    main() # main(sys.stdin) w/ cat feed.json | python3 roam.py
    drone.endThreads()