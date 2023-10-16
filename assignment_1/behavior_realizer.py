from qibullet import SimulationManager
import gtts
from playsound import playsound
import threading
import time
import tempfile
from collections import namedtuple

from math import pi


class WavingSkill():

    """
    A class used to implement a waving skill. It is implemented as an Finite State Machine (FSM) where every state represents a robot configuration. 
    The actual motion is implemented by setting joint angles through the pibullet APIs.

    ...

    Attributes
    ----------
    pepperInstance : qibullet.pepper_virtual.PepperVirtual
        pepper instance
    speed : float
        value between 0 and 1 expressing the execution speed
    waveAngle: int
        angle to which extend the elbow is waving

    Methods
    -------
    degtorad(x)
        Converts x degrees into radians 
    execute_state(x)
        Executes the state described as a tuple of parameters
    __call__(execTime)
        Performs the actual FSM commanding joint angles for execTime seconds
    """

    def __init__(self, pepperInstance, speed=.3, waveAngle=45) -> None:
        assert (speed >= 0.0 and speed <= 1.0)
        assert (waveAngle > 0 and waveAngle < 90)

        self.speed = speed
        # The variable self.state represents the current FSM state
        self.state = 0
        self.pepper = pepperInstance
        self.waveAngle = waveAngle

        state = namedtuple(
            'state', ['jointName', 'targetDegree', 'speed', 'nextState', 'threshold'])

        # Basic FSM Diagram
        # 0 -> 1 -> 2 -> 3 -> 4
        #                ^    |
        #                |____|

        self.fsm = [
            # Set the right shoulder in default position
            state(jointName="RShoulderPitch", targetDegree=0,
                  speed=1, nextState=1, threshold=1e-2),
            # Moves the arm to right direction rotating the shoulder
            state(jointName="RShoulderRoll", targetDegree=- \
                  90, speed=1, nextState=2, threshold=1e-2),
            # Flip the arm facing upward
            state(jointName="RShoulderPitch", targetDegree=- \
                  90, speed=1, nextState=3, threshold=1e-2),
            # Bend the elbow to 90 degree (first waving step)
            state(jointName="RElbowRoll", targetDegree=90,
                  speed=self.speed, nextState=4, threshold=1e-2),
            # Bend the elbow back to 90-self.waveAngle degree (second waving step).
            # Once this last state is executed, the following state will be again the state 3
            state(jointName="RElbowRoll", targetDegree=90-self.waveAngle,
                  speed=self.speed, nextState=3, threshold=1e-2),
        ]

    def degtorad(self, x):
        return x*pi/180

    def execute_state(self, state):
        # Setting the desired joint angle
        target = self.degtorad(state.targetDegree)
        # Error between the desired joint angle and the actual one
        error = abs(self.pepper.getAnglesPosition(state.jointName) - target)

        # If the error is small enough, then execute the state transition
        if error < state.threshold:
            self.state = state.nextState
        else:
            # Otherwise issue the command
            self.pepper.setAngles(state.jointName, target, state.speed)

    def __call__(self, execTime):
        beginTime = time.time()
        while time.time() - beginTime < execTime:
            self.execute_state(self.fsm[self.state])

        # Finally go back to the base configuration again
        self.pepper.goToPosture("StandZero", 1.)
        self.state = 0


class SaySkill():
    """
    A class used to implement a human-like robot speaking skill. It uses a Text To Speech plugin to synthesize a text.

    ...
    Methods
    -------
    __call__(text)
        Performs the actual TTS pronouncing the text passed as parameter
    """

    def __call__(self, text):
        # Creating a temporary file which will be deleted as soon as the associated object is closed
        with tempfile.NamedTemporaryFile(suffix=".mp3") as tmpFile:
            # Write the tts file
            gtts.gTTS(text).save(tmpFile.name)
            # Execute the tts file
            playsound(tmpFile.name)


class BehaviorRealizer():

    def __init__(self):
        # Loading Robot and  Ground
        simulation_manager = SimulationManager()
        client = simulation_manager.launchSimulation(gui=True)
        self.pepper = simulation_manager.spawnPepper(
            client, spawn_ground_plane=True)
        self.theSaySkill = SaySkill()
        self.theWavingSkill = WavingSkill(self.pepper)

    def say(self, text):
        threading.Thread(target=self.theSaySkill, args=(text,)).start()

    def waving(self, execTime=5):
        threading.Thread(target=self.theWavingSkill, args=(execTime,)).start()


if __name__ == "__main__":

    behavior_realizer_class = BehaviorRealizer()

    INPUT_OPTIONS = ["done", "waving", "say"]

    repeat_ = True
    while repeat_:
        user_input = input("INPUT : ")
        user_input = user_input.split(" ", 1)

        if user_input[0] == INPUT_OPTIONS[0]:
            repeat_ = False

        elif user_input[0] == INPUT_OPTIONS[1]:
            print("Executing waving")
            if len(user_input) > 1 and user_input[1].isnumeric():
                behavior_realizer_class.waving((int)(user_input[1]))
            else:
                print(
                    "\nTIP: you can also specify the duration of the waving by typing 'waving <TimeInSeconds>', e.g. 'waving 5'\n")
                behavior_realizer_class.waving()

        elif user_input[0] == INPUT_OPTIONS[2]:
            print("Executing say")
            if len(user_input) > 1 and user_input[1]:
                behavior_realizer_class.say(user_input[1])
            else:
                print(
                    "\nPlease specify the sentence to say. You can write 'say <sentence>', e.g. 'say hello world'\n")

        if not user_input[0] in INPUT_OPTIONS:
            print("Please enter 'done' to exit.")
