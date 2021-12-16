import sqlite3
import pandas as pd
import datetime,webbrowser, pyautogui
import pywhatkit as kit
import time
import datetime
freq=int(input("Please enter the frequency(In min.) to update your Stock Portfolio: "))
print("Extacting json data from moenycontrol.\nPlease wait!!!\n")
while(1):
    #now=datetime.datetime.now()
    #t_time=now.strftime("%H:%M:%S, %d-%m-%Y")

    def share_price_details(company_name,moneycontrol_path):
        import urllib.request
        import json
        weburl=urllib.request.urlopen(moneycontrol_path)
        if str(weburl.getcode())=="200":
            #print("Processing "+company_name)
            weburl
        data=weburl.read()
        data=json.loads(data)
        share_details=[company_name,data["data"]["lastupd"][0:10],data["data"]["lastupd"][11:16],round(float(data["data"]["pricecurrent"]),2),round(float(data["data"]["priceprevclose"]),2),round(float(data["data"]["pricechange"]),2),round(float(data["data"]["pricepercentchange"]),2)]
        return share_details

    #data["data"]["SC_SUBSEC"]

    #print("\nFunction readed successfully")

    con1 = sqlite3.connect('Dashboard.db')
    c=con1.cursor()
    query = "SELECT * from symbol_link;"

    df = pd.read_sql_query(query,con1)


    share_det=pd.DataFrame(columns = ["Symbol","Date","Time","LTP","Prev_day","Day_Chng","Perc_Daychng"])
    #print("Please wait, it's processing!!!\n")
    for i in range(len(df)):
        ser=pd.Series(share_price_details(df["company_symbol"][i],df["link"][i]),index=share_det.columns)
        #print(ser)
        share_det=share_det.append(ser, ignore_index=True)
    #print("**********Extraction has been finished**********")

    try:
        
        con1.execute('''DROP TABLE cmpny_share_prev''')
        
        con1.commit()
        
        share_det.to_sql(name='cmpny_share_prev', con=con1)

    except:
        
        share_det.to_sql(name='cmpny_share_prev', con=con1)

    groww_day_change=pd.read_sql_query('''SELECT sum(Total_Day_Change) AS 'Groww_Total_Day_change' FROM Groww_Port_Details;''',con1)
    upstox_day_change=pd.read_sql_query('''SELECT sum(Total_Day_Change) AS 'Upstox_Total_Day_change' FROM Upstox_Port_Details;''',con1)
    zerodha_day_change=pd.read_sql_query('''SELECT sum(Total_Day_Change) AS 'Zerodha_Total_Day_change' FROM Zerodha_Port_Details;''',con1)

    last_updated=pd.read_sql_query('''SELECT Date,Time from cmpny_share_prev WHERE Symbol='AXISBANK';''',con1)
    gainers_5=pd.read_sql_query('''SELECT Symbol,Perc_Daychng from cmpny_share_prev WHERE Symbol NOT IN ('TATACHEM_Upstox','TATAMOTORS_Upstox') AND Perc_Daychng>0 ORDER BY Perc_Daychng DESC LIMIT 5;''',con1)
    losers_5=pd.read_sql_query('''SELECT Symbol,Perc_Daychng from cmpny_share_prev WHERE Symbol NOT IN ('TATACHEM_Upstox','TATAMOTORS_Upstox') AND Perc_Daychng<0 ORDER BY Perc_Daychng LIMIT 5;''',con1)
    gain_n=pd.read_sql_query('''SELECT count(*) as 'Gainers' From cmpny_share_prev WHERE Perc_Daychng>0;''',con1)['Gainers'].iloc[0]
    loss_n=pd.read_sql_query('''SELECT count(*) as 'Losers' From cmpny_share_prev WHERE Perc_Daychng<0;''',con1)['Losers'].iloc[0]  
    html_con=open('Test_Portfolio.html','w')
    message='''<!DOCTYPE html>
    <html>
    <body>
    <div class="bg"></div>
    <h1>Stock Portfolio</h1>
    <h2 style="font-family:verdana;"">Market Update</h2> 
    <p style="font-family:courier;">Last Update : {}</p>
    <p>Groww   Day Change : %d</p>
    <p>Upstox  Day Change : %d</p>
    <p>Zerodha Day Change : %d</p>
    <p></p>
    <p>Total Day Change   : %d</p>
    <p></p>
    <p>Top 5 Gainers      : %d</p>
    <table>
        <tr>
            <th>{}</th>
            <th>{}</th>
        </tr>
        <tr>
            <th>{}</th>
            <th>{}</th>
        </tr>
        <tr>
            <th>{}</th>
            <th>{}</th>
        </tr>
        <tr>
            <th>{}</th>
            <th>{}</th>
        </tr>
        <tr>
            <th>{}</th>
            <th>{}</th>
        </tr>
        <tr>
            <th>{}</th>
            <th>{}</th>
        </tr>
    </table>
    <p>Top 5 Losers      : %d</p>
    <table>
        <tr>
            <th>{}</th>
            <th>{}</th>
        </tr>
        <tr>
            <th>{}</th>
            <th>{}</th>
        </tr>
        <tr>
            <th>{}</th>
            <th>{}</th>
        </tr>
        <tr>
            <th>{}</th>
            <th>{}</th>
        </tr>
        <tr>
            <th>{}</th>
            <th>{}</th>
        </tr>
        <tr>
            <th>{}</th>
            <th>{}</th>
        </tr>
    </table>
    <p> Last Run @ {}</p>
    </body>
    </html>'''.format(last_updated["Time"][0]+", "+last_updated["Date"][0],gainers_5.columns[0],gainers_5.columns[1],gainers_5.iloc[0][0],gainers_5.iloc[0][1],gainers_5.iloc[1][0],gainers_5.iloc[1][1],gainers_5.iloc[2][0],gainers_5.iloc[2][1],gainers_5.iloc[3][0],gainers_5.iloc[3][1],gainers_5.iloc[4][0],gainers_5.iloc[4][1],losers_5.columns[0],losers_5.columns[1],losers_5.iloc[0][0],losers_5.iloc[0][1],losers_5.iloc[1][0],losers_5.iloc[1][1],losers_5.iloc[2][0],losers_5.iloc[2][1],losers_5.iloc[3][0],losers_5.iloc[3][1],losers_5.iloc[4][0],losers_5.iloc[4][1],datetime.datetime.now().strftime("%H:%M:%S")+"IST")%(groww_day_change["Groww_Total_Day_change"][0],upstox_day_change["Upstox_Total_Day_change"][0],zerodha_day_change["Zerodha_Total_Day_change"][0],(groww_day_change["Groww_Total_Day_change"][0]+upstox_day_change["Upstox_Total_Day_change"][0]+zerodha_day_change["Zerodha_Total_Day_change"][0]),gain_n,loss_n)
    html_con.write(message)
    html_con.close()
    print("Last update at:",datetime.datetime.now().strftime("%H:%M:%S"),"IST","[Day Change :",round(groww_day_change["Groww_Total_Day_change"][0]+upstox_day_change["Upstox_Total_Day_change"][0]+zerodha_day_change["Zerodha_Total_Day_change"][0],2),"]")
    time.sleep(60*freq)
    
    
    con1.commit()

    con1.close()

    #print("Extarcted data pushed into new table")
