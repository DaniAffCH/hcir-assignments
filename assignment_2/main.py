from BLMparser import Parser
from coordinator import Coordinator
from qibullet import SimulationManager

if __name__ == "__main__":
    simulation_manager = SimulationManager()
    client = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(
        client, spawn_ground_plane=True)
    parser = Parser("bml.json")
    c = Coordinator(parser, pepper)
    c.spawn()
