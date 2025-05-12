pth_path = '/pth/dlv3p_do_rgb_3.pth'


from app.galore.weedsgalore.src.nets import deeplabv3plus_resnet50
import torch
import torch.nn as nn
import cv2
import numpy as np

def getModel(path, num_classes=3, in_channels=3):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    net = deeplabv3plus_resnet50(num_classes=num_classes)
    net = net.to(device)
    net.backbone.conv1 = nn.Conv2d(in_channels, net.backbone.conv1.out_channels, kernel_size=7, stride=2, padding=3, bias=False, device=device)
    net.eval()
    return net

class predictor:
    def __init__(self):
        self.prevision = getModel(pth_path)

    def predict(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = torch.from_numpy(image).float() / 255.0  # Normaliza se necessário
        image = image.permute(2, 0, 1).unsqueeze(0)       # [1, 3, H, W]

        with torch.no_grad():
            output = self.prevision(image)               # Esperado: [1, 3, H, W]

        if output.dim() == 4:
            prediction = torch.argmax(output, dim=1)     # [1, H, W]
        else:
            raise ValueError("Saída do modelo não tem 4 dimensões (esperado [1, C, H, W])")

        mask = prediction.squeeze(0).cpu().numpy().astype(np.uint8)  # [H, W] com valores 0,1,2

        return mask
