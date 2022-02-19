from discord_webhook import DiscordWebhook, DiscordEmbed
webhook = DiscordWebhook(
    url='https://discord.com/api/webhooks/885747859687866378/XZJEkus2I98yXl6Xuep0d_ckPeQz1msU9zs9INvomU3c8TAdvI6oiWSkln3SXd0dUK3y', username="Exchange Scraped File")
from bs4 import BeautifulSoup as bs
import pandas as pd   
import requests
import datetime
import re

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }


def get_data(url, df):
    print(url)
    try:
        try:
            page = bs(requests.get(url).text, 'lxml')   
            data = {
                'Product Number': url.split('-')[-1],
                'Product Link': url,
                'Availability': page.find('div', {'class': 'text-left font-size-9 text-md-center'}).text if page.find('div', {'class': 'text-left font-size-9 text-md-center'}) else '',
                'Brand': page.find('div', {'class': 'ProductTitle d-flex justify-content-between flex-row'}).find('a').text.strip(),
                'Name': page.find('div', {'class': 'ProductTitle d-flex justify-content-between flex-row'}).find('h1').text.strip(),
                'Price': f"{page.find('meta', {'itemprop': 'price'}).get('content')} {page.find('meta', {'itemprop': 'priceCurrency'}).get('content')}",
                'Image': page.find('img', {'id': 'products_images'}).get('src'),
                'Description': page.find('div', {'id': 'p_description'}).text.strip(),
                'Review': page.find('div', {'itemprop': 'aggregateRating'}).find('meta', {'itemprop': 'ratingValue'}).get('content') if page.find('div', {'itemprop': 'aggregateRating'}) else '0',
                'Timestamp': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            }

            for cat in page.find_all('li', {'class': 'breadcrumb-item'})[1:]:
                data[f"Category {cat.find('meta').get('content')}"] = cat.text.strip()

            for x in range(len(page.find_all('a', {'class': 'thumb'}))):
                data[f"Image {x+1}"] = page.find_all('a', {'class': 'thumb'})[x].get('data-img-big')

            data['Net Weight'] = re.findall('\d+.*g', url)[0] if re.findall('\d+.*g', url) else ''

            df.loc[len(df)] = data
            print(df.loc[len(df)-1])
        except:
            data = {
                'Product Number': url.split('-')[-1],
                'Product Link': url,
                'Availability': '-',
                'Brand': '-',
                'Name': '-',
                'Price': '-',
                'Image': '-',
                'Description': '-',
                'Review': '-',
                'Timestamp': '-'
            }
            for cat in page.find_all('li', {'class': 'breadcrumb-item'})[1:]:
                data[f"Category {cat.find('meta').get('content')}"] = cat.text.strip()

            for x in range(len(page.find_all('a', {'class': 'thumb'}))):
                data[f"Image {x+1}"] = page.find_all('a', {'class': 'thumb'})[x].get('data-img-big')

            data['Net Weight'] = re.findall('\d+.*g', url)[0] if re.findall('\d+.*g', url) else ''

            df.loc[len(df)] = data
            print(df.loc[len(df)-1])
    except:
        print(f'Something Went Wrong.. in this link:{url}')
        pass
    



def main():
    sitemap = 'https://static.greenweez.com/assets/uploaded/store-1/any-language/sitemap-products.xml'
    df = pd.DataFrame(columns=[
        'Product Number',
        'Product Link',
        'Availability',
        'Category 1',
        'Category 2',
        'Category 3',
        'Category 4',
        'Brand',
        'Name',
        'Price',
        'Image 1',
        'Image 2',
        'Image 3',
        'Description',
        'Net Weight',
        'Review',
        'Timestamp'
    ])

    # urls = ['https:'+x.split(':')[-1].strip() for x in open('Product_links.txt', 'r', encoding='utf-8').read().strip().split('\n')[1::2]]
    urls = pd.read_excel('products_links.xlsx')['Product link'].tolist()
    for url in urls:
        get_data(url, df)
        df = df.fillna('')

        df.to_excel('greenweez_full_scrape.xlsx', index=None, encoding='utf-32')


if __name__ == '__main__':
    main()

 

embed = DiscordEmbed(title='greenweez_full', description=f'''Scraping Done!''')
with open(f'greenweez_full_scrape.xlsx', "rb") as f:
    webhook.add_file(file=f.read(), filename=f'greenweez_full_scrape.xlsx')
webhook.add_embed(embed)
response = webhook.execute()
webhook.remove_embeds()
webhook.remove_files()
    

    