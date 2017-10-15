#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import oss2
import glob
# 首先初始化AccessKeyId、AccessKeySecret、Endpoint等信息。
# 通过环境变量获取，或者把诸如“<你的AccessKeyId>”替换成真实的AccessKeyId等。
#
# 以杭州区域为例，Endpoint可以是：
#   http://oss-cn-hangzhou.aliyuncs.com
#   https://oss-cn-hangzhou.aliyuncs.com
# 分别以HTTP、HTTPS协议访问。

access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', '6dEKHef6WIaqELi5')
access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', 'LE3QTczCIAY01SR7BhiNoFSxEn9zkm')
bucket_name = os.getenv('OSS_TEST_BUCKET', 'yanxx')
endpoint = os.getenv('OSS_TEST_ENDPOINT', 'http://oss-cn-hangzhou.aliyuncs.com')


# 确认上面的参数都填写正确了
for param in (access_key_id, access_key_secret, bucket_name, endpoint):
    assert '<' not in param, '请设置参数：' + param


# 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

#bucket.put_object("aliyun/test/video/a.txt",'a.txt')


def uploadVideo(foder_name):
    print 'upload video  filepath ：%s' % foder_name
    os.chdir(foder_name)
    filepath=str(foder_name)
    paths=filepath.split('\\')
    l=len(paths)
    outputpath=paths[l-2]+'/'+paths[l-1]
    child_env = os.environ.copy()
    all_uid_file = glob.glob("uid_*.txt")

    for uid_file in all_uid_file:
        uid = os.path.splitext(uid_file)[0][4:]
        uid = uid[0:uid.rindex('_')]
        print uid
        if os.path.exists(uid+".mp4"):
            print 'video file is exist'
            videofile=filepath+"/%s.mp4" %uid
            bucket.put_object_from_file("aliyun/kkvideo/%s/%s.mp4" %(outputpath,uid),videofile)
            print ' %s.mp4 upload done' % uid

def uploadVideoByParts(foder_name):
    print 'upload video by parts filepath ：%s' % foder_name
    os.chdir(foder_name)
    filepath = str(foder_name)
    paths = filepath.split('\\')
    l = len(paths)
    outputpath = paths[l - 2] + '/' + paths[l - 1]
    child_env = os.environ.copy()
    all_uid_file = glob.glob("uid_*.txt")
    for uid_file in all_uid_file:
        uid = os.path.splitext(uid_file)[0][4:]
        uid = uid[0:uid.rindex('_')]
        print uid
        if os.path.exists(uid+".mp4"):
            key="aliyun/kkvideo/%s/%s.mp4" %(outputpath,uid)
            videofile = filepath + "/%s.mp4" % uid
            total_size = os.path.getsize(videofile)
            part_size = oss2.determine_part_size(total_size, preferred_size=128 * 1024)

            # 初始化分片上传，得到Upload ID。接下来的接口都要用到这个Upload ID。
            upload_id = bucket.init_multipart_upload(key).upload_id

            # 逐个上传分片
            # 其中oss2.SizedFileAdapter()把fileobj转换为一个新的文件对象，新的文件对象可读的长度等于num_to_upload
            with open(videofile, 'rb') as fileobj:
                parts = []
                part_number = 1
                offset = 0
                while offset < total_size:
                    num_to_upload = min(part_size, total_size - offset)
                    result = bucket.upload_part(key, upload_id, part_number,
                                                oss2.SizedFileAdapter(fileobj, num_to_upload))
                    parts.append(oss2.models.PartInfo(part_number, result.etag))

                    offset += num_to_upload
                    part_number += 1

                # 完成分片上传
                bucket.complete_multipart_upload(key, upload_id, parts)
                print ' %s.mp4 upload done' % uid