# Magyar Üzemanyagárak Home Assistant Integráció

Ez az integráció a magyarországi üzemanyagárakat jeleníti meg a Home Assistant-ban.

## ✨ Funkciók

- 🔄 Automatikus frissítés óránként
- ⛽ Különböző üzemanyagtípusok árainak megjelenítése
- 💰 Átlagár, legolcsóbb és legmagasabb ár megjelenítése
- 📊 Részletes információk az üzemanyagokról

## 🛠️ Telepítés

1. Másold a `custom_components/magyar_uzemanyag` mappát a Home Assistant `custom_components` könyvtárába
2. Indítsd újra a Home Assistant-ot
3. Menj a Beállítások > Eszközök és szolgáltatások menüpontba
4. Kattints az "Integráció hozzáadása" gombra
5. Keresd meg a "Magyar üzemanyagárak" integrációt
6. Kövesd a telepítési varázsló lépéseit

## ⚙️ Beállítás

1. Menj a Home Assistant beállításaiba
2. Válaszd az "Integrációk" menüpontot
3. Kattints a "+" gombra az új integráció hozzáadásához
4. Keresd meg a "Magyar Üzemanyagárak" integrációt
5. Kövesd a telepítési varázsló lépéseit

## 📊 Entitások

### Szenzorok

Minden szenzor a következő tulajdonságokkal rendelkezik:

| Tulajdonság | Típus | Példa | Leírás |
|-------------|-------|-------|---------|
| Állapot | `number` | 608.6 | Az üzemanyag aktuális átlagára |
| Icon | `string` | mdi:fuel | Üzemanyag ikon |
| Device Class | `monetary` | - | Pénzügyi érték típus |
| State Class | `measurement` | - | Mérési érték típus |
| Mértékegység | `string` | Ft/l | Magyar Forint / liter |

### Szenzor attribútumok

| Attribútum | Típus | Példa érték | Leírás |
|------------|-------|-------------|---------|
| Info | `string` | "95-98-as oktánszámú benzin legfeljebb 10% etanollal" | Részletes információ |
| Legolcsóbb ár | `number` | 561.0 | A legalacsonyabb elérhető ár |
| Legmagasabb ár | `number` | 671.9 | A legmagasabb elérhető ár |
| Átlagár | `number` | 608.6 | Az országos átlagár |

## 🤝 Közreműködés

Ha hibát találsz vagy fejlesztési javaslatod van, kérlek nyiss egy [issue](https://github.com/fantnhu/magyar_uzemanyag/issues)-t.

## 📄 Licensz

Ez a projekt az MIT licensz alatt áll - további információkért lásd a [LICENSE](LICENSE) fájlt.

## 🙏 Köszönetnyilvánítás

- A Home Assistant közösségnek a támogatásért

## 🔗 Hasznos linkek

- [Home Assistant közösség](https://community.home-assistant.io/)
