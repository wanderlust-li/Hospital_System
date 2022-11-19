import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "hospitalnau"
)

mycursor = mydb.cursor(buffered = True)

def LoginToTheSystem():
    mycursor.execute("USE hospitalnau")

    try:
        count = 0
        while(count < 3):
            login_name = input("Введіть ім'я користувача: ")
            login_surname = input("Введіть фамілію: ")
            check_name = f"SELECT name FROM patients WHERE name = '{login_name}'"
            check_surname = f"SELECT surname FROM patients WHERE surname = '{login_surname}'"
            temp_name = False; temp_surname = False # для звичайного користувача
            temp_admin_name = False; temp_admin_surname = False # для адміна 
            

            mycursor.execute(check_name)
            name_result = mycursor.fetchall()
            for i in name_result: # перевіряємо ім'я
                if login_name in i:
                    temp_name = True
                if "admin" in i:
                    temp_name = False
                    temp_admin_name = True

            mycursor.execute(check_surname)
            surname_result = mycursor.fetchall()
            for j in surname_result: # перевіряємо фамілію
                if login_surname in j:
                    temp_surname = True
                if "admin" in j:
                    temp_surname = False
                    temp_admin_surname = True

            if temp_admin_name and temp_admin_surname:
                choose = int(input("\nЯкщо ви хочете подивитись всiх користувачiв, натисність '1'.\nЯкщо ви хочете видалити користувача, натисніть '2'.\nДля завершення програми, натисність '0'.\n"))

                if choose == 1:
                    mycursor.execute("SELECT * FROM patients")
                    result = mycursor.fetchall()
                    for i in result:
                        print(i)
                elif choose == 2:
                    DeleteUser()
                elif choose == 0:
                    exit(1)
                    
                break
            
            if temp_name and temp_surname: 
                mycursor.execute(f"SELECT * FROM patients WHERE name ='{login_name}' AND surname = '{login_surname}'")
                result = mycursor.fetchall()
                print("\nВітаю, ви увійшли в систему!\n")
                for i in result:
                    print(f"Дані про пацієнта: {i}")
                break

            elif (count < 2):
                print("У доступі відхилено.")
                count += 1

            elif(count == 2):
                print("Доступ заблоковано. Завершення програми")
                break

    except Exception as error:
        print("Не вдалося підключитися.")
        print(f"Головна помилка: {error}")


def RegisterUser():
    mycursor.execute("USE hospitalnau")
    new_name = input("Введіть ім'я: ")
    new_surname = input("Введіть фамілію: ")
    new_health = input("Введіть стань пацієнта 'лікар': ")
    new_disease = input("Введіть хворобу пацієнта 'лікар': ")

    insert_new_user = "INSERT INTO patients (name, surname, health, disease) VALUES (%s, %s, %s, %s)"
    new_user = (new_name, new_surname, new_health, new_disease)

    mycursor.execute(insert_new_user, new_user)

    mydb.commit()
    print("Користувача успішно створено! ")


def DeleteUser(): # видалити користувача
    try:
        mycursor = mydb.cursor()

        delete_name = input("Введіть ім'я: ")
        delete_surname = input("Введіть фамілію: ")
        if (delete_name != "admin" and delete_surname != "admin"):
            delete_user = f"DELETE FROM patients WHERE name = '{delete_name}' AND surname = '{delete_surname}'"
            
            
            temp_name = False; temp_surname = False
            check_name = f"SELECT name FROM patients WHERE name = '{delete_name}'"
            check_surname = f"SELECT surname FROM patients WHERE surname = '{delete_surname}'"
            mycursor.execute(check_name)
            name_result = mycursor.fetchall()
            for i in name_result: # перевіряємо ім'я
                if delete_name in i:
                    temp_name = True

            mycursor.execute(check_surname)
            surname_result = mycursor.fetchall()
            for j in surname_result: # перевіряємо фамілію
                if delete_surname in j:
                    temp_surname = True

            if (temp_name and temp_surname):
                print("Користувача успішно видалено!")
            else:
                print("Такого користувача не існує!")

            mycursor.execute(delete_user)

            mydb.commit()
        else:
            print("Адміна видалити неможливо!")

    except:
        print("Виникла помилка, спробуйте ще раз!")


def Options():
    print("1: Вхід\n2: Реєстрація\n3: Завершення програми\n")
    choose = int(input("Оберіть, що вам потрібно: 1, 2 або 3: "))

    if choose == 1:
        LoginToTheSystem()
    elif choose == 2:
        RegisterUser()
    elif choose == 3:
        print("Бережіть себе!")
    else: 
        print("Такої функції не знайдено! Будь ласка, спробуйте ще раз!")
        Options()

Options()