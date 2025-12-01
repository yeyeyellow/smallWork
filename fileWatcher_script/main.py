from pathlib import Path
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


scriptName = 'main.py'
FILE_CATEGORIES = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "文档": [".pdf", ".docx", ".doc", ".txt", ".xlsx",'.xls'],
    "安装包": [".exe", ".msi", ".dmg", ".pkg"],
    "压缩包": [".zip", ".rar", ".7z", ".tar"],
    '视频':['.mp4']
}
def classify(i:Path)-> None: 
        if i.name == scriptName:
            return
        if i.is_file():
            for k,v in FILE_CATEGORIES.items():
                if i.suffix in v:
                    CATEGORIES_path = Path(i.parent/k)
                    CATEGORIES_path.mkdir(parents=True,exist_ok=True)
                    target = Path(CATEGORIES_path/i.name)
                    if target.exists():
                        org_name = i.stem
                        suffix = i.suffix
                        index =1
                        while True:
                            new_target_name = f'{org_name}({index}){suffix}'
                            new_target = Path(CATEGORIES_path/new_target_name)
                            if new_target.exists():
                                index+=1
                            else:
                                break
                        shutil.move(i,new_target)
                    else:
                        shutil.move(i,target)

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        event_Path=Path(event.src_path)
        i=0
        while i<9:
            try:
                classify(event_Path)
                break
            except Exception:
                time.sleep(1)
                i+=1
    def on_moved(self, event):
        event_Path=Path(event.dest_path)
        classify(event_Path)

def main(path,path_str):
    for entry in path.iterdir():
        classify(entry)
    myHandler = MyHandler()
    observer = Observer()
    observer.schedule(myHandler,path_str,recursive=False,)
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