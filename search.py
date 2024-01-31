import os
import clip
import torch

from PIL import Image
from torch.nn.functional import normalize

def clip_search(query_path, dataset_path, device="cuda", n_results=10):
    model, preprocess = clip.load("ViT-B/32", device=device) #Must set jit=False for training
    
    filenames = os.listdir(dataset_path)
    images = []
    for filename in filenames:
        im_path = f"{dataset_path}/{filename}"
        images.append(preprocess(Image.open(im_path)).unsqueeze(0).to(device))

    image_inputs = torch.cat(images)
    with torch.no_grad():
        dataset_image_features = model.encode_image(image_inputs)
    
    image_input = preprocess(Image.open(query_path)).unsqueeze(0).to(device)
    image_features = model.encode_image(image_input)

    image_x_norm = normalize(image_features)
    image_y_norm = normalize(dataset_image_features)

    image_sim = torch.mm(image_x_norm, image_y_norm.T)[0]

    image_sim_pairs = []
    for i in range(len(image_sim)):
        image_sim_pairs.append((i, image_sim[i].item()))
    sort_by_sim = lambda x: x[1]

    image_sim_pairs.sort(key=sort_by_sim, reverse=True)

    return list(map(lambda x: filenames[x[0]], image_sim_pairs[:n_results]))

