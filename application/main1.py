import smtplib
import mysql.connector as mysql
import random

mine_email = ""  # write your smtp email id which will be used to send otp
password = ""  # write your smtp password

server = smtplib.SMTP('smtp.gmail.com', 587)

server.starttls()

server.login(mine_email, password)

print("Press 1 if you want to save your password")
print("Press 2 if you want to retrieve your password")
choice = input("Enter your choice :-")
if choice == '1':
    with open("serial_number.txt", "r") as serial:
        serial_get = serial.read()
        print(serial_get)
        S_no_fake = int(float(serial_get))
        S_no = S_no_fake + 1
        serial.close()

    with open("serial_number.txt", "w") as serial:
        S_no = str(S_no)
        serial.write(S_no)
        serial.close()

    email_id = input("enter the email id :-")
    our_otp = str(random.randint(111111, 999999))

    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.starttls()

    server.login(mine_email, password)

    message = "Your otp is " + our_otp + ", Please don't share it to anyone"

    receiver_email = email_id
    server.sendmail(mine_email, receiver_email, message)
    print("Otp Send successfully")

    server.quit()
    user_otp = input("enter the otp :-")
    if user_otp == our_otp:
        print("User Login Successful :-")
        Name = input("enter the name :-")
        new_password = input("enter your password :-")
        password = new_password

        phone_number = input("enter the phone number :-")
        file = open("password.txt", "a")
        d = {password: new_password}
        file.write(str(d))

        sql_password = ""  # use your sql password to login to sql
        sql_database = ""  # write your sql database name

        mydb = mysql.connect(host="localhost", user="root", password=sql_password, database=sql_database)
        mycursor = mydb.cursor()
        data = (S_no, Name, password, email_id, phone_number)
        query = "insert into password_user values(%s,%s,%s,%s,%s)"
        mycursor.execute(query, data)
        mydb.commit()
        print("done")
    else:
        print("Incorrect otp")
        print("Try Again")
        exit()
else:
    print("You opted for retrieve ")
    our_otp = str(random.randint(111111, 999999))

    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.starttls()

    server.login(mine_email, password)

    message = "Your otp is " + our_otp + ", Please don't share it to anyone"

    receiver_email = input("enter receiver email address:- ")
    server.sendmail(mine_email, receiver_email, message)
    print("Otp Send successfully")

    server.quit()

    user_otp = input("Enter the otp :-")

    if user_otp == our_otp:
        print("User Login Successful")
        user_email = receiver_email
        sql_password = ""  # use your sql password to login to sql
        sql_database = ""  # write your sql database name
        mydb = mysql.connect(host="localhost", user="root", password=sql_password, database=sql_database)
        mycursor = mydb.cursor()
        query = "Select * from password_user"
        mycursor.execute(query)
        data = mycursor.fetchall()

        data_list = list(data)
        length = len(data_list)
        for i in range(length):
            if data_list[i][3] == user_email:
                user_password = data_list[i][2]
                message = "{} is your password linked to your email id".format(user_password)

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.starttls()

                server.login(mine_email, password)
                server.sendmail(mine_email, receiver_email, message)
                print("password(s) sent to your email id ")

                server.quit()

            else:
                print("Email id not found")
                print("Please try again!!")

    else:
        print("Wrong OTP")
print("Thanks for being here")
print("\U0001F60D")
