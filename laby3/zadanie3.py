import hashlib

#funkcja liczaca h24 (pierwsze 3 bajty SHA-256 jako hex)
def h24(dane):
    skrot = hashlib.sha256(dane).digest()
    return skrot[:3].hex()

with open('pliki-dla-studentow/oryginal.txt', 'rb') as f:
    oryginalne_wiersze = f.readlines()

with open('pliki-dla-studentow/zmieniony.txt', 'rb') as f:
    zmienione_wiersze = f.readlines()

#funkcja generujaca wariant v dla zestawu wierszy
def generuj_wariant(wiersze, v):
    nowe_wiersze = []
    for i, wiersz in enumerate(wiersze):
        tresc = wiersz[:-1]
        koniec = wiersz[-1:]
        #dopisuje spacje przed \n, jesli i-ty bit w v wynosi 1
        if (v >> i) & 1:
            nowe_wiersze.append(tresc + b' ' + koniec)
        else:
            nowe_wiersze.append(wiersz)
    return b''.join(nowe_wiersze)

#obliczenie h24 dla wszystkich 8192 wariantow oryginalu
slownik_oryginalow = {}
for v in range(8192):
    dane = generuj_wariant(oryginalne_wiersze, v)
    skrot = h24(dane)
    if skrot not in slownik_oryginalow:
        slownik_oryginalow[skrot] = v

#przeglądanie wariantów zmienionego dokumentu i znalezienie pierwszej kolizji
znaleziona_para = None
for v_zmieniony in range(8192):
    dane = generuj_wariant(zmienione_wiersze, v_zmieniony)
    skrot = h24(dane)
    
    if skrot in slownik_oryginalow:
        v_oryginal = slownik_oryginalow[skrot]
        znaleziona_para = (v_oryginal, v_zmieniony, skrot)
        print(f"Znaleziona para -> v_oryginal: {v_oryginal}, v_zmieniony: {v_zmieniony}, h24: {skrot}")
        break

#sprawdzenie wszystkich 8192 wariantów zmienionego dokumentu z h24 oryginału (wariant 0)
dane_oryginal_0 = generuj_wariant(oryginalne_wiersze, 0)
h24_bazowy = h24(dane_oryginal_0)

licznik_trafien = 0
for v_zmieniony in range(8192):
    dane = generuj_wariant(zmienione_wiersze, v_zmieniony)
    if h24(dane) == h24_bazowy:
        licznik_trafien += 1

print(f"Liczba trafien z h24 wariantu 0: {licznik_trafien}")