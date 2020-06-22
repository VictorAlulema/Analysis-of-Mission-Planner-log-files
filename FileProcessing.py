from LogFile import Parameters
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np


class LogFileProcessing:
    """
    Provide the filename of the log to be analyzed
    example: '000039.log'
    To instantiate the class, type something like:
    Analysis = LogFileProcessing('000039.log')
    """

    def __init__(self, filename):
        self.file = filename
        self.Params = Parameters.keys()
        self.Data = LogFileProcessing.GetData(self)

    def GetData(self):
        """
        This function does the hard work: Read the log file and
        store the data in a Python dictionary, very convenient to access the
        data. 
        """
        LogFile = open(self.file, 'r')
        for line in LogFile:
            content = line.rstrip().split(',')
            if content[0] in self.Params:
                for key in Parameters[content[0]].keys():
                    index = Parameters[content[0]][key][0]
                    if content[index] == 'NaN':
                        pass
                    else:
                        Parameters[content[0]][key].append(float(content[index]))
            else:
                pass
        LogFile.close()
        return Parameters

    def Subparams(self, Param):
        """
        This function tells you the subparams of a param:
        Example:
        Subparams('BAT')
        Output will be:
           ['Volt','VoltR','Curr','CurrTot','Temp','Res']
        Now, you know what subparams you could plot against the variable Time
        """
        return self.Data[Param].keys()

    def Plot(self, Param, Subparam, logx=False,
             matrix=False, color='k'):
        """
        This functions plots the results
        Just type something like:
        Plot('GPS','Alt')
        That's it!
        """
        # Data
        y = self.Data[Param][Subparam][1:]
        x = np.linspace(0, 100, len(y))
        # Plot settings
        plt.rc('font', family='serif')
        plt.rc('font', size=9)
        plt.rc('axes', labelsize=9)
        fig = plt.figure(figsize=(5, 2.5))
        if matrix:
            # TODO
            pass
        else:
            ax = fig.add_subplot(111)
            if logx:
                ax.semilogx(x, y, 'b-', linewidth=0.75)
            else:
                ax.plot(x, y, 'b-', linewidth=0.75)
            ax.set_xlabel('Time')
            ax.set_ylabel(Param + ' ' + Subparam)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            fig.tight_layout()
            plt.show()


if __name__ == '__main__':
    analysis = LogFileProcessing('00000039.log')
    analysis.Plot('GPS', 'Alt')
    analysis.Plot('GPS', 'Spd')
    analysis.Plot('BARO', 'Alt')
    analysis.Plot('BAT', 'Volt')
    analysis.Plot('POWR', 'VServo')
    # Get data for further analysis
    y = analysis.Data['GPS']['Alt'][1:]  # This is the variable of interest
    x = np.linspace(0, 100, len(y))      # This is the variable Time
