
from flask import Flask, request, flash, render_template, session, url_for, redirect
from requests import Session
from flask import request, render_template, make_response
from datetime import date, datetime, timedelta 
from flask import Flask
from custDB import Customers
from base import Session, Base, engine
from loansDB import Loans
from booksDB import Books
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

def print_date_time():
   print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yasha pass'
Base.metadata.create_all(engine)


session = Session()

#home page
@app.route('/')
def home():
        return render_template('home.html') 

@app.route('/about')
def about():
        return render_template('about.html')         


#customer fuctions
@app.route('/cust')
def show_cust():
   show_cust = session.query(Customers).all()
   return render_template('cust.html', show_cust = show_cust)

@app.route('/add_cust', methods = ['GET', 'POST'])
def add_cust():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['age']:
        flash('Please enter all the fields', 'error')
      else:
        customer = Customers(request.form['name'], request.form['city'],request.form['age'])
         
        session.add(customer)
        session.commit()
         
        flash('customer was successfully added')
        return redirect(url_for('show_cust'))
   return render_template('add_cust.html')

@app.route('/delete_cust', methods = ['GET', 'POST'])
def delete_cust():
   try:
      if request.method == 'POST':
        customer = session.query(Customers).filter(Customers.name==request.form['name']).first()
        session.delete(customer)
        session.commit()  
        return redirect(url_for('show_cust'))
   except:
      flash('there is no such customer')     
   return render_template('delete_cust.html')    

#loan functions

#add loan
@app.route('/add_loan', methods = ['GET', 'POST'])
def add_loan():
   if request.method == 'POST':
      if not request.form['cust_id'] or not request.form['book_id']:
         flash('Please enter all the fields', 'error')
      else:
         loan = Loans(request.form['cust_id'], request.form['book_id'],
         loan_date = date.today())
        
      
         session.add(loan)
         session.commit()
        
         choise = session.query(Books, Loans, Customers).select_from(Books).join(Loans).filter(Loans.loan_id==loan.loan_id).all()

         for book, loan, customer in choise:
            book_type = book.type
            loan.loan_date = date.today()
            if int(book_type) == 1:
               loan.return_date = loan.loan_date + timedelta(days = 10)
            elif int(book_type) == 2:
               loan.return_date = loan.loan_date + timedelta(days = 5)
            elif int(book_type) == 3:
               loan.return_date = loan.loan_date + timedelta(days = 2)
         session.commit() 
         session.close() 
         return redirect (url_for('show_loans'))
   return render_template('add_loan.html')

# show loans
@app.route('/loans')
def show_loans():
   show_loans = session.query(Books, Loans, Customers).select_from(Books).join(Loans).join(Customers).all()

   session.close()
   return render_template('loans.html', show_loans = show_loans)
   
#show late loans
@app.route('/late_loans')
def late_loans():
   late_loans = session.query(Books, Loans, Customers).select_from(Books).join(Loans).join(Customers).filter(Loans.status == 'late loan').all

   session.close()
   return render_template('late_loans.html', late_loans = late_loans)
   

#return loan
@app.route('/return_loan', methods = ['GET', 'POST'])
def return_loan():
   try:
      if request.method == 'POST':
         if not request.form['cust_id'] or not request.form['book_id']:
              flash('Please enter all the fields', 'error')
         else:
            loan = session.query(Loans).filter(Loans.cust_id==request.form['cust_id'],Loans.book_id==request.form['book_id'],Loans.status != 'late loan').first()
            loan.status = 'returned'
            session.commit()
            return redirect(url_for('show_loans'))
         session.close()
   except: 
      flash('such ID is not existing')
      return redirect(url_for('show_loans'))
      
   return render_template('return_loan.html')

#Book functions
@app.route('/books')
def show_books():
    show_books = session.query(Books).all()
    return render_template('books.html', show_books = show_books)

@app.route('/delete_book', methods = ['GET', 'POST'])
def delete_book():
   try:
      if request.method == 'POST':
         book = session.query(Books).filter(Books.name==request.form['name']).first()
         session.delete(book)
         session.commit()  
         return redirect(url_for('show_books'))
         
   except:
      flash('There is no such boook')
      redirect(url_for('delete_book'))
   return render_template('delete_book.html')       

@app.route('/new_book', methods = ['GET', 'POST'])
def new_book():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['author'] or not request.form['year_published'] or not request.form['type']:
         flash('Please enter all the fields', 'error')
      else:
         book = Books(request.form['name'], request.form['author'],request.form['year_published'], request.form['type'])
         
         session.add(book)
         session.commit()
         
         flash('new book was successfully added')
         return redirect(url_for('show_books'))
   return render_template('new_book.html')

# search function
@app.route('/search_book', methods = ['GET', 'POST'])
def search_book():
   try:
      if request.method == 'POST':
         if not request.form['name']:
            flash('enter book name to search')
         else:
            search_book = session.query(Books).filter(Books.name==request.form['name']).all()
            session.close()
            return render_template('search_book.html', search_book=search_book)  
   except:
      flash('there is no such book')     
      redirect(url_for('search_book'))    
   return render_template('search_book.html') 


@app.route('/search_customer', methods = ['GET', 'POST'])
def search_customer():
   
      if request.method == 'POST':
         if not request.form['name']:
            flash('enter customer name to search')
         else:
            search_customer = session.query(Customers).filter(Customers.name==request.form['name']).all()
            session.close()
            if search_customer==[]:
               flash('no such customer')
            return render_template('search_customer.html', search_customer=search_customer)   
      return render_template('search_customer.html')      
      

   
       

if __name__ == '__main__':
         

   # Create the background scheduler
   scheduler = BackgroundScheduler()
   # Create the job
   scheduler.add_job(func=print_date_time, trigger="interval", seconds=3)
   # Start the scheduler
   scheduler.start()

   # /!\ IMPORTANT /!\ : Shut down the scheduler when exiting the app
   atexit.register(lambda: scheduler.shutdown())
   app.run(debug=True)


