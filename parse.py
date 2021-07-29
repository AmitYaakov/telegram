
import pandas as pd
import os
import re
from geopy.geocoders import Nominatim
from gmplot import gmplot
import plotly.graph_objects as go

info_dict= {'מסווג' : 0 , 'בלתי מסווג' : 0, 'סודי' : 0,
             'סודי ביותר' : 0, 'שמור' : 0, 'בהול' : 0,
             'דחוף' : 0, 'מיידי' : 0, 'אל' : 0,
             'מברק יוצא' : 0, 'מברק נכנס' : 0, 'מאת' : 0, 'מס מברקים' : 0}
to_write = 1
from_country = ""
from_dict = {}
to_dict = {}
all = open('./all.txt', 'a', encoding='utf-8')
x = os.listdir("./letters/")
to = False
from_ = False
fields = []
for x in range(2, 120):
    if (os.path.isfile("./letters/page"+ str(x)+".txt")):
        f = open("./letters/page"+ str(x)+".txt", "r", encoding='utf-8')
        list = f.readlines()
        fields = []
        flag = 0

        for line in list:
            reversed = line.strip()
            if ('בלתי מסווג' in reversed.strip()):
                fields.append('בלתי מסווג')
                to_write = 0
            elif('מסווג' in reversed.strip()):
                fields.append('מסווג')
                to_write = 0
                #סודי ביותר
            if ('סודי ביותר' in reversed.strip()):
                fields.append('סודי ביותר')
                to_write = 0
            #סודי
            elif ('סודי' in reversed.strip()):
                fields.append('סודי')
                to_write = 0
            #שמור
            if ('שמור' in reversed.strip() and len(reversed) == 4):
                fields.append('שמור')
                to_write = 0
            #דחוף
            if ('דחוף' in reversed.strip() and len(reversed) == 4):
                fields.append('דחוף')
                to_write = 0
            #בהול
            if ('בהול' in reversed.strip() and len(reversed) == 4):
                fields.append('בהול')
                to_write = 0
            if(('מיידי' in reversed.strip() and len(reversed) == 5) or ('מידי' in reversed.strip() and len(reversed) == 4)):
                fields.append('מיידי')
                to_write = 0

            if (bool(re.search(r'\b\s*מאת\s*:\s*\b',line.strip())) and re.search(r'\b\s*מאת\s*:\s*\b',line.strip()).span()[0] == 0):
                from_ = True
                flag = 1
                to_write = 0
                line = re.sub(' +',' ',line.strip())
                from_country = line.split(":")
                if from_country[1].strip() in from_dict:
                    from_dict[from_country[1].strip()] = from_dict[from_country[1].strip()]+1;
                else:
                    from_dict[from_country[1].strip()] =1;

            elif (bool(re.search(r'\b\s*מאת\s+\b',line.strip()))) and re.search(r'\b\s*מאת\s+\b',line.strip()).span()[0] == 0:
                to_write = 0
                flag = 1
                line = re.sub(' +',' ',line.strip())
                from_country = line.split(" ")
                if from_country[1].strip() in from_dict:
                    from_dict[from_country[1].strip()] = from_dict[from_country[1].strip()]+1;
                else:
                    from_dict[from_country[1].strip()] =1

            if (bool(re.search(r'\b\s*אל\s*:\s*\b',line.strip()))) and re.search(r'\b\s*אל\s*:\s*\b',line.strip()).span()[0] == 0:
                to_write = 0
                line = re.sub(' +',' ',line.strip())
                to_country = line.split(":")
                if (" " in to_country[1]):
                    to_country = to_country[1].split(" ")
                for country in to_country[1:]:
                    country = re.sub(',', ' ', country)
                    if country.strip() in to_dict:
                        to_dict[country.strip()] = to_dict[country.strip()]+1;
                    else:
                        to_dict[country.strip()] =1;

            elif (bool(re.search(r'\b\s*אל\s+\b',line.strip()))) and re.search(r'\b\s*אל\s+\b',line.strip()).span()[0] == 0:
                to_write = 0
                line = re.sub(' +',' ',line.strip())
                to_country = line.split(" ")
                for country in to_country[1:]:
                    country = re.sub(',', ' ', country)
                    if country.strip() in to_dict:
                        to_dict[country.strip()] = to_dict[country.strip()]+1;
                    else:
                        to_dict[country.strip()] =1;
            if (('מברק יוצא' in reversed)):
                fields.append('מברק יוצא')
                to_write = 0
            if (('מברק נכנס' in reversed)):
                fields.append('מברק נכנס')
                to_write = 0
            if (to_write == 1):
                all.write(reversed + "\n")
            else:
                to_write = 1
        if (flag == 1): #if its new letter
            for f in fields:
                info_dict[f] = info_dict[f] + 1
            fields = []
            flag = 0
        else:
            fields = []
            flag = 0

geolocator = Nominatim(user_agent="parse")
combined = []
flag1 = 0
counter = 0

for key in from_dict:
     if (key == 'המשרד'):
         place = 'ישראל'
         print(place)
         location = geolocator.geocode(place)
         combined.append({key: [location.latitude, location.longitude, 34.8667654, 31.5313113, from_dict.get(key), 0,from_dict.get(key)]})
     else:
         print(key)
         location = geolocator.geocode(key)
         combined.append({key: [location.latitude, location.longitude, 34.8667654, 31.5313113, from_dict.get(key), 0,from_dict.get(key)]})
print(combined)
for key in to_dict:
    for item in combined:
         if(counter <= len(combined) - 1 and key in combined[counter]):
             flag1 = 1

             temp = combined[counter].get(key)
             combined[counter] = {key: [temp[0], temp[1], temp[2], temp[3], temp[4], to_dict.get(key), temp[6] + to_dict.get(key)]}
             break
         else:
             counter = counter+1

    if (flag1 == 0):
         print(key)
         location = geolocator.geocode(key)
         combined.append({key: [34.8667654, 31.5313113, location.latitude, location.longitude, 0, to_dict.get(key),to_dict.get(key)]})
    else:
        flag1 = 0
l = []

for dct in combined:
     l.append(pd.DataFrame(dct).transpose())
tmp = pd.concat(l)  # aggregate them all
df = pd.DataFrame(tmp)
df.to_csv(r'Telegrams_data.csv', index=True, mode='a', header=False, encoding='utf-8-sig')

print(info_dict)



