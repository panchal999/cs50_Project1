import csv
import os
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():

	"""Add User Query """
	# dateTimeObj = datetime.now()
	# timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S.%f")
	# db.execute("INSERT INTO users (name,password,email,created_on) VALUES (:name,:password,:email,:created_on)",{"name": 'abc',"password":'123',"email":'abc@gmail.com',"created_on": timestampStr })
	
	"""Add dummy Book Reviews """
	db.execute("INSERT INTO book_review (user_id,book_id,rating,review) VALUES (:user_id,:book_id,:rating,:review)",{"user_id": 1,"book_id":2934 ,"rating": 4,"review": "1-Must Read, Amazing book!!" })
	db.execute("INSERT INTO book_review (user_id,book_id,rating,review) VALUES (:user_id,:book_id,:rating,:review)",{"user_id": 2,"book_id":2934 ,"rating": 5,"review": "2-I love this book, enjoy present moment" })
	db.execute("INSERT INTO book_review (user_id,book_id,rating,review) VALUES (:user_id,:book_id,:rating,:review)",{"user_id": 1,"book_id":4199 ,"rating": 5,"review": "1-BestSeller,Great Explanation!! " })
	db.execute("INSERT INTO book_review (user_id,book_id,rating,review) VALUES (:user_id,:book_id,:rating,:review)",{"user_id": 2,"book_id":4199 ,"rating": 3,"review": "2-Hard English words but great book" })
	db.execute("INSERT INTO book_review (user_id,book_id,rating,review) VALUES (:user_id,:book_id,:rating,:review)",{"user_id": 1,"book_id":4 ,"rating": 4,"review": "Dedicated to future generation, Robots, Also has Movie" })
	
	db.commit()

""" Add csv file data of book to database """
# f = open("/home/parth/Documents/cs50/project1/books.csv")
# reader = csv.reader(f)

# for isbn,title,author,year in reader:
#     db.execute("INSERT INTO books (isbn,title,author,year) VALUES (:isbn,:title,:author,:year)",
#                 {"isbn": isbn, "title": title, "author": author,"year": year})
#     print(f"Added book: {isbn} {title} {author} {year}.")


if __name__ == "__main__":
    main()

