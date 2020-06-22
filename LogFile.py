author = 'Victor Alulema'
"""
Data processing of log files
(Pixhawk log files - recorded through MissionPlanner)

Processing strategy: the log file will be read line by line.
For each line we are retrieving the data for the keys defined in the dictionary
defined below. In the following dictionary, the pre-defined numerical values represent
the index of the value in their corresponding row.

The parameters FMT, MODE, MESSAGE, PARM, ORGN and STRT have been omitted from the analysis, since
they do not contribute with data.
"""

Parameters = {'GPS': {'Ail': [2], 'Elev': [3], 'Thr': [4], 'Rudd': [5], 'Flap': [6]},
              'AOA': {'AOA': [2], 'SSA': [3]},
              'ARSP': {'Airspeed': [2], 'DiffPress': [3], 'Temp': [4], 'RawPress': [5],
                       'Offset': [6], 'U': [7]},
              'ATT': {'DesRoll': [2], 'Roll': [3], 'DesPitch': [4], 'Pitch': [5], 'DesYaw': [6],
                      'Yaw': [7], 'ErrRP': [8], 'ErrYaw': [9]},
              'BARO': {'Alt': [2], 'Press': [3], 'Temp': [4], 'CRt': [5], 'SMS': [6],
                       'Offset': [7], 'GndTemp': [8]},
              'BAT': {'Volt': [2], 'VoltR': [3], 'Curr': [4], 'CurrTot': [5], 'Temp': [6], 'Res': [7]},
              'CAM': {'GPSTime': [2], 'GPSWeek': [3], 'Lat': [4], 'Lng': [5], 'Alt': [6], 'RelAlt': [7],
                      'GPSAlt': [8], 'Roll': [9], 'Pitch': [10], 'Yaw': [11]},
              'CMD': {'CTot': [2], 'CNum': [3], 'Cld': [4], 'Prm1': [5], 'Prm2': [6], 'Prm3': [7],
                      'Prm4': [8], 'Lat': [9], 'Lng': [10], 'Alt': [11]},
              'CTUN': {'NavRoll': [2], 'Roll': [3], 'NavPitch': [4], 'Pitch': [5], 'ThrOut': [6],
                       'RdrOut': [7], 'ThrDem': [8], 'Aspd': [9]},
              'DSF': {'Dp': [2], 'IErr': [3], 'Blk': [4], 'Bytes': [5], 'FMn': [6], 'FMx': [7], 'FAv': [8]},
              'GPA': {'VDop': [2], 'HAcc': [3], 'VAcc': [4], 'SAcc': [5], 'VV': [6], 'SMS': [7], 'Delta': [8]},
              'GPS': {'Status': [2], 'GMS': [3], 'GWk': [4], 'NStas': [5], 'HDop': [6], 'Lat': [7],
                      'Lng': [8], 'Alt': [9], 'Spd': [10], 'GCrs': [11], 'VZ': [12], 'U': [13]},
              'GPSD': {'thrDem': [2], 'GSPDthr': [3], 'PErr': [4], 'EDelta': [5]},
              'IMU': {'GyrX': [2], 'GyrY': [3], 'GyrZ': [4], 'AccX': [5], 'AccY': [6], 'AccZ': [7], 'EG': [8],
                      'EA': [9], 'T': [10], 'GH': [11], 'AH': [12], 'GHz': [13], 'AHz': [14]},
              'IMU2': {'GyrX': [2], 'GyrY': [3], 'GyrZ': [4], 'AccX': [5], 'AccY': [6], 'AccZ': [7], 'EG': [8],
                       'EA': [9], 'T': [10], 'GH': [11], 'AH': [12], 'GHz': [13], 'AHz': [14]},
              'IMU3': {'GyrX': [2], 'GyrY': [3], 'GyrZ': [4], 'AccX': [5], 'AccY': [6], 'AccZ': [7], 'EG': [8],
                       'EA': [9], 'T': [10], 'GH': [11], 'AH': [12], 'GHz': [13], 'AHz': [14]},
              'LAND': {'stage': [2], 'f1': [3], 'f2': [4], 'slope': [5], 'slopeInit': [6], 'alt0': [7]},
              'MAG': {'MagX': [2], 'MagY': [3], 'MagZ': [4], 'OfsX': [5], 'OfsY': [6], 'OfsZ': [7],
                      'MOfsX': [8], 'MOfsY': [9], 'MOfsZ': [10], 'Health': [11], 'S': [12]},
              'MAG2': {'MagX': [2], 'MagY': [3], 'MagZ': [4], 'OfsX': [5], 'OfsY': [6], 'OfsZ': [7],
                       'MOfsX': [8], 'MOfsY': [9], 'MOfsZ': [10], 'Health': [11], 'S': [12]},
              'MAG3': {'MagX': [2], 'MagY': [3], 'MagZ': [4], 'OfsX': [5], 'OfsY': [6], 'OfsZ': [7],
                       'MOfsX': [8], 'MOfsY': [9], 'MOfsZ': [10], 'Health': [11], 'S': [12]},
              'NTUN': {'WpDist': [2], 'TargBrg': [3], 'NavBrg': [4], 'AltErr': [5], 'XT': [6],
                       'XTi': [7], 'ArspErr': [8]},
              'PIDP': {'Des': [2], 'P': [3], 'I': [4], 'D': [5], 'FF': [6], 'AFF': [7]},
              'PIDR': {'Des': [2], 'P': [3], 'I': [4], 'D': [5], 'FF': [6], 'AFF': [7]},
              'PIDS': {'Des': [2], 'P': [3], 'I': [4], 'D': [5], 'FF': [6], 'AFF': [7]},
              'PIDY': {'Des': [2], 'P': [3], 'I': [4], 'D': [5], 'FF': [6], 'AFF': [7]},
              'PM': {'NLon': [2], 'NLoop': [3], 'MaxT': [4], 'MinT': [5], 'LogDrop': [6], 'Mem': [7]},
              'POS': {'Lat': [2], 'Lng': [3], 'Alt': [4], 'RelHomeAlt': [5], 'RelOriginAlt': [6]},
              'POWR': {'VCc': [2], 'VServo': [3], 'Flags': [4]},
              'RAD': {'RSSI': [2], 'RemRSSI': [3], 'TxBuf': [4], 'Noise': [5], 'RemNoise': [6],
                      'RxErrors': [7], 'Fixed': [8]},
              'RCIN': {'C1': [2], 'C2': [3], 'C3': [4], 'C4': [5], 'C5': [6], 'C6': [7], 'C7': [8], 'C8': [9],
                       'C9': [10], 'C10': [11], 'C11': [12], 'C12': [13], 'C13': [14], 'C14': [15]},
              'RCOU': {'C1': [2], 'C2': [3], 'C3': [4], 'C4': [5], 'C5': [6], 'C6': [7], 'C7': [8], 'C8': [9],
                       'C9': [10], 'C10': [11], 'C11': [12], 'C12': [13], 'C13': [14], 'C14': [15]},
              'STAT': {'isFlying': [2], 'isFlyProb': [3], 'Armed': [4], 'Safety': [5], 'Crash': [6],
                       'Still': [7], 'Stage': [8], 'Hit': [9]},
              'TEC2': {'KErr': [2], 'PErr': [3], 'EDelta': [4], 'LF': [5]},
              'TECS': {'h': [2], 'dh': [3], 'hdem': [4], 'dhdem': [5], 'spdem': [6], 'sp': [7], 'dsp': [8],
                       'ith': [9], 'iph': [10], 'th': [11], 'ph': [12], 'dspdem': [13], 'w': [14], 'f': [15]},
              'TERR': {'Status': [2], 'Lat': [3], 'Lng': [4], 'Spacing': [5], 'TerrH': [6], 'CHeight': [7],
                       'Pending': [8], 'Loaded': [9]},
              'UBX1': {'Instance': [2], 'noisePerMS': [3], 'jamlnd': [4], 'aPower': [5], 'agcCnt': [6], 'config': [7]},
              'UBX1': {'Instance': [2], 'ofsl': [3], 'magl': [4], 'ofsQ': [5], 'magQ': [6]},
              'VIBE': {'VibeX': [2], 'VibeY': [3], 'VibeZ': [4], 'Clip0': [5], 'Clip1': [6], 'Clip2': [7]}
              }
