print('欢迎来到测试场地')
print('--------------------------')
#从下面开始编写代码
import os
def search(path,fileName):
    fileList = os.listdir(path)
    if len(fileList)>0:
        for name in fileList:
            if '.' not in name:
                side_path = os.path.join(path,name)
                search(side_path,fileName)
            elif fileName in name:
                print(name)
                file_path = os.path.join(path,name)
                print(file_path)
    else:
        return

if __name__ =="__main__":
    path = '.'
    flieName = 'r'
    search(path,flieName)
