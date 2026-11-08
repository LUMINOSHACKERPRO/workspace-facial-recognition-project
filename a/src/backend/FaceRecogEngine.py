from facenet_pytorch import InceptionResnetV1, MTCNN
import torch
from PIL import Image

from pathlib import Path
from itertools import combinations

import torch.nn.functional as Func

import io
import base64


class FaceRecognitionEngine():
    
    def __init__(self) -> None:
        self.device = "cpu"
        self.mtcnn = MTCNN(image_size= 160, margin=20, device=self.device)
        self.model = InceptionResnetV1(pretrained="vggface2").eval().to(self.device)
    
    @staticmethod
    def __decode_base64_image(base64_img: str):
        raw_bytes = base64.b64decode(base64_img)
        return Image.open(io.BytesIO(raw_bytes)).convert("RGB")

    def embed(self, base64_img):
        image = self.__decode_base64_image(base64_img)
        
        face = self.mtcnn(image)
        if face is None:
            return None
        with torch.no_grad():
            embedding = self.model(face.unsqueeze(0).to(self.device)).cpu()

        embedding  = Func.normalize(embedding, p=2, dim=1)

        return embedding.squeeze(0).cpu().numpy()
