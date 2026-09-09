# Web Renaty Macounové

Statický web. Kořenem publikovaného webu je tato složka (obsahuje `CNAME`). Lokální náhled: spusťte zde `python3 -m http.server 8000` a otevřete http://localhost:8000/.

## Přidání úryvku do Zamyšlení

1. Ve složce `zamysleni/` vytvořte složku s názvem úryvku bez diakritiky, malými písmeny a s pomlčkami, například `novy-text/`. Zkopírujte do ní `zamysleni/jak-nastavujeme-vlastni-deti/index.html` jako `index.html`. Každý úryvek tak má jediný HTML soubor a adresu `/zamysleni/novy-text/` bez přípony.
2. V kopii změňte `<h1>`, text odstavců, datum v `<time datetime="RRRR-MM-DD">` i jeho viditelný český zápis. Změňte `<title>`, description, canonical, všechny `og:*` hodnoty a `article:published_time`. V JSON-LD změňte `headline`, `description`, `datePublished`, `url` a `mainEntityOfPage.@id`. Autor zůstává Renata Macounová. Zachovejte `branch-zamysleni`, připojený styl a navigaci pod úryvkem.
3. Do `<ul>` v sekci `reading-list` souboru `zamysleni/index.html` přidejte jeden řádek, nejnovější nahoře:
   ```html
   <li class="reading-card"><article><time datetime="RRRR-MM-DD">České datum</time><h3>Název nového úryvku</h3><p>První dvě věty úryvku.</p><a href="/zamysleni/novy-text/" aria-label="Číst: Název nového úryvku">Číst →</a></article></li>
   ```
   Tím je nový úryvek přístupný. Není potřeba měnit JavaScript, CSS ani nastavení serveru.
4. Rozcestník načítá odkaz na nejnovější úryvek automaticky z první karty přehledu pomocí `assets/js/latest-excerpt.js`; build ani ruční změna odkazu nejsou potřeba. V hlavním `index.html` zůstává funkční záložní odkaz `reading-latest` pro vypnutý JavaScript nebo chybu načtení; pro aktuálnost i v těchto případech jej můžete aktualizovat. Do `sitemap.xml` doplňte `<url><loc>https://renatamacounova.cz/zamysleni/novy-text/</loc></url>`.
5. V úryvcích aktualizujte navigaci `reading-related` pod textem: pokud existují jiné úryvky, vložte nadpis `<h2>Další úryvky</h2>` a seznam odkazů na ně (bez odkazu na právě otevřený úryvek). Pokud další úryvky nejsou, ponechte návratový odkaz na `/zamysleni/`.
6. V lokálním náhledu ověřte odkaz ze seznamu, datum, mobilní zobrazení a návratové odkazy. Publikujte změněné soubory obvyklým nasazením webu.

## Série a samostatné úryvky

Blok `reading-series` je pouze oznámení připravované série „Denní naučení s Pěti Tibeťany“. Seznam `reading-list` je samostatná sekce „Úryvky ze třetí knihy“. Úryvek „Jak nastavujeme vlastní děti“ není kapitolou série. Budoucí kapitoly série nemíchejte automaticky se samostatnými úryvky.

Datum 7. září 2026 označuje zveřejnění přesunutého textu na samostatné stránce Zamyšlení; původní sekce datum publikace neuváděla.
