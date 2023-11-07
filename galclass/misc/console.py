###########
# Imports #
###########

# System #

import sys
import time
import shutil

# Local #

#############
# Constants #
#############

# Console styles
consoleStyles={'bold':'\033[1m', 'end':'\033[0m', 'red':'\033[91m', 'green':'\033[92m', 'yellow':'\033[93m'}

# Symbols of joblevels
jobSymbol=['+', '-', '>', '*', '=']

###########
# Classes #
###########

#*********#
# Console #
#*********#

class Console:

    # Attributes

    njobs=0
    job=[]
    jobLevel=[]
    jobLineAdvance=[]

    isLineClear=True
    lineLength=shutil.get_terminal_size()[0]

    # Methods

    @staticmethod
    def format(text, styles):

        # Evaluate styles
        stylesArray=styles.split(',')

        # Determine stylePrefix
        stylePrefix=''
        for style in stylesArray:
            stylePrefix=stylePrefix+consoleStyles[style]

        # Return
        return stylePrefix+text+consoleStyles['end']
    
    @staticmethod
    def moveCursorUp(nlines=1):

        # Move cursor up nlines times
        print('\033['+str(nlines)+'A', end='')
        
        # Return
        return
    
    @staticmethod
    def moveCursorDown(nlines=1):

        # Move cursor down nlines times
        print('\033['+str(nlines)+'B', end='')
        
        # Return
        return
    
    @staticmethod
    def moveCursorToBeginningOfLine():

        # Move cursor to beginning of line
        print('\r', end='')
        
        # Return
        return
    
    @staticmethod
    def saveCursorPosition():

        # Save cursor position
        print('\033[s', end='')
        
        # Return
        return
    
    @staticmethod
    def restoreCursorPosition():

        # Restore cursor position
        print('\033[u', end='')
        
        # Return
        return
    
    @staticmethod
    def printNewLine():

        # Print a new line
        print('', end='\n')
        
        # Return
        return
    
    @staticmethod
    def clearToEndOfLine():

        # Clear to end of line
        print('\033[0K', end='')
        
        # Return
        return
    
    @classmethod
    def clearLine(cls):

        # Move cursor to beginning of line
        cls.moveCursorToBeginningOfLine()

        # Clear to end of line
        cls.clearToEndOfLine()

        # Set line status
        cls.isLineClear=True
        
        # Return
        return
    
    @classmethod
    def newLine(cls):

        # Print a new line
        cls.printNewLine()

        # Register the line advance
        cls.registerLineAdvance()

        # Set the line status
        cls.isLineClear=True
        
        # Return
        return

    @classmethod
    def pushJob(cls, job):

        # Print job
        cls.printJob(job, jobLevel=cls.njobs)

        # Push job
        cls.job.append(job)
        cls.jobLevel.append(cls.njobs)
        cls.jobLineAdvance.append(0)
        cls.njobs=cls.njobs+1

        # Return
        return
    
    @classmethod
    def popJob(cls, success=True):

        # Evaluate job status
        if(success):
            jobStatus=1
        else:
            jobStatus=-1
        
        # Save job line advance status
        jobLineAdvance=cls.jobLineAdvance[-1]
        
        if(jobLineAdvance>0):
        
            # Save line status
            isLineClear=cls.isLineClear
        
            # Move cursor up to the job line
            cls.moveCursorUp(cls.jobLineAdvance[-1])
        
        # Set line status
        cls.isLineClear=False

        # Print job
        cls.printJob(cls.job[-1], jobLevel=cls.jobLevel[-1], jobStatus=jobStatus, overwrite=True)
        
        if(jobLineAdvance>0):

            # De-register line advance
            cls.deregisterLineAdvance()

            # Move cursor down to its initial line
            cls.moveCursorDown(cls.jobLineAdvance[-1]-1)

            # Restore line status
            cls.isLineClear=isLineClear

        # Pop job
        cls.job.pop()
        cls.jobLevel.pop()
        cls.jobLineAdvance.pop()
        cls.njobs=cls.njobs-1

        # Return
        return
    
    @classmethod
    def registerLineAdvance(cls):

        # Register line advance
        for ijob in range(cls.njobs):
            cls.jobLineAdvance[ijob]=cls.jobLineAdvance[ijob]+1

        # Return
        return
    
    @classmethod
    def deregisterLineAdvance(cls):

        # De-register line advance
        for ijob in range(cls.njobs):
            cls.jobLineAdvance[ijob]=cls.jobLineAdvance[ijob]-1

        # Return
        return
    
    @classmethod
    def print(cls, text, textType='raw', jobLevel=0, jobStatus=0, overwrite=False):

        # Evaluate text
        textLines=text.splitlines()

        # Determine the typeSymbol
        if(textType=='info'):
            typeSymbol='i'
        elif(textType=='warning'):
            typeSymbol='!'
        elif(textType=='error'):
            typeSymbol='x'
        elif(textType=='job'):
            typeSymbol=jobSymbol[jobLevel]
        
        # Determine the prefix
        prefix=''
        if(textType!='raw'):
            prefix=prefix+'['+typeSymbol+'] '

        # Determine the suffix
        suffix=''
        if(textType=='job'):
            if(jobStatus<0):
                suffix=cls.format('[','bold')+' '+cls.format('failed','bold,red')+' '+cls.format(']','bold')
            elif(jobStatus>0):
                suffix=cls.format('[','bold')+' '+cls.format('ok','bold,green')+' '+cls.format(']','bold')
            else:
                suffix=cls.format('[','bold')+' '+cls.format('running','bold,yellow')+' '+cls.format(']','bold')
        
        # Determine the end
        end='\n'
        if((textType=='raw')or((textType=='job')and(jobStatus==0))):
            end=''
        
        # Get a clear line
        if(not cls.isLineClear):
            if(overwrite):
                # Clear the line
                cls.clearLine()
            else:
                # Get a new line
                cls.newLine()

        # Print text
        for textLine in textLines:

            # Populate the blank space
            if(textType=='job'):
                dummyText=prefix+textLine+suffix
                formatLength=0
                for consoleStyle in consoleStyles.values():
                    formatLength=formatLength+dummyText.count(consoleStyle)*len(consoleStyle)
                blankSpaceLength=cls.lineLength-(len(dummyText)-formatLength)
                blankSpace=' '*blankSpaceLength
            else:
                blankSpace=''
            
            # Print the text
            print(prefix+textLine+blankSpace+suffix, end=end)

            # Register the end line advance
            if(end=='\n'):
                cls.registerLineAdvance()
                cls.isLineClear=True
            else:
                cls.isLineClear=False
        
        # Flush stdout
        sys.stdout.flush()
        
        # Return
        return
    
    @classmethod
    def printRaw(cls, raw, overwrite=False):
        return cls.print(raw, textType='raw', overwrite=overwrite)
    
    @classmethod
    def printInfo(cls, info):
        return cls.print(info, textType='info')
    
    @classmethod
    def printWarning(cls, warning):
        return cls.print(warning, textType='warning')
    
    @classmethod
    def printError(cls, error):
        return cls.print(error, textType='error')
    
    @classmethod
    def printJob(cls, job, jobLevel=0, jobStatus=0, overwrite=False):
        return cls.print(job, textType='job', jobLevel=jobLevel, jobStatus=jobStatus, overwrite=overwrite)

    def __init__(self, total, prefix = '', suffix = '', decimals = 1, length = None, fill = '█', printEnd = "\r", printComplete = "\n"):

        # Save the specified configuration
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.printEnd = printEnd
        self.printComplete = printComplete

        # Determine the length of the progress bar
        if(length is None):
            lineLength=shutil.get_terminal_size()[0]
            self.length=lineLength-len(prefix)-(4+decimals)-len(suffix)-6-16
        
        # Reset the progressBar
        self.reset()
        
        # Return
        return

    def show(self, iteration):

        # Generate the bar
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (iteration / float(self.total)))
        filledLength = int(self.length * iteration // self.total)

        bar = self.fill * filledLength + '-' * (self.length - filledLength)

        # Generate the ETA
        etaInSec=self.computeETA(iteration)
        if(etaInSec is not None):
            hours=etaInSec//3600
            minutes=(etaInSec%3600)//60
            seconds=(etaInSec%3600)%60
            eta = 'ETA: '+f'{hours:02}'+':'+f'{minutes:02}'+':'+f'{seconds:02}'
        else:
            eta = 'ETA: --:--:--'

        # Print the bar
        print(f'\r{self.prefix} |{bar}| {percent}% [{eta}] {self.suffix}', end = self.printEnd)

        # Print printComplete on complete
        if(iteration == self.total):
            print(self.printComplete, end='')

        # Return
        return

    def computeETA(self, iteration):

        if(iteration>0):

            # Compute the elapsed time
            dt=time.time()-self.t0

            # Determine the eta
            eta=int(dt*(float(self.total/iteration)-1.0))
        
        else:

            eta=None

        # Return
        return eta

    def reset(self):

        # Reset t0
        self.t0=time.time()

        # Return
        return