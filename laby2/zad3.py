import math
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def oblicz_entropie(dane):
    dlugos = len(dane)
    if dlugos == 0:
        return 0.0
    
    #zliczanie czestotliwosci wystepowania kazdego bajtu
    czestotliwosci = {}
    for bajt in dane:
        czestotliwosci[bajt] = czestotliwosci.get(bajt, 0) + 1
        
    entropia = 0.0
    for licznik in czestotliwosci.values():
        p = licznik / dlugos
        if p > 0:
            entropia -= p * math.log2(p)
            
    return entropia

def doOdszyfrowaniaPKCS7(dane):
    # usuwanie dopelnienia PKCS#7
    liczba_pad = dane[-1]
    return dane[:-liczba_pad]

def zad3():
    nazwa_pliku = "slaby_ecb.bin"

    try:
        with open(nazwa_pliku, "rb") as plik:
            kryptogram = plik.read()
    except FileNotFoundError:
        print(f"Brak pliku {nazwa_pliku} w folderze!")
        return
        
    # pierwsze 4096 bajtow do analizy entropii
    probka = kryptogram[:4096]
    
    # 36 mozliwosci
    alfabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    wyniki = []
    
    print("--- SPRAWDZANIE SLABYCH KLUCZY ---")
    for znak in alfabet:
        #klucz to 16 kopii jednego znaku ASCII
        klucz = (znak * 16).encode('ascii')
        
        # AES ECB bez usuwania dopelnienia
        szyfr = Cipher(algorithms.AES(klucz), modes.ECB())
        deszyfrator = szyfr.decryptor()
        
        try:
            odszyfrowane_probka = deszyfrator.update(probka) + deszyfrator.finalize()
            entropia = oblicz_entropie(odszyfrowane_probka)
            wyniki.append((znak, entropia, klucz))
        except Exception:
            continue
            
    # sortowanie rosnaco wedlug entropii H
    wyniki.sort(key=lambda x: x[1])
    
    print("Top 5 najlepszych kandydatow:")
    for i in range(min(5, len(wyniki))):
        znak, entropia, _ = wyniki[i]
        print(f"{i+1}. Znak klucza: '{znak}' | Entropia H: {entropia:.4f}")
        
    # najlepszy klucz (z najmniejsza entropia)
    najlepszy_znak, _, najlepszy_klucz = wyniki[0]
    print(f"\nNajlepszy odzyskany znak klucza: '{najlepszy_znak}'")
    
    # odszyfrowanie calego pliku najlepszym kluczem
    szyfr_pelny = Cipher(algorithms.AES(najlepszy_klucz), modes.ECB())
    deszyfrator_pelny = szyfr_pelny.decryptor()
    odszyfrowane_pelne_z_pad = deszyfrator_pelny.update(kryptogram) + deszyfrator_pelny.finalize()
    
    # usuniecie PKCS#7 i odzyskanie czytelnego tekstu
    odszyfrowane_pelne = doOdszyfrowaniaPKCS7(odszyfrowane_pelne_z_pad)
    
    # pobranie pierwszego wiersza tekstu
    linie = odszyfrowane_pelne.splitlines()
    pierwszy_wiersz = linie[0].decode('utf-8', errors='ignore') if linie else ""
    
    print(f"Pierwszy wiersz tekstu: {pierwszy_wiersz}")

if __name__ == "__main__":
    zad3()