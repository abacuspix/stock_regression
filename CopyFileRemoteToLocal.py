import shutil
import datetime
from datetime import datetime

start = datetime.now()

#Copy the file
print ("copy etf.db")
original1 = r'z:\stock\etf.db'
target1 = r'c:\stock\etf.db'
delta = datetime.now() - start
shutil.copyfile(original1, target1)
print("etf file transfer elapsed time in seconds", delta.seconds)
#Copy the file
print ("copy stock.db")
original2 = r'z:\stock\stock.db'
target2 = r'c:\stock\stock.db'

shutil.copyfile(original2, target2)

delta = datetime.now() - start
print("all file transfer elapsed time in seconds", delta.seconds)