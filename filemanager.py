from os.path import isfile

class FileManager:
    def __init__(self):
        self.suffix = '-0.txt'
        print("File Manager initialized!")

    # Determines whether there is existing genome data saved as txt files (located in the data folder)
    def loadable(self):
        gen = 0                                                 # Starts loadable generation at 0
        if isfile('data/0'+self.suffix):                        # Check to see if data/0-0.txt exists
            while(isfile('data/'+str(gen)+self.suffix)):        # Iterate until we get to a generation that is not in the files
                hasData = isfile('data/'+str(gen)+self.suffix)  # Get a boolean value as to whether data/gen-0.txt exits
                if hasData:                                     # Check hasData to increment generation if true
                    gen += 1                                    # Increase generation by 1
            return (True, gen - 1)                              # Return True, and the highest generation that exists
        else:
            return (False, 0)                                   # Return False, saying that the genome data files need to be created
