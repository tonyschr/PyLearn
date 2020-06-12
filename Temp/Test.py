import os
 
# specify your path of directory
path = r"C:\Users\saba\Documents"
 
# call listdir() method
# path is a directory of which you want to list
directories = os.listdir( path )
 
# This would print all the files and directories
for file in directories:
   print(file)