from sqlalchemy.orm import Session
# from . import models, schemas
from app import models, schemas
def get_news(db: Session, news_id: int):
    return db.query(models.News).filter(models.News.id == news_id).first()

def get_news_list(db: Session, skip: int = 0, limit: int = 10):
    print(db, skip, limit)
    return db.query(models.News).order_by(models.News.datetime.desc()).offset(skip).limit(limit).all()


def get_or_create_category(db: Session, name: str, description: str):
    # print(db, name, description)
    category = db.query(models.Category).filter(models.Category.name == name).first()
    # print("DB Response: ", category)
    if category is None:
        category = models.Category(name=name, description=description)
        db.add(category)
        db.commit()
        db.refresh(category)
    return category

def get_or_create_reporter(db: Session, name: str, email: str):
    reporter = db.query(models.Reporter).filter(models.Reporter.name == name).first()
    if reporter is None:
        reporter = models.Reporter(name=name, email=email)
        db.add(reporter)
        db.commit()
        db.refresh(reporter)
    return reporter

def get_or_create_publisher(db: Session, name: str, website: str, email: str):
    publisher = db.query(models.Publisher).filter(models.Publisher.name == name).first()
    if publisher is None:
        publisher = models.Publisher(name=name, website=website,email=email)
        db.add(publisher)
        db.commit()
        db.refresh(publisher)
    return publisher


def get_news_existance(db: Session, news_title: str):
    return db.query(models.News).filter(models.News.title == news_title).first()


def create_image(db: Session, news_id: int, url: str):
    db_image = models.Image(news_id=news_id, url=url)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def create_news(db: Session, news: schemas.NewsCreate):
    print(f"news catagory:{news.news_category}, news repoorter:{news.news_reporter}, publisher:{news.news_publisher}")
    category = get_or_create_category(db, news.news_category, f"{news.news_category} description")
    reporter = get_or_create_reporter(db, news.news_reporter, f"{news.news_reporter}@example.com")
    publisher = get_or_create_publisher(db, news.news_publisher, f"https://{news.news_publisher}",f"{news.news_publisher}@example.com")
    news_exist = get_news_existance(db, news_title=news.title)

    print(category.name, reporter.name, publisher.name)
    print(category.id, category.name, category.description)
    print(reporter.id, reporter.name, reporter.email)
    print(publisher.id, publisher.name,publisher.email, publisher.website)
    if news_exist:
        return news_exist

    db_news = models.News(
        # publisher_website=news.publisher_website,
        title=news.title,
        datetime=news.datetime,
        body=news.body,
        link = news.link,
        category_id=category.id,
        reporter_id=reporter.id,
        publisher_id=publisher.id
        # category=category,
        # reporter=reporter,
        # publisher=publisher
    )
    print(db_news)
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    print(db_news.title,db_news.id,db_news.datetime,db_news.body,db_news.link,db_news.category_id,db_news.reporter_id,db_news.publisher_id)
    for image_url in news.images:
        create_image(db, news_id=db_news.id, url=image_url)
    print("Images added")
    return db_news


def insert_summary(db: Session, news_id: int, summary_text: str):
    db_summary = models.Summary(news_id=news_id, summary_text=summary_text)
    db.add(db_summary)
    db.commit()
    db.refresh(db_summary)
    return db_summary


def get_summary(db: Session, summary_id: int):
    return db.query(models.Summary).filter(models.Summary.id == summary_id).first()