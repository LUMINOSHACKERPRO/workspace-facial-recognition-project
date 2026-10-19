from facenet_pytorch import InceptionResnetV1, MTCNN
import torch
from PIL import Image

from pathlib import Path
from itertools import combinations

device = "cpu"
mtcnn = MTCNN(image_size= 160, margin=20, device=device)
model = InceptionResnetV1(pretrained="vggface2").eval.to(device)

def embed(path):
    face = mtcnn(Image.open(path).convert("RGB"))
    if face is None:
        return None
    with torch.no_grad():
        return model(face.unsqueeze(0).to(device))[0].cpu()
