# Milník 1: bezpečné ověření Decap Turbo

Stav: připravená konfigurace, nikoliv úspěšně dokončený test uživatele.
Produkční HTML, CSS, sitemap ani ochrana větve se nemění. Koncepty ve veřejném
GitHub repozitáři nejsou tajné; nikdy sem nevkládejte osobní nebo citlivé údaje.

## Před spuštěním

1. Renata je jediným uživatelem Turbo Free. Daniel zůstává správcem GitHubu.
2. V Turbo vytvořte Site pro `danielmacoun/renatamacounova-web`, branch `main`,
   config path `.cms-test/config.yml`, admin URL `http://localhost:8000/`.
3. Site ID z Overview nahraďte za `REPLACE_WITH_TURBO_SITE_ID` přes tento PR.
   ID není tajemství. Hesla a tokeny do repozitáře nepatří.
4. Ověřte instalaci App pouze pro tento repozitář, bez bypassu ochrany main.
   Plná pravidla včetně povinných lidských reviews musí Daniel zkontrolovat v GitHubu.
5. Turbo potřebuje konfiguraci na cílové větvi. Nejprve ověříme kontroly tohoto
   přípravného PR a vyžádáme Danielův výslovný souhlas s jeho sloučením.
   Bez toho nelze slíbit, že Turbo načte kolekci z main.

## Lokální administrace

Z kořene checkoutu obsahujícího tyto soubory:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory .cms-test
```

Otevřete `http://localhost:8000/`. Přihlaste Renatu přes Login with Turbo.
Administrace směřuje do živého Git repozitáře, nikoliv na lokální disk.
Neprovádějte publikaci bez souhlasu pro konkrétní PR. Pro použití na Renatině
počítači musí stejný checkout i server běžet tam; localhost není vzdálená adresa.

## Ověření chybové a úspěšné cesty

1. Renata vytvoří nový záznam s neosobním názvem a textem. Zapne pole
   „Záměrně zablokovat publikování“ a uloží koncept.
2. Zapište URL, autora a head SHA skutečného PR vytvořeného Turbo do main.
   Přípravný PR vytvořený Codexem není důkaz fungování CMS.
3. Počkejte na selhání jobu `Website checks` kvůli `force_failure: true`.
4. Až Daniel výslovně schválí pokus o publikaci tohoto konkrétního PR,
   zkuste publikovat. Musí být zablokováno a main musí zůstat na původním SHA.
   Bez souhlasu se o merge nepokoušejte ani při červené kontrole.
5. Renata vypne chybové pole a uloží stejný koncept. Zapište nové SHA,
   počkejte na nové zelené kontroly a zkontrolujte diff: pouze testovací JSON.
6. Znovu si vyžádejte Danielův výslovný souhlas pro konkrétní PR a nové SHA.
   Teprve poté Renata klikne na Publikovat. Ověřte merge přes CMS, historii,
   úspěšný Pages build a nezměněný veřejný obsah.
7. Ověřte, že `/.cms-test/config.yml`, `/.cms-test/index.html` a cesta
   testovacího JSON na produkčním webu vracejí 404.

Po každé další úpravě znovu čekejte na kontroly nové verze.
Pokud CMS potřebuje vypnout ochranu nebo přidat bypass, zastavte test.

## Důkazy pro závěr

- Potvrzení tarifu Free a jediné identity (bez kopírování credentials).
- Renatino přihlášení bez GitHub účtu.
- URL CMS PR, jeho větev a obě head SHA.
- URL selhaného a úspěšného běhu Website checks.
- Odmítnutí publikace při selhání; main SHA před a po pokusu.
- Samostatný souhlas s úspěšnou publikací a výsledný merge SHA.
- Pages build, HTTP 404 testovacích cest a kontrola veřejných stránek.

Omezení: tento milník neověřuje plnou administraci, obrázky, migraci článků,
náhledy skutečných článků ani obnovu přístupu k Turbo účtu.
