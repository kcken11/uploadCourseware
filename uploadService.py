# -*- coding:utf-8 -*-
import this
import oss2
import os.path
import psycopg2
import sys
import countFiles

reload(sys)
sys.setdefaultencoding("utf8")

# pg setting
# conn = psycopg2.connect(database="kkworld", user="kkworld", password="kkworld2015", host="10.0.0.15", port=5432)
# cur = conn.cursor()

confLesson = open("confLesson.sql", mode="w")
courseware = open("courseware.sql", mode="w")
updateConfLesson = open("updateConfLesson.sql", mode="w")


this.temp_level=None

def setAtrr(lessonname):
    sql = "select lesson_id,lesson_level,sub_level from conf_lesson where lesson_name='" + lessonname + "'"
    #print sql
    this.cur.execute(sql)
    row = this.cur.fetchall()
    if (len(row) == 0) :
        #print lessonname
        #print "lesson name is not exist: %s " % lessonname
        return None

    return row[0]


def uploadImg(rootdir,process,total):
    initBucket();
    initConnetDB();
    process.SetRange(total)
    tempkey=0
    tempLessonName=""
    index=0
    for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:
            index=index+1
            if filename.endswith(".jpg") or filename.endswith(".JPG"):

                filepath = os.path.join(parent, filename)

               # print filepath
                params = filepath.split("\\")
                lessonname = params[len(params) - 2]
                grank = filename[0:filename.rindex(".")]
                lesson = setAtrr(lessonname)
                if lesson == None:
                    if lessonname!=tempLessonName:
                        print lessonname
                        tempLessonName=lessonname
                    continue
                file = open(filepath, "rb")
                #filename2 = unicode(filename, "gbk")
               # print grank
                if grank.find("(1)")!=-1 or grank.find("debug")!=-1:
                    continue
                key = "aliyun/lesson/" + str(lesson[1]) + "/" + str(lesson[2]) + "/1/" + grank+".jpg"
                print key
                uploadFile(key, file)
                if grank == '1':
                    confLessonSql = "update conf_lesson set lesson_url='%s' where lesson_id=%s " % (key, lesson[0])
                    confLesson.write(confLessonSql + ";\n")

                coursewareSql = "insert into conf_courseware(lesson_id,cosw_url,adm_id,grank,dtime,lesson_version) values('%s','%s',19,%s,now(),1)" % (
                    lesson[0],key , grank)

                if tempkey!=lesson[0]:
                    tempkey=lesson[0]
                    deleteware=  "delete from conf_courseware where lesson_id= %s;" % tempkey
                    courseware.write(deleteware + "\n")

                # print sql2

                courseware.write(coursewareSql + ";\n")
                process.SetValue(index)
    courseware.close()
    confLesson.close()

def uploadPPT(rootdir,process,total):
    initBucket();
    initConnetDB();
    process.SetRange(total)
    index=0
    for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:
            index = index + 1
            filepath = os.path.join(parent, filename)
            # print "课程name:"+lessonname
            print  filename
            if filename.endswith(".pptx") or filename.endswith(".pdf"):
                lessonname = filename[0:filename.rindex(".")]
                lesson = setAtrr(lessonname)
                if lesson == None:
                    print  "not exist %s " % filepath
                    continue
                file = open(filepath, "rb")
                key = "aliyun/ppt/" + str(lesson[1]) + "/" + str(lesson[2]) + "/1/" + file.name
                #print key
                uploadFile(key, file)
                sql2 = "update conf_lesson set original_lesson_url='%s' where lesson_id= %d " % (key,lesson[0])
               # print sql2
                updateConfLesson.write(sql2 + ";\n")
                process.SetValue(index)
    updateConfLesson.close()

def uploadSingleFile(key,filePath,uploadCallback):
    initBucket();
    initConnetDB();
    file=open(filePath,'rb')
    uploadFile(key,file,uploadCallback)

def initBucket():
    accessKeyId = "6dEKHef6WIaqELi5"
    accessKeySecret = "LE3QTczCIAY01SR7BhiNoFSxEn9zkm"
    auth = oss2.Auth(accessKeyId, accessKeySecret)
    endpoint = 'http://oss-cn-hangzhou.aliyuncs.com'  # 假设Bucket处于杭州区域
    this.bucket = oss2.Bucket(auth, endpoint, 'yanxx')


def initConnetDB():
    this.conn = psycopg2.connect(database="kkworld", user="kkworld", password="kkworld2015", host="10.0.0.15",
                                 port=5432)
    this.cur = this.conn.cursor()


def uploadFile(key, data,uploadCallback):
    this.bucket.put_object(key=key, data=data,progress_callback=uploadCallback)


if __name__ == '__main__':

    uploadImg();
    print "over..."
    confLesson.close()
    courseware.close()
    this.cur.close()
    this.conn.close()
