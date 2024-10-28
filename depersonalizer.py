import pandas as pd
import csv


def read_csv(infile):
    inlist = []
    with open(f'A:/educ/algos/Depersonalizer/input_data/{infile}.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            inlist.append(row)
    f.close()
    tagged_data = {'shop': [], 'place': [], 'date': [], 'time': [], 'card': [], 'quantity': [],'goods': [], 'sum': []}
    for elem in inlist:
        tagged_data['shop'].append(elem[0])
        tagged_data['place'].append(elem[1])
        tagged_data['date'].append(elem[2])
        tagged_data['time'].append(elem[3])
        tagged_data['card'].append(elem[4])
        tagged_data['quantity'].append(elem[5])
        tagged_data['goods'].append('Данные удалены')
        tagged_data['sum'].append(elem[7])
    df = pd.DataFrame(tagged_data)
    return df


def shop_dict_builder(in_file='set-1'):
    source = open(f'A:/educ/algos/Depersonalizer/input_data/{in_file}.txt', "r", encoding="utf8")
    shoplist = {}
    for pstring in source:
        current_shop = list(pstring.split(' == '))
        current_shop[2] = current_shop[2].split(', ')
        current_shop[2][0] = int(current_shop[2][0])
        current_shop[2][1] = int(current_shop[2][1])

        current_shop[1] = current_shop[1].split(', ')
        current_shop[1][0] = round(float(current_shop[1][0]), 8)
        current_shop[1][1] = round(float(current_shop[1][1]), 8)

        current_shop[3] = current_shop[3].replace('\n', '')

        shoplist[current_shop[0]] = current_shop[1:4]
    source.close()
    return shoplist


def hide_shop(df, column):
    replace = []
    for shop in df[column]:
        replace.append(shops[shop][2])

    df[column] = replace
    print('Произведено обезличивание по магазинам.')
    return df


def hide_place(df, column):
    replace = []
    for place in df[column]:
        place = place.split(', ')
        if float(place[0]) < 59.9833:
            place = 'Юг'
        else:
            place = 'Север'
        replace.append(place)

    df[column] = replace
    print('Произведено обезличивание по геолокации.')
    return df


def hide_date(df, column):
    replace = []
    for date in df[column]:
        date = date.split('/')
        if int(date[1]) <= 4:
            date = '1 треть ' + date[2]
        elif 4 < int(date[1]) <= 8:
            date = '2 треть ' + date[2]
        else:
            date = '3 треть ' + date[2]
        replace.append(date)

    df[column] = replace
    print('Произведено обезличивание по дате.')
    return df


def hide_card(df, column):
    replace = []
    for card in df[column]:
        if card[:4] == '2202':
            card = 'Сбер МИР'
        elif card[:4] == '2204':
            card = 'ВТБ МИР'
        elif card[:4] == '2200':
            card = 'Тинькофф МИР'
        elif card[:4] == '4276':
            card = 'Сбер ВИЗА'
        elif card[:4] == '4475':
            card = 'ВТБ ВИЗА'
        elif card[:4] == '4377':
            card = 'Тинькофф ВИЗА'
        elif card[:4] == '5469':
            card = 'Сбер МАСТЕРКАРД'
        elif card[:4] == '5278':
            card = 'ВТБ МАСТЕРКАРД'
        else:
            card = 'Тинькофф МАСТЕРКАРД'
        replace.append(card)

    df[column] = replace
    print('Произведено обезличивание по банковской карте.')
    return df


def hide_quantity(df, column):
    replace = []
    for quantity in df[column]:
        if int(quantity) <= 19:
            quantity = 'Менее 20 товаров'
        else:
            quantity = 'От 20 до 32 товаров'
        replace.append(quantity)

    df[column] = replace
    print('Произведено обезличивание по количеству покупок.')
    return df


def hide_sum(df, column):
    replace = []
    for summ in df[column]:
        summ = int(summ)
        if summ <= 1500:
            summ = '< 1500'
        elif 1500 < summ <= 4000:
            summ = '1500 - 4000'
        elif 4000 < summ <= 30000:
            summ = '4000 - 30 000'
        elif 30000 < summ <= 250000:
            summ = '30 000 - 250 000'
        elif 250000 < summ <= 1000000:
            summ = '250 000 - 1 000 000'
        elif summ > 1000000:
            summ = '> 1 000 000'
        replace.append(summ)

    df[column] = replace
    print('Произведено обезличивание по сумме покупки.')
    return df


def hide_time(df, column):
    replace = []
    for time in df[column]:
        time = list(map(int, time.split(':')))
        time = time[0] * 3600 + time[1] * 60 + time[2]
        if time < 52200:
            time = 'В первой половине дня'
        else:
            time = 'Во второй половине дня'
        replace.append(time)

    df[column] = replace
    print('Произведено обезличивание по времени покупки.')
    return df


def count_k_anonimity(df, quasis):
    grouped = df.groupby(quasis).size().reset_index(name='k_anonimity')
    df = df.merge(grouped, on=quasis, how = 'left')

    return df


infile = input('Введите название файла с датасетом: ')
print("Квази-идентификаторы: \n"
      "1 - магазин              2 - местоположение       3 - дата покупки       4 - банковская карта\n"
      "5 - количество покупок   6 - сумма покупки        7 - время              8 - все\n")
quasi_ids = input('Введите через пробел коды необходимых идентификаторов: ')

df = read_csv(infile)
starting_len = len(df)
shops = shop_dict_builder()

used_quasis = []
if '8' in quasi_ids:
    quasi_ids += '1234567'
if '1' in quasi_ids:
    df = hide_shop(df, 'shop')
    used_quasis.append('shop')

if '2' in quasi_ids:
    df = hide_place(df, 'place')
    used_quasis.append('place')

if '3' in quasi_ids:
    df = hide_date(df, 'date')
    used_quasis.append('date')

if '4' in quasi_ids:
    df = hide_card(df, 'card')
    used_quasis.append('card')

if '5' in quasi_ids:
    df = hide_quantity(df, 'quantity')
    used_quasis.append('quantity')

if '6' in quasi_ids:
    df = hide_sum(df, 'sum')
    used_quasis.append('sum')

if '7' in quasi_ids:
    df = hide_time(df, 'time')
    used_quasis.append('time')

print(' ')

df = count_k_anonimity(df, used_quasis)

preffered_k = 5
ignore_losses = False
acceptable_losses = len(df) - int(round(len(df) / 20, 0))
'''# noinspection PyRedeclaration
ignore_losses = bool(input('Введите 1, если хотите игнорировать превышение потерь в датасете, 0 - в ином случае: '))
# noinspection PyRedeclaration
preffered_k = int(input('Введите желаемое значение к-анонимности: '))'''

print('Программа готова к применению локального подавления. Приступаем.\n')
for i in range(preffered_k):
    if not ignore_losses and len(df) < acceptable_losses:
        break
    expression = 'k_anonimity > ' + str(i)
    df = df.query(expression)

print('Осталось', len(df) / starting_len * 100, '% строк')

min_k = min(df['k_anonimity'])
percent_mink = (df['k_anonimity'] == min_k).sum() / len(df) * 100
print('К-анонимность обезличенного датасета: ', min_k)
bad_ks = []
print('Худшие варианты k-анонимности:')
for i in range(min_k, len(df)):
    if i in df['k_anonimity']:
        percent_i = (df['k_anonimity'] == i).sum() / len(df) * 100
        print(str(i) + ', ' + str(percent_i)+'%')
        bad_ks.append(i)
    if len(bad_ks) >= 5:
        break

df = df.drop(columns='k_anonimity')
df.to_excel(f'{infile}.xlsx', sheet_name='Depersonalyzed', index=False)