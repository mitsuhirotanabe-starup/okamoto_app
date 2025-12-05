import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import os

class MyModelClass(nn.Module):
    
    def __init__(self, NUM_CLASSES):
        super(MyModelClass, self).__init__()
        
        # EfficientNet-B4のベースモデルを取得
        try:
            model_base = models.efficientnet_b4(pretrained=False)
            num_filters = model_base.classifier[1].in_features
        except Exception as e:
            model_base = models.efficientnet_b4(weights=None)
            num_filters = model_base.classifier[1].in_features
            
        self.features = model_base.features
        self.avgpool = model_base.avgpool
        
        # 学習時と同じ分類器を定義
        self.classifier = nn.Sequential(
            nn.Linear(num_filters, 96),
            nn.GroupNorm(num_groups=4, num_channels=96),
            nn.Mish(),
            nn.Dropout(p=0.7),
            nn.Linear(96, NUM_CLASSES)
        )
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x
    
def predict(image): 
    # モデルの設定
    # 重みファイルは変更の可能性あり   
    NUM_CLASSES = 5
    IMG_SIZE = 512
    MODEL_PATH = "./model/finetune_with_yumawari_v2_0.pth"
    id_to_class = {
        0:"sunakui",
        1:"kirai",
        2:"dakon",
        3:"arasare",
        4:"yumawari"
    }

    # モデルのロード
    model = MyModelClass(NUM_CLASSES=NUM_CLASSES)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))

    # 画像の前処理
    val_transform = transforms.Compose([
            transforms.Resize((IMG_SIZE, IMG_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    input_tensor = val_transform(image)
    input_batch = input_tensor.unsqueeze(0).to(torch.device('cpu'))

    # 予測の実行
    model.eval()
    with torch.no_grad():
        output = model(input_batch)
        probabilities = torch.softmax(output, dim=1)
        top3_prob, top3_indices = torch.topk(probabilities, k=3, dim=1)
        
    results = []
    for i in range(top3_indices.size(1)):
        pred_id = top3_indices[0, i].item()
        pred_prob = top3_prob[0, i].item()
        results.append({
            "class_id": pred_id,
            "class_name": id_to_class[pred_id],
            "probability": pred_prob
        })
    return results

if __name__ == '__main__':
    # テストしたい画像のパス
    test_image = "./data/200.JPG"

    predictions = predict(test_image)
    
    # 結果の表示
    if predictions:
        print(f"'{test_image}' の予測結果:")
        for i, pred in enumerate(predictions):
            print(f"  {i+1}位: {pred['class_name']} (確率: {pred['probability']:.4f})")