import os
from datetime import datetime
import requests
from flask import Flask, request, jsonify,render_template, session, redirect, url_for,g
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))




@app.before_request
def before_request():
	g.user=None
	if 'user_id' in session:
		user=db.execute("SELECT * FROM users WHERE user_id = :user_id", {"user_id": session['user_id']}).fetchone()
		g.user=user	


@app.route("/")
def index():
	return render_template("index.html",is_login=True)






@app.route("/login", methods=["POST","GET"])
def login():
	session.pop('user_id',None)
	login_msg=None
	if request.method == 'POST':
		emailid=request.form['emailid']
		password=request.form["password"]

		user = db.execute("SELECT * FROM users WHERE email = :email AND password= :password ", {"email": emailid, "password":password})
		
		if user.rowcount == 0:
			login_msg="Invalid Credential. Please Try again."
			return render_template("index.html",is_login=True,login_msg=login_msg)
		login_user=user.fetchone()
		session['user_id']=login_user.user_id
		return redirect(url_for('profile'))
		
	return render_template("index.html",is_login=True)


@app.route('/profile')
def profile():
	if not g.user:
		return redirect(url_for('index'))
	return redirect(url_for('books'))


@app.route('/signup',methods=["POST","GET"])
def signup():
	login_msg=None
	if request.method == 'POST':
		name=request.form['name']
		emailid=request.form['emailid']
		password=request.form["password"]
		confirm_password=request.form['confirm_password']

		if name=='' or emailid=="" or password=="":
			return render_template("index.html",login_msg="field should not be empty")

		if confirm_password!=password:
			return render_template("index.html",login_msg="Confirm password not match")

		dateTimeObj = datetime.now()
		timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S.%f")

		db.execute("INSERT INTO users (name,password,email,created_on) VALUES (:name,:password,:email,:created_on)",{"name": name,"password":password ,"email": emailid,"created_on": timestampStr })
		db.commit()
	
		return render_template("index.html",is_login=True,login_msg="Succesfully Registered, Login Here")	


	return render_template("index.html",is_login=False)	



@app.route('/signout')
def signout():
    session.pop('user_id')
    return render_template("index.html",is_login=True,login_msg="Succesfully Logged Out")


	
@app.route('/books',methods=["GET","POST"])
def books():
	if request.method=="GET":

		search=request.args.get('search')
		
		if not search:
			books=db.execute("SELECT * FROM books LIMIT 10").fetchall()
			return render_template("profile.html",books=books)
		else:
			query = "%" + search.strip() + "%"
			query = query.title()

			rows = db.execute("SELECT * FROM books WHERE isbn LIKE :query OR title LIKE :query OR author LIKE :query LIMIT 15", {"query": query})

			if rows.rowcount ==0:
				return render_template("profile.html",search_msg=True)


			books=rows.fetchall()
			return render_template("profile.html",search_msg=False,books=books)

	return render_template("profile.html")	

@app.route("/book/<int:book_id>",methods=["POST","GET"])
def book(book_id):
	goodreads_info=None
	book = db.execute("SELECT * FROM books WHERE book_id = :book_id", {"book_id": book_id}).fetchone()
	
	api_response = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "9GUF2T1jJgHkJKcFYsnkg", "isbns": book.isbn})
	data = api_response.json()
	
	if api_response.status_code != 200:
		goodreads_info=None
	else:
		goodreads_info = data['books'][0]


	reviews=db.execute("SELECT * FROM book_review NATURAL JOIN users WHERE book_id=:book_id",{"book_id":book_id}).fetchall()	
	review_user = [x for x in reviews if x.user_id == session['user_id']]

	if request.method == "POST":
		if request.form['action'] == 'submit_review':
			selected_rating= request.form['rating']
			if selected_rating=="choose":
				return render_template('book.html',reviews=reviews ,error_msg="Rating should not be empty!",book=book,goodreads_info=goodreads_info)
			else:
				review_text=request.form['review_text']
				if review_text==None:
					review_text=""
				db.execute("INSERT INTO book_review (user_id,book_id,rating,review) VALUES (:user_id,:book_id,:rating,:review)",{"user_id": session['user_id'],"book_id":book_id ,"rating":selected_rating ,"review":review_text  })
				db.commit()
				return redirect(url_for('book',book_id=book.book_id))
	
	if review_user==[]:
		return render_template("book.html",book=book,reviews=reviews,disable="",goodreads_info=goodreads_info)


			
	return render_template("book.html",book=book,reviews=reviews,disable="disabled",sucess_msg="Your Review is Submited!!",goodreads_info=goodreads_info)


@app.route("/api/<isbn>")
def book_api(isbn):
	book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
	

	if book is None:
		return jsonify({"Error":"Invalid book search"})

	score=db.execute("SELECT count(*), avg(rating) FROM book_review WHERE book_id = :book_id",{"book_id":book.book_id}).fetchone()

	return jsonify({
			"title": book.title,
		    "author": book.author,
		    "year": str(book.year),
		    "isbn": book.isbn,
		    "review_count": str(score.count),
		    "average_score": str(score.avg)
		})	


	

