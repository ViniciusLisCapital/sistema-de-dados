ISSN 1518-3548 
CGC 00.038.166/0001-05 
Working Paper Series 
Brasília 
n. 203 
Apr. 
2010 
p. 1-65

Working Paper Series 
 
 
 
 
Edited by Research Department (Depep) – E-mail: workingpaper@bcb.gov.br 
 
Editor: Benjamin Miranda Tabak – E-mail: benjamin.tabak@bcb.gov.br 
Editorial Assistant: Jane Sofia Moita – E-mail: jane.sofia@bcb.gov.br 
Head of Research Department: Adriana Soares Sales – E-mail: adriana.sales@bcb.gov.br  
 
The Banco Central do Brasil Working Papers are all evaluated in double blind referee process. 
  
Reproduction is permitted only if source is stated as follows: Working Paper n. 203. 
 
Authorized by Carlos Hamilton Vasconcelos Araújo, Deputy Governor for Economic Policy. 
 
 
 
General Control of Publications 
 
Banco Central do Brasil 
Secre/Surel/Cogiv 
SBS – Quadra 3 – Bloco B – Edifício-Sede – 1º andar 
Caixa Postal 8.670 
70074-900 Brasília – DF – Brazil 
Phones: +55 (61) 3414-3710 and 3414-3565 
Fax: +55 (61) 3414-3626 
E-mail: editor@bcb.gov.br 
 
 
 
The views expressed in this work are those of the authors and do not necessarily reflect those of the Banco Central or  
its members. 
 
Although these Working Papers often represent preliminary work, citation of source is required when used or reproduced. 
 
 
As opiniões expressas neste trabalho são exclusivamente do(s) autor(es) e não refletem, necessariamente, a visão do Banco 
Central do Brasil. 
 
Ainda que este artigo represente trabalho preliminar, é requerida a citação da fonte, mesmo quando reproduzido 
parcialmente. 
 
 
 
Consumer Complaints and Public Enquiries Center 
 
Banco Central do Brasil 
Secre/Surel/Diate 
SBS – Quadra 3 – Bloco B – Edifício-Sede – 2º subsolo 
70074-900 Brasília – DF – Brazil 
Fax: +55 (61) 3414-2553 
Internet: http//www.bcb.gov.br/?english

Output Gap and GDP in Brazil: 
a real-time data analysis* 
 
 
 
 
Rafael Tiecher Cusinato** 
André Minella*** 
Sabino da Silva Pôrto Júnior**** 
 
 
  
 
The Working Papers should not be reported as representing the views of the Banco Central 
do Brasil. The views expressed in the papers are those of the author(s) and do not 
necessarily reflect those of the Banco Central do Brasil. 
 
 
Abstract 
 
Economic agents make decisions using real-time data. However, 
recent literature has shown that several economic activity measures go 
through important revisions over time, impairing the reliability of real-time 
data. We organize a real-time data set for Brazil’s GDP, and assess the 
revisions of both the GDP growth and the output gap. We show that GDP 
growth revisions are substantial, with a 0.7 p.p. mean absolute revision for 
the quarter-over-quarter growth, although the revisions become less 
important for four-quarter changes. To assess output gap revisions, we use 
four methods to estimate the output gap: Hodrick-Prescott filter, linear 
trend, quadratic trend, and Harvey-Clark model of unobserved components. 
The output gap revisions are substantial in all methods, with mean absolute 
revisions between 0.6 p.p. and 2.3 p.p. In three out of the four methods, the 
revisions implied changes in the output gap sign in 30 percent or more of 
the cases. In general, both the GDP data revision and the sample increase 
are relevant sources of output gap revisions. 
 
Keywords: Real-time data; Output gap; Gross Domestic Product; Business 
cycle; Brazil. 
JEL classification: C82; E32. 
 
                                                      
* We are thankful to Cláudio D. Shikida, Roberto Camps de Moraes, Ronald O. Hillbrecht and 
participants in the XXXVII Anpec National Meeting of Economics for their comments and suggestions. 
** Research Department, Central Bank of Brazil. Email: rafael.cusinato@bcb.gov.br (corresponding 
author). 
*** Research Department, Central Bank of Brazil. Email: andre.minella@bcb.gov.br. 
**** Graduate Program in Economics, Federal University of Rio Grande do Sul (UFRGS). Email: 
sabino@ppge.ufrgs.br. 
3

1. Introduction 
 
The recent literature on real-time data analysis has shown that the differences 
between the data values as initially released and those after undergoing a revision are 
important. Revisions are a natural part of the data production — as time goes by, the 
available information set is enlarged, seasonal factors are reestimated, and 
methodological revisions are implemented. Thus, data usually become more precise 
over time. The problem is that, in general, agents need to make decisions using real-
time data, without benefiting from data revisions. Several authors have studied the 
features of data revisions. If the revisions are relatively large, the capacity of non- 
revised series to help decision-making may be limited. 
 
The Gross Domestic Product (GDP) and the output gap are among the most 
important variables that agents take into account when making decisions. They are used 
in decisions of consumption, real and financial investments, and, in particular, monetary 
policy. Although the proper conduct of monetary policy requires a large information set 
on the state of the economy, the GDP and the output gap are the main economic 
measures considered. GDP is the major information on the economic activity, and the 
output gap is a key concept in monetary policy decisions as it allows us to infer about 
the actual versus potential economic growth. For instance, a positive output gap may 
call for a monetary policy reaction. This relationship is also found in the literature by 
means of monetary policy rules, such as the Taylor rule. 
 
However, the recent literature on real-time data has shown the presence of 
important revisions in the GDP and the output gap data. Croshoure and Stark (2000, 
2001) organized a real-time data set for the U.S. GDP/GNP, and found relevant growth 
revisions. Orphanides and van Norden (2002) constructed several historical series for 
the output gap using real-time data for the U.S. and estimated numerous revision 
indicators. They show inter alia that ex post revisions of the output gap have the same 
magnitude as the own estimated output gap values. The authors suggest that the output 
gap estimates in real time tend to be unreliable and should be used with great caution. 
 
4

Similar studies have been conducted for other countries. Cayen and van Norden 
(2004) analyzed the Canadian GDP growth and found out relevant revisions. Palis, 
Ramos and Robitaille (2004) found that Brazil’s GDP revisions are relatively large 
when compared to developed economies. In the case of output gap revisions, Cayen and 
van Norden (2005) and Bernhardsen et al. (2004, 2005) studied the economies of 
Canada and Norway, respectively. Both studies found that the revision indicators for the 
output gap are even more unfavorable than those for the U.S. economy. The three works 
that analyzed the output gap concluded that both GDP data revisions and the low 
precision of the end-of-sample estimates of the potential output have a relevant 
contribution for the explanation of the revisions of the output gap. 
 
In this paper, we organize a real-time data set for Brazil’s GDP. The data set is 
comprised of quarterly 51 series, containing the GDP data releases between 1996Q1 and 
2008Q2.1 The first data point in each series refers to the first quarter of 1990. Using this 
data set, we investigate the behavior of the revisions of GDP growth2 and output gap 
estimates, obtained using four methods: Hodrick-Prescott (HP) filter, linear trend (LT), 
quadratic trend (QT), and the Harvey-Clark model of unobserved components (HC). 
 
Assuming that our last available data series (referring to 2008Q2) is the best 
available estimate, we calculate several indicators about the revisions of both GDP 
growth and the output gap. Given the assumption that the revisions improve the 
estimates, part of the measurement error of the GDP and output gap is corrected by 
means of the revisions. In the case of the output gap, we decompose the revisions into 
two parts: those stemming from the GDP data revisions, and those arising from the 
inclusion of new observations in the sample. 
 
                                                      
1 With the implementation of a methodological change in Brazil’s GDP estimation, two series referring to 
2006Q4 were released. One is estimated with the previous methodology, and the other with the new one. 
2 The study by Palis, Ramos and Robitaille (2004) on Brazil’s GDP data revisions used the releases for 
data from 1994Q2 through 2001Q4, focusing on the sequence of revisions. They analyzed inter alia some 
revision indicators for the GDP: mean, absolute mean, and root mean square of the revisions. In our work, 
besides using a larger and more recent sample, we estimate several additional indicators and also assess 
the revisions of output gap estimates. 
5

This paper aims at investigating the relevance of data revisions and assessing 
whether the findings on real-time data from the international literature apply to Brazil. 
We found that the revisions of GDP growth are substantial — a 0.7 percentage point 
(p.p.) mean absolute revision of the quarter-over-quarter growth rate — although those 
revisions become less important as we increase the aggregation period (for instance, 
four-quarter growth). Likewise, the output gap estimated using any of the detrending 
methods went under substantial revisions, although the revision indicators are, in 
general, less unfavorable when compared to those in international studies. The mean 
absolute revision of the different output gaps stood between 0.6 p.p. and 2.3 p.p. In 
three out of the four methods analyzed, the revision implied changes in the output gap 
sign in 30 percent or more of the time, and the magnitude of the revision was higher 
than the own magnitude of the gap in approximately 50 percent or more of the time. In 
general, both the GDP data revision and the sample size increase were relevant sources 
of output gap revisions. 
 
The paper is organized as follows. Section 2 reviews briefly the literature and 
the concepts used in real-time data analysis. Section 3 clarifies some issues involved in 
the development of the real-time GDP data set, and analyzes the GDP growth revisions. 
The following section presents the methods used to estimate the output gap, the 
methodology to decompose the output gap revisions, and the revisions analysis. Section 
5 concludes the paper. 
 
2. Real-time data 
  
The literature on real-time data is related to analyses for which data revisions 
are relevant or the moment when the data are released is important. The studies have 
investigated the properties of data revisions, and the impact of data revisions on the 
macroeconomic research, monetary policy and economic forecasts. 
 
Diebold and Rudebush (1991), for instance, present an example that illustrates 
the importance of data revision. They show that a leading indicator of industrial 
production calculated with real-time data performed significantly worse than when 
estimated with revised data. 
6

Although the literature on real-time data appeared initially in the 1950s, it has 
been developed mainly after the construction of a large real-time data set for the U.S. 
economy by Dean Croushore and Tom Stark in mid-1990s. The data set was put 
available on the internet in 1999,3 and is still updated by cooperation between the 
Federal Reserve Bank of Philadelphia and the University of Richmond. 
 
The main issue in this literature is the following: Are data revisions large 
enough in economic terms to be worrisome? 4 Data revisions pose some difficulties for 
the analysis of forecast and monetary policy. For example, using the last available data 
set may be inadequate to compare forecasts coming from a new model with those made 
in real time. In this case, while the forecasts in real time were made with non-revised 
data, the new model forecasts have the benefits of using revised data, probably more 
precise one. Another example refers to the difficulties emerged for policymakers 
because their decisions use data that may not reflect the true state of the economy. 
 
The presence of data revisions is a fact and should not be understood as a 
criticism of the work of the institutions that produce those data. Basically, there are 
three reasons why data are revised over time: i) the information set available to estimate 
the data increases, allowing a better variable estimate; ii) seasonal factors (when 
seasonal adjustment is done) are reestimated, changing the historical series; and iii) in 
order to improve the data quality, changes in the estimation methodology are 
undertaken periodically, possibly resulting in a new historical series. 
 
In fact, the institutions that generate data face a trade-off between the speed of 
data release and data precision. On one hand, the institution can produce better data if it 
waits for a larger information set; on the other hand, economic agents and policy 
makers, which need to make decisions, demand data available in a timely way. 
 
Real-time data can be defined as the data as they existed prior to subsequent 
revisions.5 Following Croushore and Stark (2000, 2001), we use the term “vintage” to 
                                                      
3 http://www.philadelphiafed.org/research-and-data/real-time-center/real-time-data/. 
4 See Croushore (2008). 
5 See Stark (2002). 
7

designate the information set available for a variable on a specific date. In other words, 
it is the last available series, with the most recent revision up to that corresponding 
moment. The collection of those vintages is called the “real-time data set”. 
 
In order to illustrate those concepts, Table 1 shows a real-time data set for 
Brazil’s GDP (seasonally adjusted chain-weighted series). The second column (vintage 
2007Q1) presents the data available for economic agents when the 2007Q1 figure was 
released by the first time; the third column (vintage 2007Q2), in turn, records the data 
available when the 2007Q2 figure was released by the first time; and so forth. Note that 
all vintages start at the same period — in this case, in the first quarter of 2005. The data 
series in each column provides the most recent historical series available at a specific 
moment. On other hand, taking the data corresponding to each row, we can observe how 
a particular data has been revised. For instance, 2007Q1 figure was initially released as 
134.80 and, one quarter later, revised to 135.00. Five quarters after the initial release, in 
the 2008Q2 vintage, the number became 135.40. 
 
 
    
 
Table 1
Real-Time Data Set for the GDP (quarterly seasonally adjusted data - index number)
Period
2007Q1
2007Q2
2007Q3
2007Q4
2008Q1
2008Q2
2005Q1
124.60
124.60
124.80
124.80
124.80
124.90
2005Q2
126.80
126.80
127.70
127.80
127.80
127.60
2005Q3
126.70
126.70
126.60
126.70
126.70
126.70
2005Q4
127.80
127.70
127.70
127.60
127.60
127.60
2006Q1
129.40
129.50
129.70
129.50
129.50
129.70
2006Q2
128.90
128.80
129.90
130.00
130.00
129.80
2006Q3
132.40
132.40
132.20
132.30
132.30
132.30
2006Q4
133.80
133.80
134.00
133.90
133.90
134.00
2007Q1
134.80
135.00
135.50
135.20
135.20
135.40
2007Q2
136.10
137.30
137.30
137.30
137.10
2007Q3
139.60
139.80
139.80
139.60
2007Q4
142.00
142.00
142.20
2008Q1
143.00
143.30
2008Q2
145.60
Source: IBGE (See Section 3.1).
Vintage
8

The lower diagonal in Table 1, reproduced in column A of Table 2, is called 
the real-time data series. It contains the data series as they were initially calculated. 
Note that it starts in the quarter corresponding to the first vintage and ends in the quarter 
corresponding to the last vintage. Note also that this series contains one data point of 
each vintage. Column B of Table 2, in turn, records what is usually called the final data 
series. The data refers to the same period as that of the real-time data series, but the data 
are the most recent ones available at the moment of the research. Thus, all data points of 
this series come from the last vintage (in this case, the 2008Q2 vintage). In column C, 
we show the data revision series, which is obtained as the difference between the final 
and the real-time data series. Therefore, the data revision series reveals the total 
magnitude of the data revision, using as references the first vintage in which the data 
point was calculated and the last available vintage. 
 
 
 
3. Gross Domestic Product 
 
3.1. Developing a real-time GDP data set 
 
The first step of this paper was to organize a real-time GDP data set for Brazil. 
We use seasonally adjusted quarterly data, starting in 1990Q1. The first vintage refers to 
1996Q1, and the last one to 2008Q2. Because of the methodological change in the GDP 
released in 2007, there are two vintages referring to 2006Q4 – one using the previous 
Table 2
Real-Time, Final and Data Revision Series
Seasonally adjusted GDP (index number) 
Real Time
Final
Data revision
Period
(A)
(B)
(C)=B-A
2007Q1
134.80
135.40
0.60
2007Q2
136.10
137.10
1.00
2007Q3
139.60
139.60
0.00
2007Q4
142.00
142.20
0.20
2008Q1
143.00
143.30
0.30
2008Q2
145.60
145.60
0.00
Source: IBGE (See Section 3.1).
9

methodology and the other using the new one (both released in March 2007). The data 
set has been developed using the publications of the National Institute of Geography 
and Statistics (IBGE) as the source.6  
 
In the specific case of 2006Q4, the standard procedure was to use the vintage 
calculated with the new methodology, unless otherwise indicated. We make this 
decision because we consider that the information conveyed by the vintage estimated 
with the new methodology is supposed to be more relevant in real time for economic 
agents, when compared to that contained in the vintage estimated with the previous 
methodology, since the methodological change meant an improvement in GDP 
calculation. 
 
When the data series of a vintage does not go back to 1990Q1, we follow the 
procedure employed by Cayen and van Norden (2004, 2005). Say the first data point of 
vintage n refers to period t. The data information about the periods previous to period t 
of that vintage is filled with those of vintage n-1, multiplied by the 
constant , ,
⁄
, where , is the GDP index for period t, according to 
vintage n. This procedure is equivalent to proceed in such way that, for each data point 
missing in a vintage, the data is calculated as to keep the GDP percentage growth 
presented in the last vintage that contained the data. 
 
3.2. GDP revision analysis 
 
 
Although the real-time GDP data set is in levels, we analyze data revisions 
about the (real) GDP growth (percentage change with respect to the i-th previous 
quarter), calculated as follows:7   
                                                      
6 “Indicadores IBGE – Contas Nacionais Trimestrais e Valores Correntes” (2000Q3 to 2008Q2); 
“Indicadores IBGE – Produto Interno Bruto Trimestral” (1996Q1 and 1999Q1 to 2000Q2); and 
“Indicadores IBGE – Produto Interno Bruto” (1996Q2 to 1998Q4). The only exception is the 2006Q4 
vintage of the previous methodology, which was obtained from the IBGE data set (SIDRA) when that 
vintage was the most recent data series and, thus, available electronically. 
7 We use the logarithm approximation because of its analytical convenience. For example, the GDP 
growth rate in n-periods can be easily decomposed into n additive terms. To make sure that the 
10

∆, 
 100 ·  
	 ,
	 , ,   
 
     
 
 
       (1) 
 
where , is the GDP index for period t according to vintage n, ∆, is the GDP 
growth for period t according to vintage n, and log is the natural logarithm. 
 
GDP growth is a variable followed closely by economic agents and 
policymakers, in particular, by those involved with monetary policy. In general, the 
latest available GDP data point, referring to the most recent period, is the most relevant 
one for decision-making. Unfortunately, it is also the one more subject to revisions.8 
 
Figure 1 shows the GDP growth rates defined as the “final” figures (taken from 
the last available vintage) and the real-time ones.9 Although the rates are highly 
correlated, the differences may be substantial. The importance of GDP data revision is 
clearer in Figure 2, which presents the GDP growth of the first quarter of 1996 as it 
evolved over the revisions (we choose this quarter because it was released by the first 
time in the oldest vintage that we have). When the data was initially released (1996Q1 
vintage), 1996Q1 GDP growth rate was 0.13 percent. Two quarters later, in the 1996Q3 
vintage, the data was revised to -0.10 percent. The peak occurred in the 2000Q2 vintage 
                                                                                                                                                             
approximation was reasonable, we also did the calculations without the approximation, and the results 
were very similar. 
8 According to the IBGE (2008, p.44), “the National Accounts of the previous quarter are revised every 
time there is a new quarter’s  release, with the replacement of previous projections by actual data and the 
introduction of some revision of the data provided by the periodic surveys of the IBGE or other 
institutions. In the release of the third quarter of each calendar year, a broader revision is conducted, 
which incorporates the new weights of the annual National Accounts of two years ago, and possibly 
revisions in some methodological aspects. The previous year and the first and second quarters of the year 
are recalculated, incorporating the changes in the weights”. Furthermore, according to the IBGE (2008, 
p.41), the “annual changes estimated using the quarterly series are adjusted to the annual changes 
estimated by the National Accounts System in the first data release after the release of the annual 
accounts. The series are adjusted by means of the minimization of the square of the difference between 
the observed series and the adjusted one, subject to the restriction that the sum of the four quarters of a 
year, in the adjusted series, is equal to the total annual in the National Accounts System (Denton’s 
Method)” (authors’ translation). 
9 See the appendix for the graph of the GDP in level. 
11

(1.27 percent), and the trough in the 2001Q3 vintage (-0.99 percent). In the 2005Q3 
vintage, the figure was changed to 0.60 percent and has been kept since then. 
 
 
 
 
 
Figure 2 highlights the magnitude of the GDP growth revisions and the 
possible impact of data revisions on policy decisions. However, it is still a partial 
characterization since it refers to the behavior of the values of only one period 
(1996Q1). Figure 3 presents the relative frequency of GDP revision values. The graph 
shows that only in 30 percent of the time the revisions were close to zero (between -0.25 
p.p. and +0.25 p.p.). In 24 percent of the time, the magnitude of the revision was above 
1 p.p. In Figure 4, we can notice all real-time GDP figures (x-axis) and the 
corresponding final values (y-axis). When the point lies on the 45-degree line, the 
magnitude of the revision was zero. Observations above the line indicate positive 
revisions, whereas those below the line represent negative revisions. Furthermore, 
points in the upper left and lower right quadrants reveal changes in the growth sign after 
the revisions, which took place in 16 percent of the cases. 
 
-4
-3
-2
-1
0
1
2
3
4
1996
1998
2000
2002
2004
2006
2008
Final
Real time
Figure 1 – Final and real-time GDP growth (%) 
%
(quarter-over-quarter) 
12

Table 3 records the statistics for the quarter-over-quarter GDP growth rates 
series in real time and their corresponding final values as well as the statistics for the 
data revision series, calculated using the full set of vintages. We can notice that the 
average growth of real-time GDP was 0.63 percent, whereas that for the final figures 
stood at 0.75 percent. The average revision was 0.13 p.p. (the highest positive revision 
was 2.01 p.p., and the highest negative was -2.62 p.p.). The average revision is useful as 
an indicator of the revision bias, but it is limited as an indicator of the magnitude of the 
revisions since negative revisions offset positive ones and vice-versa. 
 
-1.5
-1.0
-0.5
0.0
0.5
1.0
1.5
1996
1997
1998
1999
2000
2001
2002
2003
2004
2005
2006
2007
2008
0
5
10
15
20
25
30
35
-2.5
-2
-1.5
-1
-0.5
0
0.5
1
1.5
2
-4
-3
-2
-1
0
1
2
3
4
-4
-3
-2
-1
0
1
2
3
4
45º line
Final values
Real-time values
Percent of the time
Revision in percentage points
Figure 2 – GDP growth of 1996Q1 over the revisions (%) 
Figure 3 – Relative frequency of the revision of  
                 the GDP values 
Figure 4 – GDP growth values (real-time versus final) 
Vintages 
%
(quarter-over-quarter) 
13

Table 4 records some additional revision indicators. Two of them are especially 
suitable to capture the magnitude of the revisions: the mean absolute revision (MAR) 
and the root mean square revision (RMSR). We can notice that the mean absolute 
revision was 0.67 p.p. In absolute terms, this means that, on average, the quarterly GDP 
growth was revised in 0.67 p.p. above or below the value initially released. The RMSR 
indicator is similar to the MAR, but penalizes more strongly revisions of larger 
magnitude. According to Table 4, RMSR was 0.89 p.p.10 
 
 
 
Besides, the two series have a correlation of 0.67, implying that the real-time 
series explains 44 percent of the variance of the final series. Table 4 also presents the 
N/S, OPSIGN, FRLA and AR indicators. N/S is a proxy for the noise-to-signal ratio, 
                                                      
10 Palis, Ramos and Robitaille (2004) found, for Brazil’s GDP growth between 1994Q2 and 2001Q4, an 
average revision of 0.13, a MAR of 0.88, and a RMSR of 1.11. 
Table 3
GDP Growth
(Quarter-on-quarter % change) - 1996Q1-2008Q2
Data
Mean
Standard Deviation
Minimum Value
Maximum Value
Real Time
0.63
1.04
-1.68
3.24
Final
0.75
1.12
-1.93
3.40
Revision
0.13
0.89
-2.62
2.01
Notes: Quarterly seasonally adjusted GDP series.
Due to rounding off, the sum of the means of real-time and revision series is different from the final series mean.  
Table 4
Revision indicators of the GDP growth
(Quarter-on-quarter % change) - 1996Q1-2008Q2
Mean 
Revision
MAR
RMSR
CORR
N/S
OPSIGN
FRLA
AR
0.13
0.67
0.89
0.67
0.79
0.16
0.26
-0.34
Notes: Quarterly seasonally adjusted GDP series.
MAR is the mean absolute revision.
RMSR is the root mean square revision.
CORR is the correlation betw een real-time and final GDP grow th.
N/S is a proxy for the noise-to-signal ratio (obtained by the ratio of the RMSR to the standard deviation of the final 
GDP grow th).
OPSIGN is the frequency in w hich real-time and final GDP grow th estimates have opposite signs.
FRLA is the frequency w ith w hich the absolue value of the revision is larger than the absolute value of the final 
GDP grow th.
AR is the first-order serial correlation of the revision series.
14

obtained by the ratio of the RMSR to the standard deviation of the GDP final estimate. 
Therefore, this measure captures the magnitude of the revisions in relation to the 
standard deviation of the final series. The N/S value is 0.79, meaning that the magnitude 
of the revisions is not very different from the series variability. 
 
 
OPSIGN is the frequency in which real-time GDP growth has the opposite sign 
to that of the final growth. Table 4 records an OPSIGN of 0.16, i.e. in 16 percent of the 
cases, the GDP growth data was revised such that its sign was changed. In turn, FRLA 
is the frequency in which the revision of GDP growth is higher than the final GDP 
growth, both in absolute values. Table 4 records an FRLA of 0.26, implying that the 
magnitude of the revision is greater than the magnitude of the final data in 26 percent of 
the cases. 
 
The revision indicators point that the GDP growth revisions are substantial. 
However, there is an important mitigating factor: the first-order serial correlation (AR) 
of the revision series is negative: -0.34. This implies that positive revisions of a quarter 
are usually followed by negative revisions in the following quarter and vice-versa. 
Therefore, if we aggregate the revision series, for instance, in annual periods, the 
revisions will tend to be less important. 
  
In order to check that, we also estimate the revisions of the growth rate of the 
GDP, calculated comparing the GDP of quarter i to that in i-previous quarter. In other 
words, we compare the current quarterly GDP to that up to four quarters ago. As we can 
see in Table 5, both the mean absolute revision per quarter (MAR/q) and the root mean 
square revision per quarter (RMSR/q), expressed in percentage points per quarter, 
decrease as the aggregation period increases.11 Furthermore, there is a reduction in the 
noise-to-signal ratio and a rise in the correlation between real-time and final GDP series. 
Thus, we can conclude that GDP revisions, although still relevant, become less 
important when the aggregation period increases. We should stress, however, that there 
is no significant improvement in the OPSIGN and FRLA indicators. 
 
                                                      
11 MAR/q corresponds to the MAR divided by the number of associated quarters, and RMSR/q 
corresponds to the RMSR divided by the number of associated quarters. 
15

Alternatively, we can assess the effect of the increase in the aggregation period 
by means of the growth rate of average GDP over i quarters compared to the average 
over i quarters before. Mathematically,12 
 
∆, 
 100 · ∑
,



∑
,





 .   
                   (2) 
 
In this case, it is reasonable to expect an improvement in the revision indicators 
as the aggregation period increases. When this measure is calculated in real time, only 
one GDP data point in the numerator did not go through any revision, and the 
denominator has data points that went through revision more times that the data point in 
the denominator of identity (1). In fact, Table 6 shows that this phenomenon does occur. 
There is a strong reduction in the MAR/q and RMSR/q indicators as the aggregation 
period rises. The mean absolute revision of the four-quarter GDP growth is 0.16 per 
quarter, corresponding to 0.64 in annual terms. Besides, there is a considerable 
improvement in the OPSIGN and FRLA indicators. 
 
                                                      
12  Note that, when i=1, equations (1) and (2) are equivalent to each other. 
Table 5
Revision indicators of the GDP growth
(Quarterly GDP compared with the i -th previous quarter) - 1996Q1-2008Q2
GDP growth rate in
Mean 
Revision/q
MAR/q
RMSR/q
AR
N/S
CORR
OPSIGN
FRLA
1 quarter
0.13
0.67
0.89
-0.34
0.79
0.67
0.16
0.26
2 quarters
0.07
0.41
0.50
0.14
0.64
0.80
0.18
0.26
3 quarters
0.07
0.32
0.39
0.11
0.62
0.82
0.10
0.30
4 quarters
0.08
0.23
0.29
0.42
0.52
0.89
0.16
0.22
Notes: Quarterly seasonally adjusted GDP series.
Mean revision/q is the mean revision divided by the number of quarters under analysis.
MAR/q is the mean absolute revision divided by the number of quarters under analysis.
RMSR/q is the root mean square revision divided by the number of quarters under analysis.
AR is the first-order serial correlation of the revision series.
N/S is a proxy for the noise-to-signal ratio (obtained by the ratio of the RMSR to the standard deviation of the final 
GDP grow th).
CORR is the correlation betw een real-time and final GDP grow th.
OPSIGN is the frequency in w hich real-time and final GDP grow th estimates have opposite signs.
FRLA is the frequency w ith w hich the absolue value of the revision is larger than the absolute value of the final 
GDP grow th.
16

We should pay attention to the change in methodology introduced by the IBGE 
as of the 2006Q4 vintage.13 The issue is whether that change is a relevant source of 
revisions. 
 
In Table 7, we seek to isolate the effect of the methodological change on the 
quarter-over-quarter GDP growth revisions from 1996Q1 through 2006Q4.14 The 
average real-time GDP growth was 0.55 percent per quarter. Using the 2006Q4 vintage 
with the previous methodology, the average GDP growth stood at 0.61 percent, whereas 
that with the new methodology was 0.66 percent. 
 
The lower part of Table 7 records a decomposition of the revision of the GDP 
growth up to 2006Q4. The average revision with the previous methodology was 0.66 
p.p. The introduction of the new methodology generated a further average revision of 
0.05 p.p., totaling 0.11 p.p. This means that, on average, the introduction of the new 
methodology increased the GDP growth estimates between 1996Q1 and 2006Q4. The 
                                                      
13 The quarterly GDP series also went under other methodological changes in the past. See Palis, Ramos 
and Robitaille (2004). 
14 In this analysis, real-time GDP growth in 2006Q4 (first line in Table 7) was calculated using the 
2006Q4 vintage with the previous methodology. 
Table 6
Revision indicators of the GDP growth 
(i -period average GDP compared with the previous period) - 1996Q1-2008Q2
Average GDP in
Mean 
Revision/q
MAR/q
RMSR/q
AR
N/S
CORR
OPSIGN
FRLA
1 quarter
0.13
0.67
0.89
-0.34
0.79
0.67
0.16
0.26
2 quarters
0.05
0.31
0.39
0.30
0.58
0.84
0.10
0.24
3 quarters
0.06
0.21
0.26
0.65
0.48
0.90
0.12
0.20
4 quarters
0.04
0.16
0.21
0.82
0.48
0.89
0.06
0.14
Notes: Quarterly seasonally adjusted GDP series.
Mean revision/q is the mean revision divided by the number of quarters under analysis.
MAR/q is the mean absolute revision divided by the number of quarters under analysis.
RMSR/q is the root mean square revision divided by the number of quarters under analysis.
AR is the first-order serial correlation of the revision series.
N/S is a proxy for the noise-to-signal ratio (obtained by the ratio of the RMSR to the standard deviation of the final 
GDP grow th).
CORR is the correlation betw een real-time and final GDP grow th.
OPSIGN is the frequency in w hich real-time and final GDP grow th estimates have opposite signs.
FRLA is the frequency w ith w hich the absolue value of the revision is larger than the absolute value of the final 
GDP grow th.
17

methodological change generated an additional MAR of 0.52 and an additional RMSR 
of 0.71, implying a change in the MAR from 0.53 to 0.75, and in the RMSR from 0.73 
to 0.97. Thus, those results indicate that, in fact, the methodological change was a 
relevant source of revisions, although it explains only part of the total revision. 
 
 
 
Table 8 proceeds to a similar exercise but for the year-over-year GDP growth 
rate (change in the quarterly GDP in relation to the GDP of the same quarter of the 
previous year). The average revision with the previous methodology was 0.18 p.p. The 
introduction of the new methodology generated a further average revision of 0.16 p.p., 
totaling 0.34 p.p. Furthermore, the methodological change led to a further MAR of 0.71 
and an additional RMSR of 0.93, implying a change in the MAR from 0.56 to 1.03, and 
in the RMSR from 0.74 to 1.25. Thus, Table 8 results reinforce the finding that the 
methodological change was a relevant source of revisions, although it does not preclude 
the importance of other factors. 
 
Table 7
GDP growth and methodological change in the 2006Q4 vintage
(Quarter-on-quarter % change) - 1996Q1-2006Q4
Mean
Standard 
Deviation
Minimum 
Value
Maximum 
Value
CORR
AR
MAR RMSR
Real Time(*)
0.55
1.07
-1.68
3.24
1.00
2006Q4 vintage with the previous methodology
0.61
1.02
-1.86
3.13
0.75
2006Q4 vintage with the new methodology
0.66
1.16
-1.93
3.40
0.62
Revision decomposition in 2006Q4
Revision with the previous methodology
0.06
0.74
-2.75
1.61
-0.26 0.53 0.73
Additional revision with the new methodology
0.05
0.72
-1.87
1.84
-0.38 0.52 0.71
Total revision in 2006Q4 with the new methodology 0.11
0.97
-2.62
2.13
-0.40 0.75 0.97
Notes: Quarterly seasonally adjusted GDP series.
CORR is the correlation of real time and final GDP grow th.
AR is the first-order serial correlation of the revision series.
MAR is the mean absolute revision.
RMSR is the root mean square revision.
(*) The 2006Q4 real-time GDP grow th w as computed by using the 2006Q4 vintage referring to the previous methodology.
18

To compare the revision indicators of this paper with those found for other 
countries, we use the results of Table 9 and 10. We should stress that those comparisons 
do not allow us compare the quality of the data produced by the statistics institutions of 
different countries. We are measuring the estimate errors that were corrected 
subsequently (assuming that the revisions improve the estimates) and not the total error 
of the real-time estimates (we do not know the true errors associated with the final 
estimates of each country). 
 
Table 9 compares some revision indicators for the Brazilian GDP with those 
from Cayen and van Norden’s (2004) study for Canada. We can note that the revision 
bias is higher in the Canadian case for two- and four-quarter growth rates. However, the 
magnitude of the revisions is greater in the Brazilian case (RMSR/q). Besides, the 
Canadian real-time data series are a little more correlated with the final series than in 
Brazil. In both cases, the magnitude of the revision becomes less important as the 
aggregation period increases. Furthermore, for both countries, AR is negative for one-
quarter GDP growth and positive for two- and four-quarter growth rates. 
 
Table 8
GDP growth and methodological change in the 2006Q4 vintage
(Year-on-year growth rate) - 1996Q1-2006Q4
Mean Standard 
Deviation
Minimum 
Value
Maximum 
Value
CORR
AR
MAR RMSR
Real Time(*)
2.06
2.33
-2.50
6.42
1.00
2006Q4 vintage with the previous methodology
2.24
2.08
-1.98
6.05
0.95
2006Q4 vintage with the new methodology
2.40
2.13
-1.96
7.14
0.85
Revision decomposition in 2006Q4
Revision with the previous methodology
0.18
0.72
-1.40
1.83
0.11 0.56 0.74
Additional revision with the new methodology
0.16
0.93
-2.58
2.11
0.41 0.71 0.93
Total revision in 2006Q4 with the new methodology 0.34
1.22
-2.57
2.33
0.40 1.03 1.25
Notes: Quarterly seasonally adjusted GDP series.
CORR is the correlation betw een real-time and final GDP grow th.
AR is the first-order serial correlation of the revision series.
MAR is the mean absolute revision.
RMSR is the root mean square revision.
(*) The 2006Q4 real time GDP grow th w as computed by using the 2006Q4 vintage referring to the previous methodology.
19

Table 10 compares the indicators of mean revision and MAR for Brazil with 
those analyzed by Ahmad, Bournot and Koechlin (2007) for several countries. We can 
notice that, in general, the biases are positive, as in the Brazilian case. The MAR in 
most of the cases is lower than the Brazilian one. The exceptions are Japan, for 1996Q1-
2000Q4, and the United Kingdom, for 1982Q1-1993Q4. In spite of the limitations of 
this type of comparisons, those results point to the importance of analyzing the limits of 
the use of real-time data in the Brazilian case. 
 
 
Table 9
Revision indicators of the GDP growth 
Comparison with Cayen and van Norden (2004) (*)
Brazil
Canada
Brazil
Canada(^)
Brazil
Canada
Brazil
Canada
1 quarter
0.13
0.13
0.89
0.62
-0.34
-0.21
0.67
0.75
2 quarters
0.07
0.11
0.50
0.39
0.14
0.25
0.80
0.87
4 quarters
0.08
0.11
0.29
0.26
0.42
0.60
0.89
0.92
Notes: Quarterly seasonally adjusted GDP series.
Mean revision/q is the mean revision divided by the number of quarters under analysis.
RMSR/q is the root mean square revision divided by the number of quarters under analysis.
AR is the first-order serial correlation of the revision series.
CORR is the correlation betw een real-time and final GDP grow th.
(*) Period of analysis: Brazil: 1996Q1-2008Q2; Canada: 1972Q1-2003Q4.
(^) Computed in this w ork by using the means and standard deviations presented in the original w ork.
CORR
GDP growth rate in
Mean Revision/q
RMSR/q
AR
Table 10
Revision indicators of the GDP growth  (quarter-on-quarter change)
Comparison with Ahmad, Bournot e Koechlin (2007) 
Country
Period
Mean Revision
MAR
 Brazil 
1996Q1-2008Q2
0.13
0.67
Canada 
1996Q1-2000Q4
0.20
0.28
1980Q1-1993Q4
0.08
0.39
France
1996Q1-2000Q4
0.10
0.27
1980Q1-1993Q4
0.05
0.29
Germany
1996Q1-2000Q4
-0.08
0.40
1980Q1-1993Q4
0.05
0.60
Italy
1996Q1-2000Q4
0.13
0.39
1987Q1-1993Q4
0.10
0.38
Japan
1996Q1-2000Q4
0.22
1.02
1980Q2-1993Q4
-0.01
0.50
United Kingdom
1996Q1-2000Q4
0.16
0.34
1982Q1-1993Q4
0.18
0.80
United States
1996Q1-2000Q4
0.06
0.38
1980Q1-1993Q4
0.04
0.42
Notes: Quarterly seasonally adjusted GDP series.
MAR is the mean absolute revision.
20

4. Output Gap 
 
The output gap is usually defined as the difference between output (GDP) and 
the potential output (potential GDP). In practical terms, the output gap is usually 
obtained by means of methods that estimate the trend, and it is then calculated as the 
deviation of the output from the trend.15 
 
4.1. Methods for detrending output 
 
We can decompose the output into a trend component (potential output) and a 
cycle element (output gap): 
 
  
   ,                      
   
 
 
 
 
       (3) 
 
where  is the logarithm of GDP, 
 is the logarithm of the potential output, and  is 
the output gap in period t. 
 
We use four detrending methods: the Hodrick-Prescott (HP) filter, linear trend 
(LT), quadratic trend (QT), and the Harvey-Clark model of unobserved components 
(HC).16 
 
The HP filter, introduced by Hodrick and Prescott (1997),17 may be the most 
popular method to obtain the output gap estimates. The potential output component is 
obtained through the minimization of the following loss function: 
                                                      
15 This measure is not necessarily consistent with the output gap definition of the new Keynesian theory. 
In the new Keynesian approach, the output gap is the deviation of the output from the output that would 
prevail with fully flexible prices and wages. Although theoretically appealing, that definition is much 
harder to be measured in practical terms. Thus, the use of detrending methods is the most usual way to 
estimate the output gap. 
16 Note that we do not include the production function-based method. The reason is that the main 
variables used in this method are the unemployment rate and the rate of capacity utilization. For an 
application of different methods to estimate the output gap in Brazil, see, for example, Araújo and Guillén 
(2008). 
17Although Hodrick and Prescott’s article was published in 1997, the related working paper appeared in 
1981. 
21

  ∑
 	 




 
 ∑
∆

	 ∆


	

 ,   
 
 
       (4) 
 
where 
 is the smoothing parameter and T is the sample size. The parameter 
 is a 
positive number that penalizes the variability of the potential output growth. A change 
in this parameter affects the sensitivity of the potential output to GDP changes. As 

 
 ∞, the minimization generates a constant potential output growth (in this case, the 
HP filter is equivalent to the linear trend method). On the other hand, as 
 
 0, the 
potential output follows fully the GDP (potential output is equal to actual GDP), turning 
the cyclical component (the output gap) zero. As usual, we use the value suggested by 
Hodrick and Prescott (1997) for the smoothing parameter, 
=1600. Once 
 is 
calculated, we can obtain the output gap from equation (3). 
 
The linear trend is the simplest method to obtain the output gap. We estimate 
the following regression: 
 
       ,        1, … , .   
 
 
 
 
       (5) 
 
The fitted values of  correspond to the estimated potential output, and the residual 
series corresponds to the output gap series. 
 
The quadratic trend is an extension of the linear trend as it adds a quadratic 
term. Thus, the procedure is similar to that in the case of the linear trend, except for 
estimating the following equation instead: 
 
         ,        1, … , . 
 
 
 
       (6) 
 
Finally, the Harvey-Clark method, introduced by Harvey (1985) and Clark 
(1987), uses a model of unobserved components to decompose the GDP into a 
permanent component (potential output) and a transitory one (output gap):18 
                                                      
18 We included the Harvey-Clark method in our analysis because it is probably the most popular 
detrending method among unobserved-components models. Besides, the choice for the Harvey-Clark 
method (among a large variety of unobserved-components models) allows us to compare the results with 
those of the international studies that analyzed output gap revisions. On the other hand, there are 
22

  
   
 
 
 
 
 
 
    
       (7) 

  	  	

  ,                ~ 
. 
. 
. 0,  

   
 
 
       (8) 
  	  ! ,                             !~ 
. 
. 
. 0,  


   
 
 
       (9) 
  "	  "	   ,      ~ 
. 
. 
. 0,  


. 
 
                 (10) 
 
Equation (7), which is identical to equation (3), is the decomposition of the GDP into 
potential output and output gap. Equation (8) assumes that that potential output follows 
a random walk with drift, and equation (9) assumes that the drift term follows a random 
walk. By equation (10), the output gap follows an autoregressive process of order two 
— AR(2). The processes , ! and   are mutually non-correlated. Alternatively, the 
model can be represented in the following state-space form: 
 
  &1   1   0   0' (



	

)    
 
 
 
 
        
     (11) 
 
(



	

)  (
1
0     0
1
0    "  "   0
0
1     0
0
0
0     0
1
) (
	

	
	
	
)  (


0
!
) ,  
 
            
     (12) 
 
where 
,  and  are the unobservable variables to be estimated. The variances of the 
three shocks and the coefficients " and " are the five parameters to be estimated. The 
model is estimated using maximum likelihood, implemented using the Kalman filter.19 
 
 
 
 
                                                                                                                                                             
detrending models of unobserved components that incorporate a Phillips curve in their specifications. 
However, the choice of one of these methods would not be feasible as the sample size is not sufficient to 
conduct recursive estimates since we have to disregard data of the high inflation period, previous to the 
introduction of Real in 1994. 
19 The estimations of Harvey-Clark’s model were conducted using Gauss, adapting a code of Kim and 
Nelson (1999), which is available on the internet: http://www.econ.washington.edu/user/cnelson/ 
markov/prgmlist.htm. 
23

4.2. Components of the output gap revisions 
 
Based on Orphanides and van Norden’s (2002) methodology, we analyze the 
behavior of the output gap estimates at the end of the sample and their revisions. To this 
end, we calculate three groups of output gap estimates: i) final estimates; ii) real-time 
estimates; and iii) “quasi-real” estimates. 
 
The final estimates of the output gap are conducted with the last vintage of 
GDP data used in this paper (2008Q2). The resulting series is comprised of final gaps. 
This is the usual way of estimating output gaps, employed in works that do not take into 
account the presence of data revision. 
 
We obtain the real-estimates estimates of the output gap in two steps. First, the 
output gaps are estimated for all available vintages, that is, for each vintage, we estimate 
the corresponding gap series. In the second step, we take the last observation of each 
gap series. The resulting series is comprised of the real-time output gaps. The series 
contains, in each quarter, the first output gap estimate that agents could have accessed.20 
 
The total output gap revision in each period is the difference between the final 
and the real-time gaps. This revision can be decomposed further into two sources: i) 
GDP data revisions; and ii) increase in the number of periods as time goes by (sample 
size effect).21 To isolate the importance of those sources, we estimate a third group of 
output gap estimates: quasi-real estimates. 
 
The quasi-real estimates of the output gap are calculated using the same 
sample size of the real-time estimates, but employing final instead of real-time data; so 
the sample is truncated in each considered period. Initially we estimate the output gap 
series using final data until 1996Q1; then we estimate a new series using final data up to 
1996Q2; and so on, until we estimate the last series using data up to 2008Q2. 
Subsequently, we take the last observation from each estimated series. The resulting 
                                                      
20 We should stress that the vintage and, therefore, the output gap estimate of quarter t is available for 
economic agents in quarter t+1.   
21 Part of the effect in both cases is due to the reestimation of seasonal factors.  
24

series consists of quasi-real output gaps. The difference between quasi-real and real-
time gaps stems from GDP data revisions since the estimates of the two series in each 
quarter are conducted with a sample that covers exactly the same period. On the other 
hand, the difference between the final and quasi-real estimates captures the effect of the 
sample increase. 
 
Our revision analysis consists basically in measuring the estimate changes as 
data is revised and the information set rises (i.e., as GDP data about new periods are 
released). We assume implicitly that revisions improve the output gap estimates. 
However, it is reasonable to assume that some degree of uncertainty remains in the last 
vintage of the output gap. This vintage will likely be revised or, even if this were not the 
case, it will have the methodological limitations of any GDP estimate. Furthermore, 
even with a perfectly measured GDP, the output gap is an unobservable variable, 
implying that any estimate conveys a non-negligible degree of uncertainty. Thus, the 
total revision captures part of the measurement error associated with the output gap 
estimated using real-time data. 
 
Since our methodology neither associates the revisions with specific 
applications (forecasting, monetary policy analysis, etc.) nor requires assumptions about 
the true structure of the economy or about the true data generating process, the results 
are fairly general. However, we should be cautions and not compare the adequacy of the 
different methods of calculating the output gap based on the size of the revisions. 
Assuming that revisions improve the estimates, we are measuring the estimate errors 
that are subsequently corrected, and not the total error of the estimates in real time.22 
 
4.3. Analysis of output gap total revisions 
 
Figure 5(a) shows the real-time output gap series for the four considered 
methods. The shaded area of Figure 5(b) presents, for each time period, the interval in 
which the estimated output gaps lie. That range can be interpreted as a measure of 
                                                      
22 Suppose that the series based in method A has lower revisions than that from method B. However, it is 
possible that the final estimates of the former are more imprecise than those from the latter, and thus we 
cannot conclude that method A is superior to method B.  
25

uncertainty in the sense of “thick modeling”.23 The four output gap series have strong 
short-run co-movements. All cross correlations are superior to 0.70, except for that 
between LT- and QT-based series. 
 
 
 
 
 
Figure 6 presents two graphs that are similar to the previous ones, but 
recording the final output gap series, estimated using the 2008Q2 vintage. All cross 
correlations are positive, and their values, except for those involving the Harvey-Clark 
method, are high. 
 
 
 
 
                                                      
23 See Granger and Jeon (2004). 
-6
-4
-2
0
2
4
6
1996
1998
2000
2002
2004
2006
2008
HP
LT
QT
HC
-6
-4
-2
0
2
4
6
1996
1998
2000
2002
2004
2006
2008
-6
-4
-2
0
2
4
6
1996
1998
2000
2002
2004
2006
2008
HP
LT
QT
HC
-6
-4
-2
0
2
4
6
1996
1998
2000
2002
2004
2006
2008
Figure 6 (a) – Final output gap 
Figure 6 (b) – Final output gap – Thick Modeling 
Figure 5 (b) – Real-time output gap – Thick Modeling 
%
%
%
%
Figure 5 (a) – Real-time output gap 
26

The real-time series have important differences with respect to the final ones. 
Figure 7 compares both series, estimated using the HP filter. The correlation between 
the series is 0.64. The real-time series have higher variability and, in 30 percent of the 
cases, the signs of the observations are opposite to those of the final series.24 
 
 
 
To illustrate the importance of the output gap revisions, Figure 8 depicts the 
behavior of HP-based output gap estimates for 1996Q1 over time. When the output gap 
was initially estimated (with the 1996Q1 vintage), the gap was -0.52 percent of the 
GDP. In the 1996Q4 vintage, it was revised to the trough of -1.11 percent, and, in the 
2001Q1 vintage, it peaked at 0.31 percent. In the 2006Q4 vintage, in turn, it was revised 
to -0.16 percent, kept constant afterwards. Again, as in the case of the GDP revisions, 
the figure highlights the magnitude of the revisions. 
 
Figure 9 records the relative frequency of the values of the output gap 
revisions. It shows that only in 15 percent of the cases the revisions were close to zero 
(between -0.25 p.p. and +0.25 p.p.). In 32 percent of the time, the magnitude of the 
                                                      
24 See the appendix for graphs analogous to that of Figure 7 for the methods of linear trend, quadratic 
trend and Harvey-Clark. 
-4
-3
-2
-1
0
1
2
3
4
1996
1998
2000
2002
2004
2006
2008
Final HP-filtered output gap
Real-time HP-filtered output gap
Figure 7 – Final and real-time HP-based output gaps 
%
27

revision was greater than 1 p.p. Figure 10 records all HP-based real-time output gaps (x-
axis) and the associated final values (y-axis). When the points lie on the 45-degree line, 
the revisions were zero. Points that are above that line indicate upward revisions, 
whereas those below, downward revisions. Observations that are in the upper left and 
lower right quadrants reveal changes in the sign after the revisions, which occurred in 
30 percent of the time.25 
 
 
 
 
 
 
  
 
 
                                                      
25 See the appendix for graphs analogous to those of Figures 8 to 10 for the other methods. 
-1.2
-1.0
-0.8
-0.6
-0.4
-0.2
0.0
0.2
0.4
1996
1997
1998
1999
2000
2001
2002
2003
2004
2005
2006
2007
2008
0
5
10
15
20
25
30
-2
-1.5
-1
-0.5
0
0.5
1
1.5
2
2.5
-4
-3
-2
-1
0
1
2
3
4
-4
-3
-2
-1
0
1
2
3
4
45º line
Final values
Real-time values
Percent of the time
Revision in percentage points
Figure 8 – Output gap (HP filter) of 1996Q1 over the revisions (% of GDP) 
Figure 9 – Relative frequency of the revision of the 
 values of the HP-based output gap 
Figure 10 – HP-based output gap values 
(real-time versus final)
Vintages 
%
28

Table 11 records some descriptive statistics for the series of output gap and 
their revisions. As expected, the linear trend-based output gap series have greater 
amplitude and standard deviation than HP-based series does. Since the HP smoothing 
parameter is 
=1600* ∞, potential output follows more closely GDP than in the linear 
trend case, implying lower variability and amplitude for the resulting output gap series. 
Furthermore, potential output generated by the Harvey-Clark method was the one that 
more closely followed the GDP series,26 implying a gap series with lower standard 
deviation and amplitude. No total mean revision — difference between the averages of 
final and real-time output gap series — was negative. 
 
 
 
                                                      
26 Note that, in the case of the real-time and quasi-real series, this claim refers only to the GDP and 
potential output of the last period of each estimation, since the gap that is included in these series is 
always the last period’s gap of each estimation. 
Table 11
Output Gap (%)
1996Q1-2008Q2
            Method
Mean
Standard 
Deviation
Minimum Value
Maximum Value
  Hodrick-Prescott (HP)
        Real-time
-0.04
1.37
-3.91
1.93
        Quasi-real
0.11
1.37
-3.03
3.06
        Final
0.01
1.18
-2.32
2.55
        Total Revision
0.04
1.09
-1.77
2.75
  Linear Trend (LT)
        Real-time
-0.55
2.58
-5.36
5.62
        Quasi-real
-0.17
2.45
-4.03
5.62
        Final
-0.15
2.45
-4.54
5.62
        Total Revision
0.40
1.08
-1.51
2.97
  Quadratic Trend (QT)
        Real-time
0.01
2.25
-4.56
4.33
        Quasi-real
0.54
2.35
-3.53
4.46
        Final
0.01
2.23
-4.26
4.65
        Total Revision
0.00
2.80
-3.88
5.52
  Harvey-Clark (HC)
        Real-time
-0.19
1.04
-2.89
1.31
        Quasi-real
0.13
0.93
-2.09
2.13
        Final
0.10
0.77
-1.68
1.78
        Total Revision
0.29
0.74
-1.38
2.20
Notes: The data sample for the output gap estimation starts in 1990Q1.
Due to rounding off, the sum of real-time gap and total revision means may be different from final gap mean.  
29

Table 12 shows several revision indicators. The mean revision, also recorded in 
the previous table, was higher for the LT (0.40 p.p.) and HC (0.29 p.p.) methods. The 
mean revision was only 0.04 for the HP method, and zero for the QT method. Although 
high revision mean figures imply substantial magnitude of revisions, low values do not 
necessarily imply a low magnitude since negative revisions may offset positive 
revisions and vice-versa. In fact, the mean revision measure is more appropriate to 
gauge the bias of the revision than its magnitude. 
 
 
 
In order to measure the magnitude of the revisions, we use the same indicators 
used for GDP growth: the mean absolute revision (MAR) and the root mean square 
revision (RMSR). According to those indicators, the output gap measured by all the 
analyzed methods was revised substantially. The QT-based gap, which has a zero mean 
revision, had the largest MAR (2.16 p.p.). In absolute terms, this means that the QT-
based output gaps were revised 2.26 p.p. on average, above or below the real-time initial 
release. The lowest MAR corresponds to the HC method (0.59 p.p.). The MAR of HP- 
and LT-based gaps was 0.84 p.p. and 0.89 p.p., respectively. Furthermore, the RMSR, 
which penalizes more strongly the larger revisions, is high for all the methods. 
 
The first-order correlation (AR) shows the degree of persistence of the 
revisions. A high persistence reveals that the “errors” of the real-time gap estimates 
Table 12
Revision Indicators - Output Gap (%)
1996Q1-2008Q2
Mean 
Revision
MAR
RMSR
AR
N/S
CORR
OPSIGN
FRLA
Hodrick-Prescott (HP)
0.04
0.84
1.08
0.63
0.92
0.64
0.30
0.46
Linear Trend (LT)
0.40
0.89
1.15
0.47
0.47
0.91
0.14
0.16
Quadratic Trend (QT)
0.00
2.26
2.78
0.91
1.25
0.21
0.44
0.60
Harvey-Clark (HC)
0.29
0.59
0.78
0.57
1.01
0.71
0.30
0.52
Notes: The data sample for the output gap estimation starts in 1990Q1.
MAR is the mean absolute revision.
RMSR is the root mean square revision.
AR is the first-order serial correlation of the revision series.
N/S is a proxy for the noise-to-signal ratio (obtained by the ratio of the RMSR to the standard deviation of 
the final output gap).
CORR is the correlation betw een real-time and final output gap.
OPSIGN is the frequency w hich real-time and final output gap estimates have opposite signs.
FRLA is the frequency w ith w hich the absolue value of the revision is larger than the absolute value of the final gap.
30

(considering that the final estimates are the “best” available estimates) persist over long 
periods. In this case, real-time output gap estimates may lead policy makers and other 
economic agents to mistaken perceptions about the business cycle state.27 Among the 
analyzed methods, the series of revision of the QT method shows the highest 
persistence (0.91) and that of the LT method, the lowest (0.47). 
 
The noise-to-signal ratio (N/S) is an important measure because it considers the 
differences in the variability of the gaps estimated by the different methods. The QT- 
and HC-based gaps show N/S values greater than 1, whereas for the HP it is 0.92. In the 
case of linear trend, the N/S ratio is relatively low (0.47), at the same time the 
correlation between final and real-time gaps is the highest (0.91). This means that the 
real-time series of the LT explains 81 percent of the variance of the final series. The 
lowest correlation coefficient was that of the QT method, 0.21 – the real-time series 
explains only 5 percent of the variance of the final series. 
 
However, we should note that the correlations can underestimate the 
importance of the revisions because they do not take into account the level of the series. 
Thus, we also use a further indicator, OPSIGN, which is the relative frequency in which 
the sign of the real-time output gap is different from that of the final estimate. This 
indicator is particularly important to assess the capability of the output gap to point 
whether monetary policy is tight or loose. The absence of any revision or change in the 
sign would generate a zero value for the OPSIGN. If we replaced the real-time series by 
a Gaussian white noise, we would obtain a value close to 0.50. Table 12 shows a high 
OPSIGN for three out of the four methods:  QT (0.44), HP (0.30) and HC (0.30). For 
instance, this means that 44 percent of the real-time gaps estimated by the QT method 
show the “wrong” sign. The LT method presents the lowest OPSIGN (0.14). 
 
                                                      
27 High persistence does not mean that revisions are predictable, but implies that future information will 
affect the output gap estimates of consecutive periods in a similar way. For instance, let say the real-time 
gap for a specific period is a substantial positive value. However, let’s assume that the final gap for the 
same period ends up showing that the gap was negative. In this case, in real time, based only on the gap 
measure, economic agents would have a mistaken perception about the business cycle state. If the AR 
parameter is high (i.e., if the series shows high persistence), this implies that the mistaken perception 
about the business cycle tends to persist over several quarters. 
31

Finally, Table 12 records the FRLA indicator, which is the relative frequency 
in which the gap revision is greater than the final gap, both in absolute values. FRLA is 
superior to 0.50 for the QT and HC methods, indicating that, in more than 50 percent of 
the cases, the magnitude of the revisions is higher than the magnitude of the final gap. 
The HP gap also has large FRLA, 0.46, whereas the lowest is that of LT, 0.16. 
 
Although, based on the revisions, we are not able to compare the methods 
according to their capacity of estimating the gaps correctly — we do not know the true 
errors associated with the final estimates of each method — some considerations about 
the revisions are warranted. Notwithstanding the quadratic trend-based output gap does 
not have revision bias (the total average revision is zero), in general, it has the most 
unfavorable revision indicators — the highest MAR, RMSR, N/S, FRLA, and AR, the 
lowest correlation between the real-time and final series, and the highest relative 
frequency of wrong signs. On the other hand, although the linear trend-based gap has 
the highest bias and large MAR and RMSR indicators, it shows the most favorable 
results for other revision indicators — the lowest N/S, FRLA, AR, and relative 
frequency of wrong signs (OPSIGN), and the highest correlation between the real-time 
and final series. 
 
In order to compare our indicators to those of other countries, Table 13 records 
also the revision indicators of the output gap estimated in studies for the United States, 
Canada and Norway. In general, the revision indicators in these countries are even more 
unfavorable. In most of the cases, the revisions show higher RMSR, AR, N/S, OPSIGN 
and FRLA, and lower correlation between the final and real-time gaps. For some 
indicators, however, the QT-based output gaps for the U.S. and Canada had results more 
favorable than those for Brazil. 
 
32

4.4. Decomposition of the output gap revisions 
 
As stressed in Section 4.2, the total output gap revisions can be decomposed 
into two components — part associated with the GDP series revision, and part related to 
the sample size (revisions associated with the increase in the sample are mainly related 
Table 13
Revision Indicators - Output Gap (%)
Results of some studies (*)
Mean 
Revision
MAR
RMSR
AR
N/S
CORR
OPSIGN
FRLA
Hodrick-Prescott (HP)
      Brazil
0.04
0.84
1.08
0.63
0.92
0.64
0.30
0.46
      United States (+)
0.30
**
1.83
0.93
1.11
0.49
0.41
**
      Canada (++)
0.33
**
1,85(^)
0.93
1,23(^)
0.38
0.45
**
      Norway (+++)
0.02
**
2,13(^)
0.73
1.53
-0.01
0.53
0.75
Linear Trend (LT)
      Brazil
0.40
0.89
1.15
0.47
0.47
0.91
0.14
0.16
      United States (+)
4.78
**
5.12
0.91
1.32
0.89
0.49
**
      Canada (++)
12.51
**
13,65(^)
0.99
1,48(^)
0.81
0.51
**
      Norway (+++)
1.79
**
2,58(^)
0.82
0.79
0.83
0.25
0.33
Quadratic Trend (QT)
      Brazil
0.00
2.26
2.78
0.91
1.25
0.21
0.44
0.60
      United States (+)
1.25
**
2.91
0.96
1.07
0.58
0.35
**
      Canada (++)
3.33
**
5,12(^)
0.99
1,30(^)
0.60
0.40
**
      Norway (+++)
-4.39
**
5,66(^)
0.94
1.53
0.33
0.44
0.64
Harvey-Clark (HC)
      Brazil
0.29
0.59
0.78
0.57
1.01
0.71
0.30
0.52
      United States (+)
1.17
**
1.82
0.92
0.84
0.77
0.34
**
      Canada (++)
1.62
**
2,82(^)
0.92
2,03(^)
-0.19
0.63
**
      Norway (+++)
0.58
**
3,15(^)
0.83
1.00
0.22
0.53
0.53
Notes: The data sample for the output gap estimation starts in 1990Q1 for Brazil, in 1947Q1 for the United States,
and in 1947Q1 for Canada. This information is not available for Norw ay .
MAR is the mean absolute revision.
RMSR is the root mean square revision.
AR is the first-order serial correlation of the revision series.
N/S is a proxy for the noise-to-signal ratio (obtained by the ratio of the RMSR to the standard deviation of 
the final output gap).
CORR is the correlation betw een real-time and final output gap.
OPSIGN is the frequency in w hich real-time and final output gap estimates have opposite signs.
FRLA is the frequency w ith w hich the absolue value of the revision is larger than the absolute value of the final gap.
(*) Analysis periods: Brazil: 1996Q1-2008Q2; United States: 1966Q1-1997Q4; Canada: 1972Q1-2003Q4; 
Norw ay: 1993Q1-2002Q1.
(**) Not available.
(^) Computed in this w ork by using the means and standard deviations presented in the original w orks.
(+) Orphanides and van Norden (2002). 
(++) Cayen and van Norden (2005).
(+++) Bernhardsen et al. (2004).
33

to the low precision of the end-of-sample estimates of the output trend). Those 
components are identified in Table 14.28 
 
 
 
In the HP method, the positive bias generated by the data revision (0.15 p.p.) is 
largely offset by the negative bias resulted from the sample increase (-0.11 p.p.). The 
MAR, RMSR and N/S indicators show that both data revision and the sample increase 
are relevant to explain the magnitude of total revisions. For instance, the MAR coming 
from the data revision is 0.60 p.p., and the one stemming from the sample increase is 
1.02 p.p.  However, we cannot assert in an unambiguous way that the sample increase 
accounts for the largest part of the total MAR since, without that effect, the MAR would 
                                                      
28 In Table 14, the “total revision” refers to the series obtained by the difference between the final and 
real-time series; the “effect of the data revision” refers to the series obtained by the difference between 
the quasi-real and real-time series; and the “effect of the sample size” refers to the series obtained by the 
difference between the final and quasi-real series. 
Table 14
Decomposition of Output Gap Revision (%)
1996Q1-2008Q2
           Method
Mean
Standard 
Deviation
Minimum 
Value
Maximum 
Value
MAR
RMSR
N/S
AR
  Hodrick-Prescott (HP)
       Total revision
0.04
1.09
-1.77
2.75
0.84
1.08
0.92
0.63
       Data revision effect
0.15
0.79
-2.49
1.73
0.60
0.80
0.68
0.39
       Sample size effect
-0.11
1.21
-1.84
2.42
1.02
1.20
1.02
0.97
  Linear Trend (LT)
       Total revision
0.40
1.08
-1.51
2.97
0.89
1.15
0.47
0.47
       Data revision effect
0.38
1.47
-3.08
3.28
1.19
1.50
0.61
0.72
       Sample size effect
0.02
1.67
-1.93
2.93
1.45
1.66
0.68
0.98
  Quadratic Trend (QT)
       Total revision
0.00
2.80
-3.88
5.52
2.26
2.78
1.25
0.91
       Data revision effect
0.52
0.78
-1.66
2.12
0.69
0.93
0.42
0.36
       Sample size effect
-0.52
3.15
-4.24
5.17
2.79
3.17
1.42
0.96
  Harvey-Clark (HC)
       Total revision
0.29
0.74
-1.38
2.20
0.59
0.78
1.01
0.57
       Data revision effect
0.32
0.67
-1.57
1.97
0.55
0.73
0.94
0.42
       Sample size effect
-0.03
0.33
-0.55
0.80
0.28
0.33
0.42
0.77
Notes: The data sample for the output gap estimation starts in 1990Q1.
MAR is the mean absolute revision.
RMSR is the root mean square revision.
N/S is a proxy for the noise-to-signal ratio (obtained by the ratio of the RMSR to the standard deviation of 
the final output gap).
AR is the first-order serial correlation of the revision series.
34

be 0.60 p.p., close to the total MAR, of 0.84 p.p. In other words, at the margin, the 
effect of the sample size raised the MAR by 0.24 p.p. Similar reasoning applies to the 
case of the RMSR and N/S indicators. Figure 11 depicts the quasi-real and real-time 
series of the HP-based output gap. The difference between them is the revision of the 
gaps due to the GDP data revision. Figure 12, in turn, presents the final and real-time 
output gap series.29 The difference between them is the revision stemming from the 
sample increase. The effect of the sample increase, in turn, includes the border problem 
of the HP filter.30 
 
 
 
 
 
In the case of the LT method, the total revision bias (0.40 p.p.) stems basically 
from the data revision (0.38 p.p.). However, the MAR, RMSR and N/S indicators show 
that the effect of the sample increase is also important to explain the magnitude of the 
total revision. 
 
                                                      
29 See the appendix for graphs analogous to those of Figures 11 and 12 for the other three detrending 
methods. 
30 Close to the end of the sample, the HP filter eliminates cycles with frequency higher than it is supposed 
to eliminate. See Baxter and King (1999), and Mise, Kim and Newbold (2005). 
-4
-3
-2
-1
0
1
2
3
4
1996
1998
2000
2002
2004
2006
2008
HP-based real-time output gap
HP-based quasi-real output gap
Figure 11 – HP-based output gap – Real-time and quasi-real series 
%
35

In the QT method, the total revision does not have bias. However, this results 
from a positive bias (0.52 p.p.) generated by the data revision that is fully offset by a 
negative bias arising from the sample increase (-0.52 p.p.). The MAR, RMSR, and N/S 
indicators show that the effect of the sample increase is highly superior to the effect of 
the data revision on the magnitude of total revision. 
 
In the HC method, the total revision bias (0.29 p.p.) is basically due to the data 
revision (0.32 p.p.), offset only partially by the negative bias from the sample increase 
(-0.03 p.p.). Differently from the previous methods, the MAR, RMSR, and N/S 
indicators show that the effect of the data revision is greater than the effect of the 
sample increase on the magnitude of total revision. 
 
Therefore, in general, in order to explain the magnitude of the total revision, 
the effect of both the sample increase and the data revision are relevant. However, in the 
QT method, the effect of the sample increase is clearly more important, whereas in the 
HC method the effect of the data revision is preponderant. Besides, in all methods, the 
largest part of the persistence of the total revision series comes from the sample 
increase. 
-4
-3
-2
-1
0
1
2
3
4
1996
1998
2000
2002
2004
2006
2008
HP-based quasi-real output gap
HP-based final output gap
Figure 12– HP-based output gap – Quasi-real and final series 
%
36

On the other hand, in most of the cases, the largest part of the total revision 
bias stems from the data revision. Table 15 suggests that this is largely due to the 
methodological change in the GDP calculation introduced with the 2006Q4 vintage. 
With the previous methodology, in all methods, most of the bias up to 2006Q4 arose 
from the sample size. With the introduction of the new methodology, the bias coming 
from the data revision became predominant. 
 
 
 
In order to compare the decomposition of the revisions in Brazil with the 
results found in studies for other countries, we use Table 16, which shows some 
indicators of revision decomposition for Brazil, United States, Canada and Norway. 
Among those, the most adequate to assess the decomposition of the total revision 
Table 15
Output gap bias and the 2006Q4 methodological change
1996Q1-2006Q4
Previous methodology (*)     
New methodology (**) 
  Hodrick-Prescott (HP)
       Total revision
0.28
0.22
       Data revision effect
-0.01
0.13
       Sample size effect
0.28
0.08
  Linear Trend (LT)
       Total revision
1.59
1.25
       Data revision effect
-0.14
0.37
       Sample size effect
1.73
0.88
  Quadratic Trend (QT)
       Total revision
0.61
0.48
       Data revision effect
0.13
0.55
       Sample size effect
0.49
-0.07
  Harvey-Clark (HC)
       Total revision
0.05
0.32
       Data revision effect
0.01
0.33
       Sample size effect
0.05
-0.01
Notes: The data sample for the output gap estimation starts in 1990Q1.
Due to rounding off, the sum of the data revision and  sample size means may be different from the total revision mean.
(*) The output gap series from this column w ere computed by using the 2006Q4 vintage referring to the previous methodology.
(**) The output gap series from this column w ere computed by using the 2006Q4 vintage referring to the new  methodology.
           Method
Mean
37

magnitude is the noise-to-signal ratio. When this information is not available, we can 
observe the mean — when the magnitude of the mean of one of the effects is large and 
much superior to the magnitude of the mean of the other effect, this effect is likely to be 
preponderant in absolute terms.31 
 
 
 
We can observe that, in most of the cases in Table 16, in line with the findings 
for Brazil, both the effect of the sample increase and the effect of the data revision play 
an important role to explain the magnitude of total revision, although we can note that 
                                                      
31 The noise-to-signal ratio is calculated as /    
⁄
, where  is the root mean square 
revision, and   is the standard deviation of the final output gap series. However,  


	

 
	 , where  and  are the mean and the standard deviation of the revision series, 
respectively. Thus, the higher the magnitude of the revision series mean, the higher the RMSR and the 
N/S. 
Table 16
Decomposition of the output gap revisions (%)
Results of some studies (*)
Brazil
U.S
Canada Norw ay
Brazil
U.S
Canada Norw ay
Brazil
U.S
Canada Norw ay
Hodrick-Prescott (HP)
 Total revision
0.04
0.30
0.33
0.02
0.92
1.11
1,06(^)
1.53
0.63
0.93
0.93
0.73
 Data revision effect
0.15
0.16
0.23
0.25
0.68 0,40(^) 0,37(^)
0.68
0.39
0.66
0.60
0.04
 Sample size effect
-0.11
0.14
0.11
-0.23
1.02 0,97(^) 0,94(^)
1.27
0.97
0.97
0.98
0.96
Linear Trend (LT)
 Total revision
0.40
4.78
12.51
1.79
0.47
1.32
2,13(^)
0.79
0.47
0.91
0.99
0.82
 Data revision effect
0.38
0.80
1.41
2.48
0.61 0,37(^) 0,34(^)
0.89
0.72
0.79
0.91
0.87
 Sample size effect
0.02
3.95
11.10
-0.69
0.68 1,12(^) 1,91(^)
0.28
0.98
0.96
0.99
0.95
Quadratic Trend (QT)
 Total revision
0.00
1.25
3.33
-4.39
1.25
1.07
1,11(^)
1.53
0.91
0.96
0.99
0.94
 Data revision effect
0.52
0.23
2.03
0.99
0.42 0,39(^) 0,52(^)
0.41
0.36
0.76
0.87
0.53
 Sample size effect
-0.52
1.00
1.30
-5.38
1.42 0,97(^) 0,81(^)
1.65
0.96
0.99
0.99
0.98
Harvey-Clark (HC)
 Total revision
0.29
1.17
1.62
0.58
1.01
0.84
1,77(^)
1.00
0.57
0.92
0.92
0.83
 Data revision effect
0.32
0.27
0.66
0.08
0.94 0,31(^) 0,78(^)
0.18
0.42
0.84
0.72
-0.41
 Sample size effect
-0.03
0.90
0.96
0.50
0.42
**
**
0.98
0.77
**
**
0.91
Notes: The data sample for the output gap estimation starts in 1990Q1 for Brazil, in 1947Q1 for the United States,
and in 1947Q1 for Canada. This information is not available for Norw ay .
N/S is a proxy for the noise-to-signal ratio (obtained by the ratio of the RMSR to the standard deviation of 
the final output gap).
AR is the first-order serial correlation of the revision series.
(*) Analysis periods and sources: Brazil: 1996Q1-2008Q2; United States: 1966Q1-1997Q4 (Orphanides and van Norden,
2002); Canada: 1972Q1-2003Q4 (Cayen and van Norden, 2005); Norw ay: 1993Q1-2002Q1  (Bernhardsen et al., 2004).
(**) Not available.
(^) Computed in this w ork by using the means and standard deviations presented in the original w orks.
Mean
N/S
AR
38

there is some predominance of the effect of the sample increase for the other countries. 
In fact, differently from the findings for Brazil, in most of the cases, the bias coming 
from the sample increase predominates over the bias arising from the data revision 
(except for the HP method). Besides, in most of the cases, the data revision series of the 
other countries have higher persistence than the corresponding Brazilian series. 
 
5. Conclusion 
 
We have constructed a real-time data set for Brazil, containing all vintages of 
the seasonally adjusted quarterly GDP, released by the IBGE from 1996Q1 through 
2008Q2. Based on this data set, we assess the importance of the revisions of the real-
time series of GDP growth and output gap. Since we neither associate specific 
applications with the revisions, nor make assumptions about the true structure of the 
economy or the true data generating process, the results are fairly general and capture 
part of the measurement error of those variables. 
 
Our results suggest that the revisions of the quarter-over-quarter GDP growth 
rate are substantial. In absolute values, GDP growth is revised, on average, 0.67 p.p. 
above or below the initial released value. In 16 percent of the cases, the GDP growth 
revision implies a change in the sign. In 26 percent of the time, the magnitude of the 
GDP growth revision is greater than that of the data. Isolating the effects of the 
methodological change in the 2006Q4 vintage, our analysis suggests that this change is 
a relevant source of the revisions, although it explains only part of them. 
 
 
Furthermore, corroborating Cayen and van Norden’s (2004) findings for 
Canada, the GDP growth revisions become less important as the aggregation period 
increases. In fact, as we increase the aggregation period, several indicators become 
more favorable. For example, for the year-over-year GDP growth, the mean absolute 
revision falls to 0.23 p.p. per quarter (corresponding to 0.92 p.p. per year). In the case of 
the four-quarter GDP growth, the revision is even lower (0.64 p.p. per year). 
 
To assess the output gap revisions, we used four detrending methods: HP filter, 
linear trend, quadratic trend, and the Harvey-Clark unobserved-components model. In 
39

all cases, the magnitude of the output gap revisions was high. For instance, the HP-
based output gap is revised, on average, 0.84 p.p. above or below its initial estimate. We 
found the highest revision biases for the LT- and HC-based output gaps, and the largest 
magnitude of revision for the LT- and QT-based gaps. In three out of the four methods 
(HP, QT and HC), the revisions implied a change in the output gap sign in 30 percent or 
more of the time, and the revision magnitude is higher than the gap magnitude in 
approximately 50 percent or more of the time. Some indicators show more favorable 
results for the LT method, in spite of having relevant bias and revision magnitude. 
 
We found out that, in general, the effect of both the GDP data revision and the 
sample increase play an important role in explaining the magnitude of the total revisions 
of the output gap. However, in one of the methods (QT), the effect of the sample 
increase predominates over the effect of data revision, revealing that the revisions, in 
this case, are mainly associated with the low precision of the end-of-the-sample 
estimates of the output trend, whereas, in another method (HC), the effect of the data 
revision is more relevant. The fact that both effects are important to explain total 
revisions is in line with the findings in Orphanides and van Norden (2002) for the 
United Stantes, Cayen and van Norden (2005) for Canada, and Bernhardsen et al. (2004, 
2005) for Norway. 
 
Although the revision indicators for Brazil’s output gap are, in general, less 
unfavorable than those reported by studies for other countries, the Brazilian indicators 
suggest the presence of relevant limitations in real-time output gap estimates. This has 
important implications for monetary policy. In line with Orphanides and van Norden 
(2002), the results recommend that we should be very cautious when using those 
estimates. Policymakers should consider that, in real time, the output gap estimates tend 
not to be very reliable. Our results suggest further that, to assess monetary policy 
decisions made in the past or estimate a monetary policy rule that describes monetary 
authority’s behavior (e.g. a Taylor rule), it may not be reasonable to use the last 
available data set. In these cases, one alternative is to use a real-time data set. 
Furthermore, our results question the procedure of comparing the performance of 
inflation forecasts made in real time with those of a model that employs the last 
40

available data set. As the last available data set tends to be more precise, the comparison 
may be unfair.  
 
Our results raise several questions to be investigated in more detail for the 
Brazilian case. Would monetary policy decisions made in the past be different if 
policymakers had access to all revised data? How different is a Taylor rule estimated 
with real-time data from one estimated using final data? What is the most adequate way 
of estimating a monetary policy rule (with real-time data or with final data)? To what 
extent does the use of final data, instead of real-time one, improve the performance of 
an inflation forecast model? And finally are output gap revisions predictable? Answers 
to these questions would improve our understanding of the limits that economic agents 
face in real time. Furthermore, they would allow a better comprehension of how to use 
the available information more efficiently. 
 
The results of this work also point to the importance of using a larger 
information set — including other economic series — when analyzing the state of the 
business cycle. In principle, employing more information tends to reduce the risks 
associated with the use of series subject to revision. In fact, in general, central banks use 
a broad information set about economic activity and its prospects.32 
 
32  For example, in the minutes of the meetings of the Monetary Policy Committee (Copom) of the 
Appendix – Graphs for the GDP and output gaps estimated using LT, QT and HC. 
 
A.1. Quarterly Brazil’s GDP (in natural logarithm) 
 
 
 
 
 
A.2. Linear Trend (LT) 
 
 
 
4.5
4.6
4.7
4.8
4.9
5.0
5.1
1996
1997
1998
1999
2000
2001
2002
2003
2004
2005
2006
2007
2008
-6
-4
-2
0
2
4
6
1996
1998
2000
2002
2004
2006
2008
LT-based final output gap
LT-based real-time output gap
Figure A.2 – Final and real-time LT-based output gaps 
%
Figure A.1 – Final GDP (corresponding to the 2008Q2 vintage) 
44

-1.0
-0.5
0.0
0.5
1.0
1.5
2.0
1996
1997
1998
1999
2000
2001
2002
2003
2004
2005
2006
2007
2008
0
5
10
15
20
25
-1.5
-1
-0.5
0
0.5
1
1.5
2
2.5
3
-4
-3
-2
-1
0
1
2
3
4
-4
-3
-2
-1
0
1
2
3
4
45º line
Final values
Real-time values
Percent of the time
Revision in percentage points
Figure A.3 – Output Gap (Linear Trend) of 1996Q1 over the revisions (% of GDP) 
Figure A.4 – Relative frequency of the revisions of the  
    LT-based output gap values
Figure A.5 – LT output gap values  
                    (real time versus final) 
Vintages 
% 
45

-6
-4
-2
0
2
4
6
1996
1998
2000
2002
2004
2006
2008
LT-based real-time output gap
LT-based quasi-real output gap
-6
-4
-2
0
2
4
6
1996
1998
2000
2002
2004
2006
2008
LT-based quasi-real output gap
LT-based final output gap
Figure A.6 – LT-based output gaps: Real-time and quasi-real series 
Figure A.7 – LT-based output gaps: Quasi-real and final series 
%
%
46

A.3. Quadratic Trend (QT) 
 
 
 
 
 
 
 
 
 
 
-6
-4
-2
0
2
4
6
1996
1998
2000
2002
2004
2006
2008
QT-based final output gap
QT-based real-time output gap
-3.0
-2.5
-2.0
-1.5
-1.0
-0.5
0.0
0.5
1.0
1.5
2.0
1996
1997
1998
1999
2000
2001
2002
2003
2004
2005
2006
2007
2008
Figure A.9 – Output gap (Quadratic Trend) of 1996Q1 over the revisions (% of GDP) 
Figure A.8 – Final and real-time QT-based output gaps 
Vintages 
% 
%
47

0
5
10
15
20
25
30
-4
-3
-2
-1
0
1
2
3
4
5
-5
-3
-1
1
3
5
-5
-4
-3
-2
-1
0
1
2
3
4
5
45º line
Final values
Real-time values
Percent of the time
Revision in percentage points
-6
-4
-2
0
2
4
6
1996
1998
2000
2002
2004
2006
2008
QT-based real-time output gap
QT-based quasi-real output gap
Figure A.11 – QT-based output gap values  
       (real time versus final) 
Figure A.12 –QT-based output gap – Real-time and quasi-real series 
%
Figure A.10 – Relative frequency of the revisions  
      of the QT-based output gap values
48

A.4. Harvey-Clark (HC) 
 
 
 
 
 
-6
-4
-2
0
2
4
6
1996
1998
2000
2002
2004
2006
2008
QT-based quasi-real output gap
QT-based final output gap
-3
-2
-1
0
1
2
3
1996
1998
2000
2002
2004
2006
2008
HC-based final output gap
HC-based real-time output gap
Figure A.14 – Final and real-time HC-based output gaps 
Figure A.13 – QT-based output gap – Quasi-real and final series 
%
%
49

-1.0
-0.8
-0.6
-0.4
-0.2
0.0
0.2
0.4
0.6
0.8
1.0
1996
1997
1998
1999
2000
2001
2002
2003
2004
2005
2006
2007
2008
0
5
10
15
20
25
30
35
40
-1.5
-1
-0.5
0
0.5
1
1.5
2
-4
-3
-2
-1
0
1
2
3
4
-4
-3
-2
-1
0
1
2
3
4
45º line
Final values
Real-time values
Percent of the time
Revision in percentage points
Figure A.15 – Output gap (Harvey-Clark) of 1996Q1 over the revisions (% of GDP) 
Vintages 
%
Figure A.16 – Relative frequency of the revision of the  
       HC-based output gap values 
Figure A.17 – HC-based output gap values  
                      (real time versus final) 
50

-3
-2
-1
0
1
2
3
1996
1998
2000
2002
2004
2006
2008
HC-based real-time output gap
HC-based quasi-real output gap
-3
-2
-1
0
1
2
3
1996
1998
2000
2002
2004
2006
2008
HC-based quasi-real output gap
HC-based final output gap
Figure A.18 – HC-based output gap values  – Real-time and quasi-real series 
Figure A.19 – HC-based output gap values – Quasi-real and final series 
%
%
51

Banco Central do Brasil 
 
 
Trabalhos para Discussão 
Os Trabalhos para Discussão podem ser acessados na internet, no formato PDF, 
no endereço: http://www.bc.gov.br 
 
Working Paper Series 
Working Papers in PDF format can be downloaded from: http://www.bc.gov.br 
 
 
 
 
1 
Implementing Inflation Targeting in Brazil 
Joel Bogdanski, Alexandre Antonio Tombini and Sérgio Ribeiro da Costa 
Werlang 
 
Jul/2000
2 
Política Monetária e Supervisão do Sistema Financeiro Nacional no 
Banco Central do Brasil 
Eduardo Lundberg 
 
Monetary Policy and Banking Supervision Functions on the Central 
Bank 
Eduardo Lundberg 
 
Jul/2000
Jul/2000
3 
Private Sector Participation: a Theoretical Justification of the Brazilian 
Position 
Sérgio Ribeiro da Costa Werlang 
 
Jul/2000
4 
An Information Theory Approach to the Aggregation of Log-Linear 
Models 
Pedro H. Albuquerque 
 
Jul/2000
5 
The Pass-Through from Depreciation to Inflation: a Panel Study 
Ilan Goldfajn and  Sérgio Ribeiro da Costa Werlang 
 
Jul/2000
6 
Optimal Interest Rate Rules in Inflation Targeting Frameworks 
José Alvaro Rodrigues Neto, Fabio Araújo and Marta Baltar J. Moreira 
 
Jul/2000
7 
Leading Indicators of Inflation for Brazil 
Marcelle Chauvet 
 
Sep/2000
8 
The Correlation Matrix of the Brazilian Central Bank’s Standard Model 
for Interest Rate Market Risk 
José Alvaro Rodrigues Neto 
 
Sep/2000
9 
Estimating Exchange Market Pressure and Intervention Activity 
Emanuel-Werner Kohlscheen 
 
Nov/2000
10 
Análise do Financiamento Externo a uma Pequena Economia 
Aplicação da Teoria do Prêmio Monetário ao Caso Brasileiro: 1991–1998 
Carlos Hamilton Vasconcelos Araújo e Renato Galvão Flôres Júnior 
 
Mar/2001
11 
A Note on the Efficient Estimation of Inflation in Brazil 
Michael F. Bryan and Stephen G. Cecchetti 
 
Mar/2001
12 
A Test of Competition in Brazilian Banking 
Márcio I. Nakane 
 
Mar/2001
52

13 
Modelos de Previsão de Insolvência Bancária no Brasil 
Marcio Magalhães Janot 
 
Mar/2001
14 
Evaluating Core Inflation Measures for Brazil 
Francisco Marcos Rodrigues Figueiredo 
 
Mar/2001
15 
Is It Worth Tracking Dollar/Real Implied Volatility? 
Sandro Canesso de Andrade and Benjamin Miranda Tabak 
 
Mar/2001
16 
Avaliação das Projeções do Modelo Estrutural do Banco Central do 
Brasil para a Taxa de Variação do IPCA 
Sergio Afonso Lago Alves 
 
Evaluation of the Central Bank of Brazil Structural Model’s Inflation 
Forecasts in an Inflation Targeting Framework 
Sergio Afonso Lago Alves 
 
Mar/2001
Jul/2001
17 
Estimando o Produto Potencial Brasileiro: uma Abordagem de Função 
de Produção 
Tito Nícias Teixeira da Silva Filho 
 
Estimating Brazilian Potential Output: a Production Function Approach
Tito Nícias Teixeira da Silva Filho 
 
Abr/2001
Aug/2002
18 
A Simple Model for Inflation Targeting in Brazil 
Paulo Springer de Freitas and Marcelo Kfoury Muinhos 
 
Apr/2001
19 
Uncovered Interest Parity with Fundamentals: a Brazilian Exchange 
Rate Forecast Model 
Marcelo Kfoury Muinhos, Paulo Springer de Freitas and Fabio Araújo 
 
May/2001
20 
Credit Channel without the LM Curve 
Victorio Y. T. Chu and Márcio I. Nakane 
 
May/2001
21 
Os Impactos Econômicos da CPMF: Teoria e Evidência 
Pedro H. Albuquerque 
 
Jun/2001
22 
Decentralized Portfolio Management 
Paulo Coutinho and Benjamin Miranda Tabak 
 
Jun/2001
23 
Os Efeitos da CPMF sobre a Intermediação Financeira 
Sérgio Mikio Koyama e Márcio I. Nakane 
 
Jul/2001
24 
Inflation Targeting in Brazil: Shocks, Backward-Looking Prices, and 
IMF Conditionality 
Joel Bogdanski, Paulo Springer de Freitas, Ilan Goldfajn and 
Alexandre Antonio Tombini 
 
Aug/2001
25 
Inflation Targeting in Brazil: Reviewing Two Years of Monetary Policy 
1999/00 
Pedro Fachada 
 
Aug/2001
26 
Inflation Targeting in an Open Financially Integrated Emerging 
Economy: the Case of Brazil 
Marcelo Kfoury Muinhos 
 
Aug/2001
27 
 
Complementaridade e Fungibilidade dos Fluxos de Capitais 
Internacionais 
Carlos Hamilton Vasconcelos Araújo e Renato Galvão Flôres Júnior 
 
Set/2001
53

28 
 
Regras Monetárias e Dinâmica Macroeconômica no Brasil: uma 
Abordagem de Expectativas Racionais 
Marco Antonio Bonomo e Ricardo D. Brito 
 
Nov/2001
29 
Using a Money Demand Model to Evaluate Monetary Policies in Brazil 
Pedro H. Albuquerque and Solange Gouvêa 
 
Nov/2001
30 
Testing the Expectations Hypothesis in the Brazilian Term Structure of 
Interest Rates 
Benjamin Miranda Tabak and Sandro Canesso de Andrade 
 
Nov/2001
31 
Algumas Considerações sobre a Sazonalidade no IPCA 
Francisco Marcos R. Figueiredo e Roberta Blass Staub 
 
Nov/2001
32 
Crises Cambiais e Ataques Especulativos no Brasil 
Mauro Costa Miranda 
 
Nov/2001
33 
Monetary Policy and Inflation in Brazil (1975-2000): a VAR Estimation 
André Minella 
 
Nov/2001
34 
Constrained Discretion and Collective Action Problems: Reflections on 
the Resolution of International Financial Crises 
Arminio Fraga and Daniel Luiz Gleizer 
 
Nov/2001
35 
Uma Definição Operacional de Estabilidade de Preços 
Tito Nícias Teixeira da Silva Filho 
 
Dez/2001
36 
Can Emerging Markets Float? Should They Inflation Target? 
Barry Eichengreen 
 
Feb/2002
37 
Monetary Policy in Brazil: Remarks on the Inflation Targeting Regime, 
Public Debt Management and Open Market Operations 
Luiz Fernando Figueiredo, Pedro Fachada and Sérgio Goldenstein 
 
Mar/2002
38 
Volatilidade Implícita e Antecipação de Eventos de Stress: um Teste para 
o Mercado Brasileiro 
Frederico Pechir Gomes 
 
Mar/2002
39 
Opções sobre Dólar Comercial e Expectativas a Respeito do 
Comportamento da Taxa de Câmbio 
Paulo Castor de Castro 
 
Mar/2002
40 
Speculative Attacks on Debts, Dollarization and Optimum Currency 
Areas 
Aloisio Araujo and Márcia Leon 
 
Apr/2002
41 
Mudanças de Regime no Câmbio Brasileiro 
Carlos Hamilton V. Araújo e Getúlio B. da Silveira Filho 
 
Jun/2002
42 
Modelo Estrutural com Setor Externo: Endogenização do Prêmio de 
Risco e do Câmbio 
Marcelo Kfoury Muinhos, Sérgio Afonso Lago Alves e Gil Riella 
 
Jun/2002
43 
The Effects of the Brazilian ADRs Program on Domestic Market 
Efficiency 
Benjamin Miranda Tabak and Eduardo José Araújo Lima 
 
Jun/2002
54

44 
Estrutura Competitiva, Produtividade Industrial e Liberação Comercial 
no Brasil 
Pedro Cavalcanti Ferreira e Osmani Teixeira de Carvalho Guillén 
 
Jun/2002
45 
Optimal Monetary Policy, Gains from Commitment, and Inflation 
Persistence  
André Minella 
 
Aug/2002
46 
The Determinants of Bank Interest Spread in Brazil 
Tarsila Segalla Afanasieff, Priscilla Maria Villa Lhacer and Márcio I. Nakane
 
Aug/2002
47 
Indicadores Derivados de Agregados Monetários  
Fernando de Aquino Fonseca Neto e José Albuquerque Júnior 
 
Set/2002
48 
Should Government Smooth Exchange Rate Risk?
Ilan Goldfajn and Marcos Antonio Silveira 
 
Sep/2002
49 
Desenvolvimento do Sistema Financeiro e Crescimento Econômico no 
Brasil: Evidências de Causalidade 
Orlando Carneiro de Matos 
 
Set/2002
50 
Macroeconomic Coordination and Inflation Targeting in a Two-Country 
Model 
Eui Jung Chang, Marcelo Kfoury Muinhos and Joanílio Rodolpho Teixeira 
 
Sep/2002
51 
Credit Channel with Sovereign Credit Risk: an Empirical Test 
Victorio Yi Tson Chu 
 
Sep/2002
52 
Generalized Hyperbolic Distributions and Brazilian Data 
José Fajardo and Aquiles Farias 
 
Sep/2002
53 
Inflation Targeting in Brazil: Lessons and Challenges 
André Minella, Paulo Springer de Freitas, Ilan Goldfajn and 
Marcelo Kfoury Muinhos 
 
Nov/2002
54 
Stock Returns and Volatility 
Benjamin Miranda Tabak and Solange Maria Guerra 
 
Nov/2002
55 
Componentes de Curto e Longo Prazo das Taxas de Juros no Brasil 
Carlos Hamilton Vasconcelos Araújo e Osmani Teixeira de Carvalho de 
Guillén 
 
Nov/2002
56 
Causality and Cointegration in Stock Markets: 
the Case of Latin America 
Benjamin Miranda Tabak and Eduardo José Araújo Lima 
 
Dec/2002
57 
As Leis de Falência: uma Abordagem Econômica 
Aloisio Araujo 
 
Dez/2002
58 
The Random Walk Hypothesis and the Behavior of Foreign Capital 
Portfolio Flows: the Brazilian Stock Market Case 
Benjamin Miranda Tabak 
 
Dec/2002
59 
Os Preços Administrados e a Inflação no Brasil 
Francisco Marcos R. Figueiredo e Thaís Porto Ferreira 
 
Dez/2002
60 
Delegated Portfolio Management 
Paulo Coutinho and Benjamin Miranda Tabak 
 
Dec/2002
55

61 
O Uso de Dados de Alta Freqüência na Estimação da Volatilidade e 
do Valor em Risco para o Ibovespa  
João Maurício de Souza Moreira e Eduardo Facó Lemgruber 
 
Dez/2002
62 
Taxa de Juros e Concentração Bancária no Brasil
Eduardo Kiyoshi Tonooka e Sérgio Mikio Koyama 
 
Fev/2003
63 
Optimal Monetary Rules: the Case of Brazil 
Charles Lima de Almeida, Marco Aurélio Peres, Geraldo da Silva e Souza 
and Benjamin Miranda Tabak 
 
Feb/2003
64 
Medium-Size Macroeconomic Model for the Brazilian Economy
Marcelo Kfoury Muinhos and Sergio Afonso Lago Alves 
 
Feb/2003
65 
On the Information Content of Oil Future Prices 
Benjamin Miranda Tabak 
 
Feb/2003
66 
A Taxa de Juros de Equilíbrio: uma Abordagem Múltipla 
Pedro Calhman de Miranda e Marcelo Kfoury Muinhos 
 
Fev/2003
67 
Avaliação de Métodos de Cálculo de Exigência de Capital para Risco de 
Mercado de Carteiras de Ações no Brasil 
Gustavo S. Araújo, João Maurício S. Moreira e Ricardo S. Maia Clemente  
 
Fev/2003
68 
Real Balances in the Utility Function: Evidence for Brazil 
Leonardo Soriano de Alencar and Márcio I. Nakane 
 
Feb/2003
69 
r-filters: a Hodrick-Prescott Filter Generalization
Fabio Araújo, Marta Baltar Moreira Areosa and José Alvaro Rodrigues Neto 
 
Feb/2003
70 
Monetary Policy Surprises and the Brazilian Term Structure of Interest 
Rates 
Benjamin Miranda Tabak 
 
Feb/2003
71 
On Shadow-Prices of Banks in Real-Time Gross Settlement Systems 
Rodrigo Penaloza 
 
Apr/2003
72 
O Prêmio pela Maturidade na Estrutura a Termo das Taxas de Juros 
Brasileiras 
Ricardo Dias de Oliveira Brito, Angelo J. Mont'Alverne Duarte e Osmani 
Teixeira de C. Guillen 
 
Maio/2003
73 
Análise de Componentes Principais de Dados Funcionais – uma 
Aplicação às Estruturas a Termo de Taxas de Juros 
Getúlio Borges da Silveira e Octavio Bessada 
 
Maio/2003
74 
Aplicação do Modelo de Black, Derman & Toy à Precificação de Opções 
Sobre Títulos de Renda Fixa  
Octavio Manuel Bessada Lion, Carlos Alberto Nunes Cosenza e César das 
Neves 
 
Maio/2003
75 
Brazil’s Financial System: Resilience to Shocks, no Currency 
Substitution, but Struggling to Promote Growth 
Ilan Goldfajn, Katherine Hennings and Helio Mori 
 
Jun/2003
 
 
56

76 
Inflation Targeting in Emerging Market Economies 
Arminio Fraga, Ilan Goldfajn and André Minella 
 
Jun/2003
77 
Inflation Targeting in Brazil: Constructing Credibility under Exchange 
Rate Volatility 
André Minella, Paulo Springer de Freitas, Ilan Goldfajn and Marcelo Kfoury 
Muinhos 
 
Jul/2003
78 
Contornando os Pressupostos de Black & Scholes: Aplicação do Modelo 
de Precificação de Opções de Duan no Mercado Brasileiro 
Gustavo Silva Araújo, Claudio Henrique da Silveira Barbedo, Antonio 
Carlos Figueiredo, Eduardo Facó Lemgruber 
 
Out/2003
79 
Inclusão do Decaimento Temporal na Metodologia  
Delta-Gama para o Cálculo do VaR de Carteiras  
Compradas em Opções no Brasil 
Claudio Henrique da Silveira Barbedo, Gustavo Silva Araújo,  
Eduardo Facó Lemgruber 
 
Out/2003
 
80 
Diferenças e Semelhanças entre Países da América Latina: 
uma Análise de Markov Switching para os Ciclos Econômicos 
de Brasil e Argentina 
Arnildo da Silva Correa 
 
Out/2003
81 
Bank Competition, Agency Costs and the Performance of the  
Monetary Policy 
Leonardo Soriano de Alencar and Márcio I. Nakane 
 
Jan/2004
82 
Carteiras de Opções: Avaliação de Metodologias de Exigência de Capital 
no Mercado Brasileiro 
Cláudio Henrique da Silveira Barbedo e Gustavo Silva Araújo 
 
Mar/2004
83 
Does Inflation Targeting Reduce Inflation? An Analysis for the OECD 
Industrial Countries 
Thomas Y. Wu 
 
May/2004
84 
Speculative Attacks on Debts and Optimum Currency Area: a Welfare 
Analysis 
Aloisio Araujo and Marcia Leon 
 
May/2004
85 
Risk Premia for Emerging Markets Bonds: Evidence from Brazilian 
Government Debt, 1996-2002 
André Soares Loureiro and Fernando de Holanda Barbosa 
 
May/2004
86 
Identificação do Fator Estocástico de Descontos e Algumas Implicações 
sobre Testes de Modelos de Consumo 
Fabio Araujo e João Victor Issler 
 
Maio/2004
87 
Mercado de Crédito: uma Análise Econométrica dos Volumes de Crédito 
Total e Habitacional no Brasil 
Ana Carla Abrão Costa 
 
Dez/2004
88 
Ciclos Internacionais de Negócios: uma Análise de Mudança de Regime 
Markoviano para Brasil, Argentina e Estados Unidos 
Arnildo da Silva Correa e Ronald Otto Hillbrecht 
 
Dez/2004
89 
O Mercado de Hedge Cambial no Brasil: Reação das Instituições 
Financeiras a Intervenções do Banco Central 
Fernando N. de Oliveira 
 
Dez/2004
57

90 
Bank Privatization and Productivity: Evidence for Brazil 
Márcio I. Nakane and Daniela B. Weintraub 
 
Dec/2004
91 
Credit Risk Measurement and the Regulation of Bank Capital and 
Provision Requirements in Brazil – a Corporate Analysis 
Ricardo Schechtman, Valéria Salomão Garcia, Sergio Mikio Koyama and 
Guilherme Cronemberger Parente 
 
Dec/2004
92 
 
 
 
Steady-State Analysis of an Open Economy General Equilibrium Model 
for Brazil 
Mirta Noemi Sataka Bugarin, Roberto de Goes Ellery Jr., Victor Gomes 
Silva, Marcelo Kfoury Muinhos 
 
Apr/2005
93 
Avaliação de Modelos de Cálculo de Exigência de Capital para Risco 
Cambial 
Claudio H. da S. Barbedo, Gustavo S. Araújo, João Maurício S. Moreira e 
Ricardo S. Maia Clemente 
 
Abr/2005
94 
Simulação Histórica Filtrada: Incorporação da Volatilidade ao Modelo 
Histórico de Cálculo de Risco para Ativos Não-Lineares 
Claudio Henrique da Silveira Barbedo, Gustavo Silva Araújo e Eduardo 
Facó Lemgruber  
 
Abr/2005
95 
Comment on Market Discipline and Monetary Policy by Carl Walsh 
Maurício S. Bugarin and Fábia A. de Carvalho 
 
Apr/2005
96 
O que É Estratégia: uma Abordagem Multiparadigmática para a 
Disciplina 
Anthero de Moraes Meirelles 
 
Ago/2005
97 
Finance and the Business Cycle: a Kalman Filter Approach with Markov 
Switching 
Ryan A. Compton and Jose Ricardo da Costa e Silva 
 
Aug/2005
98 
Capital Flows Cycle: Stylized Facts and Empirical Evidences for 
Emerging Market Economies 
Helio Mori e Marcelo Kfoury Muinhos 
 
Aug/2005
99 
Adequação das Medidas de Valor em Risco na Formulação da Exigência 
de Capital para Estratégias de Opções no Mercado Brasileiro 
Gustavo Silva Araújo, Claudio Henrique da Silveira Barbedo,e Eduardo 
Facó Lemgruber  
 
Set/2005
100 Targets and Inflation Dynamics 
Sergio A. L. Alves and Waldyr D. Areosa 
 
Oct/2005
101 Comparing Equilibrium Real Interest Rates: Different Approaches to 
Measure Brazilian Rates 
Marcelo Kfoury Muinhos and Márcio I. Nakane 
 
Mar/2006
102 Judicial Risk and Credit Market Performance: Micro Evidence from 
Brazilian Payroll Loans 
Ana Carla A. Costa and João M. P. de Mello 
 
Apr/2006
103 The Effect of Adverse Supply Shocks on Monetary Policy and Output 
Maria da Glória D. S. Araújo, Mirta Bugarin, Marcelo Kfoury Muinhos and 
Jose Ricardo C. Silva 
 
Apr/2006
 
58

104 Extração de Informação de Opções Cambiais no Brasil 
Eui Jung Chang e Benjamin Miranda Tabak 
 
Abr/2006
105 Representing Roommate’s Preferences with Symmetric Utilities 
José Alvaro Rodrigues Neto 
 
Apr/2006
106 Testing Nonlinearities Between Brazilian Exchange Rates and Inflation 
Volatilities 
Cristiane R. Albuquerque and Marcelo Portugal 
 
May/2006
107 Demand for Bank Services and Market Power in Brazilian Banking 
Márcio I. Nakane, Leonardo S. Alencar and Fabio Kanczuk 
 
Jun/2006
108 O Efeito da Consignação em Folha nas Taxas de Juros dos Empréstimos 
Pessoais 
Eduardo A. S. Rodrigues, Victorio Chu, Leonardo S. Alencar e Tony Takeda 
 
Jun/2006
109 The Recent Brazilian Disinflation Process and Costs 
Alexandre A. Tombini and Sergio A. Lago Alves 
 
Jun/2006
110 Fatores de Risco e o Spread Bancário no Brasil 
Fernando G. Bignotto e Eduardo Augusto de Souza Rodrigues 
 
Jul/2006
111 Avaliação de Modelos de Exigência de Capital para Risco de Mercado do 
Cupom Cambial  
Alan Cosme Rodrigues da Silva, João Maurício de Souza Moreira e Myrian 
Beatriz Eiras das Neves 
 
Jul/2006
112 Interdependence and Contagion: an Analysis of Information 
Transmission in Latin America's Stock Markets  
Angelo Marsiglia Fasolo 
 
Jul/2006
113 Investigação da Memória de Longo Prazo da Taxa de Câmbio no Brasil 
Sergio Rubens Stancato de Souza, Benjamin Miranda Tabak e Daniel O. 
Cajueiro 
 
Ago/2006
114 The Inequality Channel of Monetary Transmission 
Marta Areosa and Waldyr Areosa 
 
Aug/2006
115 Myopic Loss Aversion and House-Money Effect Overseas: an 
Experimental Approach 
José L. B. Fernandes, Juan Ignacio Peña and Benjamin M. Tabak  
 
Sep/2006
116 Out-Of-The-Money Monte Carlo Simulation Option Pricing: the Join 
Use of Importance Sampling and Descriptive Sampling 
Jaqueline Terra Moura Marins, Eduardo Saliby and Joséte Florencio dos 
Santos 
 
Sep/2006
117 An Analysis of Off-Site Supervision of Banks’ Profitability, Risk and 
Capital Adequacy: a Portfolio Simulation Approach Applied to Brazilian 
Banks 
Theodore M. Barnhill, Marcos R. Souto and Benjamin M. Tabak  
 
Sep/2006
118 Contagion, Bankruptcy and Social Welfare Analysis in a Financial 
Economy with Risk Regulation Constraint 
Aloísio P. Araújo and José Valentim M. Vicente  
 
Oct/2006
59

119 A Central de Risco de Crédito no Brasil: uma Análise de Utilidade de 
Informação 
Ricardo Schechtman  
 
Out/2006
120 Forecasting Interest Rates: an Application for Brazil 
Eduardo J. A. Lima, Felipe Luduvice and Benjamin M. Tabak 
 
Oct/2006
121 The Role of Consumer’s Risk Aversion on Price Rigidity 
Sergio A. Lago Alves and Mirta N. S. Bugarin 
 
Nov/2006
122 Nonlinear Mechanisms of the Exchange Rate Pass-Through: a Phillips 
Curve Model With Threshold for Brazil 
Arnildo da Silva Correa and André Minella 
 
Nov/2006
123 A Neoclassical Analysis of the Brazilian “Lost-Decades” 
Flávia Mourão Graminho 
 
Nov/2006
124 The Dynamic Relations between Stock Prices and Exchange Rates: 
Evidence for Brazil 
Benjamin M. Tabak 
 
Nov/2006
125 Herding Behavior by Equity Foreign Investors on Emerging Markets 
Barbara Alemanni and José Renato Haas Ornelas 
 
Dec/2006
126 Risk Premium: Insights over the Threshold 
José L. B. Fernandes, Augusto Hasman and Juan Ignacio Peña 
 
Dec/2006
127 Uma Investigação Baseada em Reamostragem sobre Requerimentos de 
Capital para Risco de Crédito no Brasil  
Ricardo Schechtman  
 
Dec/2006
128 Term Structure Movements Implicit in Option Prices 
Caio Ibsen R. Almeida and José Valentim M. Vicente 
Dec/2006
129 Brazil: Taming Inflation Expectations  
Afonso S. Bevilaqua, Mário Mesquita and André Minella 
Jan/2007
130 The Role of Banks in the Brazilian Interbank Market: Does Bank Type 
Matter? 
Daniel O. Cajueiro and Benjamin M. Tabak 
 
Jan/2007
131 Long-Range Dependence in Exchange Rates: the Case of the European 
Monetary System  
Sergio Rubens Stancato de Souza, Benjamin M. Tabak and Daniel O. 
Cajueiro 
 
Mar/2007
132 Credit Risk Monte Carlo Simulation Using Simplified Creditmetrics’ 
Model: the Joint Use of Importance Sampling and Descriptive Sampling 
Jaqueline Terra Moura Marins and Eduardo Saliby 
  
Mar/2007
133 A New Proposal for Collection and Generation of Information on 
Financial Institutions’ Risk: the Case of Derivatives 
Gilneu F. A. Vivan and Benjamin M. Tabak 
  
Mar/2007
134 Amostragem Descritiva no Apreçamento de Opções Européias através 
de Simulação Monte Carlo: o Efeito da Dimensionalidade e da 
Probabilidade de Exercício no Ganho de Precisão 
Eduardo Saliby, Sergio Luiz Medeiros Proença de Gouvêa e Jaqueline Terra 
Moura Marins  
 
Abr/2007
60

135 Evaluation of Default Risk for the Brazilian Banking Sector 
Marcelo Y. Takami and Benjamin M. Tabak 
 
May/2007
136 Identifying Volatility Risk Premium from Fixed Income Asian Options 
Caio Ibsen R. Almeida and José Valentim M. Vicente  
 
May/2007
137 Monetary Policy Design under Competing Models of Inflation 
Persistence 
Solange Gouvea e Abhijit Sen Gupta 
 
May/2007
138 Forecasting Exchange Rate Density Using Parametric Models:  
the Case of Brazil  
Marcos M. Abe, Eui J. Chang and Benjamin M. Tabak  
 
May/2007
139 Selection of Optimal Lag Length inCointegrated VAR Models with 
Weak Form of Common Cyclical Features 
Carlos Enrique Carrasco Gutiérrez, Reinaldo Castro Souza and Osmani 
Teixeira de Carvalho Guillén 
 
Jun/2007
140 Inflation Targeting, Credibility and Confidence Crises 
Rafael Santos and Aloísio Araújo 
 
Aug/2007
141 Forecasting Bonds Yields in the Brazilian Fixed income Market 
Jose Vicente and Benjamin M. Tabak 
 
Aug/2007
142 Crises Análise da Coerência de Medidas de Risco no Mercado Brasileiro 
de Ações e Desenvolvimento de uma Metodologia Híbrida para o 
Expected Shortfall 
Alan Cosme Rodrigues da Silva, Eduardo Facó Lemgruber, José Alberto 
Rebello Baranowski e Renato da Silva Carvalho 
 
Ago/2007
143 Price Rigidity in Brazil: Evidence from CPI Micro Data 
Solange Gouvea 
 
Sep/2007
144 The Effect of Bid-Ask Prices on Brazilian Options Implied Volatility: a 
Case Study of Telemar Call Options 
Claudio Henrique da Silveira Barbedo and Eduardo Facó Lemgruber 
 
Oct/2007
145 The Stability-Concentration Relationship in the Brazilian Banking 
System 
Benjamin Miranda Tabak, Solange Maria Guerra, Eduardo José Araújo 
Lima and Eui Jung Chang 
 
Oct/2007
146 Movimentos da Estrutura a Termo e Critérios de Minimização do Erro 
de Previsão em um Modelo Paramétrico Exponencial 
Caio Almeida, Romeu Gomes, André Leite e José Vicente 
 
Out/2007
147 Explaining Bank Failures in Brazil: Micro, Macro and Contagion Effects 
(1994-1998) 
Adriana Soares Sales and Maria Eduarda Tannuri-Pianto 
 
Oct/2007
148 Um Modelo de Fatores Latentes com Variáveis Macroeconômicas para a 
Curva de Cupom Cambial 
Felipe Pinheiro, Caio Almeida e José Vicente 
 
Out/2007
149 Joint Validation of Credit Rating PDs under Default Correlation 
Ricardo Schechtman 
 
Oct/2007
61

150 A Probabilistic Approach for Assessing the Significance of Contextual 
Variables in Nonparametric Frontier Models: an Application for 
Brazilian Banks 
Roberta Blass Staub and Geraldo da Silva e Souza 
 
Oct/2007
151 Building Confidence Intervals with Block Bootstraps for the Variance 
Ratio Test of Predictability 
Nov/2007
 
Eduardo José Araújo Lima and Benjamin Miranda Tabak 
152 Demand for Foreign Exchange Derivatives in Brazil:  
Hedge or Speculation?  
Fernando N. de Oliveira and Walter Novaes  
 
Dec/2007
153 Aplicação da Amostragem por Importância 
à Simulação de Opções Asiáticas Fora do Dinheiro 
Jaqueline Terra Moura Marins 
 
Dez/2007
154 Identification of Monetary Policy Shocks in the Brazilian Market  
for Bank Reserves 
Adriana Soares Sales and Maria Tannuri-Pianto 
 
Dec/2007
155 Does Curvature Enhance Forecasting? 
Caio Almeida, Romeu Gomes, André Leite and José Vicente 
 
Dec/2007
156 Escolha do Banco e Demanda por Empréstimos: um Modelo de Decisão 
em Duas Etapas Aplicado para o Brasil 
Sérgio Mikio Koyama e Márcio I. Nakane 
 
Dez/2007
157 Is the Investment-Uncertainty Link Really Elusive? The Harmful Effects 
of Inflation Uncertainty in Brazil 
Tito Nícias Teixeira da Silva Filho  
 
Jan/2008
158 Characterizing the Brazilian Term Structure of Interest Rates 
Osmani T. Guillen and Benjamin M. Tabak 
 
Feb/2008
159 Behavior and Effects of Equity Foreign Investors on Emerging Markets 
Barbara Alemanni and José Renato Haas Ornelas 
 
Feb/2008
160 The Incidence of Reserve Requirements in Brazil: Do Bank Stockholders 
Share the Burden? 
Fábia A. de Carvalho and Cyntia F. Azevedo 
 
Feb/2008
161 Evaluating Value-at-Risk Models via Quantile Regressions 
Wagner P. Gaglianone, Luiz Renato Lima and Oliver Linton 
 
Feb/2008
162 Balance Sheet Effects in Currency Crises: Evidence from Brazil 
Marcio M. Janot, Márcio G. P. Garcia and Walter Novaes 
 
Apr/2008
163 Searching for the Natural Rate of Unemployment in a Large Relative 
Price Shocks’ Economy: the Brazilian Case  
Tito Nícias Teixeira da Silva Filho  
 
May/2008
164 Foreign Banks’ Entry and Departure: the recent Brazilian experience 
(1996-2006) 
Pedro Fachada 
 
Jun/2008
165 Avaliação de Opções de Troca e Opções de Spread Européias e 
Americanas  
Giuliano Carrozza Uzêda Iorio de Souza, Carlos Patrício Samanez e 
Gustavo Santos Raposo 
Jul/2008
62

166 Testing Hyperinflation Theories Using the Inflation Tax Curve: a case 
study  
Fernando de Holanda Barbosa and Tito Nícias Teixeira da Silva Filho 
 
Jul/2008
167 O Poder Discriminante das Operações de Crédito das Instituições 
Financeiras Brasileiras  
Clodoaldo Aparecido Annibal 
 
Jul/2008
168 An Integrated Model for Liquidity Management and Short-Term Asset 
Allocation in Commercial Banks  
Wenersamy Ramos de Alcântara 
 
Jul/2008
169 Mensuração do Risco Sistêmico no Setor Bancário com Variáveis 
Contábeis e Econômicas 
Lucio Rodrigues Capelletto, Eliseu Martins e Luiz João Corrar 
 
Jul/2008
170 Política de Fechamento de Bancos com Regulador Não-Benevolente: 
Resumo e Aplicação 
Adriana Soares Sales 
 
Jul/2008
171 Modelos para a Utilização das Operações de Redesconto pelos Bancos 
com Carteira Comercial no Brasil 
Sérgio Mikio Koyama e Márcio Issao Nakane 
 
Ago/2008
172 Combining Hodrick-Prescott Filtering with a Production Function 
Approach to Estimate Output Gap 
Marta Areosa 
 
Aug/2008
173 Exchange Rate Dynamics and the Relationship between the Random 
Walk Hypothesis and Official Interventions 
Eduardo José Araújo Lima and Benjamin Miranda Tabak 
 
Aug/2008
 
174 Foreign Exchange Market Volatility Information: an investigation of 
real-dollar exchange rate 
Frederico Pechir Gomes, Marcelo Yoshio Takami and Vinicius Ratton 
Brandi 
 
Aug/2008
175 Evaluating Asset Pricing Models in a Fama-French Framework 
Carlos Enrique Carrasco Gutierrez and Wagner Piazza Gaglianone 
 
Dec/2008
176 Fiat Money and the Value of Binding Portfolio Constraints 
Mário R. Páscoa, Myrian Petrassi and Juan Pablo Torres-Martínez 
 
Dec/2008
177 Preference for Flexibility and Bayesian Updating 
Gil Riella 
 
Dec/2008
178 An Econometric Contribution to the Intertemporal Approach of the 
Current Account 
Wagner Piazza Gaglianone and João Victor Issler 
 
Dec/2008
179 Are Interest Rate Options Important for the Assessment of Interest 
Rate Risk? 
Caio Almeida and José Vicente 
 
Dec/2008
180 A Class of Incomplete and Ambiguity Averse Preferences 
Leandro Nascimento and Gil Riella 
 
Dec/2008
181 Monetary Channels in Brazil through the Lens of a Semi-Structural 
Model 
André Minella and Nelson F. Souza-Sobrinho 
Apr/2009
63

182 Avaliação de Opções Americanas com Barreiras Monitoradas de Forma 
Discreta 
Giuliano Carrozza Uzêda Iorio de Souza e Carlos Patrício Samanez 
 
Abr/2009
183 Ganhos da Globalização do Capital Acionário em Crises Cambiais 
Marcio Janot e Walter Novaes 
 
Abr/2009
184 Behavior Finance and Estimation Risk in Stochastic Portfolio 
Optimization 
José Luiz Barros Fernandes, Juan Ignacio Peña and Benjamin  
Miranda Tabak 
 
Apr/2009
185 Market Forecasts in Brazil: performance and determinants 
Fabia A. de Carvalho and André Minella 
 
Apr/2009
186 Previsão da Curva de Juros: um modelo estatístico com variáveis 
macroeconômicas 
André Luís Leite, Romeu Braz Pereira Gomes Filho e José Valentim 
Machado Vicente 
 
Maio/2009
187 The Influence of Collateral on Capital Requirements in the Brazilian 
Financial System: an approach through historical average and logistic 
regression on probability of default  
Alan Cosme Rodrigues da Silva, Antônio Carlos Magalhães da Silva, 
Jaqueline Terra Moura Marins, Myrian Beatriz Eiras da Neves and Giovani 
Antonio Silva Brito 
 
Jun/2009
188 Pricing Asian Interest Rate Options with a Three-Factor HJM Model 
Claudio Henrique da Silveira Barbedo, José Valentim Machado Vicente and 
Octávio Manuel Bessada Lion 
 
Jun/2009
189 Linking Financial and Macroeconomic Factors to Credit Risk 
Indicators of Brazilian Banks 
Marcos Souto, Benjamin M. Tabak and Francisco Vazquez 
 
Jul/2009
190 Concentração Bancária, Lucratividade e Risco Sistêmico: uma 
abordagem de contágio indireto 
Bruno Silva Martins e Leonardo S. Alencar 
 
Set/2009
191 Concentração e Inadimplência nas Carteiras de Empréstimos dos 
Bancos Brasileiros 
Patricia L. Tecles, Benjamin M. Tabak e Roberta B. Staub 
 
Set/2009
192 Inadimplência do Setor Bancário Brasileiro: uma avaliação de  
suas medidas 
Clodoaldo Aparecido Annibal 
 
Set/2009
193 Loss Given Default: um estudo sobre perdas em operações prefixadas no 
mercado brasileiro 
Antonio Carlos Magalhães da Silva, Jaqueline Terra Moura Marins e 
Myrian Beatriz Eiras das Neves 
 
Set/2009
194 Testes de Contágio entre Sistemas Bancários – A crise do subprime 
Benjamin M. Tabak e Manuela M. de Souza  
 
Set/2009
195 From Default Rates to Default Matrices: a complete measurement of 
Brazilian banks' consumer credit delinquency 
Ricardo Schechtman 
 
Oct/2009
64

196 The role of macroeconomic variables in sovereign risk 
Marco S. Matsumura and José Valentim Vicente 
 
Oct/2009
197 Forecasting the Yield Curve for Brazil 
Daniel O. Cajueiro, Jose A. Divino and Benjamin M. Tabak 
 
Nov/2009
198 Impacto dos Swaps Cambiais na Curva de Cupom Cambial: uma análise 
segundo a regressão de componentes principais 
Alessandra Pasqualina Viola, Margarida Sarmiento Gutierrez, Octávio 
Bessada Lion e Cláudio Henrique Barbedo 
 
Nov/2009
199 Delegated Portfolio Management and Risk Taking Behavior 
José Luiz Barros Fernandes, Juan Ignacio Peña and Benjamin Miranda 
Tabak  
 
Dec/2009
200 Evolution of Bank Efficiency in Brazil: A DEA Approach 
Roberta B. Staub, Geraldo Souza and Benjamin M. Tabak  
 
Dec/2009
201 Efeitos da Globalização na Inflação Brasileira 
Rafael Santos e Márcia S. Leon 
 
Jan/2010
202 Considerações sobre a Atuação do Banco Central na Crise de 2008 
Mário Mesquita e Mario Torós 
 
Mar/2010
203 Hiato do Produto e PIB no Brasil: uma Análise de Dados em  
Tempo Real 
Rafael Tiecher Cusinato, André Minella e Sabino da Silva Pôrto Júnior 
 
Abr/2010
204 Fiscal and monetary policy interaction: a simulation based analysis  
of a two-country New Keynesian DSGE model with heterogeneous 
households 
Marcos Valli and Fabia A. de Carvalho 
 
Apr/2010
205 Model selection, estimation and forecasting in VAR models with  
short-run and long-run restrictions 
George Athanasopoulos, Osmani Teixeira de Carvalho Guillén,  
João Victor Issler and Farshid Vahid 
 
Apr/2010
206 Fluctuation Dynamics in US interest rates and the role of monetary 
policy 
Daniel Oliveira Cajueiro and Benjamin M. Tabak 
 
Apr/2010
207 Brazilian Strategy for Managing the Risk of Foreign Exchange Rate 
Exposure During a Crisis 
Antonio Francisco A. Silva Jr. 
 
Apr/2010
208 Correlação de default: uma investigação empírica de créditos de varejo 
no Brasil 
Antonio Carlos Magalhães da Silva, Arnildo da Silva Correa, Jaqueline 
Terra Moura Marins e Myrian Beatriz Eiras das Neves 
 
Maio/2010
209 Produção Industrial no Brasil: uma análise de dados em tempo real 
Rafael Tiecher Cusinato, André Minella e Sabino da Silva Pôrto Júnior 
 
Maio/2010
210 Determinants of Bank Efficiency: the case of Brazil 
Patricia Tecles and Benjamin M. Tabak 
 
Apr/2010
 
65