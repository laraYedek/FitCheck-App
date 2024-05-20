import customtkinter
import psycopg2
import bcrypt
from PyQt5.QtWidgets import QApplication, QWidget
from psycopg2 import OperationalError
from MainPage import FitCheckApp

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = None  # Initialize app globally

def main():
    global app
    app = QApplication([])  # Create QApplication here

    root = customtkinter.CTk()
    root.geometry("500x350")

    db_name = "FitCheck"
    db_user = "postgres"
    db_password = "123123"
    db_host = "localhost"
    db_port = "5432"

    connection = create_connection(db_name, db_user, db_password, db_host, db_port)

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame, text="FitCheck Hesabınıza Giriş Yapın")
    label.pack(pady=12, padx=10)

    entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="E-mail")
    entry1.pack(pady=12, padx=10)

    entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Şifre", show="*")
    entry2.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(master=frame, text="Giriş Yap", command=lambda: login(root, entry1, entry2, connection))
    button.pack(pady=12, padx=10)

    label = customtkinter.CTkLabel(master=frame, text="FitCheck hesabınız yoksa lütfen web sitemiz üzerinden üye olun.")
    label.pack(pady=10, padx=8)

    error_label = customtkinter.CTkLabel(master=frame, text="", fg_color="red")
    
    root.mainloop()

def create_connection(db_name, db_user, db_password, db_host, db_port):
    try:
        return psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
    except OperationalError as e:
        print(f"Hata oluştu: '{e}'")
        return None

def login(root, entry1, entry2, connection):
    user_mail = entry1.get()
    user_sifre = entry2.get().encode()
    success, result = validate_user(user_mail, user_sifre, connection)

    if success:
        root.destroy()  # Close the login window
        mainWindow = FitCheckApp(result)  # Initialize your main application window
        mainWindow.show()
        app.exec_()  # Start the QApplication event loop

def validate_user(mail, sifre, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT sifre FROM kullanicilar WHERE mail = %s;", (mail,))
    result = cursor.fetchone()
    cursor.close()
    
    if result:
        hashed_sifre = result[0]
        return (bcrypt.checkpw(sifre, hashed_sifre.encode('utf-8')), mail) if bcrypt.checkpw(sifre, hashed_sifre.encode('utf-8')) else (False, "Şifre yanlış")
    return False, "Bu mail adresiyle bir kullanıcı bulunmuyor"

if __name__ == '__main__':
    main()
