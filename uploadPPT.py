# coding=utf-8
import this
import oss2
import os.path
import psycopg2
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
accessKeyId = "LTAIzMumvziQwhk6"
accessKeySecret = "drWYRiZM19vAL254kkwkmBgVseM8iR"
auth = oss2.Auth(accessKeyId, accessKeySecret)
endpoint = 'http://oss-cn-hangzhou.aliyuncs.com'  # 假设Bucket处于杭州区域
bucket = oss2.Bucket(auth, endpoint, 'kkworld')

# service=oss2.Service(auth,endpoint)

# pg setting
conn = psycopg2.connect(database="kkworld", user="kkworld", password="kkworld2015", host="10.0.0.15", port=5432)
cur = conn.cursor()

sqltext = open("updateConfLesson.txt", mode="w")



def uploadPPT(rootdir):
    for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:
            filepath = os.path.join(parent, filename)
            # print "课程name:"+lessonname
            print  filename
            if filename.endswith(".pptx") or filename.endswith(".pdf"):

                lessonname = filename[0:filename.rindex(".")]

                sql = "select lesson_id,lesson_level,sub_level from conf_lesson where lesson_name='" + lessonname + "'"
                cur.execute(sql)
                row = cur.fetchall()
                if (len(row) == 0):
                    print  "not exist %s " % filepath
                    continue
                for r in row:
                    this.lessonId = r[0]
                    this.lessonlevel = r[1]
                    this.sublevel = r[2]
                filepath = unicode(filepath, "gbk")
                file = open(filepath, "rb")
                filename2 = unicode(filename, "gbk")
                key = "aliyun/ppt/" + str(this.lessonlevel) + "/" + str(this.sublevel) + "/1/" + filename2
                print key
                bucket.put_object(key=key, data=file)

                sql2 = "update conf_lesson set original_lesson_url='%s' where lesson_id= %d " % (key,this.lessonId)
               # print sql2
                sqltext.write(sql2 + ";\n")
            # cur.execute(sql2)

print "over..."
sqltext.close()
cur.close()
conn.close()
