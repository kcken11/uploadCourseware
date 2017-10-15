#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import oss2
import sys

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


def uploadFile(key,filepath,callback):
    bucket.put_object_from_file(key, filepath,progress_callback=callback)


def uploadCallBack(bytes_consumed,total_bytes):
     percent=float(bytes_consumed)*100/float(total_bytes)
     return "上传进度%.2f" % percent,'%'


if __name__=='__main__':
    print 'upload file'
    uploadFile("a/b/ppt.zip","ppt.zip")