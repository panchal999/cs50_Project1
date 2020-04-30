CREATE TABLE users (
	user_id serial PRIMARY KEY,
	name VARCHAR (50) NOT NULL ,
	password VARCHAR (50) NOT NULL,
	email VARCHAR (355) UNIQUE NOT NULL,
	created_on TIMESTAMP NOT NULL,
	last_login TIMESTAMP
) ;

CREATE TABLE book_review (
	user_id integer NOT NULL,
	book_id integer NOT NULL,
	rating integer CHECK( rating>=1 AND rating <=5) NOT NULL,
	review text ,
	PRIMARY KEY (user_id, book_id),
	CONSTRAINT user_book_review_fkey FOREIGN KEY (user_id)
      REFERENCES users(user_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT books_book_review_fkey FOREIGN KEY (book_id)
      REFERENCES books(book_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
	
) ;

ALTER TABLE books
ADD CONSTRAINT book_unique UNIQUE (book_id);