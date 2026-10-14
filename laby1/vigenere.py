def vigenere_szyfruj(tekst_jawny: bytes, klucz: bytes) -> bytes:
    if not klucz:
        return tekst_jawny
    kryptogram = bytearray()
    dl_klucza = len(klucz)
    for i, p in enumerate(tekst_jawny):
        c = (p + klucz[i % dl_klucza]) % 256
        kryptogram.append(c)
    return bytes(kryptogram)

def vigenere_odszyfruj(kryptogram: bytes, klucz: bytes) -> bytes:
    if not klucz:
        return kryptogram
    tekst_jawny = bytearray()
    dl_klucza = len(klucz)
    for i, c in enumerate(kryptogram):
        p = (c - klucz[i % dl_klucza]) % 256
        tekst_jawny.append(p)
    return bytes(tekst_jawny)

def main():
    #Test z plikiem tekst_pl.txt i kluczem ZAMEK
    klucz = b"ZAMEK"
    try:
        with open("tekst_pl.txt", "rb") as f:
            dane_zrodlowe = f.read()
    except FileNotFoundError:
        dane_zrodlowe = b"Przykladowy tekst testowy."

    zaszyfrowane = vigenere_szyfruj(dane_zrodlowe, klucz)
    odszyfrowane = vigenere_odszyfruj(zaszyfrowane, klucz)

    #prawdzam zgodnosci bajt po bajcie
    assert dane_zrodlowe == odszyfrowane, "Blad odszyfrowania!"
    print("Test pliku tekst_pl.txt: OK (zgodnosc bajt po bajcie)")

    with open("vigenere.bin", "wb") as f:
        f.write(zaszyfrowane)

    #Sprawdzam puste dane oraz bajty 0 i 255
    assert vigenere_odszyfruj(vigenere_szyfruj(b"", klucz), klucz) == b""
    dane_brzegowe = bytes([0, 255, 128])
    assert vigenere_odszyfruj(vigenere_szyfruj(dane_brzegowe, klucz), klucz) == dane_brzegowe
    print("Testy brzegowe (puste dane, 0, 255): OK")

    wiadomosc = b"BRAMABRAMABRAMA"
    for k_str in ["SZYFR", "KOD"]:
        k_bajty = k_str.encode("ascii")
        zasz = vigenere_szyfruj(wiadomosc, k_bajty)
        hex_str = zasz.hex()
        #Podzial na trzy fragmenty po 5 bajtow 1b=2hex
        fragmenty = [hex_str[j:j+10] for j in range(0, len(hex_str), 10)]
        print(f"Klucz {k_str}: " + " | ".join(fragmenty))

if __name__ == "__main__":
    main()