import pandas as pd

from fredapi import Fred
from datetime import date

import numpy as np


def unpivot (frame, index):
    
    frame.set_index(index, inplace = True)
   
    Rows, Cols = frame.shape 
    
    data = {
        
        "Values" : frame.to_numpy().ravel("F"),
        "Name": np.asanyarray(frame.columns).repeat(Rows),
        "Date" : np.tile(np.asanyarray(frame.index), Cols)

    }

    OutPutFrame = pd.DataFrame(data)

    return OutPutFrame




def FredUniFrame(NameSerie, IdSerie, StartDate, EndDate):
    
    fred = Fred(api_key = 'fc857446fbf5fdc0b8461e05618bb6fc')

    UniFrame = pd.DataFrame(fred.get_series(IdSerie, observation_start= StartDate, observation_end= EndDate), )

    UniFrame.reset_index(inplace=True)
    
    UniFrame.columns = ['Date', NameSerie]

    return UniFrame


def FredMultFrame(DictData, StartDate, EndDate, Pivot=False):

    fred = Fred(api_key = 'fc857446fbf5fdc0b8461e05618bb6fc')

    IdSerieS = list(DictData.values())
    NameSerieS = list(DictData.keys())

    
    for Id in IdSerieS:
        
        if Id != IdSerieS[0]: 

            FrameToAdd = pd.DataFrame(fred.get_series(Id, observation_start= StartDate, observation_end= EndDate))
            
            FrameToAdd.reset_index(inplace = True)    

            ColumnName = [Name for Name in NameSerieS if DictData[Name] == Id]

            FrameToAdd.columns = ['Date', ColumnName[0]]

            OutFrame = OutFrame.merge(FrameToAdd, how = 'outer', left_on = 'Date', right_on = 'Date')
         
              
        else:


            OutFrame = pd.DataFrame(fred.get_series(Id, observation_start= StartDate, observation_end= EndDate))
            
            OutFrame.reset_index(inplace=True)

            OutFrame.columns = ['Date', NameSerieS[0]]
            
    if Pivot == True:
    
        PivotOutFrame = unpivot(OutFrame, 'Date')
        return PivotOutFrame
    
    else:
        
        return OutFrame


def US_IndexNormalize(FrameToNormalize, InitialDate, EndDate):
    

    """
    This function serves to expand Quarterly Data to Monthly data, filling the data to month missed months.
    
    FrameToNormalize: Correspond to the frame of Quartely data;

    
    """
    
    # - Get Index Frame

    DateTimeIndexFrame = FredUniFrame('CPI_GET_Index', 'CPIAUCSL', InitialDate, EndDate)


    # - Merge the IndexDateTime frame and the outframe 

    df = DateTimeIndexFrame.merge(FrameToNormalize, how = 'outer', left_on = 'Date', right_on = 'Date')
    
    # - Fill the Nan Values

    OutPutFrame = df.ffill(axis = 'index', limit = 2)


    # - Drop Unecessary Columns 

    OutPutFrame.drop(columns = {'CPI_GET_Index'}, inplace=True)


    return OutPutFrame



