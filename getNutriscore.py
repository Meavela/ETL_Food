def calculeNutriscore(product):
    negative_point = 0
    positive_point = 0
    if (product.energy_kj_100g != ""):
        if (float(product.energy_kj_100g) > 335 and float(product.energy_kj_100g) <= 670):
            negative_point += 1
        elif (float(product.energy_kj_100g) > 670 and float(product.energy_kj_100g) <= 1005):
            negative_point += 2
        elif (float(product.energy_kj_100g) > 1005 and float(product.energy_kj_100g) <= 1340):
            negative_point += 3
        elif (float(product.energy_kj_100g) > 1340 and float(product.energy_kj_100g) <= 1675):
            negative_point += 4
        elif (float(product.energy_kj_100g) > 1675 and float(product.energy_kj_100g) <= 2010):
            negative_point += 5
        elif (float(product.energy_kj_100g) > 2010 and float(product.energy_kj_100g) <= 2345):
            negative_point += 6
        elif (float(product.energy_kj_100g) > 2345 and float(product.energy_kj_100g) <= 2680):
            negative_point += 7
        elif (float(product.energy_kj_100g) > 2680 and float(product.energy_kj_100g) <= 3015):
            negative_point += 8
        elif (float(product.energy_kj_100g) > 3015 and float(product.energy_kj_100g) <= 3350):
            negative_point += 9
        elif (float(product.energy_kj_100g) > 3350):
            negative_point += 10
    if (product.sugars_100g != ""):
        if (float(product.sugars_100g) > 4.5 and float(product.sugars_100g) <= 9):
            negative_point += 1
        elif (float(product.sugars_100g) > 9 and float(product.sugars_100g) <= 13.5):
            negative_point += 2
        elif (float(product.sugars_100g) > 13.5 and float(product.sugars_100g) <= 18):
            negative_point += 3
        elif (float(product.sugars_100g) > 18 and float(product.sugars_100g) <= 22.5):
            negative_point += 4
        elif (float(product.sugars_100g) > 22.5 and float(product.sugars_100g) <= 27):
            negative_point += 5
        elif (float(product.sugars_100g) > 27 and float(product.sugars_100g) <= 31):
            negative_point += 6
        elif (float(product.sugars_100g) > 31 and float(product.sugars_100g) <= 36):
            negative_point += 7
        elif (float(product.sugars_100g) > 36 and float(product.sugars_100g) <= 40):
            negative_point += 8
        elif (float(product.sugars_100g) > 40 and float(product.sugars_100g) <= 45):
            negative_point += 9
        elif (float(product.sugars_100g) > 45):
            negative_point += 10
    if (product.saturated_fat_100g != ""):
        if (float(product.saturated_fat_100g) > 1 and float(product.saturated_fat_100g) <= 2):
            negative_point += 1
        elif (float(product.saturated_fat_100g) > 2 and float(product.saturated_fat_100g) <= 3):
            negative_point += 2
        elif (float(product.saturated_fat_100g) > 3 and float(product.saturated_fat_100g) <= 4):
            negative_point += 3
        elif (float(product.saturated_fat_100g) > 4 and float(product.saturated_fat_100g) <= 5):
            negative_point += 4
        elif (float(product.saturated_fat_100g) > 5 and float(product.saturated_fat_100g) <= 6):
            negative_point += 5
        elif (float(product.saturated_fat_100g) > 6 and float(product.saturated_fat_100g) <= 7):
            negative_point += 6
        elif (float(product.saturated_fat_100g) > 7 and float(product.saturated_fat_100g) <= 8):
            negative_point += 7
        elif (float(product.saturated_fat_100g) > 8 and float(product.saturated_fat_100g) <= 9):
            negative_point += 8
        elif (float(product.saturated_fat_100g) > 9 and float(product.saturated_fat_100g) <= 10):
            negative_point += 9
        elif (float(product.saturated_fat_100g) > 10):
            negative_point += 10
    if (product.sodium_100g != ""):
        if (float(product.sodium_100g) > 0.09 and float(product.sodium_100g) <= 0.180):
            negative_point += 1
        elif (float(product.sodium_100g) > 0.180 and float(product.sodium_100g) <= 0.270):
            negative_point += 2
        elif (float(product.sodium_100g) > 0.270 and float(product.sodium_100g) <= 0.360):
            negative_point += 3
        elif (float(product.sodium_100g) > 0.360 and float(product.sodium_100g) <= 0.450):
            negative_point += 4
        elif (float(product.sodium_100g) > 0.450 and float(product.sodium_100g) <= 0.540):
            negative_point += 5
        elif (float(product.sodium_100g) > 0.540 and float(product.sodium_100g) <= 0.630):
            negative_point += 6
        elif (float(product.sodium_100g) > 0.630 and float(product.sodium_100g) <= 0.720):
            negative_point += 7
        elif (float(product.sodium_100g) > 0.720 and float(product.sodium_100g) <= 0.810):
            negative_point += 8
        elif (float(product.sodium_100g) > 0.810 and float(product.sodium_100g) <= 0.900):
            negative_point += 9
        elif (float(product.sodium_100g) > 0.900):
            negative_point += 10
    if (product.fiber_100g != ""):
        if (float(product.fiber_100g) > 0.9 and float(product.fiber_100g) <= 1.9):
            positive_point += 1
        elif (float(product.fiber_100g) > 1.9 and float(product.fiber_100g) <= 2.8):
            positive_point += 2
        elif (float(product.fiber_100g) > 2.8 and float(product.fiber_100g) <= 3.7):
            positive_point += 3
        elif (float(product.fiber_100g) > 3.7 and float(product.fiber_100g) <= 4.7):
            positive_point += 4
        elif (float(product.fiber_100g) > 4.7):
            positive_point += 5
    if (product.proteins_100g != ""):
        if (float(product.proteins_100g) > 1.6 and float(product.proteins_100g) <= 3.2):
            positive_point += 1
        elif (float(product.proteins_100g) > 3.2 and float(product.proteins_100g) <= 4.8):
            positive_point += 2
        elif (float(product.proteins_100g) > 4.8 and float(product.proteins_100g) <= 6.4):
            positive_point += 3
        elif (float(product.proteins_100g) > 6.4 and float(product.proteins_100g) <= 8):
            positive_point += 4
        elif (float(product.proteins_100g) > 8):
            positive_point += 5
    total = negative_point - positive_point
    if (total < 0):
        return 'a'
    elif (total >= 0 & total <= 2):
        return 'b'
    elif (total >= 3 & total <= 10):
        return 'c'
    elif (total >= 11 & total <= 18):
        return 'd'
    elif (total >= 19):
        return 'e'