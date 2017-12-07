#control
trading_days = 40 #number of daily data files to open

import os as os
import pandas as pd
import csv

all_survivors = []

def rashomon(exchange):

    #find latest trading_days date files, open them and create Dataframes
    dlist = os.listdir("C:/Users/USER/PycharmProjects/Data archives/EOD %s"%exchange)
    dlist.sort(reverse = True)
    date_list = dlist[:trading_days+1]

    daily_df={}
    for i in range(1,trading_days+1):

        daily_df[i] = pd.read_table("C:/Users/USER/PycharmProjects/Data archives/EOD %s/%s"%(exchange, date_list[i-1]), sep= ",", names=["Symbol", "Date", "O", "H", "L", "C", "V"], index_col=0)


    #create starting survivor list from last trading day and remove symbols that do not appear in all trading_days dataframes
    start_survivors = list(daily_df[1].index)

    for j in range(2,trading_days+1):

        for i in daily_df[1].index:
            try:
                if i not in daily_df[j].index:
                    start_survivors.remove(i)
            except:
                pass


    green_survivors = list(start_survivors)
    red_survivors = list(start_survivors)


    #analyze 5 data files per week to create weekly_df dictionary of weekly HLCs, weekly_hlc is placeholder for nested list of symbol index number : HLC-tuples
    weekly_df = {}
    weekly_hlc = {}

    w = 0 #week_counter
    for i in range(1,trading_days/5 +1):
        h1 = []
        l1 = []
        c1 = []
        o1 = []

        w += 1

        for j in start_survivors:

            x = max(daily_df[w*5-4].loc[j,"H"],daily_df[w*5-3].loc[j,"H"],daily_df[w*5-2].loc[j,"H"], daily_df[w*5-1].loc[j,"H"],daily_df[w*5].loc[j,"H"])
            h1.append(x)

            y = min(daily_df[w*5-4].loc[j,"L"],daily_df[w*5-3].loc[j,"L"],daily_df[w*5-2].loc[j,"L"], daily_df[w*5-1].loc[j,"L"],daily_df[w*5].loc[j,"L"])
            l1.append(y)

            z = daily_df[w*5-4].loc[j,"C"]
            c1.append(z)

            m = daily_df[w*5].loc[j, "O"]
            o1.append(m)

        weekly_hlc[i] = zip(o1,h1,l1,c1)


    for i in range(1, trading_days/5 +1):
        weekly_df[i] = pd.DataFrame(weekly_hlc[i], index= start_survivors, columns=["O","H","L","C"])


    #define AV
    def av(week, symbol):
        return (weekly_df[week+1].loc[symbol,"H"] + weekly_df[week+1].loc[symbol,"L"] + weekly_df[week+1].loc[symbol,"C"] + \
               weekly_df[week+2].loc[symbol,"H"] + weekly_df[week+2].loc[symbol,"L"] + weekly_df[week+2].loc[symbol,"C"] + \
               weekly_df[week+3].loc[symbol,"H"] + weekly_df[week+3].loc[symbol,"L"] + weekly_df[week+3].loc[symbol,"C"])/9



    #screen stocks that closed last 3 weeks up and above AV, 1 week prior below AV
    for i in start_survivors:
        if weekly_df[1].loc[i,"O"] > weekly_df[1].loc[i,"C"] or weekly_df[2].loc[i,"O"] > weekly_df[2].loc[i,"C"] or weekly_df[3].loc[i,"O"] > weekly_df[3].loc[i,"C"] or \
                        weekly_df[1].loc[i,"C"] < av(1,i) or weekly_df[2].loc[i,"C"] < av(2,i) or weekly_df[3].loc[i,"C"] < av(3,i) or weekly_df[4].loc[i,"C"] > av(4,i) or weekly_df[5].loc[i,"C"] > av(5,i) or \
                        abs(weekly_df[1].loc[i, "O"] - weekly_df[1].loc[i, "C"]) / (weekly_df[1].loc[i, "H"] - weekly_df[1].loc[i, "L"]) < 0.5 or abs(weekly_df[2].loc[i, "O"] - weekly_df[2].loc[i, "C"]) / (weekly_df[2].loc[i, "H"] - weekly_df[2].loc[i, "L"]) < 0.5 or abs(weekly_df[3].loc[i, "O"] - weekly_df[3].loc[i, "C"]) / (weekly_df[3].loc[i, "H"] - weekly_df[3].loc[i, "L"]) < 0.5:
            green_survivors.remove(i)


    #vice versa for red list
    for i in start_survivors:
        if weekly_df[1].loc[i,"O"] < weekly_df[1].loc[i,"C"] or weekly_df[2].loc[i,"O"] < weekly_df[2].loc[i,"C"] or weekly_df[3].loc[i,"O"] < weekly_df[3].loc[i,"C"] or \
                        weekly_df[1].loc[i,"C"] > av(1,i) or weekly_df[2].loc[i,"C"] > av(2,i) or weekly_df[3].loc[i,"C"] > av(3,i) or weekly_df[4].loc[i,"C"] < av(4,i) or weekly_df[5].loc[i,"C"] < av(5,i) or \
                        abs(weekly_df[1].loc[i,"O"]-weekly_df[1].loc[i,"C"])/(weekly_df[1].loc[i,"H"]-weekly_df[1].loc[i,"L"]) < 0.5 or abs(weekly_df[2].loc[i,"O"]-weekly_df[2].loc[i,"C"])/(weekly_df[2].loc[i,"H"]-weekly_df[2].loc[i,"L"]) < 0.5 or abs(weekly_df[3].loc[i,"O"]-weekly_df[3].loc[i,"C"])/(weekly_df[3].loc[i,"H"]-weekly_df[3].loc[i,"L"]) < 0.5:
            red_survivors.remove(i)

    all_survivors.extend(green_survivors)
    all_survivors.extend(red_survivors)




exchanges = ['AMEX','NASDAQ','NYSE']

for exchange in exchanges:
    rashomon(exchange)

for x in all_survivors:
    print x