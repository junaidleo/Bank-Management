from flask import Flask,render_template,url_for,redirect,request, flash, session, abort
from sqlalchemy.orm import sessionmaker
from tabledef import *
import datetime
import os

app = Flask(__name__)
Session = sessionmaker(bind=engine)
temp_var=1
temp_id=""

def _get_date():
    return datetime.datetime.now()

@app.route('/')
def main_page():
    return render_template('base.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        s = Session()
        user=request.form['username']
        pas=request.form['password']
        temp=s.query(Login_details).filter(Login_details.username.in_([user]),Login_details.password.in_([pas]))
        temp=temp.first()
        if temp:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash("Invalid Details")
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    if session.get('logged_in'):
        session['logged_in'] = False
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/reg',methods=["POST","GET"])
def reg():
    if session.get('logged_in'):
        if request.method=="POST":
            try:
                temp=cust_data(request.form['cus_ssnid'],request.form['cus_name'],request.form['cus_age'],request.form['cus_address'],request.form.get('cus_state'),request.form.get('cus_city'))
                s = Session()
                s.add(temp)
                s.commit()
            except Exception as e:
                print(e);
                flash("Enter Valid Details")
                return render_template("cus_reg.html")
            flash("Customer data successfully uploaded")
            return render_template("cus_reg.html")
        else:
            return render_template("cus_reg.html")
    else:
        return redirect(url_for('login'))

@app.route("/update",methods=['POST','GET'])
def update():
    global temp_var,temp_id
    if session.get('logged_in'):
        if request.method=="POST" and temp_var==1:
            try:
                s = Session()
                ssnid=request.form['ssn_id']
                temp_id=ssnid
                temp=s.query(cust_data).filter(cust_data.ssn_id.in_([ssnid]))
                temp=temp.first()
                if temp:
                    temp_var=2
                    return render_template("cus_up.html",temp=temp)
                else:
                    flash("Enter Valid Details")
                    return render_template('cust_up.html')
            except Exception as e:
                print(e);
                return render_template("cus_up.html")
        elif request.method=="POST" and temp_var==2:
            try:
                s = Session()
                temp=s.query(cust_data).filter(cust_data.ssn_id.in_([temp_id]))
                temp=temp.first()
                temp.cust_name=request.form['name']
                temp.cust_add=request.form['add']
                temp.cust_age=request.form['age']
                temp.lst_up=_get_date()
                s.commit()
                flash("Details Updated Successfully")
                temp_var=1
                return render_template("cus_up.html")
            except Exception as e:
                print(e);
                flash("Enter Valid Details")
                return render_template("cus_up.html")
        else:
            return render_template("cus_up.html")
    else:
        return redirect(url_for('login'))

@app.route("/delete",methods=['POST','GET'])
def delete():
    if session.get('logged_in'):
        if request.method=="POST":
            try:
                s=Session()
                ssnid=request.form['ssnid']
                temp=s.query(cust_data).filter(cust_data.ssn_id.in_([ssnid]))
                temp=temp.first()
                s.delete(temp)
                s.commit()
                flash("Customer Deleted Successfully")
                return render_template('del_cust.html')
            except Exception as e:
                print(e)
                flash("Enter Valid Details")
                return render_template('del_cust.html')
        else:
            return render_template('del_cust.html')
    else:
        return redirect(url_for('login'))

@app.route("/acc_cre",methods=['POST','GET'])
def acc_cre():
    if session.get('logged_in'):
        if request.method=='POST':
            try:
                s=Session()
                cusid=request.form["cusid"]
                temp=s.query(cust_data).filter(cust_data.cust_id.in_([cusid]))
                temp=temp.first()
                temp.acc_type=request.form.get('acc_type')
                temp.dep_amt=request.form['dept_amt']
                temp.lst_up=_get_date()
                s.commit()
                flash("Account Created Successfully")
                return render_template("acc_cre.html")
            except Exception as e:
                print(e)
                flash("Enter Valid Details")
                return render_template('acc_cre.html')
        else:
            return render_template('acc_cre.html')
    else:
        return redirect(url_for('login'))

@app.route("/acc_del",methods=['POST','GET'])
def acc_del():
    if session.get('logged_in'):
        if request.method=='POST':
            try:
                s=Session()
                cusid=request.form['cust_id']
                temp=s.query(cust_data).filter(cust_data.cust_id.in_([cusid]))
                temp=temp.first()
                temp.acc_type=None
                temp.dep_amt=None
                temp.lst_up=_get_date()
                s.commit()
                flash("Account Deleted Successfully")
                return render_template("acc_del.html")
            except Exception as e:
                print(e)
                flash("Enter Valid Details")
                return render_template('acc_del.html')
        else:
            return render_template('acc_del.html')
    else:    
        return redirect(url_for('login'))

@app.route("/search",methods=['POST','GET'])
def search():
    if session.get('logged_in'):
        if request.method=="POST":
            try:
                s=Session()
                ssnid=request.form['ssn_id']
                temp=s.query(cust_data).filter(cust_data.ssn_id.in_([ssnid]))
                temp=temp.first()
                if temp:
                    return render_template("search.html",temp=temp)
                else:
                    flash("Enter Valid Details")
                    return render_template('search.html')
            except Exception as e:
                print(e)
                flash("Enter Valid Details")
                return render_template('search.html')
        else:
            return render_template('search.html')
    else:
        redirect(url_for('login'))

@app.route("/home")
def home():
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        redirect(url_for('login'))

@app.route('/deposit',methods=['POST','GET'])
def deposit():
    if session.get('logged_in'):
        if request.method=='POST':
            try:
                s=Session()
                cusid=request.form['cus_id']
                amt=request.form['deposit']
                temp=s.query(cust_data).filter(cust_data.cust_id.in_([cusid]))
                temp=temp.first()
                temp.dep_amt=temp.dep_amt+int(amt) 
                s.commit()
                flash('Successfully Deposited')
                return render_template('acc_dep.html')
            except Exception as e:
                print(e)
                flash("Enter Valid Details")
                return render_template('acc_dep.html')
        else:
            return render_template('acc_dep.html')
    else:
        redirect(url_for('login'))

@app.route('/withdraw',methods=['POST','GET'])
def withdraw():
    if session.get('logged_in'):
        if request.method=='POST':
            try:
                s=Session()
                cusid=request.form['cus_id']
                amt=request.form['withdraw']
                temp=s.query(cust_data).filter(cust_data.cust_id.in_([cusid]))
                temp=temp.first()
                if temp.dep_amt>=int(amt):
                    temp.dep_amt=temp.dep_amt-int(amt)
                else:
                    flash('Balance Insufficient')
                    return render_template('acc_wit.html') 
                s.commit()
                flash('Successfully Withdrawn')
                return render_template('acc_wit.html')
            except Exception as e:
                print(e)
                flash("Enter Valid Details")
                return render_template('acc_wit.html')
        else:
            return render_template('acc_wit.html')
    else:
        redirect(url_for('login'))

@app.route('/transfer',methods=['POST','GET'])
def transfer():
    if session.get('logged_in'):
        if request.method=='POST':
            try:
                s=Session()
                cusid1=request.form['cus_id1']
                cusid2=request.form['cus_id2']
                amt=request.form['transfer']
                temp1=s.query(cust_data).filter(cust_data.cust_id.in_([cusid1]))
                temp1=temp1.first()
                temp2=s.query(cust_data).filter(cust_data.cust_id.in_([cusid2]))
                temp2=temp2.first()
                if temp1.dep_amt>=int(amt):
                    temp1.dep_amt=temp1.dep_amt-int(amt)
                    temp2.dep_amt=temp2.dep_amt+int(amt)
                else:
                    flash('Balance Insufficient')
                    return render_template('transfer.html')
                s.commit()
                flash('Successfully Transferred')
                return render_template('transfer.html')
            except Exception as e:
                print(e)
                flash("Enter Valid Details")
                return render_template('transfer.html')
        else:
            return render_template('transfer.html')
    else:
        redirect(url_for('login'))

if __name__=='__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)