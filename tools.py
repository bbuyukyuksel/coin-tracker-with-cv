import json
import os, sys
import datetime




class JSON():
    @classmethod
    def get(cls, filename):
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    return json.load(f)
            else:
                with open(filename, 'w') as f:
                    pass
                return {}
        except:
            print("Json Error!", sys.exc_info())
            return {}
    
    @classmethod
    def set(cls, filename, obj):
        with open(filename, 'w') as f:
            json.dump(obj, f, indent=3)

class Logging():
    @classmethod
    def write(cls, path, text):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'a+') as f:
            f.write(text + "\n")
    @classmethod
    def success(cls, path, content = ''):
        text = f"# Success : {str(datetime.datetime.now()).split('.')[0]}, {content}" 
        cls.write(path, text)
    
    @classmethod
    def fail(cls, path, content = ''):
        text = f"# Fail    : {str(datetime.datetime.now()).split('.')[0]}, {content}" 
        cls.write(path, text)
    
        