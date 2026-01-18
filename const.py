# 不良名 → 不良グループ
label_to_group = {
    "kirai": 1,
    "sunakui": 1,
    "arasare": 1,
    # "norokami": 1,
    "dakon": 2,
    "ware": 2,
    "hike": 3,
    "hikesu": 3,
    "migui": 4,
    "nakago-koware": 5,
    "yusakai": 6,
}

# 不良グループ → 不良名
group_to_label = {}
for label, group_id in label_to_group.items():
    if group_id not in group_to_label:
        group_to_label[group_id] = []
    group_to_label[group_id].append(label)

# 不良グループ → ステップ2の質問コードリスト
group_to_step2 = {
    "1": ["V002", "V008", "V009"],
}

# 不良グループ → ステップ3の質問コードリスト
group_to_step3 = {
    "1": ["P004", "P005", "P001"],
}

label_name = ['キライ', '砂喰い', '荒らされ', '打こん', '湯境', '中子壊れ', 'ひけ巣', '身喰い', '割れ', 'ひけ']

ja_to_en_label = {
    'キライ': 'kirai',
    '砂喰い': 'sunakui',
    '荒らされ': 'arasare',
    '打こん': 'dakon',
    '湯境': 'yusakai',
    '中子壊れ': 'nakago-koware',
    'ひけ巣': 'hikesu',
    '身喰い': 'migui',
    '割れ': 'ware',
    'ひけ': 'hike',
}

en_to_ja_label = {v: k for k, v in ja_to_en_label.items()}