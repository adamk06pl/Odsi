# Wyniki lab 3
**Autor:** Adam Kun

## Zadanie 1 - ECB i CBC

Obserwacje zachowania równych bloków w obu trybach:
- W trybie ECB wszystkie cztery bloki kryptogramu są ze sobą identyczne.
- W trybie CBC wszystkie cztery bloki kryptogramu różnią się między sobą.

Wyniki weryfikacji po odszyfrowaniu:
- Odszyfrowane bajty w trybie ECB zgadzają się z wejściem: `True`
- Odszyfrowane bajty w trybie CBC zgadzają się z wejściem: `True`

Wyjaśnienie obserwacji:
Identyczne bloki wejściowe w trybie ECB ujawniają powtarzający się wzorzec strukturalny bezpośrednio w szyfrogramie. Z kolei tryb CBC całkowicie ukrywa te powtórzenia dzięki kaskadowemu wiązaniu sąsiednich bloków oraz zastosowaniu unikalnego wektora inicjalizującego (IV).

## Zadanie 2 - Szyfrowanie z hasłem

Wyniki testów i długości kryptogramów (z uwzględnieniem dopełnienia PKCS#7):
- Puste dane: długość pierwotna 0 B, kryptogram 16 B, zgodność bajtów: `True`
- 16 bajtów ASCII: długość pierwotna 16 B, kryptogram 32 B, zgodność bajtów: `True`
- Plik wiadomosc.txt: długość pierwotna 247 B, kryptogram 256 B, zgodność bajtów: `True`

Porównanie szyfrowań (nowa sól i IV):
Szyfrowanie tej samej wiadomości przy użyciu tego samego hasła, ale z nową solą i nowym wektorem IV daje całkowicie odmienne kryptogramy (identyczność: `False`).

Różnica między solą a IV:
- **Sól** służy do losowej modyfikacji wyprowadzanego klucza kryptograficznego, co zabezpiecza przed atakami słownikowymi i tablicami tęczowymi.
- **IV (wektor inicjalizujący)** losuje początkowy stan łańcucha bloków w trybie CBC, dzięki czemu ten sam tekst jawny zaszyfrowany tym samym kluczem za każdym razem wygląda zupełnie inaczej.

## Zadanie 3 - Odzyskanie słabego klucza

Ranking 5 najlepszych kandydatów:
1. Znak klucza: 'm' | Entropia H: 4.4536
2. Znak klucza: 'b' | Entropia H: 7.9472
3. Znak klucza: 'x' | Entropia H: 7.9490
4. Znak klucza: 'o' | Entropia H: 7.9493
5. Znak klucza: '2' | Entropia H: 7.9502

- **Odzyskany znak klucza:** `m`
- **Pierwszy wiersz tekstu:** `Record 000. The archive contains laboratory notes about symmetric encryption and careful handling of binary files.`

Wyjaśnienia:
- **Dlaczego jest tylko 36 kluczy?** Ponieważ badany klucz składał się z 16 kopii jednego znaku ASCII wybranego ze zbioru małych liter i cyfr (a-z oraz 0-9), co daje dokładnie 36 niezależnych możliwości do sprawdzenia.
- **Kiedy ranking entropii mógłby zawieść?** Taka metoda mogłaby nie zadziałać w przypadku danych skompresowanych, ponieważ cechują się one z natury wysoką entropią i nie wykazują wyraźnego spadku wartości $H$ charakterystycznego dla czytelnego tekstu w języku naturalnym.