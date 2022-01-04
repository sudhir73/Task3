import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    database="task",
    user="postgres",
    password="Sudh!r9899",
    port = "5432")
sudhir = conn.cursor()
#sudhir.execute('create database task;')
# sudhir.execute("create table employee(id serial primary key,name varchar(25) not null,password varchar(16) not null,aadhaar bigint not null,secq text not null,seca text not null,mobile bigint not null,designation varchar(25), salary int, status varchar(18) default 'inactive', check (mobile > 999999999) );")
# sudhir.execute("create table emp_audit(id int not null,time text not null,reg varchar(5) default 'no',update varchar(5) default 'no');")
# sudhir.execute("create table admin(id int,password varchar(16));")
# sudhir.execute("insert into admin values(10530,'admin');")

def registration():
    
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    aadhaar = input("Enter your Aadhaar number: ")
    secq = input("Enter a secret question: ")
    seca = input("Enter the password to your secret question: ")
    mobile = int(input("Enter your mobile number: "))
    
    if mobile < 999999999:
        print("Invalid mobile number. Try again.")
        registration()
    else:
        
        y="insert into employee (name, password, aadhaar, secq, seca, mobile) values ('{}','{}',{},'{}','{}',{});"
        sudhir.execute(y.format(name,password,aadhaar,secq,seca,mobile))
        
        temp = "select id from employee where name='{}';"
        x=temp.format(name)
        sudhir.execute(x)
        id=sudhir.fetchone()
        print("Registered successfully. Your ID is: ",list(id))
        select()

        
def operations():
    operation = int(input("1. Update \n2. View \n3. Log \nChoose:"))
    
    admin_id = input("Enter admin ID: ")
    admin_pass = input("Enter your password: ")
    
    adm = "select * from admin where id = {} and password = '{}';"
    ad = adm.format(admin_id, admin_pass)
    
    sudhir.execute(ad)
    b = sudhir.fetchall()
    
    if operation == 1:
        if len(b)!=0:
            update = int(input("1. Mobile \n2. Designation \n3. Salary \n4. Status \nChoose: "))
            update_id = input("Enter employee ID: ")
            sudhir.execute("Select status from employee where id = "+update_id +";")
            d = sudhir.fetchall()
            if update < 4 and update > 0:
                if d == 'active':
                    if update == 1:
                        update_no = input("Enter new mobile number: ")
                        sudhir.execute("update employee set mobile = "+update_no+" where id = "+update_id+";")
                        print("Mobile number updated")
                        select()
                        
                    elif update == 2:
                        update_desig = input("Enter designation: ")
                        sudhir.execute("update employee set designation = "+update_desig+" where id = "+update_id+";")
                        print("Designation updated")
                        select()
                        
                    elif update == 3:
                        update_salary = input("Enter new salary: ")
                        sudhir.execute("update employee set salary = " + update_salary + " where id = "+update_id+";")
                        print("Salary updated")
                        select()
                else:
                    print("Inactive user.")
                    select()
        
            if update == 4:
                sudhir.execute("select * from employee where id = "+update_id+";")
                c = sudhir.fetchall()
                if len(c)!=0:
                    update_status = input("Enter status: ")
                    sudhir.execute("update employee set status = '"+update_status+"' where id = "+update_id+";")
                    if update_status == 'active':
                        update_desig = input("Enter designation: ")
                        update_salary = input("Enter new salary: ")
                        sudhir.execute("update employee set designation = '"+update_desig+"', salary =" + update_salary+"  where id = "+update_id+";")
                    elif update_status == 'inactive':
                        sudhir.execute("update employee set designation = null, salary = null where id = "+update_id+";")
                    print("Status updated")
                    select()
                else:
                    print("Invalid user.")
                
            elif update > 5 or update < 1:
                print("Invalid selection")
                operations()
        else:
            print("Invalid access. Only admin can update the table.")
            operations() 
            
    elif operation == 2:
        if len(b)!=0:
             view_id = input("Enter ID to view details: ")
             sudhir.execute("select *  from employee where id = " +view_id +";")
             c=sudhir.fetchall()
             
             if len(c)!=0:
                 print(c)
             else:
                print("Enter valid details.")
                operation()
                
        else:
            print("Invalid access.")
        select()

    elif operation==3:
        if len(b)!=0:
            
            sudhir.execute("select * from emp_audit order by time desc;")
            d=sudhir.fetchall()
            if len(d)!=0:
                df = pd.DataFrame(d, columns=['ID', 'Time', 'Reg', 'Update'])
                
                print(df.to_string(index = False))
            else:
                print("No records found ")
        else:
            print("Invalid access.")
            select()

def login():
    log_id=int(input("Enter your ID: "))
    log_name=input("Enter your name: ")
    log_pwd=input("Enter your password: ")
    
    x = "select * from employee where id={} and name='{}' and password = '{}';"
    y = x.format(log_id,log_name,log_pwd)
    sudhir.execute(y)
    z=sudhir.fetchall()
    if len(z)!=0:
        print("Welcome {}.".format(log_name))
    else:
        print("Invalid credentials.")
        
def forgot_password():

    fp_id=input("Enter your ID: ")
    sudhir.execute("Select status from employee where id = "+fp_id +";")
    z = sudhir.fetchall()
    if z == 'active':
        fp_que=input("Enter your security question: ")
        fp_ans=input("Enter your answer: ")
        fp_newpwd=input("Enter your new password :")
        x = "select * from employee where id={} and secq='{}' and seca = '{}';"
        y = x.format(fp_id,fp_que,fp_ans)
        sudhir.execute(y)
        z=sudhir.fetchall()
        if len(z)!=0:
            temp="update employee set password ='{}' where id={} and secq='{}' and seca='{}';"
            f=temp.format(fp_newpwd,fp_id,fp_que,fp_ans)
            sudhir.execute(f) 
            print("Password changed successfully ")
            select()
        else:
            print("Invalid data")
            forgot_password()
    else:
        print("Inactive user.")
        select()
            
        
def select():
    print()
    select=int(input("1. Registration \n2. Login \n3. Update or View data \n4. Forgot password \n5. Exit \nSelect an option: "))
    if select ==1:
        registration()
    elif select ==2:
        login()
    elif select ==3:
        operations()
    elif select ==4:
        forgot_password()
    elif select == 5:
        print("Thank you.")
    else:
        print("give valid option ")
select()

conn.commit()        
        
sudhir.close()        

conn.close()