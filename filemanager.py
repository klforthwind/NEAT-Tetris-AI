from os.path import isfile

class FileManager:
    def __init__(self):
        self.suffix = '-0.txt'
        print("File Manager initialized!")

    def loadable(self):
        gen = 0
        isLoadable = isfile('data/0'+self.suffix)
        while(isfile('data/'+str(gen)+self.suffix)):
            gen += 1
        return (isLoadable, gen - 1)
