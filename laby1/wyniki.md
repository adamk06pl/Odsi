# wyniki 1
**Autor:** Adam Kun

## Zadanie 1 - Cezar

Przesunięcie k = 233. 

Wybór najsensowniejszych tekstów na podstawie odsetku wypisywalnych znaków ASCII, pośród których znalazł się ten faktycznie mający sens.

Szyfr cezara tylko przesuwa bajty, ale ich nie miesza ani nie zmienia ich liczby. Ponieważ unikalne bajty występują dokładnie z tą samą częstotliwością (zmienia się tylko ich pozycja w tabeli), histogram i entropia całego pliku pozostają identyczne dla każdego klucza. Dlatego sama entropia nie wskaże, które przesunięcie daje poprawny tekst.

## Zadanie 2 - Vigenere

Kryptogramy dla ciągów:

- Klucz "SZYFR" - 95ac9a9393   95ac9a9393   95ac9a9393

- Klucz "KOD" - 8da1859890   869d90918c   91968c9c85

Powtarzalność fragmentów:

Powtarzalność fragmentów w kryptogramie zależy od relacji między długością powtarzalnego wzorca w tekście jawnym a długością klucza. Jeśli okres powtarzania tekstu dzieli się przez długość klucza (lub odwrotnie), te same znaki trafiają na te same bajty klucza, tworząc identyczne fragmenty w kryptogramie. Gdy długości te są niezgrane, wzorce w tekście jawnym przesuwają się względem klucza, przez co kryptogram wygląda bardziej losowo i powtórzenia nie są widoczne w ten sam sposób.

## Zadanie 3 - RC4
Odnaleziony klucz: tat   


Ranking 5 najlepszych kandydatów:   


Klucz=tat, Entropia=4.3910   


Klucz=neg, Entropia=7.4304   


Klucz=mcn, Entropia=7.4512   


Klucz=oxo, Entropia=7.4536   

Klucz=tnx, Entropia=7.4592   

Statystyki testu:

Liczba prób: 17576

Czas przeszukiwania: 3.61 s

Entropia całego kryptogramu: 7.9271

Entropia całego odszyfrowania: 4.3259   


Wyjaśnienia:

Dlaczego ponowne szyfrowanie może odtworzyć kryptogram również dla błędnego klucza? Operacja XOR jest odwracalna dla każdego strumienia pseudolosowego. Użycie błędnego klucza wygeneruje inny strumień i da jakiś wynik, jednak nie będzie on czytelnym tekstem w naturalnym języku.   

Kiedy ranking entropii mógłby zawieść? Ranking oparty na minimalnej entropii mógłby zawieść, jeśli oryginaly tekst przed zaszyfrowaniem miałby nienaturalnie wysoką entropię (np. byłby silnie skompresowany) lub gdyby błędny klucz przypadkowo odszyfrował dane do powtarzalnego, monotonnego ciągu o niskiej entropii.