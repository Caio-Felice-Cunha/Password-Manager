import sys
import os
from pathlib import Path
import json
from datetime import datetime

sys.path.append(os.path.abspath(os.curdir))

from model.password import Password
from views.password_views import FernetHasher

def save_password(fernet_user):
    domain = input('Domain: ').strip()
    
    # Ask if user wants to generate a password
    gen_pass = input('Generate password automatically? (y/n): ').lower().strip() == 'y'
    
    if gen_pass:
        length = int(input('Password length (minimum 8): ').strip())
        password = Password.generate_password(length=length)
        print(f'Generated password: {password}')
    else:
        password = input('Enter password: ').strip()
        
        if not Password.validate_password(password):
            print("Password too weak! Must contain uppercase, lowercase, numbers and special characters.")
            return

    notes = input('Notes (optional): ').strip()
    
    encrypted_password = fernet_user.encrypt(password).decode('utf-8')
    password_entry = Password(domain=domain, password=encrypted_password, notes=notes)
    password_entry.save()
    print("Password saved successfully!")

def get_password(fernet_user):
    domain = input('Domain: ').strip()
    data = Password.get()
    
    for entry in data:
        if domain.lower() in entry['domain'].lower():
            try:
                decrypted = fernet_user.decrypt(entry['password'].encode())
                print(f'\nDomain: {entry["domain"]}')
                print(f'Password: {decrypted.decode()}')
                if entry.get('notes'):
                    print(f'Notes: {entry["notes"]}')
                print(f'Created at: {entry["created_at"]}')
                return
            except Exception as e:
                print(f"Error decrypting: {e}")
    
    print('No password found for this domain.')

def list_domains():
    domains = Password.list_domains()
    if not domains:
        print("No domains found.")
        return
    
    print("\nSaved domains:")
    for domain in domains:
        print(f"- {domain}")

def delete_password():
    domain = input('Enter domain to delete: ').strip()
    if Password.delete(domain):
        print(f"Password for {domain} deleted successfully!")
    else:
        print(f"Domain {domain} not found.")

def backup_passwords():
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)
    
    backup_file = backup_dir / f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    data = Password.get()
    with open(backup_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Backup created in: {backup_file}")

def main():
    while True:
        print("\n=== Password Manager ===")
        print("1. Save new password")
        print("2. Retrieve password")
        print("3. List domains")
        print("4. Delete password")
        print("5. Create backup")
        print("6. Exit")
        
        action = input('\nChoose an option: ').strip()
        
        if action == '6':
            break
            
        if action not in ('1', '2', '3', '4', '5'):
            print("Invalid option!")
            continue
            
        try:
            if action == '3':
                list_domains()
                continue
                
            if action == '4':
                delete_password()
                continue
                
            if action == '5':
                backup_passwords()
                continue

            passwords = Password.get()
            if action == '1' and not passwords:
                key, path = FernetHasher.create_key(archive=True)
                print('Your key has been created, save it carefully!')
                print(f'Key: {key.decode("utf-8")}')
                if path:
                    print(f'Key saved in: {path}')
                fernet_user = FernetHasher(key)
            else:
                key = input('Enter your encryption key: ').strip()
                fernet_user = FernetHasher(key)
            
            if action == '1':
                save_password(fernet_user)
            elif action == '2':
                get_password(fernet_user)
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()