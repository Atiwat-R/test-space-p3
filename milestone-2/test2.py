from redis import StrictRedis
from rq import Queue

q = Queue(connection=StrictRedis(host="redis", port=6379))


jobs = q.jobs
print(jobs)
