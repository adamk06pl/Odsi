import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def zad1():
    #przygotowanie 64 bajtów
    tekst_wzorzec = b"0123456789ABCDEF"
    dane_wejsciowe = tekst_wzorzec * 4
    
    #klucz AES-128
    klucz = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    
    print(f"Dane wejsciowe ({len(dane_wejsciowe)} bajtow):")
    print(dane_wejsciowe)
    print("-" * 50)
    
     # ECB Wylaczam automatyczne dopelnienie
    szyfr_ecb = Cipher(algorithms.AES(klucz), modes.ECB())
    szyfrator_ecb = szyfr_ecb.encryptor()
    kryptogram_ecb = szyfrator_ecb.update(dane_wejsciowe) + szyfrator_ecb.finalize()
    
    # CBC losuje IV 16 bajt
    iv = os.urandom(16)
    szyfr_cbc = Cipher(algorithms.AES(klucz), modes.CBC(iv))
    szyfrator_cbc = szyfr_cbc.encryptor()
    kryptogram_cbc = szyfrator_cbc.update(dane_wejsciowe) + szyfrator_cbc.finalize()
    
    #wypisanie czterech 16bajt blokow kazdego kryptogramu
    bloki_ecb = [kryptogram_ecb[i:i+16] for i in range(0, len(kryptogram_ecb), 16)]
    bloki_cbc = [kryptogram_cbc[i:i+16] for i in range(0, len(kryptogram_cbc), 16)]
    
    print("Kryptogram ECB w blokach (hex):")
    for idx, blok in enumerate(bloki_ecb):
        print(f"Blok {idx+1}: {blok.hex()}")
        
    print("\nKryptogram CBC w blokach (hex):")
    for idx, blok in enumerate(bloki_cbc):
        print(f"Blok {idx+1}: {blok.hex()}")
        
    print("-" * 50)
    
    # ktore bloki powtarzaja sie w kryptogramach
    unikalne_ecb = len(set(bloki_ecb))
    unikalne_cbc = len(set(bloki_cbc))
    
    print(f"Liczba unikalnych blokow w ECB: {unikalne_ecb} (z 4)")
    print(f"Liczba unikalnych blokow w CBC: {unikalne_cbc} (z 4)")
    
    #odszyfrowanie
    deszyfrator_ecb = szyfr_ecb.decryptor()
    odszyfrowane_ecb = deszyfrator_ecb.update(kryptogram_ecb) + deszyfrator_ecb.finalize()
    
    deszyfrator_cbc = Cipher(algorithms.AES(klucz), modes.CBC(iv)).decryptor()
    odszyfrowane_cbc = deszyfrator_cbc.update(kryptogram_cbc) + deszyfrator_cbc.finalize()
    
    #prownanie bajtow z wejsciem
    zgodne_ecb = (odszyfrowane_ecb == dane_wejsciowe)
    zgodne_cbc = (odszyfrowane_cbc == dane_wejsciowe)
    
    print("-" * 50)
    print(f"Odszyfrowane ECB zgadza sie z wejsciem: {zgodne_ecb}")
    print(f"Odszyfrowane CBC zgadza sie z wejsciem: {zgodne_cbc}")

if __name__ == "__main__":
    zad1()