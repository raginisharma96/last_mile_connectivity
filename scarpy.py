import lxml.html as lh
import pandas as pd
import pickle as pkl
from os.path import join


def scarpy(busNumberFile,saveToFilePath,kind):
    with open(busNumberFile,"r") as f:
        bus_numbers_html = f.read()
    
    tree = lh.fromstring(bus_numbers_html)
    bus_numbers = tree.xpath("//option/text()")
    busnum_routes = {}
    
    for bus_number in bus_numbers:
        url = "https://narasimhadatta.info/cgi-bin/find.cgi"

        payload = {"route":bus_number}
        headers = {
            'origin': "https://narasimhadatta.info",
            'upgrade-insecure-requests': "1",
            'content-type': "application/x-www-form-urlencoded",
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'cache-control': "no-cache",
            'postman-token': "f64130d3-9129-185a-44a3-15b36a71f316"
            }

        response = requests.request("POST", url, data=payload, headers=headers)
        response_tree = lh.fromstring(response.text)
        bus_routes = response_tree.xpath("//li/text()")
        busnum_routes[bus_number] = bus_routes

    max_rows = max(list(map(lambda x: len(busnum_routes[x]),busnum_routes)))
    for i in busnum_routes:
        if len(busnum_routes[i]) < max_rows:
            l = ['Nan']*(max_rows-len(busnum_routes[i]))
            busnum_routes[i] +=l

    if kind == 'pickle':
        with open(join(saveToFilePath,"route.pkl"),"wb") as f:
            pkl.dump(busnum_routes,f)
    else:
        pd.DataFrame(busnum_routes).to_csv(join(saveToFilePath,"route.csv"))

    
    