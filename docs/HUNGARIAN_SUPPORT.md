# Hungarian Language Support / Magyar Nyelvi Támogatás

## Overview / Áttekintés

The RAI demo now includes comprehensive Hungarian language support for analyzing Hungarian advertisements and displaying results in both Hungarian and English.

Az RAI demó mostantól átfogó magyar nyelvi támogatást nyújt a magyar reklámok elemzéséhez és az eredmények magyar és angol nyelven történő megjelenítéséhez.

---

## Features / Funkciók

### 1. Automatic Language Detection / Automatikus Nyelvfelismerés

The system automatically detects if ad copy is in Hungarian based on:
- Hungarian-specific characters (á, é, í, ó, ö, ő, ú, ü, ű)
- Common Hungarian words (és, hogy, van, nem, egy, az, etc.)

A rendszer automatikusan felismeri, ha a reklámszöveg magyar nyelvű:
- Magyar-specifikus karakterek alapján (á, é, í, ó, ö, ő, ú, ü, ű)
- Gyakori magyar szavak alapján (és, hogy, van, nem, egy, az, stb.)

### 2. Bilingual Interface / Kétnyelvű Felület

**Language Selector / Nyelvválasztó:**
- Switch between English 🇬🇧 and Magyar 🇭🇺 interface
- Located in sidebar: "Interface Language / Felület Nyelve"
- Váltás az angol 🇬🇧 és magyar 🇭🇺 felület között
- Helyezkedik az oldalsávban: "Interface Language / Felület Nyelve"

**UI Elements Translated / Lefordított Felületi Elemek:**
- Titles and headers / Címek és fejlécek
- Button labels / Gombfeliratok
- Section headings / Szekciócímek
- Framework descriptions / Keretrendszer leírások

### 3. Bilingual Analysis Results / Kétnyelvű Elemzési Eredmények

When analyzing Hungarian ads, the AI provides insights in **both English and Hungarian**:

Magyar reklámok elemzésekor az AI **magyar és angol nyelven** is ad betekintést:

**Dimension Findings / Dimenziók Megállapításai:**
- Primary language displayed based on interface setting
- Expandable section to view alternate language
- Elsődleges nyelv a felület beállítása szerint jelenik meg
- Kinyitható szekció az alternatív nyelv megtekintéséhez

**Summary Sections / Összefoglaló Szekciók:**
- Strengths / Erősségek
- Concerns / Aggályok
- Recommendations / Ajánlások

All available in both languages with easy toggle.
Mindegyik mindkét nyelven elérhető, könnyű váltással.

### 4. Hungarian Cultural Context / Magyar Kulturális Kontextus

The AI analysis is instructed to:
- Be sensitive to Hungarian cultural norms
- Understand local context and values
- Recognize Hungarian-specific references
- Respect regional sensitivities

Az AI elemzés figyelembe veszi:
- A magyar kulturális normákat
- A helyi kontextust és értékeket
- A magyar-specifikus utalásokat
- A regionális érzékenységeket

---

## Scoring Framework Translations / Pontozási Keretrendszer Fordítások

### Climate Responsibility / Klímafelelősség
- Sustainability messaging presence and authenticity
- Fenntarthatósági üzenetek jelenléte és hitelessége
- Absence of greenwashing or exaggerated claims
- Zöldre festés és túlzó állítások hiánya

### Social Responsibility / Társadalmi Felelősség
- Diversity in representation
- Sokszínűség a megjelenítésben
- Avoidance of harmful stereotypes
- Káros sztereotípiák elkerülése

### Cultural Sensitivity / Kulturális Érzékenység
- Respectful use of cultural symbols and traditions
- Kulturális szimbólumok és hagyományok tiszteletteljes használata
- Sensitivity to local norms and values
- Érzékenység a helyi normák és értékek iránt

### Ethical Communication / Etikus Kommunikáció
- Transparency in intent and disclosures
- Átláthatóság a szándékban és közlésekben
- Avoidance of manipulative techniques
- Manipulatív technikák elkerülése

---

## Example Hungarian Ad / Példa Magyar Reklám

The demo includes a built-in Hungarian example ad:

**ÖkoFonál - Javítási Forradalom**

A demó tartalmaz egy beépített magyar példareklámot:

```
Minden ÖkoFonál ruhadarab élethosszig tartó javítási garanciával érkezik.
Elromlott cipzár? Megjavítjuk. Elszakadt varrás? Megfoltozuk.

2019 óta 14 000 darabot javítottunk meg, távol tartva őket a hulladéklerakóktól.

Anyagunk: 100% organikus pamut, GOTS minősítéssel.
Gyáraink: Fair Trade tanúsítvánnyal, átlátható ellátási lánccal.
Ígéretünk: Vásárolj kevesebbet, viselj tovább.
```

Expected score: ~90/100 (Excellent sustainability and social responsibility)
Várható pontszám: ~90/100 (Kiváló fenntarthatóság és társadalmi felelősség)

---

## How to Use / Használati Útmutató

### For English Users:

1. Open the demo: `streamlit run app.py`
2. Keep interface in English (default)
3. Upload Hungarian ad or try the "Magyar: Fenntartható Divat" example
4. Analysis will detect Hungarian language automatically
5. Results show English findings by default
6. Click expanders to view Hungarian translations

### Magyar Felhasználóknak:

1. Nyissa meg a demót: `streamlit run app.py`
2. Válassza a Magyar 🇭🇺 felületet az oldalsávban
3. Töltsön fel magyar reklámot vagy próbálja a "Magyar: Fenntartható Divat" példát
4. Az elemzés automatikusan felismeri a magyar nyelvet
5. Az eredmények magyarul jelennek meg
6. Kattintson a kinyitható szekciókra az angol fordítás megtekintéséhez

---

## Technical Implementation / Technikai Megvalósítás

### Language Detection Function

```python
def detect_language(text: str) -> str:
    """Detect if the text is primarily Hungarian or English"""
    hungarian_chars = sum(1 for c in text if c in 'áéíóöőúüűÁÉÍÓÖŐÚÜŰ')
    hungarian_words = ['és', 'hogy', 'van', 'nem', 'egy', 'az', 'ezt', 'csak', 'még', 'vagy']
    hungarian_word_count = sum(1 for word in hungarian_words if word in text.lower())

    if hungarian_chars > 5 or hungarian_word_count > 2:
        return 'hu'
    return 'en'
```

### Bilingual Prompt Structure

When Hungarian is detected, the AI receives a modified prompt:
- Instructions to provide bilingual output
- Hungarian framework translations
- Cultural sensitivity guidelines
- Structured JSON format for both languages

Magyar nyelv észlelésekor az AI módosított promptot kap:
- Kétnyelvű kimenet utasításai
- Magyar keretrendszer fordítások
- Kulturális érzékenységi irányelvek
- Strukturált JSON formátum mindkét nyelvhez

---

## JSON Response Format / JSON Válasz Formátum

For Hungarian ads, the AI returns:

```json
{
    "overall_score": 85,
    "ad_language": "hu",
    "dimensions": {
        "Climate Responsibility": {
            "score": 90,
            "findings": ["English finding 1", "English finding 2", "English finding 3"],
            "findings_hu": ["Magyar megállapítás 1", "Magyar megállapítás 2", "Magyar megállapítás 3"]
        }
    },
    "summary": {
        "strengths": ["English strength 1", "English strength 2", "English strength 3"],
        "strengths_hu": ["Magyar erősség 1", "Magyar erősség 2", "Magyar erősség 3"],
        "concerns": ["English concern 1", "English concern 2", "English concern 3"],
        "concerns_hu": ["Magyar aggály 1", "Magyar aggály 2", "Magyar aggály 3"],
        "recommendations": ["English rec 1", "English rec 2", "English rec 3"],
        "recommendations_hu": ["Magyar ajánlás 1", "Magyar ajánlás 2", "Magyar ajánlás 3"]
    }
}
```

---

## Benefits for Telekom Demo / Előnyök a Telekom Demóhoz

✅ **Analyze Hungarian Telekom ads directly**
- No need for translation
- Culturally relevant analysis
- Native language insights

✅ **Magyar Telekom reklámok közvetlen elemzése**
- Nincs szükség fordításra
- Kulturálisan releváns elemzés
- Anyanyelvi betekintések

✅ **Bilingual presentation ready**
- Show Hungarian stakeholders results in their language
- Provide English translations for international audiences
- Professional and inclusive

✅ **Kétnyelvű prezentáció kész**
- Magyar érdekelt feleknek anyanyelvükön mutathatók az eredmények
- Angol fordítás nemzetközi közönség számára
- Professzionális és befogadó

✅ **Cultural sensitivity respected**
- AI understands Hungarian context
- Local norms and values considered
- More accurate assessments

✅ **Kulturális érzékenység tiszteletben tartása**
- Az AI érti a magyar kontextust
- Helyi normák és értékek figyelembevétele
- Pontosabb értékelések

---

## Future Enhancements / Jövőbeli Fejlesztések

- PDF reports in Hungarian / PDF jelentések magyarul
- More Hungarian example ads / Több magyar példareklám
- Hungarian-specific greenwashing patterns / Magyar-specifikus zöldre festési minták
- Regional cultural sensitivity database / Regionális kulturális érzékenység adatbázis

---

## Support / Támogatás

For questions about Hungarian language support:
- Check CLAUDE.md for technical details
- See DEMO_GUIDE.md for presentation tips
- Review this file for usage instructions

Magyar nyelvi támogatással kapcsolatos kérdésekhez:
- Tekintse meg a CLAUDE.md-t a technikai részletekhez
- Lásd a DEMO_GUIDE.md-t prezentációs tippekhez
- Nézze át ezt a fájlt a használati utasításokhoz

---

**Köszönjük! / Thank you!** 🇭🇺 🇬🇧
