from typing import Any
import gtts
from pygame import mixer
import time
import tempfile
from collections import namedtuple

from math import pi, atan2, sin
class PoseSkill():

    """
    A class used to implement a pose skill. The skill brings the robot to a given configuration.

    ...

    Attributes
    ----------
    pepper : qibullet.pepper_virtual.PepperVirtual
        pepper instance

    Methods
    -------
    degtorad(x)
        Converts x degrees into radians 
    __call__(poseDict, execTime)
        brings the robot in the configuration specified in poseDict for execTime seconds
    """

    def __init__(self, pepper) -> None:
        self.pepper = pepper

    def degtorad(self, x):
        return x*pi/180

    def __call__(self, poseDict, execTime) -> Any:
        beginTime = time.time()
        while time.time() - beginTime < execTime:
            # set every joint angle specified in the dictionary
            for k in poseDict:
                self.pepper.setAngles(k, self.degtorad(poseDict[k]), 0.5)
        self.pepper.goToPosture("StandInit", 0.5)


class NodSkill():
    """
    A class used to implement a top to down nod skill.

    ...

    Attributes
    ----------
    pepper : qibullet.pepper_virtual.PepperVirtual
        pepper instance

    Methods
    -------
    __call__(execTime)
        executes the top to down nod given an execution time.
    """

    def __init__(self, pepper) -> None:
        self.pepper = pepper

    def __call__(self, execTime) -> Any:
        beginTime = time.time()

        # sinusoidal trajectory for the head pitch
        def f(t): return -pi/4*sin(2*pi*t/execTime)

        while time.time() - beginTime < execTime:
            t = time.time() - beginTime
            # apply f(t)
            self.pepper.setAngles("HeadPitch", f(t), 1.)

        self.pepper.goToPosture("StandZero", 0.5)


class LookAtRelativePointSkill():
    """
    A class used to orient the head torward a relative point.

    ...

    Attributes
    ----------
    pepper : qibullet.pepper_virtual.PepperVirtual
        pepper instance

    Methods
    -------
    __call__(x,y,z,execTime)
        orient the head torward the 3D relative point (x,y,z) and look at that point for execTime seconds.
    """
    def __init__(self, pepper) -> None:
        self.pepper = pepper

    def __call__(self, x, y, z, execTime):
        beginTime = time.time()
        while time.time() - beginTime < execTime:
            # head yaw angle obtained by applying the atan2 function to the x,y components
            yawAngle = atan2(y, x)
            self.pepper.setAngles("HeadYaw", yawAngle, 1.)
            # head pitch angle obtained by applying the atan2 function to the -z,x components.
            # The minus in front of the z axis is because the reference frame axis points down.
            pitchAngle = atan2(-z, x)
            self.pepper.setAngles("HeadPitch", pitchAngle, 1.)

        self.pepper.goToPosture("StandInit", 0.5)


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
                  0, speed=1, nextState=3, threshold=1e-2),
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
        self.pepper.goToPosture("StandInit", 1.)
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
    def __init__(self) -> None:
        mixer.init()

    def __call__(self, text):
        # Creating a temporary file which will be deleted as soon as the associated object is closed
        with tempfile.NamedTemporaryFile(suffix=".mp3") as tmpFile:
            # Write the tts file
            gtts.gTTS(text).save(tmpFile.name)
            # Execute the tts file
            sound = mixer.Sound(tmpFile.name)
            sound.play()
            time.sleep(sound.get_length())

class BehaviorRealizer():

    def __init__(self, pepper):
        self.theSaySkill = SaySkill()
        self.theWavingSkill = WavingSkill(pepper)
        self.theLookAtRelativePointSkill = LookAtRelativePointSkill(pepper)
        self.theNodeSkill = NodSkill(pepper)
        self.thePoseSkill = PoseSkill(pepper)
        self.pepper = pepper

    def say(self, text):
        self.theSaySkill(text)

    def waving(self, execTime=5):
        self.theWavingSkill(execTime)

    def cross(self, execTime=5):
        joint_angles = {
            "RShoulderPitch": -90, 
            "LShoulderPitch": -90,
            "RElbowRoll": 90,
            "LElbowRoll": -90,
        }
        self.thePoseSkill(joint_angles, execTime)

    def lookAtRelativePoint(self, x, y, z, execTime=5):
        self.theLookAtRelativePointSkill(x, y, z, execTime)

    def nod(self, execTime=5):
        self.theNodeSkill(execTime)

    def happySwirl(self, execTime=5):
        joint_angles = {
            "HipRoll": 60.0,
            "KneePitch": 5.0,
            "LShoulderPitch": -90.0,
            "RShoulderPitch": -90.0,
        }
        self.thePoseSkill(joint_angles, execTime)

    def standInit(self):
        self.pepper.goToPosture("StandInit", 0.5)
        
    def talkingPose(self, execTime=5):
        joint_angles = {
            "RShoulderPitch": 90, 
            "LShoulderPitch": 50,
            "RElbowRoll": 70,
            "LElbowRoll": -20,
            "LElbowYaw": -104,
            "RElbowYaw": 120,
            "LWristYaw": -104,
            "RWristYaw": 120
        }
        self.thePoseSkill(joint_angles, execTime)

    def agreeGesture(self, execTime=5):
        joint_angles = {
            "RShoulderPitch": 50, #
            "RShoulderRoll": 10,
            "RElbowRoll": 50,
            "RElbowYaw": 120,
            "RWristYaw": 70,
            "LShoulderPitch": 100
        }
        self.thePoseSkill(joint_angles, execTime)