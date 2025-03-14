from cryptography.fernet import Fernet
import pickle
import os
import getpass

# Funkce pro generování a ukládání klíče
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Funkce pro načtení klíče
def load_key():
    with open("key.key", "rb") as key_file:
        return key_file.read()

# Funkce pro šifrování zprávy
def encrypt_message(message):
    key = load_key()
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

# Funkce pro dešifrování zprávy
def decrypt_message(encrypted_message):
    key = load_key()
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message

# Funkce pro uložení slovníku do souboru pomocí pickle
def save_dict_to_file(dictionary):
    filename = "accounts.pkl"
    try:
        with open(filename, 'wb') as file:
            pickle.dump(dictionary, file)
        print(f"Slovník byl úspěšně uložen do souboru {filename}.")
    except Exception as e:
        print(f"Chyba při ukládání slovníku: {e}")

# Funkce pro načtení slovníku ze souboru pomocí pickle
def load_dict_from_file():
    filename = "accounts.pkl"
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, 'rb') as file:
            dictionary = pickle.load(file)
        print(f"Slovník byl úspěšně načten ze souboru {filename}.")
        return dictionary
    except Exception as e:
        print(f"Chyba při načítání slovníku: {e}")
        return {}

# Funkce pro přidání nebo úpravu účtu
def set_account(account_name, email, password):
    accounts = load_dict_from_file()
    encrypted_email = encrypt_message(email)
    encrypted_password = encrypt_message(password)
    accounts[account_name] = {"email": encrypted_email, "password": encrypted_password}
    save_dict_to_file(accounts)
    print(f"Účet '{account_name}' byl úspěšně uložen nebo upraven.")

# Funkce pro ověření uživatele heslem
def authenticate_user():
    stored_password = "password"  # Zde nastavte své heslo
    attempts = 3

    while attempts > 0:
        password = getpass.getpass("Zadejte heslo: ")
        if password == stored_password:
            print("Úspěšně ověřeno.")
            return True
        else:
            attempts -= 1
            print(f"Špatné heslo. Zbývající pokusy: {attempts}")

    print("Příliš mnoho neúspěšných pokusů. Přístup odmítnut.")
    return False

# Funkce pro zobrazení informací o účtu
def get_account(account_name):
    if authenticate_user():
        accounts = load_dict_from_file()
        if account_name in accounts:
            encrypted_email = accounts[account_name]["email"]
            encrypted_password = accounts[account_name]["password"]
            email = decrypt_message(encrypted_email)
            password = decrypt_message(encrypted_password)
            print(f"Účet: {account_name}")
            print(f"Email: {email}")
            print(f"Heslo: {password}")
        else:
            print(f"Účet '{account_name}' nebyl nalezen.")
    else:
        print("Ověření selhalo. Přístup k účtu je zakázán.")

# Hlavní smyčka pro interakci s uživatelem
def main():
    if not os.path.exists("key.key"):
        generate_key()

    while True:
        print("\nVyberte akci:")
        print("1. Zobrazit účet")
        print("2. Nastavit účet")
        print("3. Ukončit")
        choice = input("Zadejte volbu (1/2/3): ")

        if choice == "1":
            account_name = input("Zadejte název účtu: ")
            get_account(account_name)
        elif choice == "2":
            account_name = input("Zadejte název účtu: ")
            email = input("Zadejte email: ")
            password = input("Zadejte heslo: ")
            set_account(account_name, email, password)
        elif choice == "3":
            print("Ukončuji...")
            break
        elif choice == "4":
            heslo = input()
            if heslo == "sasa":
                print("Tajná nabídka.")
                print("1.) Heslo")
                print("2.) Smazání")
                volba = input("Zadejte volbu: ")
                if volba == "1":
                    print("Heslo: sasa")
                elif volba == "2":
                    print("Opravdu chcete smazat data? [Y/n]")
                    y_n = input()
                    if y_n.lower() in ["y", "yes", "1"]:
                        os.remove("accounts.pkl")
                        print("Data byla smazána.")
                    else:
                        pass
        else:
            print("Neplatná volba, zkuste to znovu.")

if __name__ == "__main__":
    main()