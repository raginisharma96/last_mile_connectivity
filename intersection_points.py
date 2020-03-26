import pandas as pd
from ordered_set import OrderedSet
import pickle as pkl
import seaborn as sns
import matplotlib.pyplot as plt
from os.path import join

def intersection_point(routesFilePath,starting_location="Koramangala",ending_location="Devarabisanahalli"):
    routes = pd.read_excel(join(routesFilePath,"route.xlsx"))
    direct_buses =  []

    for bus_num in routes.columns:
        if starting_location in routes[bus_num].values and ending_location in routes[bus_num].values:
            direct_buses.append(bus_num)
    
    print("Direct Buses from",starting_location,"to",ending_location,":","\n",direct_buses)  
    
    routes.drop(direct_buses, axis=1, inplace=True)     
    
    buses_crossing_from_start = []
    buses_crossing_from_end = []
    all_bus_num = routes.columns
    
    for bus_num in all_bus_num:
        bus_route = OrderedSet(routes[bus_num])
        if starting_location in bus_route:
            buses_crossing_from_start.append(bus_num)
        if ending_location in bus_route:
            buses_crossing_from_end.append(bus_num)
    
    routes_connecting_ending_loc = []
    
    for bus_num in buses_crossing_from_end:
        route = routes[bus_num].values.tolist()
    #     print(route)
        routes_connecting_ending_loc = routes_connecting_ending_loc + route
    routes_connecting_ending_loc = OrderedSet(routes_connecting_ending_loc)

    intersected_buses = {}
    with open('Dictionary_busroute.pkl','rb') as f:
        bus_route_dict = pkl.load(f)

    for route in routes_connecting_ending_loc:
        bus_list = bus_route_dict[route]
        if len(set(buses_crossing_from_start).intersection(set(bus_list))) != 0:
            intersected_buses[route] = len(set(buses_crossing_from_start).intersection(set(bus_list)))

    plot = pd.DataFrame.from_dict(intersected_buses,orient='index')
    plot['Place'] = plot.index
    plot.drop('Nan',axis=0,inplace=True)
    plot.sort_values(0,ascending=False,inplace=True)
    print("Top 10 intersection Points of bus from",starting_location,"to",ending_location,":\n",plot.iloc[:10],"\n\n")
    all_bb = []
    bus = set(bus_route_dict[ending_location])
    for i in plot['Place'].values.tolist():
        bus1 = bus.intersection(set(bus_route_dict[i]))
        print("Buses from",i,"to",ending_location,":",bus1,"\n\n\n")
        all_bb += list(bus1)  

    print("All buses from Top 10 intersection point to",ending_location,"\n",all_bb) 
