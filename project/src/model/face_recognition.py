
from typing import Any
import numpy as np
from utils_ import FaceClasses
from torch import nn
import torch.nn.functional as F
import torch
from facenet_pytorch import InceptionResnetV1
from PIL import Image
import cv2
from torchvision import transforms
from facenet_pytorch import MTCNN

class Head(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.fc1 = nn.Linear(in_features=16128, out_features=1024, bias=False)
        self.fc2 = nn.Linear(1024, 3)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = F.normalize(x, p=2, dim=1)
        x = self.fc2(x)
        return F.softmax(x, dim=1)
    
class FaceRecognition():
    def __init__(self, path) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.trainedWeights = torch.load(path,map_location=self.device)

        originalInception = InceptionResnetV1(pretrained='vggface2', device=self.device, classify= True, num_classes=3).to(self.device)
        originalInception = nn.Sequential(*list(originalInception.children())[:-5])

        head = Head().to(self.device)
        self.recognitionModel = nn.Sequential(originalInception, head).to(self.device)

        self.cropModel = MTCNN(image_size=160, margin=0, keep_all=True, min_face_size=40)
        
        self.recognitionModel.load_state_dict(self.trainedWeights)
        self.recognitionModel.eval()

        self.data_transforms = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        self.classNames = [FaceClasses.DANIELE, FaceClasses.KLARA, FaceClasses.UNAUTHORIZED]


    def __call__(self, img: np.ndarray) -> FaceClasses:

        if img is None:
            print("Error reading frame from video capture.")
            return FaceClasses.UNAUTHORIZED
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_cropped_list, prob_list = self.cropModel(img, return_prob=True) 
        classification = None
        box = None

        if img_cropped_list is not None:

            box, _ = self.cropModel.detect(img)
            box = box[0]
            if prob_list[0]>0.90:
                custom_frame = img_cropped_list[0].unsqueeze(0).to(self.device)
                res = self.recognitionModel(custom_frame)
                m = torch.argmax(res.detach())
                classification = self.classNames[m]

        return classification, box