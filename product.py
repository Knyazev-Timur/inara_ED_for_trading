import requests
# Выводит ID всех товаров в ED
# чтобы не формировать список вручную

url = 'https://inara.cz/elite/commodities-list/'
answer = requests.get(url)
page = answer.text.split()

product = {i.split('/')[3] for i in page if 'href="/elite/commodity/' in i}


print(product)
