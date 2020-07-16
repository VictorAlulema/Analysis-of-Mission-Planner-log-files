from LogFile import Parameters
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import cm
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
        i = 0
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
            i = i + 1
        LogFile.close()
        print('Read {} lines '.format(i))
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


    def Plot(self,Param=None,Subparam=None,
             logx=False,logy=False,
             matrix=False,FigureSize=None):
        """
        This functions plots the results
        Just type something like:
        Plot('GPS','Alt')
        That's it!
        """
        # Data
        y = self.Data[Param][Subparam][1:]
        x = np.linspace(0, 30, len(y))
        if FigureSize:
            pass
        else:
            FigureSize = [5,2.5]
        fig, ax = LogFileProcessing.Plot_config(self,FigureSize)
        if matrix:
            # TODO
            pass
        else:
            if logx:
                ax.semilogx(x, y, 'b-', linewidth=0.75)
            if logy:
                ax.semilogy(x, y, 'b-', linewidth=0.75)
            else:
                ax.plot(x, y, 'b-', linewidth=0.75)
            ax.set_xlabel('Time')
            ax.set_ylabel(Param + ' ' + Subparam)
        fig.tight_layout()
        plt.show()
        
            
    def Plot_config(self,FigureSize):
        plt.rc('font', family='serif')
        plt.rc('font', size=9)
        plt.rc('axes', labelsize=9)
        fig = plt.figure(figsize=(FigureSize[0],FigureSize[1]))
        ax = fig.add_subplot(111)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        return fig, ax

    
    def PlotDemo(self,X,Y,FigureSize=[5,2.5]):
        fig, ax = fig, ax = LogFileProcessing.Plot_config(self,FigureSize)
        ax.plot(X,Y, 'b-', linewidth=0.75)
        ax.set_xlabel('Time [min]')
        ax.set_ylabel('Power [W]')
        fig.tight_layout()
        plt.show()

    def PieChart(self,labels,sizes):
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.show()


# Let's analyze the flight data

if __name__ == '__main__':    
    analysis = LogFileProcessing('00000104.log')
    analysis.Plot(Param='GPS',Subparam='Alt')
    analysis.Plot(Param='GPS',Subparam='Spd')
    analysis.Plot(Param='BARO',Subparam='Alt')
    analysis.Plot(Param='BAT',Subparam='Volt')
    analysis.Plot(Param='POWR',Subparam='VServo')
    analysis.Plot(Param='BAT',Subparam='CurrTot')
    
    # Get data for further analysis
    Voltage = analysis.Data['BAT']['Volt'][1:]       # This is the variable of interest
    Current = analysis.Data['BAT']['Curr'][1:]
    Power = np.array([Voltage[i] * Current[i] for i in range(len(Voltage))])
    # PowerCruise = Power[np.where(Power > 50)]
    time = np.linspace(0, 30, len(Power))      # This is the variable Time
    analysis.PlotDemo(time,Power)
    
    # 3D Plot of flight data
    latitude = analysis.Data['GPS']['Lat'][1:]
    longitude = analysis.Data['GPS']['Lng'][1:]
    altitude = analysis.Data['GPS']['Alt'][1:]
    fig = plt.figure(figsize=(8,6))
    ax = plt.subplot(111, projection='3d')
    ax.xaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('white')
    ax.yaxis.pane.fill = False
    ax.yaxis.pane.set_edgecolor('white')
    ax.zaxis.pane.fill = False
    ax.zaxis.pane.set_edgecolor('white')
    ax.grid(False)
    ax.plot(latitude, longitude, altitude)
    New_Power = []
    m = 0
    for i in range(0,int(len(Power)/2)-1):
        New_Power.append(Power[m])
        m = m + 2
    size = [100 * power / max(New_Power)  for power in New_Power]
    s = ax.scatter(latitude, longitude, altitude ,
                   s = size, marker = 'o' , c = New_Power,
                   cmap = cm.jet, linewidths = 0.025,
                   edgecolors = 'k') 
    c_bar = fig.colorbar(s, ax = ax)
    plt.show()

    # Just to check the new Power have the same behaviour of the original data due to the resampling
    t1 = np.linspace(0,30,len(Power))
    plt.plot(t1, Power)
    t2 = np.linspace(0,30,len(New_Power))
    plt.plot(t2,New_Power)
    plt.show()

    # Power breackdown respect to flight time
    CurrTot = analysis.Data['BAT']['CurrTot'][1:]
    # mAh consumed during take-off
    mAh_TakeOff = CurrTot[(np.where(Power == max(Power)))[0][0]]
    t_TakeOff = time[np.where(Power == max(Power))][0]

    # mAh consumed during cruise (i.e. during the mission)
    # t = 27 ===> time when the UAV starts descending
    mAh_cruise = CurrTot[(np.where(time >= 27))[0][0]] - mAh_TakeOff
    t_cruise = time[(np.where(time >= 27))[0][0]] - t_TakeOff

    # mAh consumed during landing
    mAh_landing =  CurrTot[-1] - mAh_cruise - mAh_TakeOff
    t_landing = time[-1] - t_cruise - t_TakeOff

    Cumulative_Current = max(CurrTot)
    # Let's see the results

    # First, let's see the fractions of mAhs consumed during each flight phase respect to
    # the total of mAhs consumed
    
    f_TakeOff =  mAh_TakeOff / Cumulative_Current
    f_Cruise = mAh_cruise / Cumulative_Current
    f_Landing = mAh_landing / Cumulative_Current
    
    labels = ['Takeoff', 'Cruise', 'Landing']
    sizes = [f_TakeOff, f_Cruise, f_Landing]
    analysis.PieChart(labels, sizes)

    # Now, let'se see the fractions respect to the battery capacity\
    Bat_Capacity = 8000
    f_TakeOff =  mAh_TakeOff / Bat_Capacity
    f_Cruise = mAh_cruise / Bat_Capacity
    f_Landing = mAh_landing / Bat_Capacity
    f_Remaining = (Bat_Capacity - Cumulative_Current) / Bat_Capacity

    labels = ['Takeoff', 'Cruise', 'Landing', 'Remaining']
    sizes = [f_TakeOff, f_Cruise, f_Landing, f_Remaining]
    analysis.PieChart(labels, sizes)
    
    
