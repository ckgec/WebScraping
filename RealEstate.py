import pandas
from bs4 import BeautifulSoup #bs4 is beautifulsoup library
base_url="https://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s=" #A cached real estate website
l=[]
for page in range(0,30,10): # 0,10,20
    r=requests.get(base_url+str(page)+".html")
    c=r.content

    soup=BeautifulSoup(c,"html.parser")
    all=soup.find_all("div",{"class":"propertyRow"})

    #all[0].find_all("h4",{"class":"propPrice"})[0].text.replace("\n","")
    for item in all:
        d={}
        d["Price"]=item.find("h4",{"class","propPrice"}).text.replace("\n","") #For Price of the property
        d["Address"]=item.find_all("span",{"class","propAddressCollapse"})[0].text #Address
        d["Locality"]=item.find_all("span",{"class","propAddressCollapse"})[1].text #Address

        try:                                                                 #No. of beds may not be avaialble for all properties that's why try,except
            d["Beds"]=item.find("span",{"class","infoBed"}).find("b").text #For no. of beds
        except:
            d["Beds"]=None

        try:
            d["Area"]=item.find("span",{"class","infoSqFt"}).find("b").text #For Area Squarefit
        except:
            d["Area"]=None

        try:
            d["FullBaths"]=item.find("span",{"class","infoValueFullBath"}).find("b").text #For no. of FullBaths
        except:
            d["FullBaths"]=None

        try:
            d["HalfBaths"]=item.find("span",{"class","infoValueHalfBath"}).find("b").text #For no. of HalfBaths
        except:
            d["HalfBaths"]=None

        for column_group in item.find_all("div",{"class","columnGroup"}):
           # print(column_group)
            for feature_group,feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}),column_group.find_all("span",{"class":"featureName"})):
                #print(feature_group.text,feature_name.text)
                if "Lot Size" in feature_group.text: #To display lotSize only (e.g. 0.21Acres)
                    d["Lot Size"]=feature_name.text
        l.append(d)
        #print("")

    df=pandas.DataFrame(l)
    df
    df.to_csv("New Data.csv")

# For any query contact:-
# Chanchal Kumar
# ckgec98@gmail.com
