import os
import secrets
from random import randrange

import redis
from minio import Minio
from minio.error import InvalidResponseError, S3Error
from moviepy.editor import *
from rq import Queue
from rq.job import Job


def watch_queue(queue, redis_conn, client, ext, timeout=30):
    active = True
    print("Watching work queue on extract...")
    while active:
        for job_id in queue.job_ids:
            print(job_id)
            if(job_id=='dead'):
                active = False
                Job.fetch(job_id,redis_conn).cancel() 
                break
            elif(job_id[-1]=='e'):
                try:
                    bucket_name = "vid"
                    file = job_id + ext
                    data = client.get_object(bucket_name, file)
                    dir = job_id
                    os.mkdir(dir)
                    with open(file, "wb") as file_data:
                        for d in data.stream(32 * 1024):
                            file_data.write(d)
                    print("finished wiriting")
                    extract_frames(file, dir)
                    filenames = os.listdir(dir)
                    # print(filenames)
                    filenames = [dir+"/"+f for f in filenames]
                    bucket_name = "images"
                    found = client.bucket_exists(bucket_name)
                    if not found:
                        client.make_bucket(bucket_name)
                    else:
                        print("Bucket already exists")
                    for f in filenames:
                        client.fput_object(
                            bucket_name,
                            # change folder name in response to uploaded id from work queue
                            f,
                            f,
                        )
                        os.remove(f)
                    Job.fetch(job_id,redis_conn).cancel()
                    # cancel_job(job_id)
                    queue.enqueue(randrange, 0, 10, 1, job_id=job_id+"g")
                    print(f"images with job_id ({job_id}) uploaded to images bucket.")

                except InvalidResponseError as err:
                    print(err)
def crange(s,e,step):
    c = s
    while c < e:
        yield c
        c += step

def extract_frames(movie, img_dir):
        clip = VideoFileClip(movie)
        clip.resize(height=360) 
        duration = clip.duration
        # x = 10
        # in_range = crange(30,50,0.5) 
        if duration < 10:
            in_range = crange(0,10,0.25) 
            times = [i for i in in_range]
        elif duration < 40:
            in_range = crange(12,22,0.25) 
            times = [i for i in in_range]
        else:
            start_t = int(duration * 0.66) - 20
            end_t = int(duration * 0.66) + 20
            in_range = crange(start_t,end_t,0.5) 
            times = [i for i in in_range]
        print(len(times))
        for t, i in zip(times, range(1, len(times)+1)):
            img_path = os.path.join("{}.png".format(i))
            clip.save_frame(img_dir + "/" + img_path, t)

def main():
    print("Welcome to extract & resize worker")
    ip = os.environ["IP"]
    client = Minio(
        ip + ":9000",
        access_key="minio",
        secret_key="minio123",
        secure=False,
    )
    redis_conn = redis.Redis(host="redis",port=6379)
    queue = Queue(connection=redis_conn)
    watch_queue(queue,redis_conn,client,".mp4")
        # uploaded id from work queue
        # bucket_name = "vid"
        # found = client.bucket_exists(bucket_name)
        # if not found:
        #     client.make_bucket(bucket_name)
        # else:
        #     print("Bucket already exists")
        # tmp_video = "test.mp4"
        # data = client.get_object(bucket_name, tmp_video)
        # dir = "tmp/"
        # os.mkdir(dir)
        # with open(tmp_video, "wb") as file_data:
        #     for d in data.stream(32 * 1024):
        #         file_data.write(d)
        # print("finished wiriting")

        # extract_frames(tmp_video, dir)
        # filenames = os.listdir(dir)
        # bucket_name = "images"
        # for f in filenames:
        #     client.fput_object(
        #         bucket_name,
        #         # change folder name in response to uploaded id from work queue
        #         dir + f,
        #         dir + f,
        #     )
        #     os.remove(dir + f)
        # print("images uploaded to images bucket.")


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)
