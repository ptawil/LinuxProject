#scrapes the rank of popularity of subway stations from the mta website. My regex doesn't work perfectly yet. 
import re
import urllib.request
pattern2 = re.compile(r'(<strong>[^>]*>*[^>]*)*>*(.+?) *<')
pattern = re.compile(r'<div.+?>*>(<span class ="style6">)*(<a href="ridership_sub_statClosure.htm">)*([^<]+)<.+?alt="(\w) subway".+\n.+\n.+\n.+\n.+\n.+\n\s+<td align="right">([^<]+)</td>\n.+\n.+\n\s+<td align="right".*?>([^<]+)</td>')
f = urllib.request.urlopen("http://web.mta.info/nyct/facts/ridership/ridership_sub.htm")
data = f.read().decode()
file = open("subwayRankings.txt", "w")
if data:
    found = re.findall(pattern, data)
    if found:
        for x in found:
            temp = re.sub(r'\s{2,}', " ", x[2].strip())
            stationLines = x[3].strip()
            stationName = re.sub(r'Avenue', "Av", temp)
            stationName = re.sub(r'Beverley', "Beverly", stationName)
            stationName = re.sub(r'Newkirk Plaza', "Newkirk Av", stationName)
            file.write(stationName+"|"+ stationLines + "|"+ x[4].strip()+ "|"+ x[5].strip()+"\n") 

            

