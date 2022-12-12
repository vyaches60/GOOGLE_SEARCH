from serpapi import GoogleSearch
import pandas as pd
import re
import webbrowser
import os
import locale

#export(LC_ALL=C)
locale.setlocale(locale.LC_ALL, 'uk_UA')

api_key = "0ffdacf420dfd292f4842a537fa3349da9d5ad86e252c88eabef66052afbeaa2"
product = "Електрочайник Gorenje K17GWE"
#product = product('utf8')
pattern = '(?i).*'+product.replace(" ", ".*")

def scrap_price_results():
    params = {
      "q": product,
      "location": "Ukraine",
      "tbm":"shop",
      "hl": "en", ##"Google UI Language"
      "gl": "ua", ##"Google Country"
      "api_key": api_key
    }

    search = GoogleSearch(params)

    data = search.get_dict()

    result = []
    for shopping_result in data['shopping_results']:
        Price = shopping_result.get('extracted_price'),
        Title = shopping_result.get('title'),
        Source = shopping_result.get('source'),
        Thumbnail = shopping_result.get('thumbnail'),
        Link = shopping_result.get('link')

        result.append({
            "Price": Price,
            "Position": shopping_result["position"] + 1,
            "Title": Title,
            "Thumbnail": Thumbnail,
            "Source": Source,
            "Link": Link})

    return result
        #result = pd.DataFrame(result)

result = pd.DataFrame(scrap_price_results())

df = pd.DataFrame()

Source = pd.DataFrame(result["Source"].tolist())
Title = pd.DataFrame(result["Title"].tolist())
Price = pd.DataFrame(result["Price"].tolist())
Position = pd.DataFrame(result["Position"].tolist())
Thumbnail = pd.DataFrame(result["Thumbnail"].tolist())
Link = pd.DataFrame(result["Link"].tolist())

df = {
    'Source': Source.values.tolist(),
    'Title': Title.values.tolist()
}

result = pd.DataFrame(Source)
result['Title'] = pd.DataFrame(Title)
result['Price'] = pd.DataFrame(Price)
result['Position'] = pd.DataFrame(Position)
result['Thumbnail'] = pd.DataFrame(Thumbnail)
result['Link'] = pd.DataFrame(Link)
result.rename(columns = {0:'Source'}, inplace = True)
result = pd.DataFrame(result)
result = result.sort_values('Price')
#result['Link'] = result['Link'].encode('utf-8')

#result = result[result['Title'].str.contains(pattern)]

result['Thumbnail']=  '''<img src="''' + result['Thumbnail'] + '''"width="60" height="60">'''
with open('r.html', 'w', encoding='utf-8') as fo:
    fo.write(result.to_html(render_links=True,escape=False))
result['Link'] = result['Link'].apply(lambda x: '<a href="{0}">link</a>'.format(x))
result['Link'] = result['Link'].replace("http://example.com/", ' ')

result.to_html(r"google_search_results.html",escape=False)
#print(result)

def scrap_price_results_to_csv():
    result.to_csv(r"google_search_results.csv", index=False, encoding='utf-8-sig', sep =";")
    print("Результат сохранён.")

#print(scrap_price_results())
scrap_price_results_to_csv()

webbrowser.open('file://' + os.path.realpath(r"google_search_results.html"))
