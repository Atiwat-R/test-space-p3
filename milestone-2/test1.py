# arr = os.listdir("k8s")
# print(arr)
import os
import sys
from re import X

from minio import Minio
from regex import R

# from minio.error import InvalidResponseError

addr = "127.0.0.1"
client = Minio(
    addr,
    access_key="minio",
    secret_key="minio123",
    secure=False,
)

# bucket_name = sys.argv[1]
# found = client.bucket_exists(bucket_name)
# if not found:
#     client.make_bucket(bucket_name)
# else:
#     print("Bucket already exists")
#     # client.make_bucket(bucket_name)

# # else:
# object = client.list_objects(bucket_name)
# count = 0
# for obj in object:
#     count += 1
# # print(f"total count: {count} (from {bucket_name})")
# f = "cute-cat.mp4"
# client.fput_object(
#     bucket_name,
#     # change folder name in response to uploaded id from work queue
#     "test.mp4",
#     f,
# )
# print("tmp" + ["a", "sd", "d"])
########
# d_ = client.get_object("gif", "test.gif")
# print(d_)
# with open("meow.gif", "wb") as file_data:
#     for d in d_.stream(32 * 1024):
#         file_data.write(d)
#########

# print(len([i for i in in_range]))
# x = 3
# print(len([x * 0.1 for x in range(0, 10)]))
# print(len([p / x for p in range(0, int(x * 10))]))
# data2 =client.get_object("vid", "37cba91ea747e506e.mp4")
# print(data2)
data2 =client.get_object("gif", "5490285327db7e40e.gif")
print(data2)
#
with open("meow.gif", "wb") as file_data:
    for d in data2.stream(32 * 1024):
        file_data.write(d) 
# data2 = client.get_object("vid", "ef17299ddb8c4cc4e.mp4")
# # data = client.get_object("vid", "018e78ac-9491-42d2-846c-3d2eb4f9f6fc.mp4")
# print(data2)
# # # print(d_)
# # print(data)
# print("945ee114db9dd114eg"[:-1])
data = client.list_objects("gif", prefix="37cba91ea747e506e/")
# count = 0
# for _ in data:
#     count += 1
# print(count)

# import secrets

# print(type(secrets.token_hex(8)))
# print(list(range(20, 40, 2)))
# print(str(1) + ".png")


# print(os.listdir("."))
# from minio import Minio
# from minio.error import S3Error


# def main():
#     # print('hi')
#     # while True:
#     # # Create a client with the MinIO server playground, its access key
#     print('hi_')
#     # and secret key.
#     # print(os.environ['IP'])
#     # print(os.environ['IP'])
#     ip = os.environ['IP']

#     # client = Minio(
#     #     "172.0.1.1:9000",
#     #     access_key="mini",
#     #     secret_key="minio123",
#     #     # secure=False,
#     # )
#     client = Minio(
#         ip+":9000",
#         # ip+":9005",
#         # port=9000,
#         access_key="minio",
#         secret_key="minio123",
#         secure=False,
#     )

#     # client.make_bucket("test")
#     # print(client)
#     # buckets = client.list_buckets()
#     # # pri
#     # for bucket in buckets:
#     #     print(bucket.name, bucket.creation_date)
#     # print(client)
#     #
#     # # # Make 'p2' bucket if not exist.
#     bucket_name = "p2vidthumbnail"

#     found = client.bucket_exists(bucket_name)
#     print(found)
#     if not found:
#         client.make_bucket(bucket_name)
#     else:
#         print("Bucket already exists")

#     # Upload '/home/user/Photos/asiaphotos.zip' as object name
#     # 'asiaphotos-2015.zip' to bucket 'p2'.

#     to_be_uploaded_video_path = "./cute-cat.mp4"
#     new_filename = "cat.mp4"

#     client.fput_object(
#         bucket_name, new_filename, to_be_uploaded_video_path,
#     )
#     print(
#         "'/home/user/Photos/asiaphotos.zip' is successfully uploaded as "
#         "object 'asiaphotos-2015.zip' to bucket 'p2'."
#     )


# if __name__ == "__main__":
#     try:
#         main()
#     except S3Error as exc:
#         print("error occurred.", exc)
# def extract_to_frame(video):
#     clip = VideoFileClip(video)
#     duration = clip.duration
#     if duration < 10:
#         frame = clip
#     elif duration < 30:
#         frame = clip.subclip(duration - 10, duration)
#     else:
#         start_t = duration * 0.66
#         end_t = start_t + 10
#         frame = clip.subclip(start_t, end_t)
#     return frame
