# -*- coding: utf-8 -*-
        
#combined file for reading both ingredients and sallad from files
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
            #adds the name of the salad as a key in a dict, with a list/array containing a list of all the ingredients and the total price of the salad
            dict_objects[raddelar[0]] = [ingred,raddelar[2]]
        if fil == 'ingrediens.txt':
            i = rad.strip()
            ingredienser = i.split(':')
            #adds the name of the ingredient as key and ingredienser[1] contains the price for each ingredient
            dict_objects[ingredienser[0]] = (ingredienser[1])
    return dict_objects

#function to match a salad with the ingredients sent by the customer in input
def match_sallad(sallader, ingredienser,ingredients_w_price):
    count_dict = dict()
    for i in ingredienser:
        if i not in ingredients_w_price.keys():
            print(f'{i} är inte en tillgänglig ingrediens och borträknas därför. Vänligen testa igen.')
            ingredienser.remove(i)

    #for each salad we create 2 lists, one containing matching ingredients and one not matching
    for sallad in sallader.keys():
        matching_ingred = list()
        non_matching_ingred = list()
        for i in ingredienser:
            if i in sallader[sallad][0]:
                matching_ingred.append(i)
            else:
                non_matching_ingred.append(i)
        #we store the 2 lists in a dict where the salad in question is the key
        count_dict[sallad]= [matching_ingred,non_matching_ingred,len(non_matching_ingred)]
    return count_dict

#method for calculating which salad to return
def calc_sallad(count_dict,sallader, ingredients_w_prices):
    #we sort a copy of the dict on the length of the non_matching ingredients(we stored this value in the list back in match_salad).
    #If non_matching has a length of 0 then the salad is a match
    sorted_dict = dict(sorted(count_dict.items(), key=lambda x: x[1][2]))
    #take the first key in the dict, should have the lowest number of non_matches
    target_key = next(iter(sorted_dict))
    #target_value is the shortest length of the non_matches
    target_value = sorted_dict[target_key][2]
    #temporary empty dict
    temp_dict = dict()
    #flag to keep track if information has been printed to console
    printed_flag = False
    
    for key in sorted_dict.keys():
        #if the length is 0 then the salad contains all the user's ingredients
        #all salad that contain the ingredients should be returned
        #printed_flag is set as soon as something about the salads is printed to console
        if sorted_dict[key][2] == 0:
            ingred = '\n'.join(['- ' + item for item in sallader[key][0]])
            print(f"{key} - {sallader[key][1]} kr. Innehåller: \n{ingred}.")
            printed_flag = True
            print('\n Inga ingredienser behöver läggas till\n')
        #if target_value > 0 it means that no salad matched all ingredients, and now we're trying to look for salads where subsitutions are needed
        #Target_value should be the lowest length of the non_matching ingredients.
        # len(value[1]) == target_value sorts out all salads that have the same number of non_matching ingredients as the salad that most closely matches the users specification
        elif target_value > 0 and sorted_dict[key][2] == target_value:
            temp_dict[key] = sallader[key]
    
    #check if the temporary dict has any values in it and that nothing has been printed to console so far.
    if bool(temp_dict) and not printed_flag:
        #sort the temp dict on the salad price
        sorted_price_dict = dict(sorted(temp_dict.items(), key=lambda x: x[1][1]))
        #find the salad with the lowest price
        lowest_price_key = next(iter(sorted_price_dict))
        ingred = '\n'.join(['- ' + item for item in sallader[lowest_price_key][0]])
        print(f"{lowest_price_key} - {sallader[lowest_price_key][1]} kr. Innehåller:\n{ingred}.")
        print('Följande ingredienser behöver kompletteras:')
        for item in count_dict[lowest_price_key][1]:
            print(f"{item} - {ingredients_w_prices[item]} kr.")

#Function to make the ingredient choice avoid code duplication, as the lists are kinda similar
def order_meny(option, dict_sallad_ingrediens):
    val_dict = dict()
    if option == 'sallad':
        op1 = 'sallad(er)'
        op2 = 'en sallad'
        for sallad in dict_sallad_ingrediens.keys():
            print(f"{sallad} - {dict_sallad_ingrediens[sallad][1]}")
    if option == 'extraval':
        op1 = 'vilka extra val'
        op2 = 'ett extra val'
        for extraval in dict_sallad_ingrediens.keys():
            print(f"{extraval} - {dict_sallad_ingrediens[extraval]}")
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
            count_dict = match_sallad(sallader,ingrediens,ingredients_w_prices)
            calc_sallad(count_dict,sallader,ingredients_w_prices)
            menyval = int(input(meny_text))
        if menyval == 2:
            sallad = order_meny('sallad',sallader)
            extraval = order_meny('extraval',ingredients_w_prices)
            print("Beställning lagd")

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
