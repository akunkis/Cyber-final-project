import logging
import Recorder
import os
import sys
import multiprocessing


script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# Set the script directory as the working directory
os.chdir(script_dir)

logging.basicConfig(filename='app.log', level=logging.DEBUG)
logging.info("Setting logging")

if __name__ == '__main__':
    # Pyinstaller fix
    multiprocessing.freeze_support()
    logging.info("started Recorder.main()")
    Recorder.main()



