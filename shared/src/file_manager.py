from os.path import isfile

class FileManager:

    suffix = '-0.txt'
    
    def loadable(self):
        gen = 0
        is_loadable = isfile('../data/0'+self.suffix)
        while(isfile('../data/'+str(gen)+self.suffix)):
            gen += 1
        return (is_loadable, gen - 1)
