

# - SET UP INICIAL


from connectors.not_in_production.fred import FredMultFrame, FredUniFrame, US_IndexNormalize
from datetime import date
from pandas import concat
import pandas as pd

from utils.thermometer import Score
from utils.transforms import pivot_table_to_long as unpivot


def GetScore(df, alfa, col_name, direction=1, drop_intermediary=True):
    """Wrapper: extrai coluna, define index como Date e aplica Score."""
    series = df.set_index('Date')[col_name] if 'Date' in df.columns else df[col_name]
    return Score(series, alfa * direction, col_name)

"""
    Definição de algumas variaveis importantes

"""
InicialDate = '01/01/1970'
NowDate = date.today().strftime("%m-%d-%Y") 



#----------------------------------------------- 1.) LABOR MARKET --------------------------------------------

#- 1.1) Unemployment Rate

def UnempRate():

    # - Definição de algumas variaveis
    Trend_ColumnName = 'Unemployment Rate'


    # - Data Request
    BaseUnemRate = FredUniFrame(Trend_ColumnName, 'UNRATE',  '01/01/1948', NowDate)
    
    # ExportTo(BaseUnemRate, r'\UnemRate')
    
    # - Get Score
    Trend_UnemRate = GetScore(BaseUnemRate, 1, Trend_ColumnName, -1, True)


    # - Pivot Frame
    Trend_UnemRate = unpivot(Trend_UnemRate)


    return Trend_UnemRate

Trend_UnemRate = UnempRate()


#- 1.2) Jobs per Unemployment

def Jobs_Unemp():
    
    # - Definindo algumas variaveis
    Trend_ColumnName = 'Jobs/Unemp'

    DictBase = {'Jolts': 'JTSJOL', 'Unemp' : 'UNEMPLOY'}
    BaseJobsperUnempl = FredMultFrame(DictBase, InicialDate, NowDate)

    # ExportTo(BaseJobsperUnempl, r'\BaseJobsUnemp')

    #* Criando Ratio de Jobs Openings per Unemployment
    BaseJobsperUnempl[Trend_ColumnName] = BaseJobsperUnempl['Jolts'] / BaseJobsperUnempl['Unemp']

    #* Gerando as notas
    Trend_Jobs_Unemp = GetScore(BaseJobsperUnempl, 1, Trend_ColumnName, Direction = 1, DropIntermediareCols=True)

    #* Pivotando o frame
    Trend_Jobs_Unemp = unpivot(Trend_Jobs_Unemp)

    return Trend_Jobs_Unemp
Trend_Jobs_Unemp = Jobs_Unemp()


# - 1.3) PayRoll
def PayRoll():

    # - Definição de variáveis
    Trend_ColumnName = 'PayRoll_Trend'

    # - DataRequest
    BasePayRoll = FredUniFrame('NonFarm PayRoll', 'PAYEMS', '01/01/1939', NowDate)
    
    # ExportTo(BasePayRoll, r'\BasePayroll')

    # - Get Change in PayRoll
    BasePayRoll['NetChange_MoM'] = (BasePayRoll['NonFarm PayRoll'] - BasePayRoll['NonFarm PayRoll'].shift(1)) 

    # - Get rolling average Change in PayRoll
    BasePayRoll[Trend_ColumnName] = BasePayRoll['NetChange_MoM'].rolling(12).mean()

    # - Get Score 12m PayRoll
    PayRollScore = GetScore(BasePayRoll, 1,Trend_ColumnName, 1, True)



    # - Pivot 12m PayRollFrame
    OutPutFrame = PayRollScore.tail(360)
    OutPutFrame = unpivot(OutPutFrame)

    # - Concat Frames
    FramesToConcat = [OutPutFrame]
    OutPutFrame = concat(FramesToConcat)

    return OutPutFrame
PayRollFrames = PayRoll()


#- 1.4) Earnings
def Earnings():
    
    # - Definição de Variaveis
    Trend_ColumnName = 'Earnings_YoY'
    Stationary_ColumnName = 'Earnings_MoM'

    # - Data Request
    Base_Earnings = FredUniFrame('Earnings_PerHour', 'CES0500000003', InicialDate, NowDate)

    # ExportTo(Base_Earnings, r'\Earnings')


    # - Get PCE Year over Year
    Base_Earnings[Trend_ColumnName] = ((Base_Earnings['Earnings_PerHour']/Base_Earnings['Earnings_PerHour'].shift(12))-1)*100

    # - Get Month to Month
    Base_Earnings[Stationary_ColumnName] = ((Base_Earnings['Earnings_PerHour']/Base_Earnings['Earnings_PerHour'].shift(1))-1)*100

    # - Get Score YoY
    Earnings_YoY = GetScore(Base_Earnings, 1, Trend_ColumnName, 1, True)

    # - Get Score MoM
    Earnings_MoM = GetScore(Base_Earnings, 1, Stationary_ColumnName, 1, True)

    # - Pivot Frames        
    Earnings_YoY = unpivot(Earnings_YoY)
    Earnings_MoM = unpivot(Earnings_MoM)    

    # - Concat Frames
    FramesToConcat = [Earnings_YoY, Earnings_MoM]
    OutPutFrame = concat(FramesToConcat)


    return OutPutFrame
Frame_Earnings = Earnings()


#----------------------------------------------- 2.) INLFLATION --------------------------------------------

# - 2.1) PCE

def PCE():

    # - Definição de Variaveis
    Trend_ColumnName = 'PCE_YoY'
    Stationary_ColumnName = 'PCE_MoM'

    # - Data Request
    BasePce = FredUniFrame('PCE_Index', 'PCEPI', InicialDate, NowDate)

    # ExportTo(BasePce, '\PCE')
    # - Get PCE Year over Year
    BasePce[Trend_ColumnName] = ((BasePce['PCE_Index']/BasePce['PCE_Index'].shift(12))-1)*100

    # - Get Month to Month
    BasePce[Stationary_ColumnName] = ((BasePce['PCE_Index']/BasePce['PCE_Index'].shift(1))-1)*100

    # - Get Score YoY
    PCE_YoY = GetScore(BasePce, 1, Trend_ColumnName, -1, True)

    # - Get Score MoM
    PCE_MoM = GetScore(BasePce, 1, Stationary_ColumnName, -1, True)

    # - Pivot Frames        
    PCE_YoY = unpivot(PCE_YoY)
    PCE_MoM = unpivot(PCE_MoM)    

    # - Concat Frames
    FramesToConcat = [PCE_YoY, PCE_MoM]
    OutPutFrame = concat(FramesToConcat)


    return OutPutFrame
PceFrames = PCE()

# - 2.2) Core PCE

def CorePce():

    # - Definição de variaveis
    Stationary_ColumnName = 'Core PCE_MoM'
    Trend_ColumnName =  'Core PCE_YoY'

    # - Data Request
    BaseCorePce = FredUniFrame('CorePce_Index', 'PCEPILFE', InicialDate, NowDate)
    
    # ExportTo(BaseCorePce, '\CorePce')
    
    # - Get Year over year (Trend)
    BaseCorePce[Trend_ColumnName] = ((BaseCorePce['CorePce_Index']/BaseCorePce['CorePce_Index'].shift(12))-1)*100

    # - Get Month over Month (Stationary)
    BaseCorePce[Stationary_ColumnName] = ((BaseCorePce['CorePce_Index']/BaseCorePce['CorePce_Index'].shift(1))-1)*100

    # - Get Score: Year over Year (Trend)    
    CorePCE_YoY = GetScore(BaseCorePce, 1, Trend_ColumnName, -1, True)

    # - Get Score: Month over Month (Stationary)
    CorePCE_MoM = GetScore(BaseCorePce, 1, Stationary_ColumnName, -1, True)

    # - Pivot Frames
    CorePCE_YoY = unpivot(CorePCE_YoY)
    CorePCE_MoM = unpivot(CorePCE_MoM)

    # - Concat Frames
    FramesToConcat = [CorePCE_YoY,CorePCE_MoM]

    OutPutFrame = concat(FramesToConcat)

    return OutPutFrame
CorePceFrames = CorePce()

# - 2.3) Sticky Prices

def StickPrices():
    
    # - Definição de variaveis
    Trend_ColumnName = 'Sticky Price'

    # - Data Request
    BaseStickyPrice = FredUniFrame(Trend_ColumnName, 'STICKCPIM159SFRBATL', InicialDate, NowDate)

    # ExportTo(BaseStickyPrice, '\StickyPrice')

    # - Get Score YoY
    StickyPrice_YoY = GetScore(BaseStickyPrice, 1, Trend_ColumnName, -1, True)

    # - Pivot Frame
    StickyPrice_YoY = unpivot(StickyPrice_YoY)

    return StickyPrice_YoY

StickyFrame = StickPrices()

# - 2.4) Flexible Prices

def FlexiblePrices():
    
    # - Definição de variaveis
    Trend_ColumnName = 'FlexiblePrice_YoY'

    # - Data Request
    BaseFlexiblePrice = FredUniFrame(Trend_ColumnName, 'FLEXCPIM159SFRBATL', InicialDate, NowDate)

    # ExportTo(BaseFlexiblePrice, '\FlexiblePrice')

    # - Get Score Flexible Price YoY
    FlexiblePrice_YoY = GetScore(BaseFlexiblePrice, 1, Trend_ColumnName, -1, True)

    # - Pivot Frame
    FlexiblePrice_YoY = unpivot(FlexiblePrice_YoY)

    return FlexiblePrice_YoY

FlexibleFrame = FlexiblePrices()


# - 2.5) PPI

def PPI():
    
    # - Definindo Variaveis
    Trend_ColumnName = 'PPI_YoY'
    Stationary_ColumnName = 'PPI_MoM'

    #- Data Request
    BasePPI = FredUniFrame('PPI', 'PPIACO', InicialDate, NowDate)

    # ExportTo(BasePPI, '\PPI')

    # - Get Year over Year
    BasePPI[Trend_ColumnName] = ((BasePPI['PPI']/BasePPI['PPI'].shift(12))-1)*100

    # - Get Month over Month
    BasePPI[Stationary_ColumnName] = ((BasePPI['PPI']/BasePPI['PPI'].shift(1))-1)*100

    #-  Get Score PPI YoY
    PPI_YoY = GetScore(BasePPI, 1, Trend_ColumnName, -1, True)

    #-  Get Score PPI MoM
    PPI_MoM = GetScore(BasePPI, 1, Stationary_ColumnName, -1, True)

    # - Pivot Frames
    PPI_YoY = unpivot(PPI_YoY)
    PPI_MoM = unpivot(PPI_MoM)

    # - Concat Frames
    FramesToConcat = [PPI_YoY, PPI_MoM]

    OutPutFrame = concat(FramesToConcat)

    return OutPutFrame

PPIFrames = PPI()


# - 2.6) Inflation Expectation

def InflationExpectations():
    
    # - Definição de variaveis
    Trend_ColumnName = 'Inflation Expectation'

    # - Data Request
    Base_Infl_Expectation = FredUniFrame(Trend_ColumnName, 'MICH', InicialDate, NowDate)

    # ExportTo(Base_Infl_Expectation, '\InflExpectations')

    # - Get Score Flexible Price YoY
    Inflation_Expect = GetScore(Base_Infl_Expectation, 1, Trend_ColumnName, -1, True)

    # - Pivot Frame
    Inflation_Expect = unpivot(Inflation_Expect)

    return Inflation_Expect

Infla_Expectations = InflationExpectations()


#----------------------------------------------- 3.) Activity --------------------------------------------


# - 3.1) Retail Sales

def RetailSales():
    
    # - Definindo Variaveis
    Trend_ColumnName = 'Retail_YoY'
    Stationary_ColumnName = 'Retail_MoM'

    #- Data Request
    BaseRetail = FredUniFrame('Retail_index', 'RSAFS', InicialDate, NowDate)
    
    # ExportTo(BaseRetail, r'\RetailUS')
    
    # - Get Year over Year
    BaseRetail[Trend_ColumnName] = ((BaseRetail['Retail_index']/BaseRetail['Retail_index'].shift(12))-1)*100

    # - Get Month over Month
    BaseRetail[Stationary_ColumnName] = ((BaseRetail['Retail_index']/BaseRetail['Retail_index'].shift(1))-1)*100

    #-  Get Score PPI YoY
    Retail_YoY = GetScore(BaseRetail, 1, Trend_ColumnName, 1, True)

    #-  Get Score PPI MoM
    Retail_MoM = GetScore(BaseRetail, 1, Stationary_ColumnName, 1, True)

    # - Pivot Frames
    Retail_YoY = unpivot(Retail_YoY)
    Retail_MoM = unpivot(Retail_MoM)

    # - Concat Frames
    FramesToConcat = [Retail_YoY, Retail_MoM]

    OutPutFrame = concat(FramesToConcat)

    return OutPutFrame

Retail_Frame = RetailSales()


# - 3.2) Industrial Production

def IndustrialProduction():
    
    # - Definindo Variaveis
    Trend_ColumnName = 'Ind_Prod_YoY'
    Stationary_ColumnName = 'Ind_Prod_MoM'

    #- Data Request
    BaseIndprod = FredUniFrame('Indust_Prod_index', 'INDPRO', InicialDate, NowDate)

    # ExportTo(BaseIndprod, '\IndustrialProd')

    # - Get Year over Year
    BaseIndprod[Trend_ColumnName] = ((BaseIndprod['Indust_Prod_index']/BaseIndprod['Indust_Prod_index'].shift(12))-1)*100

    # - Get Month over Month
    BaseIndprod[Stationary_ColumnName] = ((BaseIndprod['Indust_Prod_index']/BaseIndprod['Indust_Prod_index'].shift(1))-1)*100

    #-  Get Score PPI YoY
    Ind_Prod_YoY = GetScore(BaseIndprod, 1, Trend_ColumnName, 1, True)

    #-  Get Score PPI MoM
    Ind_Prod_MoM = GetScore(BaseIndprod, 1, Stationary_ColumnName, 1, True)

    # - Pivot Frames
    Ind_Prod_YoY = unpivot(Ind_Prod_YoY)
    Ind_Prod_MoM = unpivot(Ind_Prod_MoM)

    # - Concat Frames
    FramesToConcat = [Ind_Prod_YoY, Ind_Prod_MoM]

    OutPutFrame = concat(FramesToConcat)

    return OutPutFrame

Ind_Prod_Frame = IndustrialProduction()

# - 3.3) GDP_YoY

def GDP_YoY():
    
    #- Definição de variaveis
    Trend_ColumnName = 'GDP_YoY'

    #- Data Request
    BaseGDP_YoY = FredUniFrame(Trend_ColumnName, 'A191RO1Q156NBEA', InicialDate, NowDate)
    
    # ExportTo(BaseGDP_YoY, '\GDPYOY')

    #- Get Score GDP YoY
    GDP_YoY = GetScore(BaseGDP_YoY, 1, Trend_ColumnName, 1, True)


    #- Normalize Index (Expand - Quarter To Month)
    OutFrame = US_IndexNormalize(GDP_YoY, InicialDate, NowDate)

    #- Drop Nan
    OutFrame.dropna(axis = 0, how ='any', inplace = True)

    #- Pivot Frame
    OutFrame.set_index('Date', inplace = True)
    GDP_YoY = unpivot(OutFrame)

    return GDP_YoY

Gdp_YoY = GDP_YoY()


# - 3.4) GDP_MoM

def GDP_MoM():
    
    #- Definição de variaveis
    Trend_ColumnName = 'GDP_QoQ'

    #- Data Request
    BaseGDP_QoQ = FredUniFrame(Trend_ColumnName, 'A191RL1Q225SBEA', InicialDate, NowDate)
    # ExportTo(BaseGDP_QoQ, '\GDP_QoQ')

    #- Get Score Flexible Price YoY
    GDP_QoQ = GetScore(BaseGDP_QoQ, 1, Trend_ColumnName, 1, True)
    
    #- Normalize Index (Expand - Quarter To Month)
    OutFrame = US_IndexNormalize(GDP_QoQ, InicialDate, NowDate)

    #- Drop Nan
    OutFrame.dropna(axis = 0, how ='any', inplace = True)

    #- Pivot Frame
    OutFrame.set_index('Date', inplace = True)
    GDP_MoM = unpivot(OutFrame)

    return GDP_MoM
Gdp_MoM = GDP_MoM()


# ----------------------------------------------- 4.) Financial Conditions --------------------------------------------


# - 4.1) NFCI - National Financial Conditions Index

def NFCI():
    
     # - Definindo Variaveis
    Trend_ColumnName = 'NFCI_Level'
    Stationary_ColumnName = 'NFCI_MoM'

    #- Data Request
    Base_NFCI = FredUniFrame(Trend_ColumnName, 'NFCI', InicialDate, NowDate)

    

    # - Get NFCI Month over Month
    Base_NFCI[Stationary_ColumnName] = (Base_NFCI[Trend_ColumnName]-Base_NFCI[Trend_ColumnName].shift(1))

    #- Resample Frame
    Base_NFCI['Date'] = pd.to_datetime(Base_NFCI['Date'])
    
    Base_NFCI.set_index('Date', inplace=True)

    Base_NFCI = Base_NFCI.resample('BMS').mean()

    # ExportTo(Base_NFCI, r'\NFCI')

    Base_NFCI.reset_index(inplace=True)

    #-  Get NFCI Level Score
    NFCI_Level = GetScore(Base_NFCI, 1, Trend_ColumnName, -1, True)

    #-  Get NFCI MoM Score
    NFCI_MoM = GetScore(Base_NFCI, 1, Stationary_ColumnName, -1, True)

    # - Pivot Frames
    NFCI_Level = unpivot(NFCI_Level)
    NFCI_MoM = unpivot(NFCI_MoM)

    # - Concat Frames
    FramesToConcat = [NFCI_Level, NFCI_MoM]

    OutPutFrame = concat(FramesToConcat)

    return OutPutFrame
Nfci = NFCI()

# - 4.2) ANFCI - Adjusted National Financial Conditions Index

def ANFCI():
    
     # - Definindo Variaveis
    Trend_ColumnName = 'ANFCI_Level'
    Stationary_ColumnName = 'ANFCI_MoM'

    #- Data Request
    Base_ANFCI = FredUniFrame(Trend_ColumnName, 'ANFCI', InicialDate, NowDate)

    # - Get NFCI Month over Month
    Base_ANFCI[Stationary_ColumnName] = (Base_ANFCI[Trend_ColumnName]-Base_ANFCI[Trend_ColumnName].shift(1))

    #- Resample Frame.
    Base_ANFCI['Date'] = pd.to_datetime(Base_ANFCI['Date'])
    
    Base_ANFCI.set_index('Date', inplace=True)

    Base_ANFCI = Base_ANFCI.resample('BMS').mean()
    
    # ExportTo(Base_ANFCI, '\ANFCI')
    
    Base_ANFCI.reset_index(inplace=True)

    #-  Get ANFCI Level Score
    ANFCI_Level = GetScore(Base_ANFCI, 1, Trend_ColumnName, -1, True)

    #-  Get ANFCI MoM Score
    ANFCI_MoM = GetScore(Base_ANFCI, 1, Stationary_ColumnName, -1, True)

    # - Pivot Frames
    ANFCI_Level = unpivot(ANFCI_Level)
    ANFCI_MoM = unpivot(ANFCI_MoM)

    #- Concat Frames
    FramesToConcat = [ANFCI_Level, ANFCI_MoM]

    OutPutFrame = concat(FramesToConcat)

    return OutPutFrame
Anfci = ANFCI()


#----------------------------------------------- 5.) Housing --------------------------------------------
# - 5.1) House Sold
def HouseSold():


    # - Definindo Variaveis
    Trend_ColumnName = 'HomeSold_12m'
    Stationary_ColumnName = 'HomeSold_Month'

    #- Data Request
    Base_HomeSold = FredUniFrame(Stationary_ColumnName, 'HSN1F', InicialDate, NowDate)
    
    # ExportTo(Base_HomeSold, '\HomeSold')
    
    # - Cycle Definition
    Cycle = 60/len(Base_HomeSold[Stationary_ColumnName])

    # - Get Trend 12m
    Base_HomeSold[Trend_ColumnName] = Base_HomeSold[Stationary_ColumnName].rolling(12, min_periods=3).mean()

    # - Get Score Stationary
    HomeSold_M = GetScore(Base_HomeSold, Cycle, Stationary_ColumnName, 1, True)
    
    #- Get Score Trend
    HomeSold_12m = GetScore(Base_HomeSold, Cycle, Trend_ColumnName, 1, True)

    # - Pivot Frames
    HomeSold_M = unpivot(HomeSold_M)
    HomeSold_12m = unpivot(HomeSold_12m)

    #- Concat Frames
    FramesToConcat = [HomeSold_M, HomeSold_12m]

    OutPutFrame = concat(FramesToConcat)

    return OutPutFrame
df_HouseSold = HouseSold()

# - 5.2) House for Sale
def HomeForSale():

    # - Definindo Variaveis
    Trend_ColumnName = 'HomeForSale_12m'
    Stationary_ColumnName = 'HomeForSale_Month'

    #- Data Request
    Base_HomeSale = FredUniFrame(Stationary_ColumnName, 'HNFSEPUSSA', InicialDate, NowDate)

    # ExportTo(Base_HomeSale, '\HomeForSale')
    # - Cycle Definition
    # Cycle = 60/len(Base_HomeSale[Stationary_ColumnName])

    # - Get Trend 12m
    Base_HomeSale[Trend_ColumnName] = Base_HomeSale[Stationary_ColumnName].rolling(12, min_periods=3).mean()

    #- Get Score Stationary
    HomeSale_M = GetScore(Base_HomeSale, 1, Stationary_ColumnName, -1, True)
    
    #- Get Score Trend
    HomeSale_12m = GetScore(Base_HomeSale, 1, Trend_ColumnName, -1, True)

    # - Pivot Frames
    HomeSale_M = unpivot(HomeSale_M)
    HomeSale_12m = unpivot(HomeSale_12m)

    #- Concat Frames
    FramesToConcat = [HomeSale_M, HomeSale_12m]

    OutPutFrame = concat(FramesToConcat)

    return OutPutFrame
df_HouseForSale_Frame = HomeForSale()

# - 5.3) Monthly Supply
def MonthlySupply():
    
    # - Definindo Variaveis
    Trend_ColumnName = 'MonthlySupply_12m'
    Stationary_ColumnName = 'MonthlySupply_Month'

    #- Data Request
    Base_MnthSupp = FredUniFrame(Stationary_ColumnName, 'MSACSR', InicialDate, NowDate)
    
    # ExportTo(Base_MnthSupp, '\MonthLySupply')
    
    # - Cycle Definition
    # Cycle = 60/len(Base_HomeSale[Stationary_ColumnName])

    # - Get Trend 12m
    Base_MnthSupp[Trend_ColumnName] = Base_MnthSupp[Stationary_ColumnName].rolling(12, min_periods=3).mean()

    #- Get Score Stationary
    MnthSupp_M = GetScore(Base_MnthSupp, 1, Stationary_ColumnName, -1, True)
    
    # #- Get Score Trend
    MnthSupp_12m = GetScore(Base_MnthSupp, 1, Trend_ColumnName, -1, True)

    # - Pivot Frames
    MnthSupp_M = unpivot(MnthSupp_M)
    MnthSupp_12m = unpivot(MnthSupp_12m)

    #- Concat Frames
    FramesToConcat = [MnthSupp_M, MnthSupp_12m]

    OutPutFrame = concat(FramesToConcat)

    return OutPutFrame
df_MnthSupp = MonthlySupply()


# - 5.4) Mortgage Yield
def MorgtYield():
    
    # - Definindo Variaveis
    Trend_ColumnName = '30y_Mortgage_12m'
    Stationary_ColumnName = '30y_Mortgage_Month'

    #- Data Request
    Base_30yMorgt = FredUniFrame(Stationary_ColumnName, 'MORTGAGE30US', InicialDate, NowDate)
    
    # ExportTo(Base_30yMorgt, '\MorgageRate30')
   
   # - Cycle Definition
    Cycle = 60/len(Base_30yMorgt[Stationary_ColumnName])

    # - Get Trend 12m
    Base_30yMorgt[Trend_ColumnName] = Base_30yMorgt[Stationary_ColumnName].rolling(12, min_periods=3).mean()

    #- Get Score Stationary
    Morgt_Level = GetScore(Base_30yMorgt, Cycle, Stationary_ColumnName, -1, True)
    
    #- Get Score Trend
    Morgt_12m = GetScore(Base_30yMorgt, Cycle, Trend_ColumnName, -1, True)

    # - Pivot Frames
    Morgt_Level = unpivot(Morgt_Level)
    Morgt_12m = unpivot(Morgt_12m)

    #- Concat Frames
    FramesToConcat = [Morgt_Level, Morgt_12m]

    OutPutFrame = concat(FramesToConcat)

    return OutPutFrame
df_MorgtYield = MorgtYield()


# - 5.5) Shiller House Prices

def ShillerHousePrices():
    
    # - Definindo Variaveis
    Trend_ColumnName = 'House Price_YoY'
    Stationary_ColumnName = 'House Price_MoM'

    #- Data Request
    Base_HousePrice = FredUniFrame('Shiller_Index', 'CSUSHPINSA', InicialDate, NowDate)
    # ExportTo(Base_HousePrice, '\HousePrice')

    # - Get Year over Year
    Base_HousePrice[Trend_ColumnName] = ((Base_HousePrice['Shiller_Index']/Base_HousePrice['Shiller_Index'].shift(12))-1)*100

    # - Get Month over Month
    Base_HousePrice[Stationary_ColumnName] = ((Base_HousePrice['Shiller_Index']/Base_HousePrice['Shiller_Index'].shift(1))-1)*100

    #-  Get Score PPI YoY
    HousePrice_YoY = GetScore(Base_HousePrice, 1, Trend_ColumnName, -1, True)

    #-  Get Score PPI MoM
    HousePrice_MoM = GetScore(Base_HousePrice, 1, Stationary_ColumnName, -1, True)

    # - Pivot Frames
    HousePrice_YoY = unpivot(HousePrice_YoY)
    HousePrice_MoM = unpivot(HousePrice_MoM)

    # - Concat Frames
    FramesToConcat = [HousePrice_YoY, HousePrice_MoM]

    OutPutFrame = concat(FramesToConcat)

    return OutPutFrame
df_HousePrices = ShillerHousePrices()



#------------------------------------------------------------------------------------------------------------


#----------------------------------------------- X.) CONCATENAÇÃO --------------------------------------------

# - LISTA DE FRAMES

FramesToConcat = [Trend_UnemRate, 
                  Trend_Jobs_Unemp,
                  PayRollFrames,
                  PceFrames,
                  CorePceFrames,
                  StickyFrame,
                  FlexibleFrame,
                  PPIFrames,
                  Frame_Earnings,
                  Infla_Expectations,
                  Retail_Frame,
                  Ind_Prod_Frame,
                  Gdp_YoY,
                  Gdp_MoM,
                  Nfci,
                  Anfci,
                  df_HouseSold,
                  df_HouseForSale_Frame,
                  df_MnthSupp,
                  df_MorgtYield,
                  df_HousePrices]
                

# - CONCATENAR
FinalFrame = concat(FramesToConcat)

# print(FinalFrame['Name'].unique())


# ----------------------------------------------- XI.) GERANDO ARQUIVO --------------------------------------------

Path = r'C:\Users\LIS CAPITAL\LIS Capital Dropbox\LIS Capital\Macro\Sistema de dados\oraculo\us\base\US_BASE.csv'

FinalFrame.to_csv(Path, index=False)







