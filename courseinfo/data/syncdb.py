import datetime

open(r'/root/log.txt', 'a').write(str(datetime.datetime.now()) + '\n')
