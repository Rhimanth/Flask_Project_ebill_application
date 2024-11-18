
import sqlite3
con=sqlite3.connect('CaseStudy.db')
cur=con.cursor()
"""query='create table Customer (consumerid integer primary key,billno integer unique,title text ,customername text ,mobilenumber integer,emailid text ,username text  unique,password text,customerid integer)'
cur.execute(query)"""

query='create table Complaint(complaintid integer primary key,type text,category text,contactperson text,mobile_number integer,landmark text ,consumer_no integer ,problem text,address text,status text defalut "Pending",foreign key(consumer_no) references Customer(consumerid) on delete CASCADE)'
cur.execute(query)

"""cur.execute('create table admin(username text ,password text)')
cur.execute('insert into admin values("Admin_123","Admin_TCS@python1")')

cur.execute('create table bill (consumerid integer ,billno integer primary key,month text,dueamount real,payableamount real,status text,foreign key(consumerid) references Customer(consumerid) on delete CASCADE)')
cur.execute('drop table complaint')
cur.execute('create table receipt (transactionno text unique,receiptno integer primary key,tdate date,ttype text,ptype text,pgateway text,cname text,billno integer,tamt text,status text,consumeid integer)')"""

print("table created ")
con.commit()


con.close()

