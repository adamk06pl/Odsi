from hashlib import sha256

teksty = ["Ala ma kota.", "Ala ma kota!", "Ala ma kota!", "Ala ma koty!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"]
for tekst in teksty:
    skrot = sha256(tekst.encode("utf-8")).hexdigest()
    print(tekst)
    print(skrot)
