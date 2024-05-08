import os

try:
    
    os.system('python -m pip install -r utils/requirements.txt --user')
    os.system('python main.py')

    os.mkdir('download_music')
    os.mkdir('download_img')
except FileExistsError:
    pass
except:
    os.system('python -m pip install -r requirements.txt')
    os.system('python ../main.py')