# Compounds and Blends Competition Thesis

Špecializovaný nástroj na vytvorenie pracovného prostredia a správu redundancie dát.

Tento nástroj vznikol pre potreby dizertačnej práce, ktorá pracuje s lingvistickými dátami.

### Motivácia

Respondenti pomenovali neexistujúce objekty zobrazené na obrázkoch. Na obrázkoch boli objekty, ktoré vznikli syntézou dvoch reálnych objektov.
Súťaž spočíva v tom, či respondenti pri tvorbe pomenovaní uprednostnili zložené slová (compound) alebo nové "zmiešané" slová (blend).

Vytvorené pomenovania sa označujú ako menné jednotky (naming unit), ktoré sú vytvorené zo zdrojových slov (source word). Zdrojové slová sú v ideálnom prípade pôvodné reálne objekty obrázkov.

K menným jednotkám aj k zdrojovým slovám chceme priradiť anotácie, ako napríklad: počet znakov, rozdelenie na slabiky, jazyk, fonetický prepis, frekvencia v korpuse.
Takisto chceme uchovávať informácie o prepojení medzi mennými jednotkami a zdrojovými slovami.
Dátová redundancia spočíva v tom, že jednu mennú jednotku zadali viacerí respondenti a rôzne zdrojové slova sú súčasťou rôznych menných jednotiek.

### Nástroj

Preto je celý dátový model navrhnutý pre databázu SQL tak, aby sa predišlo ukladaniu rovnakej informácie na dvoch rôznych miestach. Napríklad, dĺžky zdrojových slov sú zaznamenané iba raz, napriek tomu, že sa vyskytujú vo viacerých menných jednotkách.

Vzhľadom k tomu, že na manuálnu prácu s dátami a cielenú úpravu dát s komplexným pohľadom je obzvlášť nepohodlné upravovať samostatné SQL tabuľky pomocou SQL klienta, bolo vytvorené špecializované pracovné prostredie na mieru.

Nástroj na základe dát z databázy vytvorí XLSX dokument (Excel), kde hárky zobrazujú jednotlivé SQL tabuľky, ale tiež komplexnejšie pohľady. Údaje, ktoré je možné vygenerovať alebo získať zo slovníkov, sa získajú.
Užívateľ si XLSX dokument upraví, aktualizuje informácie a pridá ručné anotácie. Po úprave nástroj vezme upravený XLSX dokument, skontroluje zmeny oproti databáze.
To, čo bolo upravené v dokumente, nahrá do databázy a to, čo bolo pridané v databáze, pridá do dokumentu. Nástroj v tomto kroku ďalej kontroluje integritu dát -- napríklad či každé zdrojové slovo je použité aspoň v jednej mennej jednotke.

Hárok *Overview* v dokumente XLSX poskytuje pre každé pomenovanie respondentov komplexný pohľad na všetky dáta v databáze.

Autor nástroja: Simeon Borko <simeon.borko@gmail.com>.
