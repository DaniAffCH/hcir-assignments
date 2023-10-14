from collections import Counter
from qibullet import SimulationManager
import gtts
from playsound import playsound
import threading
import time
import tempfile

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

    def degtorad(self, x):
        return x*pi/180

    # Basic FSM Diagram
    # 1 -> 2 -> 3 -> 4
    #           ^    |
    #           |____|

    def __call__(self, execTime):
        beginTime = time.time()
        while time.time() - beginTime < execTime:

            # Set the right shoulder in default position
            if self.state == 0:
                # Setting the desired joint angle
                target = self.degtorad(0)
                # Command the execution
                self.pepper.setAngles("RShoulderPitch", target, 1.)
                # Error between the desired joint angle and the actual one
                error = abs(self.pepper.getAnglesPosition(
                    "RShoulderPitch") - target)
                # If the error is small enough, then execute a state transition
                if error < 1e-2:
                    self.state = 1

            # Moves the arm to right direction rotating the shoulder
            elif self.state == 1:
                target = self.degtorad(-90)
                self.pepper.setAngles("RShoulderRoll", target, 1.)
                error = abs(self.pepper.getAnglesPosition(
                    "RShoulderRoll") - target)
                if error < 1e-2:
                    self.state = 2

            # Flip the arm facing upward
            elif self.state == 2:
                target = self.degtorad(-90)
                self.pepper.setAngles("RShoulderPitch", target, 1.)
                error = abs(self.pepper.getAnglesPosition(
                    "RShoulderPitch") - target)
                if error < 1e-2:
                    self.state = 3

            # Bend the elbow to 90 degree (first waving step)
            elif self.state == 3:
                target = self.degtorad(90)
                self.pepper.setAngles("RElbowRoll", target, self.speed)
                error = abs(self.pepper.getAnglesPosition(
                    "RElbowRoll") - target)
                if error < 1e-2:
                    self.state = 4

            # Bend the elbow back to 90-self.waveAngle degree (second waving step).
            # Once this last state is executed, the following state will be again the state 3
            elif self.state == 4:
                target = self.degtorad(90-self.waveAngle)
                self.pepper.setAngles("RElbowRoll", target, self.speed)
                error = abs(self.pepper.getAnglesPosition(
                    "RElbowRoll") - target)
                if error < 1e-2:
                    self.state = 3

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
                    "\n[TIP: you can also specify the duration of the waving by typing 'waving <TimeInSeconds>', e.g. 'waving 5']\n")
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
