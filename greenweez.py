from discord_webhook import DiscordWebhook, DiscordEmbed
webhook = DiscordWebhook(
    url='https://discord.com/api/webhooks/885747859687866378/XZJEkus2I98yXl6Xuep0d_ckPeQz1msU9zs9INvomU3c8TAdvI6oiWSkln3SXd0dUK3y', username="Exchange Scraped File")
from bs4 import BeautifulSoup as bs
import pandas as pd   
import requests
import re

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }


def scrape_subcategory_links():
    all_links = pd.read_excel('greenweez_categories1.xlsx')['links'].tolist() # collecting all category links from input excel(greenweez_categories.xlsx)

    data1 = {}
    lists1 = []
    for li in all_links: # going to each category link to collect, links of sub-categories
        print(f'Scraping Sub-category links from, Main Category: {li}')
        r = requests.get(li,headers = headers)
        soup = bs(r.content, 'html.parser')

        links = [m.start() for m in re.finditer('sub_category_block" href="', str(soup))]
        for tab in links:
            link = 'https://www.greenweez.com/' + str(soup)[tab+26:tab+70].split('"')[0] # sub-category link
            category = link.split('/')[-1].split('-')[-1] 
            category = link.split('/')[-1].replace(f'-{category}','') # sub-category name
            data1 = {
                'Main-Category': li,
                'Sub-Category': category,
                'Sub-Category-Link': link
            }
            lists1.append(data1)
    df1 = pd.DataFrame(lists1).drop_duplicates(subset=['Sub-Category-Link']) # removing duplicates from the links(sub-cat)
    link_count = len(df1['Sub-Category-Link'].tolist())
    print(f'Total {link_count} sub-categories found...')
    return df1



lists2 = []
data2 = {}
df = scrape_subcategory_links()
def scrape_links_from_each_subcategory(): # collecting product links from each sub-category
    sub_category_links = df['Sub-Category-Link'].tolist()
    sub_category_name = df['Sub-Category'].tolist()
    main_category = df['Main-Category'].tolist()
    count = 1
    for link,sub_cat_name,main_cat in zip(sub_category_links,sub_category_name,main_category): # looping to each sub-cat...
        print(f'Sub_category {count}: {link}')
        
        try:
            r = requests.get(link,headers = headers)
            soup = bs(r.content,'html.parser')
            num_of_products = int(soup.find('span',attrs = {'id':'page_list_nbr_article'}).text) # finding num-of-products, to determine how many times we will have to loop for pagination

            print(f'Num. of Products: {num_of_products}')
            count = count+1

            loop = num_of_products/102
            if loop is not int:
                loopy = int(loop) + 1 # if there is fraction in (num_of_products/102(product_per_page)), adding one more page(+1)


            for i in range(1,loopy+1):
                print(f'Pagination: {i}')
                link = link + f'?page={i}'
                try:
                    r = requests.get(link,headers = headers) # scraping product links from each page
                    soup = bs(r.content,'html.parser')

                    prod_link = soup.findAll('div',attrs = {'class':'titre d-flex w-100 flex-column text-left position-relative'})
                    for prod in prod_link:
                        pro_link = prod.find('a')['href']
                        data2 = { # getting pandas dataframe ready...
                            'Main Category': main_cat,
                            'Sub-Category': sub_cat_name,
                            'Sub-Category link': link,
                            'Product link': pro_link
                        }
                        lists2.append(data2)
                except:
                    pass
        except:
            pass
    df3 = pd.DataFrame(lists2).drop_duplicates(subset=['Product link']) # removing duplicates from links..
    df3.to_excel('products_links2.xlsx',encoding = 'utf-8-sig',index = False) # saving the data sheet with all links to an excel


if __name__ == '__main__':    
    scrape_links_from_each_subcategory()
 

embed = DiscordEmbed(title='greenweez', description=f'''Urls Yesterday:''')
with open(f'products_links2.xlsx', "rb") as f:
    webhook.add_file(file=f.read(), filename=f'products_links2.xlsx')
webhook.add_embed(embed)
response = webhook.execute()
webhook.remove_embeds()
webhook.remove_files()
    

    