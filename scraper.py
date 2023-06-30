from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

def get_upcoming_superkicks_releases():
    url = "https://www.superkicks.in/collections/releases"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    sk_releases = soup.find_all('div', class_='card-wrapper')
    
    for release in sk_releases:
        media_tag = release.find("div", class_="card__media")
        img_tag = media_tag.img
        image = img_tag.get("srcset")
        image_src = "https:"+image.split("?")[0]

        card_content_tag = release.find("div", class_="card__content")
        name = card_content_tag.find("a", class_="full-unstyled-link").text
        parent_tag = release.find_parent()
        price_tag = parent_tag.find("div",class_="price__regular")
        price = price_tag.text.strip().split('\n')[-1].strip()
        print(price)
    return



def get_upcoming_releases():
    url = "https://www.nike.com/in/launch?s=upcoming"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    releases = soup.find_all('a', class_='card-link')
    upcoming_releases = []

    for release in releases:
        href_tag = release.get('href')
        link = url + href_tag
        img_tag = release.find('img')
        if img_tag is not None:
            img_src = img_tag.get('src')
            main_tag = release.find_parent().find_parent().find_parent()
            release_date = main_tag.find('div', class_='available-date-component').text
            text = href_tag.split("/t/")[1]
            text_2 = text.replace('-', " ")
            name = text_2.title()
            upcoming_releases.append({
                'name': name,
                'link': link,
                'image': img_src,
                'release_date': release_date
            })
    return upcoming_releases

@app.route('/')
def home():
    # Make a request to the VegNonVeg
    r = requests.get("https://www.vegnonveg.com")

    # Use the 'html.parser' to parse the page
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find all links on the page
    links = soup.find_all('a', {'class': 'gt-product-click'})

    # Create a list to store the product information
    products = []
    
    # Print the href attribute of each link
    for link in links:
        href = link.get('href')
        if href and '/products/hyped' in href:  # check if href is not None
            data_product = link.get('data-product')
            if data_product:
                product_info = json.loads(data_product)
                product_name = product_info.get('name')
                product_price = product_info.get('price')
                img_tag = link.find('img')
                img_url = img_tag['src']
                products.append({
                    'name': product_name,
                    'price': product_price,
                    'link': link['href'],
                    'image': img_url
                })

    # Get the upcoming Nike releases
    nike_releases = get_upcoming_releases()
    superkicks_releases = get_upcoming_superkicks_releases()
    
    # Return a rendered template
    return render_template('home.html', products=products, nike_releases=nike_releases)

if __name__ == '__main__':
    app.run(debug=True)
