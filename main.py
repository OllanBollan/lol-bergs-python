# -*- coding: utf-8 -*-
        
def lasinfil(fil):
    infil = open(fil,'r', encoding='utf-8')
    dict_objects = dict()
    rader = infil.readlines()
    infil.close()
    for rad in rader:
        ingred = list()
        if fil == 'sallad.txt':
            rad2 = rad.strip()
            raddelar = rad2.split(':')
            ingredienser = raddelar[1].split(',')
            for i in ingredienser:
                ingred.append(i.strip())
            dict_objects[raddelar[0]] = [ingred,raddelar[2]]
        if fil == 'ingrediens.txt':
            i = rad.strip()
            ingredienser = i.split(':')
            dict_objects[ingredienser[0]] = (ingredienser[1])
    return dict_objects

def match_sallad(sallader, ingredienser):
    count_dict = dict()
    for sallad in sallader.keys():
        matching_ingred = list()
        non_matching_ingred = list()
        for i in ingredienser:
            if i in sallader[sallad][0]:
                matching_ingred.append(i)
            else:
                non_matching_ingred.append(i)
        count_dict[sallad]= [matching_ingred,non_matching_ingred]
    return count_dict

def calc_sallad(count_dict,sallader, ingredients_w_prices):
    sorted_dict = dict(sorted(count_dict.items(), key=lambda x: len(x[1])))
    target_key = next(iter(sorted_dict))
    target_value = len(sorted_dict[target_key][1])
    temp_dict = dict()
    printed_flag = False

    for key, value in sorted_dict.items():
        if len(value[1]) == 0:
            ingred = '\n'.join(['- ' + item for item in sallader[key][0]])
            print(f"{key} - {sallader[key][1]} kr. Innehåller: \n{ingred}.")
            printed_flag = True
            print('\n Inga ingredienser behöver läggas till\n')
        elif target_value > 0 and len(value[1]) == target_value:
            temp_dict[key] = sallader[key]
    
    if bool(temp_dict) and not printed_flag:
        print(temp_dict)
        sorted_price_dict = dict(sorted(temp_dict.items(), key=lambda x: x[1]))
        lowest_price_key = next(iter(sorted_price_dict))
        print(sallader[lowest_price_key])
        ingred = '\n'.join(['- ' + item for item in sallader[lowest_price_key][0]])
        print(f"{lowest_price_key} - {sallader[lowest_price_key][1]} kr. Innehåller:\n{ingred}.")
        print('Följande ingredienser behöver kompletteras:')
        for item in count_dict[lowest_price_key][1]:
            print(f"{item} - {ingredients_w_prices[item]} kr.")

def order_meny(option, dict_sallad_ingrediens):
    val_dict = dict()
    if option == 'sallad':
        op1 = 'sallad(er)'
        op2 = 'en sallad'
    if option == 'extraval':
        op1 = 'vilka extra val'
        op2 = 'ett extra val'
    val = input('Ange ' + op1 + ' du vill beställa (separera med kommatecken) ').split(',')
    for v in val:
        v1 = v.strip()
        if v1 not in dict_sallad_ingrediens.keys():
            if option == 'sallad':
                print('Ogiltigt val, ' + v + ' är inte ' + op2 + ' på menyn')
                val_dict = order_meny(option,dict_sallad_ingrediens)
            return val_dict
        else: val_dict[v1] = dict_sallad_ingrediens[v1]
    return val_dict
        




def main():
    sallader = lasinfil('sallad.txt')
    ingredients_w_prices = lasinfil('ingrediens.txt')
    print('Välkommen till Kalles Salladsbar')
    sallad = []
    extraval = []
    order_number = 1
    menyval = 1
    meny_text = '1 - matcha nya ingredienser \n2 - Beställa sallad och extraval \n3 - Skriv ut kvitto \n4 - Avsluta \nGör ditt val: '
    ordering = True
    while ordering == True:
        if menyval == 1:
            ingrediens = input('Vilka ingredienser vill du ha? (separera med mellanslag):').split()
            count_dict = match_sallad(sallader,ingrediens)
            calc_sallad(count_dict,sallader,ingredients_w_prices)
            menyval = int(input(meny_text))
        if menyval == 2:
            sallad = order_meny('sallad',sallader)
            extraval = order_meny('extraval',ingredients_w_prices)

            menyval = int(input(meny_text))
        if menyval == 3:
            if sallad:
                tot_cost = 0
                utfil = open('kvitto.txt','a')
                utfil.write(f'\nOrdernummer: {order_number}\n')
                utfil.write('Du har beställt:\n')
                for s in sallad.keys():
                    utfil.write(f"{s}: {sallad[s][1]} kr.\n")
                    tot_cost += int(sallad[s][1])
                for e in extraval.keys():
                    utfil.write(f"{e} - {extraval[e]} kr.\n")
                    tot_cost += int(extraval[e])
                utfil.write('Totalt: ' + str(tot_cost) + ' kr\n')
                utfil.close()
                order_number +=1
                print('Ditt kvitto skrevs ut!')
            else: print('Du har inte valt en sallad. \n')
            menyval = int(input(meny_text))
        if menyval not in [1,2,3] :
            print('Beställningsomgång avslutat. Hej då!')
            ordering = False

main()
