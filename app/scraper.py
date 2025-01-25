import datetime
from requests_html import HTMLSession
from app.database import SessionLocal
from app.crud import create_news
from app.schemas import NewsCreate, News

def single_news_scraper(url: str):
    session = HTMLSession()
    try:
        response = session.get(url)
        #response.html.render()  # This will download Chromium if not found
        print(f"Scraped news from {url}")

        publisher_website = url.split('/')[2]
        publisher = publisher_website.split('.')[-2]
        print(f"Publisher: {publisher}")
        print(f"Publisher Website: {publisher_website}")    
        title = response.html.find('h1', first=True).text
        print(f"Title: {title}")

        
        category = response.html.find('.widget-title', first=True).text
        print(f"Category: {category}")
     
        
        reporter_element = response.html.find('.author-name', first=True)
        reporter = reporter_element.text if reporter_element else "Reporter not found"
        #print(f"Reporter: {reporter}")
        # reporter_email = reporter_element.attrs.get('.author-name + href')
        # print(f"Reporter Email: {reporter_email}")
        reporter_email = "www.mzhk@gmail.com"
        
        news_datetime = response.html.find('.author-name + .date', first=True).text
        print(f"Date: {news_datetime}")


       
        
        content = '\n'.join([p.text for p in response.html.find('.print-body  .section-content  p')])
        
        #print(f"Content: {content}")
        # img_tags = response.html.find('img')
        # images = [img.attrs['src'] for img in img_tags if 'src' in img.attrs]
        # print(f"Images: {images}")
        
        
        images = []
        image_element = response.html.find('.lg-gallery')
        
        # Extract the image URL from the 'data-src' attribute
        if image_element:
            for image in image_element:
                data_src = image.attrs.get('data-src')
                images.append(data_src)
                #print(f"Image (data-src): {data_src}")
                #data_exthumbimage = image_element.attrs.get('data-exthumbimage')
                #print(f"Image (data-exthumbimage): {data_exthumbimage}")
                #return data_src, data_exthumbimage
        else:
            print("Image element not found")
        
        
        news_datetime = datetime.datetime.now()



        return NewsCreate(
            publisher_website=publisher_website,
            news_publisher=publisher,
            title=title,
            news_reporter=reporter,
            datetime=news_datetime,
            link=url,
            news_category=category,
            body=content,
            images=images,
            #email= reporter_email
        )
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def scrape_and_store_news(url: str, db: SessionLocal):
    print(f"Scraping news from {url}")
    news_data = single_news_scraper(url)
    inserted_news = None  # Initialize inserted_news to None
    if news_data:
        inserted_news = create_news(db=db, news=news_data)
    print("I am here too")
    #db.close()
    return inserted_news

if __name__ == '__main__':
    url =   "https://www.tbsnews.net/worldbiz/usa/trump-declassifies-jfk-rfk-martin-luther-king-jr-assassination-files-1051141"
    single_news_scraper(url)
    scrape_and_store_news(url, db=SessionLocal())