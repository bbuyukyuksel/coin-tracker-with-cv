import json
import os, sys


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
            
        