from os.path import isfile

class FileManager:
    def __init__(self):
        self.suffix = '-0.txt'
        print("File Manager initialized!")

    def loadable(self):
        gen = 0
        is_loadable = isfile('data/0'+self.suffix)
        while(isfile('data/'+str(gen)+self.suffix)):
            gen += 1
        return (is_loadable, gen - 1)
