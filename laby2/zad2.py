import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def doSzyfrowaniaPKCS7(dane):
    #dodawanie dopelnienia PKCS#7 do wielokrotnosci 16 bajtow
    dlugos_bloku = 16
    liczba_pad = dlugos_bloku - (len(dane) % dlugos_bloku)
    return dane + bytes([liczba_pad] * liczba_pad)

def doOdszyfrowaniaPKCS7(dane):
    #usuwanie dopelnienia PKCS#7
    liczba_pad = dane[-1]
    return dane[:-liczba_pad]

def wyprowadzKlucz(haslo_str, sol):
    #yprowadzenie klucza 32B za pomoca PBKDF2-HMAC-SHA256
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=sol,
        iterations=200000,
    )
    return kdf.derive(haslo_str.encode('utf-8'))

def szyfrujCBC(tekst_jawny, haslo_str, sol, iv):
    klucz = wyprowadzKlucz(haslo_str, sol)
    dane_uzupelnione = doSzyfrowaniaPKCS7(tekst_jawny)
    
    #szyfrowanie AES CBC
    szyfr = Cipher(algorithms.AES(klucz), modes.CBC(iv))
    szyfrator = szyfr.encryptor()
    kryptogram = szyfrator.update(dane_uzupelnione) + szyfrator.finalize()
    return kryptogram

def odszyfrujCBC(kryptogram, haslo_str, sol, iv):
    klucz = wyprowadzKlucz(haslo_str, sol)
    
    #odszyfrowanie AES CBC
    szyfr = Cipher(algorithms.AES(klucz), modes.CBC(iv))
    deszyfrator = szyfr.decryptor()
    dane_uzupelnione = deszyfrator.update(kryptogram) + deszyfrator.finalize()
    return doOdszyfrowaniaPKCS7(dane_uzupelnione)

def zad2():
    haslo = "PozdrawiamWszystkich"
    
    # przygotowanie danych testowych
    dane_puste = b""
    dane_16b = b"0123456789ABCDEF"
    
    #wiadomosc.txt
    try:
        with open("wiadomosc.txt", "rb") as plik:
            dane_plik = plik.read()
    except FileNotFoundError:
        dane_plik = b"Brak pliku wiadomosc.txt"
        
    testy = [
        ("Puste dane", dane_puste),
        ("16 bajtow ASCII", dane_16b),
        ("Plik wiadomosc.txt", dane_plik)
    ]
    
    print("--- WYNIKI TESTOW ---")
    
    # uruchomienie trzech testow
    for nazwa_testu, dane in testy:
        sol = os.urandom(16)
        iv = os.urandom(16)
        
        kryptogram = szyfrujCBC(dane, haslo, sol, iv)
        odszyfrowane = odszyfrujCBC(kryptogram, haslo, sol, iv)
        
        zgodne = (odszyfrowane == dane)
        print(f"Test: {nazwa_testu}")
        print(f"  Dlugos pierwotna: {len(dane)} B | Dlugos kryptogramu: {len(kryptogram)} B")
        print(f"  Zgodnosc bajtow przed i po: {zgodne}")
        
    # ponowne szyfrowanie tej samej wiadomosci z nowa sola i IV
    print("\n--- POROWNANIE KRYPTOGRAMOW (NOWA SOL I IV) ---")
    wiadomosc_testowa = b"Bardzo pozdrawiam SOL i IV."
    
    sol_1 = os.urandom(16)
    iv_1 = os.urandom(16)
    kryptogram_1 = szyfrujCBC(wiadomosc_testowa, haslo, sol_1, iv_1)
    
    sol_2 = os.urandom(16)
    iv_2 = os.urandom(16)
    kryptogram_2 = szyfrujCBC(wiadomosc_testowa, haslo, sol_2, iv_2)
    
    print(f"Kryptogram 1 (hex): {kryptogram_1.hex()}")
    print(f"Kryptogram 2 (hex): {kryptogram_2.hex()}")
    print(f"Czy kryptogramy sa identyczne: {kryptogram_1 == kryptogram_2}")

if __name__ == "__main__":
    zad2()