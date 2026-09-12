# Dataset Preparation Guide

## Folder Structure Required
```
dataset/
├── paper/
│   ├── img001.jpg
│   ├── img002.jpg
│   └── ...
├── plastic/
├── cardboard/
├── metal/
├── organic/
└── battery/
```

## Recommendations for Good Accuracy
- Collect **at least 80–150 images per class**.
- Capture from different angles, distances, and lighting conditions.
- Include both clean and slightly dirty / crumpled items.
- Keep background relatively consistent during training (or add variety deliberately).
- Use the same camera that will be used in the final prototype if possible.

## Public Datasets You Can Start With
- TrashNet (garythung/trashnet)
- Various Kaggle waste classification datasets
- Your own collected images (strongly recommended for better real-world performance)

## After Collecting Data
1. Place images in the correct class folders under `dataset/`.
2. Run `python train_waste_classifier.py` from the `code/` directory.
3. The script will automatically split data into training (80%) and validation (20%).
