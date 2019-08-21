from os.path import isfile

class FileManager:
    def __init__(self):
        self.suffix = '-0.txt'
        print("File Manager initialized!")

    def loadable(self):
        gen = 0
        if isfile('data/0'+self.suffix):
            while(isfile('data/'+str(gen)+self.suffix)):
                hasData = isfile('data/'+str(gen)+self.suffix)
                if hasData:
                    gen += 1
            return (True, gen - 1)
        else:
            return (False, 0)