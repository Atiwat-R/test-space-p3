import os
import secrets
from random import randrange

import redis
from flask import Flask, jsonify, request
from minio import Minio
from rq import Queue

ip = os.environ["IP"]
client = Minio(
    ip + ":9000",
    access_key="minio",
    secret_key="minio123",
    secure=False,
)
prefix = os.environ['PREFIX']
app = Flask(__name__)
# app.config['APPLICATION_ROOT'] = '/web'
q = Queue(connection=redis.Redis(host="redis", port=6379))

# @app.route(prefix)
@app.route(prefix+'/upload/')
def enqueue():
    if 'url' in request.args:
        if request.args.get('url') == 'dead':
           q.enqueue(randrange, 0, 10, 1, job_id="dead")
           return "Terminate extractor..", 200 
        else:
            bucket_name = "vid"
            found = client.bucket_exists(bucket_name)
            if not found:
                client.make_bucket(bucket_name)
            else:
                print("Bucket already exists")
                # client.make_bucket(bucket_name)
            job_id = secrets.token_hex(8) + "e"
            file = job_id + ".mp4"
            client.fput_object(
                bucket_name,
                # change folder name in response to uploaded id from work queue
                file,
                request.args.get('url'),
            )
            job = q.enqueue(randrange, 0, 10, 1, job_id=job_id)    
            return f"{file} uploaded to Minio", 200
    return "Url required!", 400
@app.route(prefix+"/results")
@app.route(prefix+"/results/<string:job_id>")
def results(job_id=None):

    if job_id is None:
        return jsonify(queued_job_ids=q.job_ids)

    job = q.fetch_job(job_id)

    if job.is_failed:
        return 'Job has failed!', 400

    if job.is_finished:
        return jsonify(result=job.result)

    return 'Job has not finished!', 202

@app.route(prefix+"/kill/<string:job_id>")
def kill(job_id):
    job = q.fetch_job(job_id)

    if job.is_failed:
        return 'Job has failed!', 400

    job.cancel()
    return "Job killed", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
