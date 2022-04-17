import json
from time import sleep
from datetime import datetime
import requests
import os
def get_random_metrics(data_size=20, filesize=1000000, file="/data/yellow_tripdata_2018-01.csv"):
    import random
    data = []
    f = open(file, "r")

    offset = random.randrange(filesize)
    f.seek(offset)  # go to random position


    for i in range(0,data_size):
        f.readline()  # discard - bound to be partial line
        random_line = f.readline()
        data+=[random_line]

    f.close()
    return data
    # return {"metrics": ["1352160000000000",15,0,"00150001","2012-11-05","5826","RD","0","-6.258584","53.340099",-361,15013,33210,4870,0]}


def propagate_to_edge(data, service_name):
    if service_name is None: return
    url = "http://%s.dublin_network:8000/"

    if os.getenv('FOGIFY_DEPLOYMENT_TYPE') == 'swarm':
        url = "http://tasks.%s.dublin_network:8000/"

    requests.post(url % (service_name), json=data, timeout=os.getenv('TIMEOUT', 20))


def get_url_from_mobility():
    mobile_url = os.getenv('5GSLICER_URL')
    service_name = os.getenv('FOGIFY_NAME')
    if get_url_from_mobility.current_nodes is None:
        get_url_from_mobility.current_nodes = requests.get("http://%s:5555/network/dublin_network" % mobile_url).json()
    current_nodes = get_url_from_mobility.current_nodes
    current_position = requests.get("http://%s:5555/network/dublin_network/%s" % (mobile_url, service_name)).json()
    closest_base_station = None
    closest_distance = float('inf')
    for node in current_nodes.get('nodes'):
        if node.get('type') == 'EDGE':
            location = node.get('location', {})
            distance = abs(location.get('lat', float('inf')) - current_position.get('lat')) + abs(
                location.get('lon', float('inf')) - current_position.get('lon')) + abs(
                location.get('alt', float('inf')) - current_position.get('alt'))
            if closest_distance > distance:
                closest_distance = distance
                closest_base_station = node.get('id')
    return closest_base_station

get_url_from_mobility.current_nodes = None

def propagate(data):
    try:
        start = datetime.now()
        requests.post("http://cloud-server:8000/", data=str(data))
        end = datetime.now()
        dif = end - start
        dif_millis = dif.microseconds / 1000
        print("timediff,",dif_millis)
    except Exception as e:
        print(e)
        print("data is lost")
        sleep(5)
        propagate(data=data)
