# ⚖️ Urheberrecht, Gemeinfreiheit & Provenienz

Dieses Dokument erläutert den rechtlichen Status des Werkes von Otto von Böhtlingk (1887), die urheberrechtliche Einordnung der verwendeten Digitalisate der Universitätsbibliothek Heidelberg, die Bereinigung von Bibliotheks-Wasserzeichen sowie die Standards guter wissenschaftlicher Praxis (Provenienz und Zitation).

---

## 1. Gemeinfreiheit des Originalwerks (Public Domain)

Das zugrundeliegende Werk **«Pâṇini's Grammatik»** von Otto von Böhtlingk (2. Auflage, Leipzig 1887) ist **vollständig gemeinfrei** (Public Domain):

* **Urheber:** Otto von Böhtlingk (* 11. Juni 1815 in Sankt Petersburg; † 1. April 1904 in Leipzig).
* **Gesetzliche Schutzfrist:** Gemäß § 64 UrhG (Deutschland), Art. 9 URG (Schweiz) sowie Richtlinie 2006/116/EG (EU) erlischt das Urheberrecht 70 Jahre nach dem Tod des Urhebers (*post mortem auctoris*).
* **Ablauf der Schutzfrist:** 1904 + 70 Jahre = Ende der Schutzfrist mit Ablauf des 31. Dezember 1974.
* **Rechtsfolge:** Das Werk ist seit dem **1. Januar 1975 frei von Urheberrechten**. Der Text, die deutsche Übersetzung, der wissenschaftliche Kommentar sowie die textkritischen Anmerkungen dürfen von jedermann ohne Einschränkungen vervielfältigt, digitalisiert, verändert, neu gesetzt und öffentlich zugänglich gemacht werden (sowohl nicht-kommerziell als auch kommerziell).

---

## 2. Status der Digitalisate (2D-Scans der UB Heidelberg)

Für die digitale Erfassung und Textausrichtung (OCR & Alignment) wird das Digitalisat der Universitätsbibliothek Heidelberg verwendet. Auch hier entsteht **kein neues Schutzrecht**:

### Europäisches und deutsches Recht (EU-DSM-Richtlinie & § 68 UrhG)
* **EU-DSM-Richtlinie (EU 2019/790), Artikel 14:**
  > *„Die Mitgliedstaaten sehen vor, dass nach Ablauf der Schutzdauer eines Werkes der bildenden Künste Material, das im Zuge einer Vervielfältigung dieses Werkes entstanden ist, weder dem Urheberrecht noch verwandten Schutzrechten unterliegt [...]“*
* **Deutsches Urheberrechtsgesetz (§ 68 UrhG):**
  Reproduktionen gemeinfreier visueller Werke genießen keinen Schutz nach verwandten Schutzrechten (§§ 70, 71, 72 oder 73 UrhG).
* **Rechtsprechung zu 2D-Scans:** Reine zweidimensionale, originalgetreue Reproduktionsscans von Textseiten entbehren einer persönlichen geistigen Schöpfung (kein Werk im Sinne von § 2 UrhG) und begründen bei gemeinfreien Vorlagen auch kein Leistungsschutzrecht für Lichtbilder (§ 72 UrhG). 

Die freie Nachnutzung, Extraktion, Bearbeitung und Veröffentlichung des darin enthaltenen Textes verletzt folglich keine Rechte Dritter.

---

## 3. Entfernung von Bibliotheks-Wasserzeichen & Stempeltexten

Auf den Scans der UB Heidelberg befinden sich am Seitenrand organisatorische Vermerke und Stempel:

```text
UNIVERSITÄTS-
BIBLIOTHEK
HEIDELBERG
Baden-Württemberg | GEFÖRDERT DURCH DIE DFG
```

### Rechtliche Einordnung
Diese Stempel dienen der Kennzeichnung der digitalisierenden Institution und Förderprojekte. Sie begründen **kein Urheberrecht** am historischen Text. Die Entfernung dieser Hinweise aus dem extrahierten Textkörper berührt keine Urheberrechte.

### Philologische & technische Notwendigkeit
In automatisierten OCR-Pipelines werden diese Randnotizen fälschlicherweise als Textteile erfasst und in Sūtra-Kommentare eingestreut. Für eine saubere digitale Edition ist die rückstandslose Entfernung unerlässlich:
* **Datenintegrität:** Keine Verfälschung des Böhtlingk-Kommentars durch moderne Bibliotheksstempel.
* **TEI-P5-Konformität:** Im XML-Body (`<div type="commentary">`) dürfen ausschließlich authentische Texte des Primärwerks stehen.
* **Seitenübergreifende Kontinuität:** Kommentare, die sich über einen Seitenwechsel erstrecken (z. B. Sūtra 1.1.58), müssen nahtlos zusammengefügt werden, anstatt durch Stempelblöcke unterbrochen zu werden.

### Technische Implementierung
Die Filterung erfolgt deterministisch in den Pipeline-Skripten ([`scripts/align_mistral_sutras.py`](https://github.com/birchville-org/boethlingk/blob/main/scripts/align_mistral_sutras.py) und [`scripts/build_sandwich_pdf.py`](https://github.com/birchville-org/boethlingk/blob/main/scripts/build_sandwich_pdf.py)):

```python
# Auszug aus scripts/align_mistral_sutras.py:
def clean_commentary_paragraphs(text: str) -> list[str]:
    lines = text.split("\n")
    cleaned_lines = []
    in_block = False
    for l in lines:
        l_str = l.strip()
        if any(k in l_str.upper() for k in [
            "UNIVERSITÄTS", "BIBLIOTHEK", "HEIDELBERG",
            "BADEN-WÜRTTEMBERG", "GEFÖRDERT DURCH", "DIGI.UB"
        ]):
            in_block = True
            continue
        elif in_block:
            if re.match(r"^\d+$", l_str) or l_str in ["B", "b", ""]:
                continue
            else:
                in_block = False
                cleaned_lines.append(l)
        else:
            cleaned_lines.append(l)
    return cleaned_lines
```

---

## 4. Wissenschaftliche Provenienz & Zitationspraxis

Während der Text frei von Urheberrechten ist, gebietet die **gute wissenschaftliche Praxis** (sowie die Dokumentation der Datenherkunft), die Quelle des Digitalisats transparent auszuweisen.

Im Projekt `boethlingk` wird die Provenienz an folgenden Stellen dokumentiert:

1. **TEI-P5-Header (`boehtlingk1887_p5.xml`):**
   ```xml
   <sourceDesc>
     <bibl xml:id="Boehtlingk1887">
       <author>Otto von Böhtlingk</author>
       <title>Pâṇini's Grammatik</title>
       <pubPlace>Leipzig</pubPlace>
       <publisher>Verlag von H. Haessel</publisher>
       <date when="1887">1887</date>
       <note type="digitization">
         Digitalisiert durch die Universitätsbibliothek Heidelberg.
         URN: urn:nbn:de:bsz:16-diglit-323605
         URL: https://digi.ub.uni-heidelberg.de/diglit/boethlingk1887
       </note>
     </bibl>
   </sourceDesc>
   ```

2. **Typst-Buchausgabe (`boethlingk1887_typeset_edition.pdf`):**
   Das Impressum nennt das historische Ersterscheinungsjahr (1887), den Verlag H. Haessel Leipzig sowie die UB Heidelberg als scangebende Institution.

3. **Master-JSON-Metadaten:**
   Jeder Sūtra-Eintrag verweist auf die zugehörige Faksimile-Seitenzahl des Heidelberger Digitalisats.

---

## 5. Lizenz der Neuausgabe

* **Historischer Textbestand:** Public Domain (Gemeinfreiheit).
* **Pipeline-Code & TEI-Modellierung:** Veröffentlicht unter [MIT License](https://github.com/birchville-org/boethlingk/blob/main/LICENSE).
