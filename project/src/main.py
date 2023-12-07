
from pepperCoordinator import PepperCoordinator
from qibullet import SimulationManager

if __name__ == "__main__":
    
    simulation_manager = SimulationManager()
    client = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)
    p = PepperCoordinator(pepper)

    while True:
        p.update()
