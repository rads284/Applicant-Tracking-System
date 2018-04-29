import sqlite3

conn=sqlite3.connect('databasetest.db')
c=conn.cursor()

def create_table():
    c.execute('create table if not exists resume( resume_id varchar(10) primary key,name varchar(10),age varchar(2),sex varchar(1),domain varchar(20),preferences varchar(30),experience varchar(30))')
    c.execute('create table if not exists candidate(candidate_id varchar(10) primary key,username varchar(40),password varchar(15),resume_id varchar(10) ,comp_id varcha(10),foreign key(resume_id) references resume(resume_id) on delete cascade,foreign key(resume_id) references resume(resume_id) on update cascade)')
    c.execute('create table if not exists resume_education(resume_id varchar(10),education varchar(20),foreign key(resume_id) references resume(resume_id) on delete cascade,foreign key(resume_id) references resume(resume_id) on update cascade)')
    c.execute('create table if not exists country(country_id varchar(10) primary key,name varchar(15),permit_req varchar(20))')
    c.execute('create table if not exists company(company_id varchar(10) primary key,name varchar(15),domain varchar(20),turnover varchar(20),no_of_employees varchar(20),country_id varchar(10),foreign key(country_id) references country(country_id) on delete cascade,foreign key(country_id) references country(country_id) on update cascade)')
    c.execute('create table if not exists job_description(job_id varchar(10) primary key,domain varchar(20),post varchar(15),salary varchar(15),working_hours varchar(5),experience varchar(5),education varchar(20),comp_id varchar(10),foreign key(comp_id) references company(company_id))')
    c.execute('create table if not exists interviewed_by(cand_id varchar(10),jo_id varchar(10),int_date date,int_time time,status varchar(10),foreign key(cand_id) references candidate(candidate_id),foreign key(jo_id) references job_description(job_id))')
    c.execute('create table if not exists applied_for(cand_id varchar(10) ,job_id varchar(10) ,date_applied date,foreign key(cand_id) references candidate(candidate_id),foreign key(job_id) references job_description(job_id))')
    c.execute('create table if not exists has_permit_for(candidate_id varchar(10) ,country_id varchar(10),duration varchar(10),foreign key(candidate_id) references candidate(candidate_id),foreign key(country_id) references country(country_id))')

def data_entry():
     c.execute("insert into resume values('R02', 'Mehul', '29', 'M', 'Bigdata', 'Test Engineer', '6'),('R03', 'Ankita', '31', 'F', 'Robotics', 'Programmer', '6'),('R04', 'Mohan', '26', 'M', 'Bigdata', 'Architect', '6'), ('R05', 'Roshni', '22', 'F', 'Machine Learning', 'Designer', '6'),('R06', 'Rashmi', '25', 'F', 'Web Design', 'Designer', '6'),('R07', 'Manish', '23', 'M', 'Bigdata', 'Test Engineer', '6'),('R08', 'Ananya', '35', 'F', 'Robotics', 'Programmer', '6'),('R09', 'Manjunath', '27', 'M', 'Bigdata', 'Architect', '6'),('R10', 'Rakesh', '24', 'M', 'Machine Learning', 'Designer', '6'),('R11', 'Rasya', '26', 'F', 'Web Design', 'Designer', '6'),('R12', 'Maanya', '29', 'F', 'Bigdata', 'Test Engineer', '6'),('R13', 'Anjana', '31', 'F', 'Robotics', 'Programmer', '6'),('R14', 'Malvika', '26', 'F', 'Bigdata', 'Architect', '6'),('R15', 'Rohan', '22', 'M', 'Machine Learning', 'Designer', '6')")
     c.execute("insert into resume values('R16', 'Rajesh', '24', 'M', 'Web Design','Designer', '6'),('R17', 'Mona', '29', 'F', 'Bigdata', 'Test Engineer', '6'),('R18', 'Akash', '31', 'M', 'Robotics', 'Programmer', '6'),('R19', 'Maria', '26', 'F', 'Bigdata', 'Architect', '6'),('R20', 'Kailash', '22', 'M', 'Machine Learning', 'Designer', '6')")
     c.execute("insert into candidate values('C001', 'R0100', 'welcome123', 'R05', 'CMP1'),('C002', 'R0101', 'student099', 'R02', 'CMP6'),('C003', 'R0102', 'hello487', 'R04', 'CMP4'),('C004', 'R0103', 'moonsun287', 'R01', 'CMP1'),('C005', 'R0104', 'vulture981', 'R03', 'CMP3'),('C006', 'R0105', 'casper67678', 'R06', 'CMP7'),('C007', 'R0106', 'henryrox82337', 'R09', 'CMP8'),('C008', 'R0107', 'sunshine8273', 'R08', 'CMP3'),('C009', 'R0108', 'moonlight38729', 'R10', 'CMP1'),('C010', 'R0109', 'sunlight379', 'R12', 'CMP7'),('C011', 'R0110', 'horse889', 'R11', 'CMP9'),('C012', 'R0111', 'giraffe_2', 'R15', 'CMP3'),('C013', 'R0112', 'college897', 'R13', 'CMP5'),('C014', 'R0113', 'liferulz', 'R14', 'CMP2'),('C015', 'R0114', 'birthday', 'R19', 'CMP5')")
     c.execute("insert into resume_education values('R01', 'BDes'), ('R02', 'BTech'),('R02', 'MSc'),('R03', 'BSc'),('R03', 'MSc'),('R03', 'PhD'),('R04', 'BDes'),('R05', 'BTech'),('R05', 'MSc'),('R05', 'PhD'),('R06', 'BDes'),('R06', 'MDes'),('R07', 'MTech'),('R08', 'BTech'),('R08', 'MSc'),('R09', 'BDes'),('R10', 'MTech'),('R11', 'BSc'),('R12', 'BCom'),('R13', 'BSc'),('R14', 'BTech'),('R15', 'MSc'),('R16', 'BDes'),('R17', 'MTech'),('R18', 'BBA'),('R19', 'BDes'),('R20', 'BPharma')")
     c.execute("insert into country values('9870', 'India', 'Yes'),('9871', 'Bangladesh', 'Yes'),('9872', 'Sweden', 'No'),('9873', 'Singapore', 'No'),('9874', 'Indianapolis', 'Yes'),('9875', 'Japan', 'Yes'),('9876', 'France', 'No'),('9877', 'UK', 'No'),('9878', 'Indonesia', 'Yes'),('9879', 'Germany', 'Yes'),('9880', 'Nepal', 'No'),('9881', 'Austria', 'No'),('9882', 'Bangladesh', 'No'),('9883', 'Indianapolis', 'Yes'),('9884', 'Japan', 'Yes'),('9885', 'Japan', 'No'),('9886', 'Indianapolis', 'No'),('9887', 'Indonesia', 'Yes'),('9888', 'Germany', 'Yes'),('9889', 'Nepal', 'No'),('9890', 'Germany', 'No')")
     c.execute("insert into company values('12340', 'IBM', 'Robotics', '100Cr', '203','9870'),('12341', 'Infosys', 'Web Design', '60Cr', '300','9871'),('12342', 'TCS', 'Bigdata', '400Cr', '900','9870'),('12343', 'HP', 'Robotics', '800Cr', '120','9872'),('12344', 'Wipro', 'Machine Learning', '1000Cr', '410','9873'),('12345', 'Cisco', 'AI', '100Cr', '203','9870'),('12346', 'Motorola', 'Web Design', '60Cr', '300','9875'),('12347', 'Delloitte', 'Bigdata', '400Cr', '900','9874'),('12348', 'GE', 'Robotics', '800Cr', '120','9877'),('12349', 'Dell', 'Machine Learning', '1000Cr', '410','9878'),('12350', 'Flipkart', 'Robotics', '100Cr', '203','9876'),('12351', 'Amazon', 'AI', '60Cr', '300','9874'),('12352', 'Lenovo', 'Bigdata', '400Cr', '900','9879'),('12353', 'Unilever', 'Robotics', '800Cr', '120','9881'),('12354', 'PWC', 'Machine Learning', '1000Cr', '410','9880'),('12355', 'Wipro', 'Robotics', '90Cr', '203','9875'),('12356', 'IBM', 'AI', '600Cr', '308','9874')")
     c.execute("insert into company values('12357', 'Cisco', 'Bigdata', '40Cr', '540','9879'),('12358', 'Unilever', 'Robotics', '80Cr', '220','9871'),('12359', 'PWC', 'Machine Learning', '100Cr', '710','9870')")
     c.execute("insert into job_description values('J01', 'Machine Learning', 'Manager', '50000', '6', '4', 'MSc', '12341'),('J02', 'Image Processing', 'Director', '100000', '5', '7', 'BSc', '12344'),('J03', 'Web Design', 'COF', '90000', '6', '9', 'MSc', '12343'),('J04', 'Machine Learning', 'Intern', '8000', '8', '0', 'BTech', '12342'),('J05', 'Robotics', 'COE', '500000', '4', '12', 'PhD', '12340'),('J06', 'Machine Learning', 'Manager', '80000', '6', '4', 'MSc', '12347'),('J07', 'Image Processing', 'Director', '80000', '5', '7', 'BSc', '12349'),('J08', 'Web Design', 'COF', '60000', '6', '9', 'MSc', '12353'),('J09', 'Web Design', 'Intern', '5000', '8', '0', 'BTech', '12352'),('J10', 'Robotics', 'COE', '80000', '4', '12', 'PhD', '12348'),('J11', 'Machine Learning', 'Manager', '1000000', '6', '4', 'MSc', '12349'),('J12', 'Image Processing', 'Director', '900000', '5', '7', 'BSc', '12354'),('J13', 'Web Design', 'COF', '70000', '6', '9', 'MSc', '12344')")
     c.execute("insert into job_description values('J14', 'Machine Learning', 'Intern', '11000', '8', '0', 'BTech', '12347'),('J15', 'Robotics', 'COE', '500000', '4', '12', 'PhD', '12349'),('J16', 'Image Processing', 'COE', '6000000', '1', '5', 'MSc', '12342'),('J17', 'Robotics', 'Intern', '1000000', '2', '8', 'BSc', '12354'),('J18', 'Machine Learning', 'COF', '780000', '7', '9', 'MSc', '12347'),('J19', 'Machine Learning', 'Manager', '15000', '8', '0', 'BTech', '12348'),('J20', 'Robotics', 'COE', '60000', '5', '12', 'PhD', '12349')")
     c.execute("insert into interviewed_by values('C001', 'J03', '2012-12-17', '17:00:54', 'Accept'),('C003', 'J01', '2018-10-23', '09:30:00', 'Accept'),('C002', 'J04', '2011-04-19', '11:20:32', 'Reject'),('C004', 'J02', '2009-08-30', '09:30:57', 'Accept'),('C005', 'J05', '2004-05-09', '06:45:36', 'Reject'),('C003', 'J04', '2012-12-17', '19:00:54', 'Accept'),('C003', 'J01', '2018-10-23', '09:30:00', 'Accept'),('C002', 'J04', '2011-04-19', '11:20:32', 'Reject'),('C004', 'J02', '2011-08-30', '09:30:57', 'Accept'),('C005', 'J05', '2004-06-09', '07:45:36', 'Reject'),('C006', 'J03', '2012-12-17', '18:00:54', 'Accept'),('C003', 'J01', '2018-11-19', '23:45:00', 'Accept'),('C002', 'J04', '2011-10-16', '11:20:32', 'Reject'),('C004', 'J02', '2009-08-15', '12:00:57', 'Accept'),('C005', 'J05', '2004-04-23', '08:45:36', 'Reject'),('C001', 'J03', '2012-12-28', '10:15:54', 'Accept'),('C003', 'J01', '2017-11-29', '09:30:00', 'Reject'),('C002', 'J04', '2017-07-28', '13:15:32', 'Reject')")
     c.execute("insert into interviewed_by values('C004', 'J02', '2009-08-30', '15:30:57', 'Accept'),('C005', 'J05', '2014-03-16', '12:20:36', 'Reject')")
     c.execute("insert into applied_for values('C001', 'J03', '2017-05-02'),('C003', 'J01', '2014-12-22'),('C002', 'J04', '2012-09-29'),('C004', 'J05', '2017-04-01'),('C005', 'J02', '2017-01-19'),('C006', 'J13', '2015-06-02'),('C009', 'J11', '2013-11-22'),('C008', 'J14', '2016-08-29'),('C011', 'J15', '2018-03-01'),('C010', 'J12', '2012-12-19'),('C012', 'J08', '2017-07-02'),('C014', 'J06', '2016-10-22'),('C013', 'J09', '2014-03-29'),('C001', 'J10', '2015-09-01'),('C002', 'J07', '2012-01-19'),('C005', 'J03', '2013-08-02'),('C006', 'J01', '2014-07-22'),('C003', 'J04', '2017-03-29'),('C012', 'J05', '2018-04-02'),('C011', 'J02', '2015-12-19')")
     c.execute("insert into has_permit_for values('C004', '9873', '9'),('C001', '9871', '4'),('C002', '9870', '12'),('C003', '9872', '8'),('C005', '9871', '19'),('C009', '9883', '3'),('C006', '9881', '10'),('C007', '9880', '6'),('C008', '9882', '2'),('C010', '9881', '12'),('C014', '9874', '15'),('C011', '9875', '5'),('C012', '9877', '1'),('C013', '9876', '6'),('C015', '9878', '11'),('C015', '9890', '18'),('C002', '9888', '14'),('C003', '9884', '3'),('C004', '9887', '7'),('C011', '9889', '10')")

     conn.commit()
     c.close()
     conn.close()

create_table()
data_entry()