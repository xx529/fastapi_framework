import sys
import os
sys.path.append(os.getcwd())

from server import FastApiServer

myapp = FastApiServer(version='0.0.1').create_app()
