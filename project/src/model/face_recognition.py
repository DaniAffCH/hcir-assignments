
from typing import Any
import numpy as np
from utils_ import FaceClasses
import random
import torch
from facenet_pytorch import InceptionResnetV1
from PIL import Image
import cv2
from torchvision import transforms


class FaceRecognition():
    def __init__(self, path) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.trainedWeights = torch.load(path,map_location=self.device)

        self.model = InceptionResnetV1(pretrained='vggface2', device=self.device, classify= True, num_classes=3).to(self.device)
        self.model.load_state_dict(self.trainedWeights)
        self.model.eval()

        self.data_transforms = transforms.Compose([
            transforms.RandomResizedCrop(299),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        self.classNames = [FaceClasses.DANIELE, FaceClasses.KLARA, FaceClasses.UNAUTHORIZED]


    def __call__(self, img: np.ndarray) -> FaceClasses:

        if img is None:
            print("Error reading frame from video capture.")
            return FaceClasses.UNAUTHORIZED
        
        pil_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img = self.data_transforms(pil_image).unsqueeze(0).to(self.device)
        res = self.model(img)
        m = torch.argmax(res.detach())
        return self.classNames[m]

        return FaceClasses.DANIELE if random.random() < 0.6 else FaceClasses.KLARA
        return FaceClasses.UNAUTHORIZED # Hardcoded for now 