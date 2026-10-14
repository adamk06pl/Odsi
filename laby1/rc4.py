import sys
import math
import itertools
import time

def rc4_inicjalizacja(klucz: bytes) -> bytearray:
    #KSA
    s = bytearray(256)
    for i in range(256):
        s[i] = i

    j = 0
    dl_klucza = len(klucz)
    for i in range(256):
        j = (j + s[i] + klucz[i % dl_klucza]) % 256
        s[i], s[j] = s[j], s[i]
    return s

def rc4_szyfruj_odszyfruj(klucz: bytes, dane: bytes) -> bytes:
    #PRGA i XOR
    s = rc4_inicjalizacja(klucz)
    i = 0
    j = 0
    wynik = bytearray(len(dane))
    
    for idx, b in enumerate(dane):
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        k = s[(s[i] + s[j]) % 256] #Strumien klucza K
        wynik[idx] = b ^ k          #XOR M[i] ^ K[i]
        
    return bytes(wynik)

def oblicz_entropie(dane: bytes) -> float:
    if not dane:
        return 0.0
    entropia = 0.0
    dl = len(dane)
    liczniki = [0] * 256
    for b in dane:
        liczniki[b] += 1
    for count in liczniki:
        if count > 0:
            p = count / dl
            entropia -= p * math.log2(p)
    return entropia

def main():
    nazwa_pliku = "rc4.bin" if len(sys.argv) < 2 else sys.argv[1]
    
    try:
        with open(nazwa_pliku, "rb") as plik:
            kryptogram = plik.read()
    except FileNotFoundError:
        print(f"Nie znaleziono pliku {nazwa_pliku}!")
        return

    #Sprawdzam czy 2 razy ta sama funckcja z tym samym kluczem odtwarza wejscie
    test_klucz = b"abc"
    test_dane = b"Test RC4"
    zaszyfrowane_test = rc4_szyfruj_odszyfruj(test_klucz, test_dane)
    odszyfrowane_test = rc4_szyfruj_odszyfruj(test_klucz, zaszyfrowane_test)
    assert odszyfrowane_test == test_dane, "Blad odwracalnosci RC4!"
    print("Test dwukrotnego zastosowania RC4: OK")

    print("Rozpoczynanie przeszukiwania kluczy (3 male litery a-z)")
    start_czas = time.time()
    
    wyniki = []
    liczba_prob = 0
    
    #Sprawdzenie wszystkich kluczy (3 litery a-z)
    alfabet = "abcdefghijklmnopqrstuvwxyz"
    for k_tuple in itertools.product(alfabet, repeat=3):
        liczba_prob += 1
        klucz_str = "".join(k_tuple)
        klucz_bajty = klucz_str.encode("ascii")
        
        #Odszyfrowanie pierwszych 512bajtow do oceny entropii
        fragment = kryptogram[:512]
        odszyfrowany_fragment = rc4_szyfruj_odszyfruj(klucz_bajty, fragment)
        entropia = oblicz_entropie(odszyfrowany_fragment)
        
        wyniki.append((entropia, klucz_str, klucz_bajty))

    wyniki.sort(key=lambda x: (x[0], x[1]))
    
    koniec_czas = time.time()
    czas_trwania = koniec_czas - start_czas

    print(f"\nPrzeszukiwanie zakonczone w {czas_trwania:.2f} sekund. Liczba prob: {liczba_prob}")
    print("Top 5 kandydatow:")
    for i in range(5):
        ent, k_str, _ = wyniki[i]
        print(f"Miejsce {i+1}: Klucz={k_str}, Entropia={ent:.4f}")

    najlepsza_entropia, najlepszy_klucz_str, najlepszy_klucz_bajty = wyniki[0]
    print(f"\nWybrany automatycznie klucz: {najlepszy_klucz_str}")

    #Odszyfrowanie calego pliku od poczatku z nowym stanem
    caly_tekst = rc4_szyfruj_odszyfruj(najlepszy_klucz_bajty, kryptogram)
    
    ent_kryptogramu = oblicz_entropie(kryptogram)
    ent_odszyfrowania = oblicz_entropie(caly_tekst)
    print(f"Entropia calego kryptogramu: {ent_kryptogramu:.4f}")
    print(f"Entropia calego odszyfrowania: {ent_odszyfrowania:.4f}")

    with open("rc4.txt", "wb") as plik:
        plik.write(caly_tekst)
    print("Zapisano pelny odszyfrowany tekst do rc4.txt")

if __name__ == "__main__":
    main()