from qibullet import SimulationManager
from typing import Any
import time
from inferenceEngine import InferenceEngine
from rasaInterface import RasaInterface
import numpy as np

simulationManager = SimulationManager()
client = simulationManager.launchSimulation(gui=True)
pepper = simulationManager.spawnPepper(client, spawn_ground_plane=True)
while True: 
	pass

