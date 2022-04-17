import logging
from threading import Thread
from time import sleep

import requests
from cachetools import TTLCache
from utils.edge_fuctionality import get_random_metrics, propagate_to_edge, get_url_from_mobility
cache = TTLCache(maxsize=128, ttl=5)
# from utils.weather import Weather
# w = Weather()
# t = w.retrieve_all_raw()
data_list = []
def helping_function(data_list = []):
    url = cache.get('url')
    if url is None:
        cache['url'] = get_url_from_mobility()
    closest_base_station = cache.get('url')
    data = get_random_metrics()
    data_list.append(data)
    try:
        print("data length", len(data_list))
        propagate_to_edge(data_list, closest_base_station)
        data_list = []
    except requests.exceptions.Timeout:
        print("Node is not connected to the network")
    return data_list

while True:
    # sleep(5)
    try:
        data_list = helping_function(data_list)
    except Exception as ex:
        print(ex)