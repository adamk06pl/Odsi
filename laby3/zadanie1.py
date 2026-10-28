import hashlib
import os

#funkcja liczaca SHA-256 pliku
def oblicz_sha256(sciezka):
    hasher = hashlib.sha256()
    with open(sciezka, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

#weryfikacja sum kontrolnych ze struktury pliki-dla-studentow
plik_sum = 'pliki-dla-studentow/SHA256SUMS.txt'

if os.path.exists(plik_sum):
    with open(plik_sum, 'r', encoding='utf-8') as f:
        for linia in f:
            linia = linia.strip()
            if not linia:
                continue
            czesci = linia.split('  ')
            if len(czesci) >= 2:
                oczekiwany_skrot = czesci[0]
                rel_sciezka = czesci[1]
                
                # Skladanie sciezki wzgledem folderu pliki-dla-studentow
                pelna_sciezka = os.path.join('pliki-dla-studentow', rel_sciezka)
                
                if os.path.exists(pelna_sciezka):
                    aktualny_skrot = oblicz_sha256(pelna_sciezka)
                    if aktualny_skrot == oczekiwany_skrot:
                        print(f"{rel_sciezka}: OK")
                    else:
                        print(f"{rel_sciezka}: BLAD")
                else:
                    print(f"{rel_sciezka}: BRAK")
else:
    print("Brak pliku SHA256SUMS.txt")

#porownanie tekstow ASCII
tekst1 = b"Ala ma kota."
tekst2 = b"Ola ma kota."

skrot1 = hashlib.sha256(tekst1).digest()
skrot2 = hashlib.sha256(tekst2).digest()

roznice_bitowe = sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(skrot1, skrot2))
print(f"Liczba roznicujacych sie bitow: {roznice_bitowe}")