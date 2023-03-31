import os

path= "/home/wolly/Desktop/WollyRaspberry/img/faces/crazy"

prefix = "wolly"

extension = ".png"

file_names = os.listdir(path)

file_names = [f for f in file_names if f.endswith(extension)]

file_names.sort()

for i,file_name in enumerate(file_names):
    newname = str(i+1)+ extension
    os.rename(os.path.join(path,file_name), os.path.join(path,newname))
    
    
