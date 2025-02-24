Aplicație de Gestionare a Inventarului
Descriere
Această aplicație este un sistem simplu de gestionare a inventarului, dezvoltat folosind Python și PyQt5. Aplicația permite utilizatorilor să adauge, șteargă, caute și aloce obiecte dintr-un inventar. Există două tipuri de utilizatori: administratori și utilizatori obișnuiți. Administratorii au acces la toate funcționalitățile, în timp ce utilizatorii obișnuiți pot doar să vizualizeze și să caute obiecte.

Funcționalități
Autentificare:

Utilizatorii trebuie să se autentifice cu un nume de utilizator și o parolă.

Există un utilizator implicit admin cu parola admin123.

Adăugare Obiect:

Doar administratorii pot adăuga obiecte în inventar.

Fiecare obiect are următoarele câmpuri:

Firma

Model

Anul achiziției

Preț

Departament

Alocat către (opțional)

Ștergere Obiect:

Doar administratorii pot șterge obiecte din inventar.

Ștergerea se face pe baza ID-ului obiectului.

Afișare Obiecte:

Toți utilizatorii pot vizualiza lista de obiecte din inventar.

Lista este afișată într-un tabel organizat, cu coloane pentru fiecare câmp al obiectului.

Căutare Obiect:

Toți utilizatorii pot căuta obiecte după diverse criterii (firma, model, an, departament, alocat către).

Alocare Obiect:

Doar administratorii pot aloca obiecte către utilizatori.

Un obiect poate fi alocat doar dacă nu este deja alocat.

Cum funcționează
Datele sunt stocate în fișiere JSON:

Utilizatorii sunt stocați în data/users.json.

Obiectele din inventar sunt stocate în data/inventory.json.

Interfața grafică:

Aplicația folosește PyQt5 pentru a oferi o interfață grafică ușor de folosit.

Butoanele sunt organizate într-un mod intuitiv, iar mesajele de confirmare/eroare sunt afișate în ferestre pop-up.

Gestionarea permisiunilor:

Doar administratorii pot adăuga, șterge și aloca obiecte.

Utilizatorii obișnuiți pot doar să vizualizeze și să caute obiecte.

Cum se folosește
Pornirea aplicației:

Rulați fișierul main.py pentru a porni aplicația.

Aplicația va deschide fereastra de autentificare.

Autentificare:

Introduceți numele de utilizator și parola.

Dacă nu aveți un cont, puteți folosi utilizatorul implicit admin cu parola admin123.

Utilizarea aplicației:

După autentificare, veți fi redirecționat către fereastra principală.

Folosiți butoanele pentru a adăuga, șterge, căuta sau aloca obiecte.

Ieșire:

Închideți fereastra pentru a ieși din aplicație.

Unde poate fi folosită
Această aplicație poate fi folosită în orice mediu unde este necesară gestionarea unui inventar, cum ar fi:

Birouri: Pentru gestionarea echipamentelor de birou (calculatoare, imprimante, etc.).

Școli: Pentru gestionarea resurselor educaționale

Depozite: Pentru urmărirea stocurilor de produse.

Companii de Închirieri de Echipamente