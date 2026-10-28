import hashlib
import hmac
import os

# Ścieżka do bazy haseł zgodna z Twoją strukturą katalogów
PLIK_HASEL = 'pliki-dla-studentow/hasla.txt'
if not os.path.exists(PLIK_HASEL):
    PLIK_HASEL = 'hasla.txt' # fallback gdyby był w tym samym folderze

def weryfikuj(login, haslo):
    if not os.path.exists(PLIK_HASEL):
        return False
    with open(PLIK_HASEL, 'r', encoding='utf-8') as f:
        for linia in f:
            parts = linia.strip().split(':')
            if len(parts) != 4:
                continue
            db_login, db_iter, db_sol_hex, db_skrot_hex = parts
            if db_login == login:
                iteracje = int(db_iter)
                sol = bytes.fromhex(db_sol_hex)
                zapisany_skrot = bytes.fromhex(db_skrot_hex)
                
                wyliczony_skrot = hashlib.pbkdf2_hmac(
                    'sha256',
                    haslo.encode('utf-8'),
                    sol,
                    iteracje,
                    dklen=32
                )
                return hmac.compare_digest(wyliczony_skrot, zapisany_skrot)
    return False

# 1. Sprawdzenie czterech przypadków (zwróć uwagę na dokładne polskie znaki!)
print("anna, Kasztan-2026:", weryfikuj("anna", "Kasztan-2026"))
print("anna, kasztan-2026:", weryfikuj("anna", "kasztan-2026"))
print("piotr, Żółw na łące:", weryfikuj("piotr", "Żółw na łące"))
print("kasia, Kasztan-2026:", weryfikuj("kasia", "Kasztan-2026"))

# 2. Funkcja dodaj
def dodaj(login, haslo):
    sol = os.urandom(16)
    iteracje = 600000
    skrot = hashlib.pbkdf2_hmac(
        'sha256',
        haslo.encode('utf-8'),
        sol,
        iteracje,
        dklen=32
    )
    return {
        'login': login,
        'iteracje': iteracje,
        'sol': sol.hex(),
        'skrot': skrot.hex()
    }

konto1 = dodaj("test1", "MojeHaslo123")
konto2 = dodaj("test2", "MojeHaslo123")

print("\n--- Nowe konta ---")
print("Konto 1 sol:", konto1['sol'])
print("Konto 2 sol:", konto2['sol'])
print("Konto 1 skrot:", konto1['skrot'])
print("Konto 2 skrot:", konto2['skrot'])
print("Sole są równe:", konto1['sol'] == konto2['sol'])
print("Skróty są równe:", konto1['skrot'] == konto2['skrot'])