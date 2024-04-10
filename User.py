import json

class User:
    def __init__(self, file='user.json'):
        self.file = file
        self.data = self.load_json()
        self.is_connected = self.data['is_connected']

    def load_json(self):
        try :
            with open(self.file, 'r') as f:
                return json.load(f)
        except:
            with open(self.file, 'w') as f:
                json.dump({'is_connected': False}, f)
            return {'is_connected': False}
        
    def save_json(self):
        try:
            with open(self.file, 'w') as f:
                json.dump(self.data, f)
        except:
            print('Error saving data')