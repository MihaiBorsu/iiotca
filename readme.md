1) run __init__.py - it creates the database and the tables
2) run script.py 

citeste la fiecare 1 (vom muta la 30 la final, dar acuma e mai ok asa pentru debugging) secunda din senzor o valoare noua pentru temperatura si o tine local

la 3 citiri > 37.3 porneste febra iar la 3 citiri <37.3 opreste febra si inregistraza local evenimentul (vom mari numarul la 10 citiri dar aceeasi treaba cu debugging-ul e mai usor cu 3 momentan)

firebase si plotify inca nu sunt implementate, dar nu incurca api-ul deloc.

Ce trebe sa faci?

serializatoare pentru tabelele create in baza de date locala, exact asa cum sunt in specificatii la feature-ul 3 (cel cu api)

testeaza cu postman ca api-ul functioneaza, si ar mai merge o aplicatie web super basic html + javascript ca sa display-uim rezultatul