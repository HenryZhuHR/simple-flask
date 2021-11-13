### Author    :  J. Yang
### Date      :  10/11/2021
### Function  :  Image reconstruction

import torch
from .modules import VectorQuantizedVAE

class Recon:
    def __init__(self, model_path, device):
        """
        :param model:       Dir of recon_model.pt, e.g. './api_recon/recon_model.pt'
        :param device:      Cuda device, e.g. 'cuda:1'
        :param image_in:    Input image tensor.
                                e.g. "/workspace/data.pt"
        """
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        ### Load Model and Parameters
        num_channels = 3
        hidden_size  = 256
        k            = 512
        self.model = VectorQuantizedVAE(num_channels, hidden_size, k).to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        self.model.eval()

    def recon(self, image_in):
        self.image_in = image_in
        img_ = self.image_in.unsqueeze(0)
        img_ = img_.to(self.device)
        reconstruction, _, _ = self.model(img_)
        return reconstruction.cpu()


# def main():
#     test = Recon(model='./api_recon/recon_model.pt', device='cuda:1')
#     r_tensor = test.recon()
#
# if __name__ == '__main__':
#     main()
