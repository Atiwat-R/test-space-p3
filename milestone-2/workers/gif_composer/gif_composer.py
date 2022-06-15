import os

import moviepy.video.io.ImageSequenceClip
import redis
from minio import Minio
from minio.error import InvalidResponseError, S3Error
from rq import Queue
from rq.job import Job


def watch_queue(queue, redis_conn, client, ext, timeout=30):
    active = True
    while active:
        for job_id in queue.job_ids: 
            if(job_id[-1]=='g'):
                try:
                    bucket_name = "images"
                    dir = job_id[:-1]
                    os.mkdir(dir)
                    for i in range(1, 41):
                        print(i)
                        path = dir + "/" + str(i) + ".png"
                        # print(path)
                        data = client.get_object(bucket_name, path)
                        with open(path, "wb") as file_data:
                            for d in data.stream(32 * 1024):
                                file_data.write(d)
                    print("finished writing")
                    # still constant due to size of frame (40)
                    images = sorted(os.listdir(dir))
                    print(images)
                    images = [dir + "/" + s for s in images]
                    gif_name = dir+ ext
                    bucket_name = "gif"
                    found = client.bucket_exists(bucket_name)
                    if not found:
                        client.make_bucket(bucket_name)
                    else:
                        print("Bucket already exists")
                    gif_composer(10, gif_name, images)
                    client.fput_object(
                        bucket_name,
                        gif_name,
                        gif_name,
                    )
                    Job.fetch(job_id,redis_conn).cancel()
                    print("finished composing")
                except InvalidResponseError as err:
                    print(err)

def gif_composer(fps, gif_name, images):
    movie_clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(images, fps)
    movie_clip.write_gif(gif_name)

def main():
    ip = os.environ["IP"]   

    client = Minio(
        ip + ":9000",
        access_key="minio",
        secret_key="minio123",
        secure=False,
    )
    redis_conn = redis.Redis(host="redis",port=6379)
    queue = Queue(connection=redis_conn)
    watch_queue(queue,redis_conn,client,".gif")


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)
