import requests
import os
import shutil
import re
# "邓小平爷爷植树", "mda-jdhjbb36a3xtft3s"
# "开满鲜花的小路", "mda-idtxx52mgg44d33q"
# "找春天", "mda-ieggwi5sw55svpy9"
# "古诗两首", "mda-jdupxkse9ysti4n0"
# "雷锋叔叔你在哪", "mda-ieswq30pdzpktv64"
lesson_name = "雷锋叔叔你在哪"
menu_name = 'mda-ieswq30pdzpktv64'
# 创建课时目录
lesson_dir=os.path.join(os.path.dirname(os.path.abspath("__file__")),lesson_name)
if not os.path.exists(lesson_dir):
    os.mkdir(lesson_dir)
    print ("目录初始化完成")
else:
    print ("目录已初始化")
menu_file = os.path.join(lesson_dir,'{}.m3u8'.format(menu_name))

def load(menu_file):
    file_names=[]
    print ("menu file: ",menu_file)
    fin = open(menu_file, 'r', encoding='UTF-8')
    for line in fin.readlines():
        # print (line)
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue
        # print (line)
        file_names.append(line)
    fin.close()
    return file_names

def download(menu_name,menu_file,lesson_dir):
    host = 'hknm5s6gzvm5a6wju24.exp.bcevod.com'
    uri='http://{}/{}'.format(host,menu_name)

    file_names=load(menu_file)

    file_count=0
    for file_name in file_names:
        url = "{}/{}".format(uri,file_name)
        file=os.path.join(lesson_dir,file_name)
        # print (url)
        # print (file)
        r = requests.get(url)
        with open(file,"wb") as f:
            f.write(r.content)
        print (file_name,"下载完毕")
        file_count+=1
    print ("下载完毕: ", "期望下载 =",len(file_names),"实际下载 =",file_count)

def merge(menu_file,lesson_dir):
    merge_dir=os.path.join(lesson_dir,'merge')
    if not os.path.exists(merge_dir):
        os.mkdir(merge_dir)
        print("合并目录初始化完成")
    else:
        print("合并目录已存在")
    file_names=load(menu_file)
    print("读取ts文件",len(file_names))
    file_copy_count=0
    file_exist_count=0
    for file_name in file_names:
        file_source=os.path.join(lesson_dir,file_name)
        # print(matched)
        file_target=os.path.join(merge_dir,re.search(r'\d+\.ts',file_name,re.I).group().rjust(6,'0'))
        # print("源文件",file_source,"目标文件",file_target)
        if not os.path.exists(file_target):
            shutil.copyfile(file_source,file_target)
            print(file_target,"拷贝完毕")
            file_copy_count+=1
        else:
            print(file_target,"已存在")
            file_exist_count+=1
    print("拷贝完成:","期望拷贝 =",len(file_names),"实际拷贝 =",file_copy_count,"实际存在 =",file_exist_count)
    # 执行merge命令
    # 打开cmd, 执行命令 copy /b *.ts merged.ts
    
# 1. 下载
download(menu_name,menu_file,lesson_dir)
# 2. h二饼
merge(menu_file,lesson_dir)
    

