import requests

# полный кортеж id товаров ED
products_id = (
    '10211', '146', '51', '148', '10437', '101', '9', '84', '53', '10243', '10257', '150', '10254', '80', '159', '83',
    '10249', '174', '56', '184', '75', '134', '10268', '10160', '20', '10209', '32', '10210', '10212', '47', '22', '65',
    '19', '157', '52', '164', '110', '10239', '169', '43', '10263', '10156', '142', '88', '27', '105', '39', '59',
    '129',
    '153', '17', '10237', '10269', '10', '122', '57', '97', '170', '10208', '50', '154', '183', '87', '10166', '6',
    '72',
    '10259', '149', '161', '138', '10221', '10220', '186', '133', '54', '15', '98', '10240', '10154', '168', '99', '76',
    '67', '137', '139', '28', '116', '10238', '10255', '10226', '10236', '55', '66', '3', '40', '45', '79', '177', '12',
    '100', '117', '81', '10258', '10157', '37', '44', '178', '69', '62', '143', '77', '103', '124', '10162', '171',
    '10245',
    '63', '151', '145', '23', '91', '173', '11', '68', '10435', '10253', '111', '156', '125', '172', '42', '175', '158',
    '10159', '74', '86', '49', '48', '21', '135', '179', '155', '102', '33', '10155', '120', '10246', '29', '10270',
    '10215', '126', '14', '104', '5', '4', '10260', '152', '181', '121', '127', '90', '118', '10235', '119', '41',
    '10158',
    '96', '166', '38', '10234', '130', '141', '31', '16', '10167', '85', '46', '10153', '10161', '35', '10264', '162',
    '78',
    '160', '61', '180', '10165', '18', '109', '140', '147', '107', '95', '36', '10250', '108', '58', '7', '89', '123',
    '182', '82', '10219', '73', '13', '10252', '10261', '144', '167', '112', '8', '34', '10207', '70', '10247', '132',
    '10164', '10262', '131', '10244', '1', '26', '10251', '10163', '10248', '60', '163', '185', '106', '10256', '71',
    '176',
    '165')

# избранные товары
# products_id = ('42', '71', '46', '10268')


black_list_id = ('45', )  # кортеж исключений


def get_price(action, product_id, sort_revers):
    """
    :param action: 1 -sell, 2 - buy
    :param product_id: id торвара
    :param sort_revers: сортировка списка
    :return: dict
    Возвращает словарь id_Наименование товара : список цен по всем системам
    """
    url = f'https://inara.cz/elite/commodities/?pi1={action}&pi2={product_id}&ps1=Derrim&pi10=2&pi11=0&pi3=3&pi9=0' \
          f'&pi4=1&pi5=8&pi12=0&pi7=0&pi8=1 '
    # Параметры url:    pi1 - покупка/продажа
    #                   pi2 - id товара
    #                   pi3 - размер платформы 1 - small, 2-middle, 3-large
    #                   ps1 - система, относительно которой происходит поиск
    #                   pi5 - время в часах, когда обновлялись данные (мин.8)
    #                   pi8 - носители (1/0)
    answer = requests.get(url)
    page = answer.text.split()
    price = [int(page[i - 2].split('"')[-2]) for i in range(len(page)) if page[i] == 'class="minor">Cr</span></td><td']
    price.sort(reverse=sort_revers)

    return {f"{product_id}_{get_name_product(page, product_id).split('<')[0]}": price}


def get_name_product(page, product_id):
    """
    :param page:  str
    :param product_id: str
    :return: str

    Получает данные с url находит id продукта и возвращает его название
    """
    product = f'value="{product_id}"'
    for i in range(len(page)):
        if page[i] == product:
            return page[i + 2].strip('>')


def dict_price():
    """
    :return: dict
    Формирует словарь по всем продуктам ED
    *рекомендуется применять для списка отобранных товаров
    """
    price_products = {}
    print('\nПрогресс', end='')
    for product_id in products_id:
        price = {}
        price_action = []

        if product_id not in black_list_id:
            product_buy = get_price(1, product_id, False)  # цены продажи
            product_sell = get_price(2, product_id, True)  # цена покупки
        else:
            continue

        product_name = list(product_buy.keys())[0]
        price['buy'] = list(product_buy.values())[0]  # добавляет в словарь значения цен при покупке
        price['sell'] = list(product_sell.values())[0]  # добавляет в словарь значения цен при продаже
        price_action.append(price)  # создает список с ценой покупки и продажи
        price_products[
            product_name] = price_action  # Формирует словарь ключ: id товара _ Название Товара, значение: список цен
        print('.', end='')
    return price_products


def output_sell_buy():
    """Выводит данные по всем товарам
    id_Название товара
    Покупка: список ключ 'buy' по всем системам
    Продажа: список ключ 'sell' по всем системам"""
    prices = dict_price()
    for i in prices.keys():
        print(f'\n{i}\nПокупка: {(prices.get(i)[0]).get("buy")}\nПродажа:{(prices.get(i)[0]).get("sell")}')


def get_all_price():
    """
    возвращает словарь с разницей sell и buy
    *рекомендуется для отбора наиболее интересных товаров по разнице цен
    """
    sell_buy = {}
    print('\nПрогресс', end='')
    for product_id in products_id:

        if product_id not in black_list_id:
            product_buy = get_price(1, product_id, False)  # цены продажи
            product_sell = get_price(2, product_id, True)  # цена покупки
        else:
            continue

        product_name = list(product_buy.keys())[0]
        price_sell = list(product_sell.values())[0]
        price_buy = list(product_buy.values())[0]

        # Список цен по каждому товару
        # print(f'\nтовар: {product_name}\n'
        #       f'Покупка: {price_buy}\n'
        #       f'Продажа: {price_sell}')

        if price_sell == [] or price_buy == []:
            continue
        else:
            sell_buy[product_name] = price_sell[0] - price_buy[0]

        print('.', end='')

    return sell_buy


def get_max(sell_buy):
    """
    :param sell_buy: dict
    :return: dict
    получает список словарей с разницей цен, возвращает
    возвращает словарь, id_наименование товара : наибольший профит,
    """
    max_sell_buy = max(sell_buy.values())
    max_item = list(sell_buy.values()).index(max_sell_buy)
    max_name = (list(sell_buy.keys())[max_item])
    return {max_name: max_sell_buy}


def output_proffit():
    """
    Выводит построчно id_Название товара разницу sell bay (профит)
    """
    sell_buy = get_all_price()
    max_proffit = get_max(sell_buy)

    print()
    for k, v in sell_buy.items():
        print(k, v)
    print(f'\nМакимум:\n{max_proffit}')


# output_sell_buy()
# выведет список цен по всем системам (id, buy, sell)


output_proffit()
# выводит только профит