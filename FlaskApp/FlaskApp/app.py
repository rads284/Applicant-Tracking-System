import sqlite3 as sql
from flask import Flask, render_template,request,session,redirect
from flask.ext.session import Session
from datetime import datetime,date,timedelta
import random
app = Flask(__name__)
app.secret_key='any string'
def uniqueid():
    seed=random.getrandbits(32)
    while True:
        yield seed
        seed +=1
@app.route('/')
def main():
    return render_template("login.html")
@app.route('/login3.html/',methods=['POST','GET'])
def login_admin():
    # con = sql.connect('database.db')
    # error = None
    # username=''
    # password=''
    # if request.method == 'POST':
    #     username = request.form['uname']
    #     password = request.form['pwd']
    # if username=='apsystem' and password=="password":
    return redirect("http://127.0.0.1:5000/admin.html/")
@app.route('/admin.html/')
def admin():
    con = sql.connect('database.db')
    cur=con.cursor()
    cur.execute("select * from candidate natural join resume")
    rows1=cur.fetchall()
    cur.execute("select candidate.candidate_id, resume.name, resume_education.education from candidate, resume_education, resume WHERE candidate.resume_id=resume.resume_id and resume_education.resume_id=resume.resume_id order by candidate.candidate_id")
    rows2=cur.fetchall()
    cur.execute("select * from country")
    rows3=cur.fetchall()
    cur.execute("select * from company")
    rows4=cur.fetchall()
    cur.execute("SELECT company.name,j.* from job_description j, company WHERE j.comp_id=company.company_id order by comp_id")
    rows5=cur.fetchall()
    cur.execute("select * from interviewed_by")
    rows6=cur.fetchall()
    return render_template("admin.html",rows1=rows1,rows2=rows2,rows3=rows3,rows4=rows4,rows5=rows5,rows6=rows6)
@app.route('/deletion',methods=['POST','GET'])
def deletion():
    con = sql.connect('database.db')
    cur=con.cursor()
    cur.execute("select * from candidate natural join resume")
    rows1=cur.fetchall()
    cur.execute("select candidate.candidate_id, resume.name, resume_education.education from candidate, resume_education, resume WHERE candidate.resume_id=resume.resume_id and resume_education.resume_id=resume.resume_id order by candidate.candidate_id")
    rows2=cur.fetchall()
    cur.execute("select * from country")
    rows3=cur.fetchall()
    cur.execute("select * from company")
    rows4=cur.fetchall()
    cur.execute("SELECT company.name,j.* from job_description j, company WHERE j.comp_id=company.company_id order by comp_id")
    rows5=cur.fetchall()

    if request.method=='POST':
        datetd=request.form['int_date']
    cur.execute("DELETE FROM interviewed_by WHERE interviewed_by.int_date=(?)",(datetd,))
    cur.execute("select * from interviewed_by")
    rows6=cur.fetchall()
    return render_template("admin.html",rows1=rows1,rows2=rows2,rows3=rows3,rows4=rows4,rows5=rows5,rows6=rows6)
@app.route('/signup.html/')
def singin():
    return render_template('signup.html')
@app.route('/reg',methods=['POST','GET'])
def reg():
    msg="none"
    if request.method=='GET':
        u_name=request.args.get('uname','')
        pwd=request.args.get('pwd','')
        name=request.args.get('name','')
        age=request.args.get('age','')
        gen=request.args.get('sex','')
        dom=request.args.get('domain','')
        pref=request.args.get('pref','')
        exp=request.args.get('exp','')
        compid='null'
        edu=request.args.getlist('edu')
        for r in edu:
            print(edu)
        with sql.connect("database.db") as con:
            cur=con.cursor()
            unique_sequence=uniqueid()
            u_id=next(unique_sequence)
            c_id=next(unique_sequence)
            cur.execute("insert into resume values(?,?,?,?,?,?,?)",(u_id,name,age,gen,dom,pref,exp,))
            cur.execute("insert into candidate values(?,?,?,?,?)",(c_id,u_name,pwd,u_id,compid,))
            for resed in edu:
                cur.execute("insert into resume_education values(?,?)",(u_id,resed,))
        return render_template("login.html")
@app.route('/login1.html/',methods=['POST','GET'])
def login_candidate():
    con = sql.connect('database.db')
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pwd']
        completion = validate_candidate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['username']=username
            return redirect("http://127.0.0.1:5000/cand1.html/")
    return render_template('login2.html', error=error)
def validate_candidate(username, password):
    con = sql.connect('database.db')
    completion = False
    with con:
                cur = con.cursor()
                cur.execute("SELECT username,password FROM candidate")
                rows = cur.fetchall()
                for row in rows:
                    dbUser = row[0]
                    dbPass = row[1]
                    if dbUser==username and dbPass==password:
                        completion=True
    return completion
@app.route('/cand1.html/',methods=['POST','GET'])
def cand():
    con = sql.connect('database.db')
    cur=con.cursor()
    if 'username' in session:
        cur=con.cursor()
        usn=session['username']
        cur.execute("SELECT candidate_id from candidate where username==(?)", (usn,))
        cid=cur.fetchone()
        cand_id=cid[0]
        print(cand_id)
        cur.execute("SELECT name FROM resume,candidate where candidate.resume_id=resume.resume_id and candidate.username =(?)", (usn,))
        #cur.execute("create view eligjob as SELECT DISTINCT job_id,j.domain as domain,j.post as post,j.salary as salary,j.working_hours as hours,co.name as cname from job_description j,company co where j.comp_id=co.company_id and j.education in(SELECT red.education from resume_education red,resume res,candidate c where c.resume_id=res.resume_id and res.resume_id=red.resume_id and c.username =(?)) order by job_id", (usn,))
        name=cur.fetchone()
        cur.execute("SELECT DISTINCT job_id,j.domain as domain,j.post as post,j.salary as salary,j.working_hours as hours, co.name as cname from job_description j,company co,resume r,resume_education re where j.comp_id=co.company_id and j.education in(SELECT red.education from resume_education red,resume res,candidate c where c.resume_id=res.resume_id and res.resume_id=red.resume_id and c.username =(?)) order by job_id", (usn,))
        rows=cur.fetchall()
        return render_template('cand1.html',name=name,rows=rows)
    return render_template('applied.html')
@app.route('/sort_cand/',methods=['POST','GET'])
def sort_cand():
    con = sql.connect('database.db')
    cur=con.cursor()
    if request.method == 'POST':
        pref = request.form['pref']
    print(pref)
    usn=session['username']
    cur.execute("SELECT name FROM resume,candidate where candidate.resume_id=resume.resume_id and candidate.username =(?)", (usn,))
    # print(pref)
    name=cur.fetchone()
    if pref=='domain':
        cur.execute("SELECT DISTINCT job_id,j.domain as domain,j.post as post,j.salary as salary,j.working_hours as hours, co.name as cname from job_description j,company co,resume r,resume_education re where j.comp_id=co.company_id and j.education in(SELECT red.education from resume_education red,resume res,candidate c where c.resume_id=res.resume_id and res.resume_id=red.resume_id and c.username =(?)) order by domain",(usn,))
    elif pref=='post':
        cur.execute("SELECT DISTINCT job_id,j.domain as domain,j.post as post,j.salary as salary,j.working_hours as hours, co.name as cname from job_description j,company co,resume r,resume_education re where j.comp_id=co.company_id and j.education in(SELECT red.education from resume_education red,resume res,candidate c where c.resume_id=res.resume_id and res.resume_id=red.resume_id and c.username =(?)) order by post", (usn,))
    elif pref=='salary':
        cur.execute("SELECT DISTINCT job_id,j.domain as domain,j.post as post,j.salary as salary,j.working_hours as hours, co.name as cname from job_description j,company co,resume r,resume_education re where j.comp_id=co.company_id and j.education in(SELECT red.education from resume_education red,resume res,candidate c where c.resume_id=res.resume_id and res.resume_id=red.resume_id and c.username =(?)) order by cast(salary as int) ", (usn,))
    elif pref=='hours':
        cur.execute("SELECT DISTINCT job_id,j.domain as domain,j.post as post,j.salary as salary,j.working_hours as hours, co.name as cname from job_description j,company co,resume r,resume_education re where j.comp_id=co.company_id and j.education in(SELECT red.education from resume_education red,resume res,candidate c where c.resume_id=res.resume_id and res.resume_id=red.resume_id and c.username =(?)) order by hours", (usn,))
    elif pref=='cname':
        cur.execute("SELECT DISTINCT job_id,j.domain as domain,j.post as post,j.salary as salary,j.working_hours as hours, co.name as cname from job_description j,company co,resume r,resume_education re where j.comp_id=co.company_id and j.education in(SELECT red.education from resume_education red,resume res,candidate c where c.resume_id=res.resume_id and res.resume_id=red.resume_id and c.username =(?)) order by cname", (usn,))
    rows=cur.fetchall()
    for row in rows:
        print(row)
    return render_template('cand1.html',name=name,rows=rows)
@app.route('/filter_cand/',methods=['POST','GET'])
def filter_cand():
    con = sql.connect('database.db')
    cur=con.cursor()
    usn=session['username']
    if request.method == 'POST':
        domain = request.form['domain']
        post=request.form['post']
        # salary=request.form['salary']
        # hours=request.form['hours']
        company=request.form['company']

    cur.execute("SELECT DISTINCT job_id,j.domain as domain,j.post as post,j.salary as salary,j.working_hours as hours, co.name as cname from job_description j,company co,resume r,resume_education re where j.comp_id=co.company_id and j.post=(?) and j.education in(SELECT red.education from resume_education red,resume res,candidate c where c.resume_id=res.resume_id and res.resume_id=red.resume_id and c.username =(?)) and j.domain=(?) order by cname", (post,usn,domain,))
    rows=cur.fetchall()
    for row in rows:
        print(row)
    cur.execute("SELECT name FROM resume,candidate where candidate.resume_id=resume.resume_id and candidate.username =(?)", (usn,))
    # print(pref)
    name=cur.fetchone()
    return render_template('cand1.html',name=name,rows=rows)
@app.route('/accept/',methods=['POST','GET'])
def accept():
    con = sql.connect('database.db')
    cur=con.cursor()
    aajkitareek=(datetime.now().date())
    if 'username' in session:
        cur=con.cursor()
        usn=session['username']
        cur.execute("SELECT candidate_id from candidate where username==(?)", (usn,))
        cid=cur.fetchone()
        cand_id=cid[0]
    if request.method=='POST':
        jobs=request.form.getlist('applyingfor')
    for job in jobs:
        print(job)
        cur.execute("insert into applied_for values(?,?,?)",(cand_id,job,aajkitareek,))
        con.commit()
    msg="none"
    aajkitareek=(datetime.now().date())
    con = sql.connect('database.db')
    cur=con.cursor()
    usn=session['username']
    cur.execute("SELECT job_id,j.domain as domain,j.post as post,j.salary as salary,j.working_hours as hours, co.name as cname from job_description j,company co  where j.comp_id=co.company_id and job_id in(SELECT job_id from applied_for,candidate where applied_for.cand_id=candidate.candidate_id and candidate.username=(?))",(usn,))
    rows=cur.fetchall()
    cur.execute("SELECT distinct interviewed_by.jo_id, job_description.domain as domain, job_description.post as post, job_description.salary as salary, job_description.working_hours as hours, company.name as company FROM job_description,interviewed_by,company, candidate WHERE job_description.job_id=interviewed_by.jo_id and candidate.candidate_id=interviewed_by.cand_id and job_description.comp_id=company.company_id and candidate.username=(?)",(usn,))
    rows2=cur.fetchall()
    cur.execute("SELECT name FROM resume,candidate where candidate.resume_id=resume.resume_id and candidate.username =(?)", (usn,))
    name=cur.fetchone()
    print(name)
    for row in rows:
        print(row)
    return render_template('applied.html',rows=rows,name=name,rows2=rows2)
@app.route('/login2.html/',methods=['POST','GET'])
def login_company():
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pwd']
        completion = validate_company(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['comp_id']=password
            return redirect("http://127.0.0.1:5000/job.html/")
    return render_template('login1.html', error=error)
def validate_company(username, password):
    con = sql.connect('database.db')
    completion = False
    with con:
                cur = con.cursor()
                cur.execute("SELECT name,company_id FROM company ")
                rows = cur.fetchall()
                for row in rows:
                    dbUser = row[0]
                    dbPass = row[1]
                    if dbUser==username and dbPass==password:
                        completion=True
    return completion
@app.route('/job.html/',methods=['POST','GET'])
def job():
    con = sql.connect('database.db')
    cur=con.cursor()
    cid=session['comp_id']
    cur.execute("select name from company where company_id=(?)",(cid,))
    name=cur.fetchone()
    # cur.execute("select applied_for.cand_id as candidate_id, resume.name, candidate.resume_id, applied_for.job_id, resume.domain from applied_for, resume, candidate, job_description, company where applied_for.cand_id=candidate.candidate_id and resume.resume_id=candidate.resume_id and applied_for.job_id=job_description.job_id and job_description.comp_id=company.company_id and company.company_id=(?)",(cid,))
    cur.execute("Select applied_for.job_id,applied_for.cand_id as candidate_id, resume.name, resume.age, resume.sex, resume.domain, resume.preferences, resume.experience from applied_for, resume, candidate, job_description, company where applied_for.cand_id=candidate.candidate_id and resume.resume_id=candidate.resume_id and applied_for.job_id=job_description.job_id and job_description.comp_id=company.company_id and company.company_id=(?)",(cid,))
    rows=cur.fetchall()
    return render_template('job.html',name=name,rows=rows)
@app.route('/sort_job/',methods=['POST','GET'])
def sort_job():
    con = sql.connect('database.db')
    cur=con.cursor()
    if request.method == 'POST':
        pref = request.form['pref']
    print(pref)
    cid=session['comp_id']
    cur.execute("select name from company where company_id=(?)",(cid,))
    name=cur.fetchone()
    if pref=='Age':
        cur.execute("Select applied_for.job_id,applied_for.cand_id as candidate_id, resume.name, resume.age, resume.sex, resume.domain, resume.preferences, resume.experience from applied_for, resume, candidate, job_description, company where applied_for.cand_id=candidate.candidate_id and resume.resume_id=candidate.resume_id and applied_for.job_id=job_description.job_id and job_description.comp_id=company.company_id and company.company_id=(?) order by resume.age",(cid,))
    elif pref=='Gen':
        cur.execute("Select applied_for.job_id,applied_for.cand_id as candidate_id, resume.name, resume.age, resume.sex, resume.domain, resume.preferences, resume.experience from applied_for, resume, candidate, job_description, company where applied_for.cand_id=candidate.candidate_id and resume.resume_id=candidate.resume_id and applied_for.job_id=job_description.job_id and job_description.comp_id=company.company_id and company.company_id=(?) order by resume.sex",(cid,))
    elif pref=='Domain':
        cur.execute("Select applied_for.job_id,applied_for.cand_id as candidate_id, resume.name, resume.age, resume.sex, resume.domain, resume.preferences, resume.experience from applied_for, resume, candidate, job_description, company where applied_for.cand_id=candidate.candidate_id and resume.resume_id=candidate.resume_id and applied_for.job_id=job_description.job_id and job_description.comp_id=company.company_id and company.company_id=(?) order by resume.domain",(cid,))
    elif pref=='Preferences':
        cur.execute("Select applied_for.job_id,applied_for.cand_id as candidate_id, resume.name, resume.age, resume.sex, resume.domain, resume.preferences, resume.experience from applied_for, resume, candidate, job_description, company where applied_for.cand_id=candidate.candidate_id and resume.resume_id=candidate.resume_id and applied_for.job_id=job_description.job_id and job_description.comp_id=company.company_id and company.company_id=(?) order by resume.preferences",(cid,))
    elif pref=='Experience':
        cur.execute("Select applied_for.job_id,applied_for.cand_id as candidate_id, resume.name, resume.age, resume.sex, resume.domain, resume.preferences, resume.experience from applied_for, resume, candidate, job_description, company where applied_for.cand_id=candidate.candidate_id and resume.resume_id=candidate.resume_id and applied_for.job_id=job_description.job_id and job_description.comp_id=company.company_id and company.company_id=(?) order by resume.experience",(cid,))
    rows=cur.fetchall()
    for row in rows:
        print(row)
    return render_template('job.html',name=name,rows=rows)
@app.route('/filter_job/',methods=['GET','POST'])
def filter_job():
    con = sql.connect('database.db')
    cur=con.cursor()
    cid=session['comp_id']
    cur.execute("select name from company where company_id=(?)",(cid,))
    name=cur.fetchone()
    if request.method == 'POST':
        domain = request.form['domain']
        pref=request.form['preferences']
        exp=request.form['experience']
        country=request.form['country']
    if country=="True":
        cur.execute("Select applied_for.job_id,applied_for.cand_id as candidate_id, resume.name, resume.age, resume.sex, resume.domain, resume.preferences, resume.experience from applied_for, resume, candidate, job_description, company, has_permit_for where applied_for.cand_id=candidate.candidate_id and resume.resume_id=candidate.resume_id and applied_for.job_id=job_description.job_id and job_description.comp_id=company.company_id and has_permit_for.candidate_id=candidate.candidate_id and has_permit_for.country_id=company.country_id and company.company_id=(?)",(cid,))
    else:
        cur.execute("Select applied_for.job_id,applied_for.cand_id as candidate_id, resume.name, resume.age, resume.sex, resume.domain, resume.preferences, resume.experience from applied_for, resume, candidate, job_description, company where applied_for.cand_id=candidate.candidate_id and resume.resume_id=candidate.resume_id and applied_for.job_id=job_description.job_id and job_description.comp_id=company.company_id and company.company_id=(?) and resume.domain=(?) and resume.experience>=(?) and resume.preferences=(?) ",(cid,domain,exp,pref))
    rows=cur.fetchall()
    return render_template('job.html',name=name,rows=rows)
@app.route('/schedule/',methods=['GET','POST'])
def schedule():
    con = sql.connect('database.db')
    cur=con.cursor()
    cid=session['comp_id']
    aajkitareek=(datetime.now().date())+timedelta(2)
    print(aajkitareek)
    if request.method=='POST':
        jids=request.form.getlist('pref1')
        cids=request.form.getlist('pref2')
        print(jids)
        print(cids)
        l=len(jids)
        status="pending"
        for i in range(0,l):
            cur.execute("insert into interviewed_by values(?,?,?,?,?)",(cids[i],jids[i],aajkitareek,"11:00:00",status,))
        con.commit()
        cur.execute("select interviewed_by.cand_id as candidate_id,interviewed_by.jo_id as job_id, resume.name as name,interviewed_by.int_date as date, interviewed_by.int_time as time, interviewed_by.status as status from interviewed_by, resume, candidate, job_description, company where resume.resume_id=candidate.resume_id and candidate.candidate_id=interviewed_by.cand_id and job_description.comp_id=company.company_id and interviewed_by.jo_id=job_description.job_id and company.company_id=(?)",(cid,))
        rows2=cur.fetchall()
    return render_template("inter.html",rows2=rows2)
if __name__ == "__main__":
    app.run(debug = True)
