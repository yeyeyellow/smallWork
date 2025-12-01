'''
用于操作文件
'''
from pathlib import Path
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


SCIPT_NAME = 'main.py'
FILE_CATEGORIES = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "文档": [".pdf", ".docx", ".doc", ".txt", ".xlsx",'.xls'],
    "安装包": [".exe", ".msi", ".dmg", ".pkg"],
    "压缩包": [".zip", ".rar", ".7z", ".tar"],
    '视频':['.mp4']
}

def classify(i:Path)-> None:
    """
    按照后缀名分类文件
    """
    if i.name == SCIPT_NAME:
        return
    if i.is_file():
        for k,v in FILE_CATEGORIES.items():
            if i.suffix in v:
                categories_path = Path(i.parent/k)
                categories_path.mkdir(parents=True,exist_ok=True)
                target = Path(categories_path/i.name)
                if target.exists():
                    org_name = i.stem
                    suffix = i.suffix
                    index =1
                    while True:
                        new_target_name = f'{org_name}({index}){suffix}'
                        new_target = Path(categories_path/new_target_name)
                        if new_target.exists():
                            index+=1
                        else:
                            break
                    shutil.move(i,new_target)
                else:
                    shutil.move(i,target)

class MyHandler(FileSystemEventHandler):
    """
    文件监听的回调
    """
    def on_created(self, event):
        event_path=Path(event.src_path)
        i=0
        while i<9:
            try:
                classify(event_path)
                break
            except PermissionError:
                time.sleep(1)
                i+=1
    def on_moved(self, event):
        event_path = Path(event.dest_path)
        classify(event_path)

def main(watching_path,watching_path_str):
    """
    主函数

    args:watching_path(Path) 接受Path类型的对象,watching_path_str(str)
    """
    for entry in watching_path.iterdir():
        classify(entry)
    my_handler = MyHandler()
    observer = Observer()
    observer.schedule(my_handler,watching_path_str,recursive=False,)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    except PermissionError:
        observer.stop()
        time.sleep(3)
        observer.start()
    observer.join()

if __name__ == '__main__':
    path_str =(input('请输入想要监听哪个文件夹:')).strip('"')
    print(f'开始监听文件夹:{path_str}')
    path=Path(path_str)
    main(path,path_str)
