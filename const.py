# 不良名 → 不良グループ
label_to_group = {
    "kirai": 1,
    "sunakui": 1,
    "arasare": 1,
    "dakon": 2,
    "yumawari": 2,
}

# 不良グループ → 不良名
group_to_label = {
    1: ["sunakui", "arasare", "kirai"],
    2: ["dakon", "yumawari"],
}

# 不良グループ → ステップ2の質問コードリスト
group_to_step2 = {
    "1": ["V002", "V008", "V009"],
}

# 不良グループ → ステップ3の質問コードリスト
group_to_step3 = {
    "1": ["P004", "P005", "P001"],
}