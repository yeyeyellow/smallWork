'''
用于操作文件
'''
from pathlib import Path
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import yaml
import argparse

SCIPT_NAME = 'main.py'
def load_categoreis_file():
    '''
    加载文件类别配置文件
    '''
    try:
        with open('./config.yaml','r',encoding='utf-8') as f:
            FILE_CATEGORIES = yaml.safe_load(f)
            print('加载成功')
            return FILE_CATEGORIES
    except FileNotFoundError:
        print('找不到文件')
        return {}
    except yaml.YAMLError:
        print('yaml格式错误')
        return {}
def classify(i:Path,FILE_CATEGORIES)-> None:
    """
    按照后缀名分类文件
    """
    if i.name == SCIPT_NAME:
        return
    if i.is_file():
        for k,v in FILE_CATEGORIES.items():
            if i.suffix.lower() in v:
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
                    print(f'moved {i.name} to {categories_path.name}')
                else:
                    shutil.move(i,target)
                    print(f'moved {i.name} to {categories_path.name}')


class MyHandler(FileSystemEventHandler):
    """
    文件监听的回调
    """
    def __init__(self,FILE_CATEGORIES):
        super().__init__()
        self.FILE_CATEGORIES = FILE_CATEGORIES
    def on_created(self, event):
        event_path=Path(event.src_path)
        i=0
        while i<9:
            try:
                classify(event_path,self.FILE_CATEGORIES)
                break
            except PermissionError:
                time.sleep(1)
                i+=1
    def on_moved(self, event):
        event_path = Path(event.dest_path)
        classify(event_path,self.FILE_CATEGORIES)

def main(watching_path,watching_path_str):
    """
    主函数

    args:watching_path(Path) 接受Path类型的对象,watching_path_str(str)
    """
    FILE_CATEGORIES = load_categoreis_file()
    for entry in watching_path.iterdir():
        classify(entry,FILE_CATEGORIES)
    my_handler = MyHandler(FILE_CATEGORIES)
    observer = Observer()
    observer.schedule(my_handler,watching_path_str,recursive=False,)
    observer.start()
    print('开始监听')
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
    parser=argparse.ArgumentParser()
    parser.add_argument('--path',help='请输入你想要监听的文件夹路径',required=True)
    args=parser.parse_args()
    path_str=args.path.strip('"')
    path=Path(path_str)
    main(path,path_str)
