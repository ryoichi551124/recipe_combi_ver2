import numpy as np
import pandas as pd
import random


main = pd.read_csv('rakuten_main.csv')
sub = pd.read_csv('rakuten_sub.csv')
soup = pd.read_csv('rakuten_soup.csv')

#基本の空のデータ
combi = pd.read_csv('combi.csv', index_col=0)
#材料のリストの取得
all_list = combi.columns[6:]
#トータル(train)データの初期化
combis = combi.copy(deep=True)


#OKかNOを判定してtrain.csvに組み合わせデータを追加する処理
def choice(main_num, sub_num, soup_num, judge):
    global combi, combis

    main_num = int(main_num)
    sub_num = int(sub_num)
    soup_num = int(soup_num)

    combi['主菜'] = main['recipeTitle'][main_num]
    combi['副菜'] = sub['recipeTitle'][sub_num]
    combi['汁物'] = soup['recipeTitle'][soup_num]
    combi['主菜ID'] = main['recipeId'][main_num]

    for material in all_list:
        if material in main['recipeMaterial'][main_num]:
            combi[material] += 1
        if material in sub['recipeMaterial'][sub_num]:
            combi[material] += 1
        if material in soup['recipeMaterial'][soup_num]:
            combi[material] += 1

    if judge:
        combi['採用/不採用'] = 1

    combis = pd.concat([combis, combi])
    #基本の空のデータをID以外初期化
    combi['ID'] += 1
    combi.iloc[0, 1:] = 0
    combis.to_csv('train.csv', index=False)


#主菜、副菜、汁物のランダムなデータを取得
def random_get():
    main_num = random.randint(0, len(main))
    sub_num = random.randint(0, len(sub))
    soup_num = random.randint(0, len(soup))

    recipe = {
        'main_image': main['mediumImageUrl'][main_num],
        'sub_image': sub['mediumImageUrl'][sub_num],
        'soup_image': soup['mediumImageUrl'][soup_num],
        'main_name': main['recipeTitle'][main_num],
        'sub_name': sub['recipeTitle'][sub_num],
        'soup_name': soup['recipeTitle'][soup_num],
        'main_num': main_num,
        'sub_num': sub_num,
        'soup_num': soup_num,
    }
    return recipe

