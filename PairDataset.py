import os
from PIL import Image
from torch.utils.data import Dataset

supported_img_formats = ('.png', '.jpg', '.jpeg')

class ContentStylePairDataset(Dataset):

    def __init__(self, contentPath, stylePath, content_transforms=None, style_transforms=None):
        super(Dataset, self).__init__()
        self.contentTransforms = content_transforms
        self.styleTransforms = style_transforms

        if str(contentPath).endswith(supported_img_formats):
            self.pairs_fn = [(contentPath, stylePath)]
        else:
            self.pairs_fn = []
            for c in os.listdir(contentPath):
                for s in os.listdir(stylePath):
                    self.pairs_fn.append((os.path.join(contentPath, c), os.path.join(stylePath, s)))

    def __len__(self):
        return len(self.pairs_fn)

    def __getitem__(self, idx):
        pair = self.pairs_fn[idx]
        content = Image.open(pair[0]).convert(mode='RGB')
        style = Image.open(pair[1]).convert(mode='RGB')

        if self.contentTransforms:
            content = self.contentTransforms(content)

        if self.styleTransforms:
            style = self.styleTransforms(style)

        return {'content': content, 'contentPath': pair[0], 'style': style, 'stylePath': pair[1]}