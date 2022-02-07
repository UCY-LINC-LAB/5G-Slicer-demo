# 5G-Slicer-demo
This demo presents the **5G-Slicer** emulator in action. 5G-Slicer is an emulation framework that facilitates the definition of mobile network slices through modeling abstractions for radio units, mobile nodes, trajectories, etc., while also offering realistic network QoS by dynamically altering -at runtime- signal strength. Moreover, 5G-Slicer provides an already realized scenario for a city-scale deployment that smart-city researchers can simply configure through a ``ready-to-use" template, leaving 5G-Slicer responsible for translating it into an emulated environment. 5G-Slicer's prototype offers a connector for the [**Fogify Framework** ](https://ucy-linc-lab.github.io/fogify/getting-started.html), which is an interactive, multi-host, and scalable fog emulator. Fogify gives the required scalability and the ability of runtime changes to the 5G-Slicer. Since the 5G-Slicer's SDK is written in Python, we utilize **Jupyter** notebook as a web-based interactive GUI for 5G-Slicer and post-experimentation utilization metrics analysis.

## Requirements

Before starting, we need to setup and configure requirements for Fogify framework. Specifically, we have to install docker, docker-compose and docker swarm on the infrastructure. For more information, we suggest the official [documentation](https://docs.docker.com/).

Furthermore, the system executes some low-level commands in order to apply specific characteristics to the network. For this reason, on each cluster of the swarm cluster, we should install the traffic control tool (tc-tool). On Debian-based destributions, tc-tool comes bundled with iproute, so in order to isntall it you have to run:

```bash
apt-get install iproute
```
## Stack Instantiation

Having a docker swarm cluster running, we have to execute the 5G-Slicer, Fogify, and Jupyter. The services are dockerized and are described through the docker-compose file. So we should run the following command at the swarm master node.

```bash
sudo docker-compose -p 5GSlicer up
```
In order to open the web interface of Jupyter, you have to find the output of the `ui` service where the system outputs the `url` and the `token`

![Jupyter Notebook](https://raw.githubusercontent.com/UCY-LINC-LAB/fogify-demo/master/images/jupyter.png)


For instance, in previous output we can open the Jupyter interface with the following url:
```bash
http://127.0.0.1:8888/?token=1cd2e914cd03e76d551a666cb0a8dcdb6361bc29ddf54eed
```

If we have more nodes in the cluster, we have to execute the following command on every node.
```bash
sudo docker-compose -p fogemulator up agent cadvisor
```

## Preparation of use-case
5GSlicer implemented a simple IoT service that is driven by real-world data to showcase a scenario of a bus operator that collects and analyzes location-based data from its fleet. The codebase of the application is under the `application` folder and can be easily build by running the following command:

./application/build-image.sh

When the containers are built, user has to create a folder named `/home/ubuntu/data` and should place the data of Dublin's buses and bus stops. Finally, the user can utilize the `demo_files/docker-compose.yaml` file as input of the 5GSlicer.

## Scenario Execution
The following snippet depicts the example of 5G-Slicer demo and its programming abstractions. Lines 1-2 import the 5G-Slicer SDK and the parameterizable smart bus testbed template. In Lines 3-5, the user introduces the Fogify Controller address (experiment orchestrator) and the docker-compose file, describing the available infrastructure and network resources along with the emulation configuration. Lines 6-8 configure the testbed according to user preferences, including the number of radio units, MECs, and buses, along with the operational bounding box. The generate_experiment method produces a new SDK object that captures a programming view of the 5G-Slicer model and materializes the testbed with the mobility scenarios. Line 11 deploys the testbed, and Line 12 generates the interactive map. With the scenario_execution method in Line 13, the user can run the mobility scenario that is generated from the datasets. Finally, Line 14 finishes the emulation and releases all resources.
```python
from 5GSlicerSDK import 5GSlicerSDK
from experiment_repo import BusExperiment
5g_slicer_sdk = 5GSlicerSDK(
                    'http://controller:5000',
                    'demo_files/docker-compose.yaml')
bus_exp = BusExperiment( 
    5g_slicer_sdk, num_of_RUs=5, num_of_edge=5, 
    num_of_buses=10, bounding_box=(...) )
5g_slicer_sdk = bus_exp.generate_experiment()
5g_slicer_sdk.generate_mobile_networks()
5g_slicer_sdk.deploy()
5g_slicer_sdk.generate_map('dublin_network')
5g_slicer_sdk.scenario_execution('mobility')
5g_slicer_sdk.undeploy()
```
