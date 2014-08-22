# coding: utf-8
try:
    import fabfile
except:
    import sys
    print("try 'pip install fabric'")
    sys.exit()

from application import app

def runserver():
    app.run()


