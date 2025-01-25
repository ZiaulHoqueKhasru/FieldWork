from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    # publisher_website = Column(String, index=True)
    datetime = Column(DateTime, nullable=False)
    title = Column(String(255), index=True)
    body = Column(Text)
    link = Column(String(255))
    
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    reporter_id = Column(Integer, ForeignKey('reporters.id'), nullable=True)
    publisher_id = Column(Integer, ForeignKey('publishers.id'), nullable=True)

    category = relationship("Category")
    reporter = relationship("Reporter")
    publisher = relationship("Publisher")

    # @property
    # def category_name(self):
    #     return self.category.name if self.category else None

    # @property
    # def reporter_name(self):
    #     return self.reporter.name if self.reporter else None

    # @property
    # def publisher_name(self):
    #     return self.publisher.name if self.publisher else None

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    description = Column(String(255))

class Reporter(Base):
    __tablename__ = "reporters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    email = Column(String(255), unique=True)

class Publisher(Base):
    __tablename__ = "publishers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    website = Column(String(255), nullable=True)

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(Integer, ForeignKey('news.id'))
    url = Column(String(255), nullable=False)

    news = relationship("News")

class Summary(Base):
    __tablename__ = "summaries"
    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(Integer, ForeignKey('news.id'))
    summary_text = Column(Text)

    news = relationship("News")