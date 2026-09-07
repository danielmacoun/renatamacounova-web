# Web Renaty Macounové

Statický web. Kořenem publikovaného webu je tato složka (obsahuje `CNAME`). Lokální náhled: spusťte zde `python3 -m http.server 8000` a otevřete http://localhost:8000/.

## Přidání článku do Zamyšlení

1. Ve složce `zamysleni/` vytvořte složku s názvem článku bez diakritiky, malými písmeny a s pomlčkami, například `novy-text/`. Zkopírujte do ní `zamysleni/jak-nastavujeme-vlastni-deti/index.html` jako `index.html`. Každý článek tak má jediný HTML soubor a adresu `/zamysleni/novy-text/` bez přípony.
2. V kopii změňte `<h1>`, text odstavců, datum v `<time datetime="RRRR-MM-DD">` i jeho viditelný český zápis. Změňte `<title>`, description, canonical, všechny `og:*` hodnoty a `article:published_time`. V JSON-LD změňte `headline`, `description`, `datePublished`, `url` a `mainEntityOfPage.@id`. Autor zůstává Renata Macounová. Zachovejte `branch-zamysleni`, připojený styl a navigaci pod článkem.
3. Do `<ul>` v sekci `reading-list` souboru `zamysleni/index.html` přidejte jeden řádek, nejnovější nahoře:
   ```html
   <li><a href="/zamysleni/novy-text/">Název nového článku <span aria-hidden="true">→</span></a></li>
   ```
   Tím je nový článek přístupný. Není potřeba měnit JavaScript, CSS ani nastavení serveru.
4. Pro aktuální propagaci a vyhledávače změňte v hlavním `index.html` odkaz `reading-latest` na nejnovější článek a do `sitemap.xml` doplňte `<url><loc>https://renatamacounova.cz/zamysleni/novy-text/</loc></url>`.
5. V lokálním náhledu ověřte odkaz ze seznamu, datum, mobilní zobrazení a návratové odkazy. Publikujte změněné soubory obvyklým nasazením webu.

## Série a samostatné články

Blok `reading-series` je pouze oznámení připravované série „Denní naučení s Pěti Tibeťany“. Seznam `reading-list` je samostatná sekce. Článek „Jak nastavujeme vlastní děti“ není kapitolou série. Budoucí kapitoly série nemíchejte automaticky se samostatnými články.

Datum 7. září 2026 označuje zveřejnění přesunutého textu na samostatné stránce Zamyšlení; původní sekce datum publikace neuváděla.
