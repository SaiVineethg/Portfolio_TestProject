import sqlite3

con1 = sqlite3.connect('Dashboard.db')

c=con1.cursor()

c_link="https://priceapi.moneycontrol.com/pricefeed/nse/equitycash/"

while(1):
    
    input1=input("Enter 1 to ***Add*** else other key: ")
        
    if input1=='1':
        cmp_code=str(input("Please enter company code to add : "))
        link=str(input("Enter correct company link to add : "))

        c.execute("INSERT INTO symbol_link (company_symbol,link) \
                    VALUES (?,?)",(cmp_code,c_link+link))
        print(cmp_code + " row has been added to the table")
    else:
        break
    
while(1):
    input1=input("Enter 1 to ***Delete*** else other key: ")

    if input1=='1':
        cmp_code1=str(input("Please enter company code to Delete : ")) 
        print(cmp_code1+ " row has been deleted from table")
        c.execute("DELETE FROM symbol_link WHERE company_symbol=(?)",(cmp_code1,))
    else:
        break
else:
    c

con1.commit()

con1.close()

print("\n Done")             
