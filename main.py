from flask import *
import sqlite3
import random
from datetime import datetime 
app=Flask(__name__)
app.secret_key="python"
global n
n=""

@app.route('/')
def login():
    
    return render_template("login.html")
@app.route('/registration')
def registration():                     
    return render_template("registration.html") 
  
 
  
#configure the Message class object and send the mail from a URL  
@app.route('/mail')  
def index():  
    msg = Message('Registration Successful ', sender = 'ebillpaymentapplication@gmail.com', recipients=['saivarshithreddy.b@gmail.com'])  
    msg.body = 'hi, this is the mail sent by using the flask web application'  
    return "Mail Sent, Please check the mail id"  

@app.route('/acknowledgment' ,methods=['POST','GET'])
def acknowledgment():
    if request.method=='POST':
        consumerid=request.form['consumer_id']  
        billno=request.form['bill_no']
        title=request.form['title']
        customername=request.form['name']
        mobilenumber=request.form['mobile_no']
        emailid=request.form['emailid']
        username=request.form['username']
        password=request.form['password']
        try:
            con=sqlite3.connect('CaseStudy.db')
            cur=con.cursor()
            cuid=cur.execute('select consumerid from Customer where consumerid=?',(request.form.get('consumer_id'),))
            p=cuid.fetchone()
            bno=cur.execute('select billno from Customer where billno=?',(request.form.get('bill_no'),))
            q=bno.fetchone()
            uname=cur.execute('select username from Customer where username=?',(request.form.get('username'),))
            r=bno.fetchone()
            cid=cur.execute('select consumerid from bill where consumerid=?',(request.form.get('consumer_id'),))
            s=cuid.fetchone()
            if p:
                return render_template('registration.html',consumerid_exists=True)
            elif q:
                return render_template('registration.html',billno_exists=True)
            elif r:
                return render_template('registration.html',username_exists=True)
            elif s:
                customerid=random.randint(10000,99999)
                cur.execute("insert into Customer values (?,?,?,?,?,?,?,?,?)",(consumerid,billno,title,customername,mobilenumber,emailid,username,password,customerid))
                con.commit()
                return render_template("acknowledgment.html",cid=customerid,name=customername,mno=mobilenumber)
        except Exception as e:
                con.rollback()
                return str(e)
        finally:
            con.close()
    """return render_template("acknowledgment.html")"""

@app.route('/home',methods=['POST','GET'])
def home():
    if request.method=='POST':
        try:
            con=sqlite3.connect('CaseStudy.db')
            cur=con.cursor()
            cuid=cur.execute('select username,password,customername,consumerid,customerid from Customer where username=? and password=?',(request.form.get('username'),request.form.get('password')))
            p=cuid.fetchone()

            
            if p:
                n=p[2]
                session['n']=n
                cid=p[3]
                session['cid']=cid
                cust_id=p[4]
                session['custid']=cust_id
                return render_template("home.html",name=session['n'])
                
            else:
                return render_template("login.html",failed=True)
        except Exception as e:
                con.rollback()
                return str(e)
        finally:
            con.close()
    else:
        return render_template("home.html",name=session['n'])
    

@app.route('/payment')
def viewbills():
    con=sqlite3.connect('CaseStudy.db')
    cur=con.cursor()
    tablequery='select billno,dueamount,payableamount from bill   where consumerid=? and status="Unpaid"'
    a=cur.execute(tablequery,(session['cid'],))
    b=a.fetchall()
    l=[]
    for i in b:
        l.append(i[0])
    session['bills']=l
    return render_template("view_pay_bill.html",b=b,name=session['n'])

@app.route('/payment/bill',methods=['POST','GET'])
def bill():
    if request.method=='POST':
        try:
            amount=request.form['total']
            if amount is not None :
                customerid=session['custid']
                session['amount']=amount
                tamount=str(int(session['amount'])+50)
                bills=request.form['bills']
                session['sbills']=bills
                return render_template("payment.html",amount=amount,bills=bills,custid=customerid,tamount=tamount,name=session['n'])
            else:
                return render_template("view_pay_bill.html")
        except:
             return redirect(url_for('viewbills'))
        

@app.route('/payment/bill/paymentgateway/cards',methods=['POST','GET'])
def cards():
    session['type']="Cards"
    amount=session['amount']
    return render_template("cards.html",amount=amount,name=session['n'])
@app.route('/payment/bill/paymentgateway/upi',methods=['POST','GET'])
def upi():
    session['type']="UPI Payment"
    amount=session['amount']
    return render_template("upi.html",amount=amount,name=session['n'])
@app.route('/payment/bill/paymentgateway/qr_code',methods=['POST','GET'])
def qr():
    session['type']="QR Payment"
    amount=session['amount']
    return render_template("qr.html",amount=amount,name=session['n'])
@app.route('/payment/bill/paymentgateway/paymentsuccess',methods=['POST','GET'])
def PaymentSuccess():
    con=sqlite3.connect('CaseStudy.db')
    cur=con.cursor()
    bills=session['sbills'].split(',')
    l=[]
    for i in bills:
        l.append(int(i))
    for i in l:
        query='update bill set payableamount=0 ,status="Paid" where billno=?'
        cur.execute(query,(i,))
        con.commit()
    transactionno=random.randint(10000000000,99999999999)
    receiptno=random.randint(10000,99999)
    tdate=datetime.now().date()
    ttype=session['type']
    ptype="Registered User"
    pgateway="Online Payment"
    cname=session['n']
    tamt=session['amount']
    status="Successfull"
    bills=session['sbills']
    cur.execute('insert into receipt values(?,?,?,?,?,?,?,?,?,?,?)',(transactionno,receiptno,tdate,ttype,ptype,pgateway,cname,bills,tamt,status,session['cid']))
    con.commit()
    con.close()
    return render_template("paymentsuccess.html",name=cname,transactionno=transactionno,receiptno=receiptno,tdate=tdate,ttype=ttype,ptype=ptype,bills=bills,pgateway=pgateway,cname=cname,tamt=tamt,status=status)

@app.route('/receipt')
def receipt():
    con=sqlite3.connect('CaseStudy.db')
    cur=con.cursor()
    query='select * from receipt'
    a=cur.execute(query)
    b=a.fetchone()
    return render_template("receipt.html",b=b)

@app.route('/complaint')
def complaint():
    cid=session['cid']
    return render_template("raise_compient.html",name=session['n'],cid=cid)
@app.route('/complaintcheck',methods=['POST','GET'])
def complaintcheck():
    if request.method=='POST':
        try:
            con=sqlite3.connect('CaseStudy.db')
            cur=con.cursor()
            type=request.form['type']
            category=request.form['category']  
            contactperson=request.form['contactperson']
            mobile_number=request.form['mobile_number'] 
            landmark=request.form['landmark']
            consumer_no=request.form['consumer_no']
            problem=request.form['problem']
            address=request.form['address']
            complaintid=random.randint(10000,99999)
            status="pending"
            data=(complaintid,type,category,contactperson,mobile_number,landmark,consumer_no,problem,address,status)
            cur.execute('insert into Complaint values(?,?,?,?,?,?,?,?,?,?)',data)
            con.commit()
            return render_template("raise_compient.html",complaint=complaintid,success=True,name=session['n'])
        except :
             render_template('raise_compient.html',error=True,name=session['n'])
       
        finally:
            con.close()

@app.route('/complaintstatus')
def ComplaintStatus():
    return render_template("s_complient.html",name=session['n'])

@app.route('/complaintstatus',methods=['POST','GET'])
def ComplaintStatuscheck():
    if request.method=='POST':
        try:
            con=sqlite3.connect('CaseStudy.db')
            cur=con.cursor()
            compid=request.form['complient_no']
            a=cur.execute('select status from complaint where complaintid=?',(compid,))
            result=a.fetchone()
            con.commit()
            if result:
                return render_template("s_complient.html",success=True,r=result[0],name=session['n'])
            else:
                return render_template("s_complient.html",nsuccess=True,name=session['n'])
        except :
             render_template('s_complient.html',error=True,name=session['n'])
       
        finally:
            con.close()

@app.route('/adminLogin')
def adminlogin():
    return render_template("adminlogin.html")

@app.route('/admin/home',methods=['POST','GET'])
def adminhome():
    if request.method=='POST':
        try:
            con=sqlite3.connect('CaseStudy.db')
            cur=con.cursor()
            cuid=cur.execute('select username,password from admin where username=? and password=?',(request.form.get('username'),request.form.get('password')))
            p=cuid.fetchone()
            if p:
                return render_template("admin.html")
                
            else:
                return render_template("adminlogin.html",failed=True)
        except Exception as e:
                con.rollback()
                return str(e)
        finally:
            con.close()
    else:
        return render_template("home.html",name=session['n'])
    return render_template("admin.html")
@app.route('/admin/homeh')
def adh():
    return render_template("header.html")
@app.route('/admin/homeb')
def adb():
    return render_template("bottom.html")
@app.route('/admin/homem')
def adm():
    return render_template("meanu.html")
@app.route('/admin/homet')
def adt():
    con=sqlite3.connect('CaseStudy.db')
    cur=con.cursor()
    cust=cur.execute('select count(password) from customer')
    customers=cust.fetchone()
    comp=cur.execute('select count(complaintid) from Complaint where status="pending"')
    complaints=comp.fetchone()
    bills=cur.execute('select count(consumerid) from bill where status="Unpaid"')
    b=comp.fetchone()
    return render_template("task.html",c=customers[0],comp=complaints[0],bill=b[0])
@app.route('/admin/addCustomer')
def addcustomer():
    con=sqlite3.connect('CaseStudy.db')
    cur=con.cursor()
    cust=cur.execute('select b.consumerid,c.customername,c.mobilenumber,c.emailid ,group_concat(b.billno )as all_bills,group_concat(distinct co.complaintid)as all_complaints from customer as c left join bill as b on c.consumerid=b.consumerid and b.status="Unpaid" left join complaint as co on c.consumerid=co.consumer_no and co.status in ("pending" ,"Inprogess")')
    customer=cust.fetchall()
    return render_template("addcustomer.html",customer=customer,customers=True)
@app.route('/admin/updateDetails')
def updatedetails():
    return render_template("updatedetails.html")
@app.route('/admin/updateDetails',methods=['POST','GET'])
def dupdatedetailscheck():
    if request.method=='POST':
        try:
            con=sqlite3.connect('CaseStudy.db')
            cur=con.cursor()
            consumerid=request.form['consumer_id']
            email=request.form['email']
            r=cur.execute('select consumerid from customer where consumerid=?',(consumerid,))
            if r.fetchone():
                cur.execute('update customer set emailid=? where consumerid=? ',(email,consumerid,))
            
                con.commit()
                return render_template("updatedetails.html",success=True,error=False,customer=False)
            else:
                return render_template("updatedetails.html",success=False,error=False,customer=True,b=consumerid)
        except Exception as e :
             return render_template('updatedetails.html',error=True,success=False,customer=False,reason=str(e))
       
        finally:
            con.close()
@app.route('/admin/deleteCustomer')
def deletecustomers():
    return render_template("deletecustomers.html")
@app.route('/admin/deleteCustomerc',methods=['POST','GET'])
def deletecustomerscheck():
    if request.method=='POST':
        try:
            con=sqlite3.connect('CaseStudy.db')
            cur=con.cursor()
            consumerid=request.form['consumer_id']
            r=cur.execute('select consumerid from customer where consumerid=?',(consumerid,))
            if r.fetchone():
                cur.execute('delete from customer where consumerid=? ',(consumerid,))
                cur.execute('delete from bill where consumerid=? ',(consumerid,))
                cur.execute('delete from complaint where consumer_no=? ',(consumerid,))
                cur.execute('delete from receipt where consumeid=? ',(consumerid,))
                con.commit()
                return render_template("deletecustomers.html",success=True,error=False,cutomer=False)
            else:
                return render_template("deletecustomers.html",success=False,error=False,customer=True,b=consumerid)
        except Exception as e :
             return render_template('deletecustomers.html',error=True,success=False,reason=str(e),cutomer=False)
       
        finally:
            con.close()
@app.route('/admin/addbill')
def addbill():
    billno=random.randint(10000,99999)
    return render_template("addbill.html",bill=billno)
@app.route('/admin/addbilll',methods=['POST','GET'])
def addbillcheck():
    if request.method=='POST':
        try:
            con=sqlite3.connect('CaseStudy.db')
            cur=con.cursor()
            consumerid=request.form['consumer_id']
            payableamount=request.form['payableamount']
            dueamount=request.form['dueamount']
            month=request.form['month']
            billno=request.form['billno']
            status=request.form['status']
            billn=random.randint(10000,99999)
            data=(consumerid,billno,month,dueamount,payableamount,status)
            cur.execute('insert into bill values(?,?,?,?,?,?)',data)
            con.commit()
            return render_template("addbill.html",success=True,error=False,bill=billn)
        except Exception as e :
             render_template('addbill.html',error=True,success=False,reason=str(e))
       
        finally:
            con.close()
@app.route('/admin/updatebill')
def updatebill():
    return render_template("updatebill.html")
@app.route('/admin/updatebill',methods=['POST','GET'])
def billupdatecheck():
    if request.method=='POST':
        try:
            con=sqlite3.connect('CaseStudy.db')
            cur=con.cursor()
            consumerid=request.form['consumer_id']
            bill_amount=request.form['bill_amount']
            month=request.form['month']
            status=request.form['status']
            r=cur.execute('select consumerid from bill where consumerid=?',(consumerid,))
            if r.fetchone():
                cur.execute('update bill set payableamount=? , status=? where consumerid=? and month=?',(bill_amount,status,consumerid,month))
                con.commit()
                return render_template("updatebill.html",success=True,error=False,customer=False)
            else:
                return render_template("updatebill.html",success=False,error=False,customer=True,b=consumerid)
        except Exception as e :
             return render_template('updatebill.html',error=True,success=False,customer=True,reason=str(e))
       
        finally:
            con.close()
@app.route('/admin/deletebill')
def deletebill():
    return render_template("deletbill.html")
@app.route('/admin/deletebilll',methods=['POST','GET'])
def deletebillcheck():
    if request.method=='POST':
        try:
            con=sqlite3.connect('CaseStudy.db')
            cur=con.cursor()
            consumerid=request.form['consumer_id']
            month=request.form['month']
            r=cur.execute('select consumerid from bill where consumerid=?',(consumerid,))
            if r.fetchone():
                cur.execute('delete from bill where consumerid=? and month=?',(consumerid,month))
                con.commit()
                return render_template("deletbill.html",success=True,error=False,customer=False)
            else:
                return render_template("deletbill.html",success=False,error=False,customer=True,b=consumerid)
        except Exception as e :
             return render_template('deletbill.html',error=True,success=False,reason=str(e),customer=Fals)
       
        finally:
            con.close()
@app.route('/admin/unpaidbill')
def unpaidbill():
    return render_template("unpaidbills.html")
@app.route('/admin/unpaidbills',methods=['POST','GET'])
def unpaidbillcheck():
    if request.method=='POST':
        try:
            con=sqlite3.connect('CaseStudy.db')
            cur=con.cursor()
            consumerid=request.form['consumer_id']
            r=cur.execute('select consumerid from bill where consumerid=?',(consumerid,))
            if r.fetchone():
                cur.execute('select * from bill where consumerid=? and status="Unpaid"',(consumerid,))
                a=cur.fetchall()
                b=len(a)
                if a:
                    con.commit()
                    return render_template("unpaidbills.html",success=True,error=False,result=a,length=b,customer=False)
                else:
                    return render_template("unpaidbills.html",success=False,error=False,cid=consumerid,customer=False)
            else:
                return render_template("unpaidbills.html",success=False,error=False,customer=True,b=consumerid)
        except Exception as e :
             return render_template('unpaidbills.html',error=True,success=False,reason=str(e),customer=False)
       
        finally:
            con.close()
@app.route('/admin/compliant')
def compliant():
    return render_template("compliants.html")
    
@app.route('/admin/compliants',methods=['POST','GET'])
def compliantcheck():
    if request.method=='POST':
        try:
            con=sqlite3.connect('CaseStudy.db')
            cur=con.cursor()
            complaintid=request.form['complaint_id']
            session['complaint_id']=complaintid
            r=cur.execute('select complaintid from complaint where complaintid=? and (status="pending"or status="Inprogess")',(complaintid,))
            if r.fetchone():
                a=cur.execute('select * from complaint where complaintid=?',(complaintid,))
                c=a.fetchone()
                b=len(c)
                return render_template("compliants.html",result=c,error=False,success=True,complaint=False,update=False)
            else:
                return render_template("compliants.html",b=complaintid,error=False,success=False,complaint=True,update=False)
        except Exception as e :
             return render_template('compliants.html',error=True,success=False,reason=str(e),customer=False,update=False)
       
        finally:
            con.close()
@app.route('/admin/compliantss',methods=['POST','GET'])
def compliantcheck1():
    if request.method=='POST':
        try:
            con=sqlite3.connect('CaseStudy.db')
            cur=con.cursor()
            s=request.form.get('st')
            complaintid=session['complaint_id']
            cur.execute('update complaint set status=? where complaintid=?',(s,complaintid))
            con.commit()
            return render_template("compliants.html",error=False,Success=False,complaint=False,update=True)
        except Exception as e :
             return render_template('compliants.html',error=True,success=False,reason=str(e),customer=False,update=False)
       
        finally:
            con.close()
@app.route('/admin/deletecompliant')
def deletecompliant():
    return render_template("deletcomplients.html")
@app.route('/admin/deletecompliants',methods=['POST','GET'])
def deletecompliantcheck():
    if request.method=='POST':
        try:
            con=sqlite3.connect('CaseStudy.db')
            cur=con.cursor()
            complaintid=request.form['complaint_id']
            r=cur.execute('select complaintid from complaint where complaintid=?',(complaintid,))
            if r.fetchone():
                b=cur.execute('delete from complaint where complaintid=?',(complaintid,))
                return render_template("deletcomplients.html",success=True,error=False,complaint=False)
            else:
                return render_template("deletcomplients.html",success=False,error=False,complaint=True,b=complaintid)
        except Exception as e :
             return render_template('deletcomplients.html',error=True,success=False,reason=str(e),complaint=False)
       
        finally:
            con.close()
@app.route('/admin/displaycustomer',methods=['GET','POST'])
def displaycustomer():
    return render_template("displaycustomer.html")
@app.route('/admin/displaycustomers',methods=['GET','POST'])
def displaycustomers():
    cid=request.form['consumer_id']
    con=sqlite3.connect('CaseStudy.db')
    cur=con.cursor()
    query='select * from customer where consumerid=?'
    a=cur.execute(query,[cid])
    b=a.fetchone()
    if b:
        return render_template("displaycustomer.html",b=b,customer=True)
    else:
        return render_template("displaycustomer.html",Nocustomer=True,cid=cid)
@app.route('/customer/billHistory',methods=['GET','POST'])
def billhistory():
    con=sqlite3.connect('CaseStudy.db')
    cur=con.cursor()
    a=cur.execute('select * from receipt where consumeid=?  order by tdate DESC limit 5',(session['cid'],))
    b=a.fetchall()
    if b:
        return render_template('billhistory.html',b=b,name=session['n'],cid=session['cid'])
    else:
        return render_template('billhistory.html',name=session['n'],cid=session['cid'])
@app.route('/view')
def display():
    con=sqlite3.connect('CaseStudy.db')
    cur=con.cursor()
    cuid=cur.execute('select * from Customer ')
    return cuid.fetchall()
@app.route('/cview')
def cdisplay():
    con=sqlite3.connect('CaseStudy.db')
    cur=con.cursor()
    cuid=cur.execute('select * from Complaint ')
    return cuid.fetchall()
@app.route('/bview')
def bdisplay():
    con=sqlite3.connect('CaseStudy.db')
    cur=con.cursor()
    cuid=cur.execute('select * from bill ')
    return cuid.fetchall()
@app.route('/rview')
def rdisplay():
    con=sqlite3.connect('CaseStudy.db')
    cur=con.cursor()
    cuid=cur.execute('select * from receipt ')
    return cuid.fetchall()




                           
if __name__=="__main__":
    app.run(debug=True)

