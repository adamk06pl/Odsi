import sys

def analizuj_tekst(dane):
    #Liczze bajty drukowalne (32-126) i biale
    poprawne_licznik = 0
    for bajt in dane:
        if 32 <= bajt <= 126 or bajt in (9, 10, 13):
            poprawne_licznik += 1
    return poprawne_licznik / len(dane) if dane else 0

def main():
    nazwa_pliku = "cezar.bin" if len(sys.argv) < 2 else sys.argv[1]
    
    try:
        with open(nazwa_pliku, "rb") as plik:
            kryptogram = plik.read()
    except FileNotFoundError:
        print(f"Nie znaleziono pliku {nazwa_pliku}!")
        return

    wyniki = []

    #Sprawdzenie wszystkich 256 przesunięć
    for k in range(256):
        #Odszyfrowanie p=(c-k)%256
        tekst_jawny_bajty = bytearray((c - k) % 256 for c in kryptogram)
        ocena = analizuj_tekst(tekst_jawny_bajty)
        wyniki.append((ocena, k, tekst_jawny_bajty))

    #Sortowanie wynikow
    wyniki.sort(key=lambda x: (-x[0], x[1]))

    print("Top 5 kandydatow:")
    for i in range(5):
        ocena, k, p_bytes = wyniki[i]
        print(f"Miejsce {i+1}: Klucz k={k}, Ocena ={ocena:.4f}")
        #Wypisuje poczatek odszyfrowania rzez repr()
        print(f"Poczatek: {repr(p_bytes[:50])}\n")
        if(i == 1):
            with open("cezar.txt", "wb") as plik:
                    plik.write(p_bytes)


    #najlepsza_ocena, najlepszy_klucz, najlepsze_bajty = wyniki[0]
    #print(f"Wybrano automatycznie najlepszy klucz: {najlepszy_klucz}")

    #Zapis do pliku odszyfrowania

    #with open("cezar.txt", "wb") as plik:
    #    plik.write(najlepsze_bajty)
    #print("Zapisano wynik do pliku cezar.txt")

if __name__ == "__main__":
    main()