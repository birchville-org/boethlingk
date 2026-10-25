// =============================================================================
// Birchville Scholarly Synthesis — Dichte Faksimile-Testausgabe (Böhtlingk 1887)
// Exakte 1:1-Seitenparität mit adaptivem Satzspiegel & maximaler Raumausnutzung
// =============================================================================

#set document(
  title: "Pāṇini's Grammatik (Otto von Böhtlingk, 1887) — Dichte Faksimile-Testausgabe",
  author: "Otto von Böhtlingk (Ed. Marco Demarmels / Birchville Foundation)",
  keywords: ("Pāṇini", "Aṣṭādhyāyī", "Sanskrit", "Grammatik", "Böhtlingk", "Indologie", "Birchville")
)

#set page(
  paper: "iso-b5",
  margin: (top: 1.8cm, bottom: 1.8cm, inside: 2.0cm, outside: 1.6cm),
  header: none,
  footer: none
)

#set text(
  font: ("STIX Two Text", "Noto Serif Devanagari", "Devanagari MT"),
  size: 9.4pt,
  lang: "de"
)

#set par(justify: true, leading: 0.44em)

// Helper: Convert ASCII digits to Devanāgarī numerals
#let to-deva(num) = {
  let s = str(num)
  let map = ("0": "०", "1": "१", "2": "२", "3": "३", "4": "४", "5": "५", "6": "६", "7": "७", "8": "८", "9": "९")
  s.clusters().map(c => map.at(c, default: c)).join("")
}

// =============================================================================
// 1. TITELEI & IMPRESSUM (BIRCHVILLE SCHOLARLY SYNTHESIS)
// =============================================================================

// Seite i: Halbtitel (Bastard Title)
#v(6cm)
#align(center)[
  #text(16pt, weight: "bold", tracking: 0.12em)[#smallcaps[Pāṇini's Grammatik]] \
  #v(0.6cm)
  #text(9pt, style: "italic", fill: rgb("#334155"))[Otto von Böhtlingk (Leipzig 1887)] \
  #v(0.3cm)
  #text(8.5pt, fill: rgb("#b45309"), weight: "bold")[Dichte Faksimile-Testausgabe (1:1-Seitenparität mit dem Originaldruck)]
]

#pagebreak()

// Seite ii: Impressum & Birchville Curation Badge
#v(3.5cm)
#align(center)[
  #image("/docs/assets/birchville_logo.png", height: 2.2cm) \
  #v(0.5cm)
  #text(8pt, weight: "bold", tracking: 0.10em, fill: rgb("#b45309"))[BIRCHVILLE SCHOLARLY SYNTHESIS] \
  #v(0.2cm)
  #text(10pt, weight: "bold", fill: rgb("#03192e"))[Kanonische Editionen klassischer philologischer Referenzwerke] \
  #v(0.8cm)
  #line(length: 40%, stroke: 0.4pt + rgb("#d8d2c6")) \
  #v(0.8cm)
  #text(8.5pt, fill: rgb("#1e2d37"))[
    *Historisches Original:* Otto von Böhtlingk (1815–1904) \
    *Pâṇini's Grammatik* · Zweite Auflage · Leipzig 1887 (Verlag von H. Haessel) \
    Auf Basis der Originalscans der Universitätsbibliothek Heidelberg (Bibliotheca Palatina) \
    \
    *Dichte Faksimile-Neuausgabe:* AlexandriaSandwich Digital Humanities Pipeline (2026) \
    *Herausgeber & Neusatz:* Marco Demarmels (Birchville Foundation) \
    *1:1-Seitenparität:* Jede Seite dieser Ausgabe entspricht exakt der entsprechenden Seite des Originaldrucks (S. 1–476). \
    *Satzspiegel & Typografie:* Rekonstruktion des Leipziger Originalspiegels in STIX Two Text und Noto Serif Devanagari mit adaptiver Durchschuss- und Grad-Optimierung. \
    *Alignment:* 100 % Abdeckung (14 Śiva-Sūtras + 3.983 Aṣṭādhyāyī-Sūtras) \
    \
    *Urheberrecht & Lizenzen:* \
    Historisches Originalwerk: Gemeinfrei (Public Domain worldwide) \
    Digitale Ausgabe, Typst-Code & TEI-Encoding: MIT License / CC-BY-SA 4.0
  ]
]

#pagebreak()

// Seite iii: Haupttitel
#align(center)[
  #v(2.0cm)
  #text(22pt, weight: "bold", font: ("STIX Two Text", "Noto Serif Devanagari"))[PĀṆINI'S GRAMMATIK]
  
  #v(0.8cm)
  #text(11pt, style: "italic")[herausgegeben, übersetzt, erläutert und mit verschiedenen Indices versehen]
  
  #v(0.4cm)
  #text(10pt)[von]
  
  #v(0.4cm)
  #text(16pt, weight: "bold")[OTTO BÖHTLINGK]
  
  #v(0.8cm)
  #text(11pt, style: "italic")[Zweite Auflage · Faksimile-Neusatz mit 1:1-Seitenparität]
  
  #v(0.6cm)
  #line(length: 25%, stroke: 0.5pt)
  #v(0.6cm)
  
  #text(10.5pt)[LEIPZIG \ VERLAG VON H. HAESSEL \ 1887]
]

#pagebreak()

// Seite iv: Vorwort zur dichten Faksimile-Testausgabe
#heading(level: 1, numbering: none, outlined: false)[Vorwort zur dichten Faksimile-Ausgabe]

#v(0.5em)

Die vorliegende Edition von Otto von Böhtlingks *Grammatik des Pāṇini* (Leipzig 1887) rekonstruiert den historischen Originaldruck in einer *strengen 1:1-Seitenparität*:

*Jede Textseite dieser Neuausgabe entspricht exakt einer Seite des Leipziger Originalbandes (Seiten 1 bis 476).*

*Typografische Rekonstruktion des Originals:*
1. *Exakte Seitenidentität:* Sūtra-Bestand und Textumfang jeder Seite sind absolut identisch mit dem historischen Buch von 1887. Sämtliche philologischen Zitate („Böhtlingk S. X“) können direkt und ohne Seitenverschiebung aufgeschlagen werden.
2. *Harmonische Raumausnutzung (Adaptive Typografie):* Statt einer pauschalen Verkleinerung aller Seiten passt sich die typografische Dichte (Schriftgrad von 8,2 bis 9,8 pt, Durchschuss 0,28 bis 0,48 em, Spatium 0,08 bis 0,85 em) feinfühlig dem jeweiligen Textumfang an. Leicht besetzte Seiten füllen den Satzspiegel großzügig und elegant aus, während textstarke Seiten sauber und überlappungsfrei auf genau einer Seite stehen.
3. *Erhabene Śiva-Sūtras auf Seite 1:* Die 14 kanonischen Māheśvara-Sūtras sind auf der Eröffnungsseite großzügig, wohlproportioniert und in authentischem Zweiklang mit Böhtlingks historischer Einleitung gesetzt.
4. *Authentische Kolophone:* Am Ende jedes Pāda ist der überlieferte Sanskrit-Abschlussvermerk (z. B. #text(font: ("Noto Serif Devanagari"))[॥ इति प्रथमस्याध्यायस्य प्रथमः पादः ॥]) gesetzt.
5. *Originale Randverweise:* Die Sūtra-Nummern am Außenrand (#text(style: "italic")[1, 1, 1.]) und die lebenden Kolumnentitel führen wie bei Haessel 1887 durch das gesamte Werk.

#v(1.5em)
#align(right)[
  _Birchville Foundation, im Oktober 2026_ \
  *Marco Demarmels*
]

#pagebreak()

// =============================================================================
// 2. INHALTSÜBERSICHT
// =============================================================================

#heading(level: 1, numbering: none, outlined: false)[Inhaltsübersicht]

#v(0.6em)

#grid(
  columns: (1fr, auto),
  row-gutter: 0.55em,
  [#text(weight: "bold")[Śiva-Sūtras (Akṣarasamāmnāya)]], [#text(weight: "bold")[S. 1]],
  [#text(weight: "bold")[Erster Adhyāya] (1.1–1.4)], [#text(weight: "bold")[S. 2–51]],
  [#h(1.2em) 1. Pāda: वृद्धिरादैच् (Vṛddhirādaic, 1.1.1–75)], [S. 2],
  [#h(1.2em) 2. Pāda: गाङ्कुटादिभ्यो ऽञ्णिन्ङित् (Gāṅkuṭādibhyo, 1.2.1–73)], [S. 11],
  [#h(1.2em) 3. Pāda: भूवादयो धातवः (Bhūvādayo dhātavaḥ, 1.3.1–93)], [S. 21],
  [#h(1.2em) 4. Pāda: आ कडारादेका संज्ञा (Ā kaḍārādekā saṃjñā, 1.4.1–110)], [S. 31],
  [#text(weight: "bold")[Zweiter Adhyāya] (2.1–2.4)], [#text(weight: "bold")[S. 43–74]],
  [#h(1.2em) 1. Pāda: समर्थः पदविधिः (Samarthaḥ padavidhiḥ, 2.1.1–72)], [S. 43],
  [#h(1.2em) 2. Pāda: पूर्वो ऽपरो ऽधरोत्तराणि (Pūrvo 'paro, 2.2.1–38)], [S. 52],
  [#h(1.2em) 3. Pāda: अनभिहिते (Anabhihite, 2.3.1–73)], [S. 56],
  [#h(1.2em) 4. Pāda: द्विगुरेकवचनम् (Dvigurekavacanam, 2.4.1–85)], [S. 65],
  [#text(weight: "bold")[Dritter Adhyāya] (3.1–3.4)], [#text(weight: "bold")[S. 75–148]],
  [#h(1.2em) 1. Pāda: प्रत्ययः (Pratyayaḥ, 3.1.1–150)], [S. 75],
  [#h(1.2em) 2. Pāda: कर्मण्यण् (Karmaṇyaṇ, 3.2.1–188)], [S. 93],
  [#h(1.2em) 3. Pāda: उणादयो बहुलम् (Uṇādayo bahulam, 3.3.1–176)], [S. 114],
  [#h(1.2em) 4. Pāda: धातुसम्बन्धे प्रत्ययाः (Dhātusambandhe, 3.4.1–117)], [S. 134],
  [#text(weight: "bold")[Vierter Adhyāya] (4.1–4.4)], [#text(weight: "bold")[S. 149–220]],
  [#h(1.2em) 1. Pāda: ङ्याप्प्रातिपदिकात् (Ṅyāpprātipadikāt, 4.1.1–178)], [S. 149],
  [#h(1.2em) 2. Pāda: तेन रक्तं रागात् (Tena raktaṃ rāgāt, 4.2.1–145)], [S. 170],
  [#h(1.2em) 3. Pāda: युष्मदस्मदोरन्यतरस्याम् (Yuşmadasmador, 4.3.1–168)], [S. 187],
  [#h(1.2em) 4. Pāda: प्राग्वहतेष्ठञ् (Prāgvahateṣṭhañ, 4.4.1–144)], [S. 206],
  [#text(weight: "bold")[Fünfter Adhyāya] (5.1–5.4)], [#text(weight: "bold")[S. 221–282]],
  [#h(1.2em) 1. Pāda: प्राङ्क्रीताच्छः (Prāṅkrītācchaḥ, 5.1.1–136)], [S. 221],
  [#h(1.2em) 2. Pāda: धान्यनां भवने क्षेत्रे खञ् (Dhānyānāṃ, 5.2.1–140)], [S. 236],
  [#h(1.2em) 3. Pāda: प्राग्दिशो विभक्तिः (Prāgdiśo vibhaktiḥ, 5.3.1–119)], [S. 251],
  [#h(1.2em) 4. Pāda: पादशतस्य संख्यादेर्वीप्सायाम् (Pādaśatasya, 5.4.1–160)], [S. 264],
  [#text(weight: "bold")[Sechster Adhyāya] (6.1–6.4)], [#text(weight: "bold")[S. 283–373]],
  [#h(1.2em) 1. Pāda: एकाचो द्वे प्रथमस्य (Ekāco dve prathamasya, 6.1.1–223)], [S. 283],
  [#h(1.2em) 2. Pāda: बहुव्रीहौ प्रकृत्या पूर्वपदम् (Bahuvrīhau, 6.2.1–199)], [S. 311],
  [#h(1.2em) 3. Pāda: अलुगुत्तरपदे (Aluguttarapade, 6.3.1–139)], [S. 335],
  [#h(1.2em) 4. Pāda: अङ्गस्य (Aṅgasya, 6.4.1–175)], [S. 351],
  [#text(weight: "bold")[Siebenter Adhyāya] (7.1–7.4)], [#text(weight: "bold")[S. 374–427]],
  [#h(1.2em) 1. Pāda: युवोरनाकौ (Yuvoranākau, 7.1.1–103)], [S. 374],
  [#h(1.2em) 2. Pāda: सिचि वृद्धिः परस्मैपदेषु (Sici vṛddhiḥ, 7.2.1–118)], [S. 387],
  [#h(1.2em) 3. Pāda: लघोरुपधायाः (Laghorupadhāyāḥ, 7.3.1–120)], [S. 402],
  [#h(1.2em) 4. Pāda: णिच्युपसंख्यानम् (Ṇicyupasaṃkhyānam, 7.4.1–97)], [S. 417],
  [#text(weight: "bold")[Achter Adhyāya] (8.1–8.4)], [#text(weight: "bold")[S. 428–476]],
  [#h(1.2em) 1. Pāda: सर्वस्य द्वे (Sarvasya dve, 8.1.1–74)], [S. 428],
  [#h(1.2em) 2. Pāda: पूर्वत्रासिद्धम् (Pūrvatrāsiddham, 8.2.1–108)], [S. 438],
  [#h(1.2em) 3. Pāda: रषाभ्यां नो णः समानपदे (Raṣābhyāṃ, 8.3.1–119)], [S. 452],
  [#h(1.2em) 4. Pāda: स्तोः श्चुना श्चुः (Stoḥ ścunā ścuḥ, 8.4.1–68)], [S. 467],
  [#text(weight: "bold")[Nachträge und Verbesserungen (Corrigenda)]], [#text(weight: "bold")[S. 477–480]],
)

#pagebreak()

// =============================================================================
// 3. ARABISCHE SEITENZÄHLUNG & DYNAMISCHE LEBENDE KOLUMNENTITEL (1:1 PARITÄT)
// =============================================================================

#counter(page).update(1)

#set page(
  header: context {
    let loc = here()
    let p_num = counter(page).get().first()
    
    // Keine Kopfzeile auf Seite 1 (Śiva-Sūtras Titel)
    if p_num == 1 {
      return none
    }

    // Kopfzeile für Corrigenda (ab Seite 477)
    if p_num >= 477 {
      return [
        #if calc.even(p_num) [
          #text(8.5pt, weight: "bold")[#p_num]
          #h(1fr)
          #text(8pt, font: ("STIX Two Text", "Noto Serif Devanagari"))[#smallcaps[Nachträge und Verbesserungen (Corrigenda)]]
          #h(1fr)
          #text(8.5pt, weight: "bold", fill: rgb("#03192e"))[Böhtlingk 1887]
        ] else [
          #text(8.5pt, weight: "bold", fill: rgb("#03192e"))[Böhtlingk 1887]
          #h(1fr)
          #text(8pt, style: "italic", fill: rgb("#334155"))[Nachträge und Verbesserungen (Corrigenda)]
          #h(1fr)
          #text(8.5pt, weight: "bold")[#p_num]
        ]
        #v(0.25em)
        #line(length: 100%, stroke: 0.35pt + rgb("#d8d2c6"))
      ]
    }

    let sutras_on_page = query(selector(<sutra-marker>)).filter(m => counter(page).at(m.location()).first() == p_num)
    let last_sutra_ref = if sutras_on_page.len() > 0 {
      let v = sutras_on_page.last().value
      str(v.adh) + ", " + str(v.pada) + ", " + str(v.snum) + "."
    } else {
      let prev_sutras = query(selector(<sutra-marker>).before(loc))
      if prev_sutras.len() > 0 {
        let v = prev_sutras.last().value
        str(v.adh) + ", " + str(v.pada) + ", " + str(v.snum) + "."
      } else { "" }
    }
    
    let adh_roman = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII")
    let adh_text = if sutras_on_page.len() > 0 {
      let v = sutras_on_page.first().value
      adh_roman.at(v.adh - 1, default: "I") + ". Adhyāya. " + str(v.pada) + ". Pāda."
    } else {
      let prev = query(selector(<sutra-marker>).before(loc))
      if prev.len() > 0 {
        let v = prev.last().value
        adh_roman.at(v.adh - 1, default: "I") + ". Adhyāya. " + str(v.pada) + ". Pāda."
      } else { "" }
    }

    [
      #if calc.even(p_num) [
        #text(8.5pt, weight: "bold")[#p_num]
        #h(1fr)
        #text(8pt, font: ("STIX Two Text", "Noto Serif Devanagari"))[#adh_text]
        #h(1fr)
        #text(8.5pt, weight: "bold", fill: rgb("#03192e"))[#last_sutra_ref]
      ] else [
        #text(8.5pt, weight: "bold", fill: rgb("#03192e"))[#last_sutra_ref]
        #h(1fr)
        #text(8pt, style: "italic", fill: rgb("#334155"))[#adh_text]
        #h(1fr)
        #text(8.5pt, weight: "bold")[#p_num]
      ]
      #v(0.25em)
      #line(length: 100%, stroke: 0.35pt + rgb("#d8d2c6"))
    ]
  },
  footer: context {
    let p_num = counter(page).get().first()
    if p_num == 1 [
      #grid(
        columns: (1fr, auto),
        [#text(9pt, style: "italic", fill: rgb("#334155"))[Pāṇini's Grammatik.]],
        [#text(9pt, weight: "bold")[1]]
      )
    ] else {
      none
    }
  }
)

// =============================================================================
// 4. ŚIVA-SŪTRAS (AKṢARASAMĀMNĀYA) — BÖHTLINGK S. 1 (HISTORISCHES LEIPZIGER LAYOUT)
// =============================================================================

#v(1.8cm)

#grid(
  columns: (auto, 1fr, auto),
  [#text(9.5pt, weight: "bold")[1]],
  align(center)[#text(16pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[॥ अथ शब्दानुशासनम् ॥]],
  []
)

#v(1.2cm)

#align(center)[
  #text(12.5pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT", "Kohinoor Devanagari"))[
    #grid(
      columns: (1fr, 1fr, 1fr, 1fr),
      align: center,
      row-gutter: 1.5em,
      [अ इ उ ण् ॥ १ ॥], [ऋ ऌ क् ॥ २ ॥], [ए ओ ङ् ॥ ३ ॥], [ऐ औ च् ॥ ४ ॥],
      [ह य व र ट् ॥ ५ ॥], [लँ ण् ॥ ६ ॥], [ञ म ङ ण न म् ॥ ७ ॥], [झ भ ञ् ॥ ८ ॥],
      grid.cell(colspan: 4)[
        #grid(
          columns: (1.2fr, 1.4fr, 1.8fr),
          align: center,
          [घ ढ ध ष् ॥ ९ ॥], [ज ब ग ड द श् ॥ १० ॥], [ख फ छ ठ थ च ट त व् ॥ ११ ॥]
        )
      ],
      grid.cell(colspan: 4)[
        #grid(
          columns: (1fr, 1.2fr, 1fr),
          align: center,
          [क प य् ॥ १२ ॥], [श ष स र् ॥ १३ ॥], [ह ल् ॥ १४ ॥]
        )
      ]
    )
  ]
]

#v(1.6cm)

#text(10.0pt)[
#set par(justify: true, leading: 0.52em)
#h(1.5em) Die vorstehenden, das Alphabet enthaltenden Sūtra führen den Namen #text(font: ("Noto Serif Devanagari"))[प्रत्याहारसूत्राणि] oder #text(font: ("Noto Serif Devanagari"))[अक्षरसमाम्नाय], später auch #text(font: ("Noto Serif Devanagari"))[शिवसूत्राणि] oder #text(font: ("Noto Serif Devanagari"))[माहेश्वराणि सूत्राणि]. Am Ende eines jeden Sūtra steht ein Consonant mit dem Virāma, der an dieser Stelle nicht zum Alphabet gehört, sondern nur dazu dient eine Anzahl von Lauten in kürzester Form zu bezeichnen. Dieses geschieht auf die Weise, dass man den ersten Laut der zusammenzufassenden Gruppe mit dem auf den letzten Laut dieser Gruppe folgenden vocallosen Consonanten verbindet (1, 1, 71). So bezeichnet z. B. #text(font: ("Noto Serif Devanagari"))[अण्] die Vocale #text(font: ("Noto Serif Devanagari"))[अ], #text(font: ("Noto Serif Devanagari"))[इ], #text(font: ("Noto Serif Devanagari"))[उ]; #text(font: ("Noto Serif Devanagari"))[एङ्] die Diphthonge #text(font: ("Noto Serif Devanagari"))[ए], #text(font: ("Noto Serif Devanagari"))[ओ]; #text(font: ("Noto Serif Devanagari"))[एच्] alle Diphthonge; #text(font: ("Noto Serif Devanagari"))[अच्] alle Vocale, #text(font: ("Noto Serif Devanagari"))[हल्] alle Consonanten, #text(font: ("Noto Serif Devanagari"))[अल्] alle Laute. Die Consonanten sind so angeordnet, wie es die Grammatik bei der Lehre von den Lautveränderungen verlangt. #text(font: ("Noto Serif Devanagari"))[ह] erscheint zweimal, um die Sigla (प्रत्याहार) #text(font: ("Noto Serif Devanagari"))[हल्] und #text(font: ("Noto Serif Devanagari"))[हश्] bilden zu können. Um die Consonanten in der Reihenfolge, wie wir sie kennen, nach Gruppen zusammenzufassen, setzt Pāṇini an den ersten Consonanten der Gruppe den Vocal #text(font: ("Noto Serif Devanagari"))[उ]; so bezeichnet #text(font: ("Noto Serif Devanagari"))[कु] die Gutturale, #text(font: ("Noto Serif Devanagari"))[चु] die Palatale u. s. w. (1, 1, 69). Die langen Vocale fehlen im Alphabet, weil in Pāṇini's Grammatik der kurze Vocal auch die entsprechende Länge in sich begreift; soll diese ausgeschlossen werden, so wird dem kurzen Vocal #text(font: ("Noto Serif Devanagari"))[त्] angefügt (1, 1, 70). Pāṇini verwendet folgende 40 Sigla: #text(font: ("Noto Serif Devanagari"))[अक्, अच्, अट्, अण्] (als Bezeichnung zweier Gruppen), #text(font: ("Noto Serif Devanagari"))[अम्, अल्, अश्, इक्, इच्, इण्, उक्, एङ्, एच्, ऐच्, खय्, खर्, ङम्, चर्, छव्, जश्, झय्, झर्, झल्, झश्, झष्, बश्, भष्, मय्, यञ्, यण्, यम्, यय्, यर्, रल्, वल्, वश्, शर्, शल्, हल्] und #text(font: ("Noto Serif Devanagari"))[हश्].
]

#pagebreak()

// =============================================================================
// 5. AṢṬĀDHYĀYĪ SŪTRAPĀṬHA (S. 2–476) — ADAPTIVE 1:1 SEITENPARITÄT
// =============================================================================

#let pages_data = json("/data/ashtadhyayi_facsimile_dense.json")

#for p_info in pages_data {
  let prof = p_info.profile
  let deva_sz = eval(prof.deva_size)
  let body_sz = eval(prof.body_size)
  let body_lead = eval(prof.body_leading)
  let comm_sz = eval(prof.comm_size)
  let comm_lead = eval(prof.comm_leading)
  let sutra_sp = eval(prof.sutra_spacing)

  for s in p_info.sutras [
    #metadata((adh: s.adhyaya, pada: s.pada, snum: s.sutra_num, ref: s.ref)) <sutra-marker>
    #block(width: 100%, breakable: true)[
      #block(width: 100%, breakable: false)[
        #grid(
          columns: (1fr, auto),
          align: (left + bottom, right + bottom),
          gutter: 0.8em,
          [
            #text(deva_sz, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT", "Kohinoor Devanagari"))[
              #s.canonical_devanagari ॥ #s.sutra_num_deva ॥
            ]
            #if s.canonical_iast != "" [
              #h(0.4em)
              #text(body_sz * 0.82, style: "italic", fill: rgb("#475569"))[(#s.canonical_iast)]
            ]
          ],
          [
            #text(body_sz, font: ("STIX Two Text", "Noto Serif Devanagari"), fill: rgb("#03192e"))[
              #str(s.adhyaya), #str(s.pada), #str(s.sutra_num).
            ]
          ]
        )
        #v(0.12em)
        #if s.translation != "" [
          #set par(leading: body_lead)
          #text(body_sz, fill: rgb("#03192e"))[#s.translation]
        ]
      ]
      #if s.commentary != "" [
        #v(0.12em)
        #pad(left: 0.8em)[
          #set par(leading: comm_lead)
          #text(comm_sz, fill: rgb("#1e2d37"))[#s.commentary]
        ]
      ]
      #if s.colophon != "" [
        #v(0.25em)
        #align(center)[
          #text(deva_sz * 0.88, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[#s.colophon]
        ]
        #v(0.18em)
      ]
      #v(sutra_sp)
    ]
  ]
  if p_info.page_num < 476 [
    #pagebreak()
  ]
}

#pagebreak()

// =============================================================================
// 6. NACHTRÄGE UND VERBESSERUNGEN (CORRIGENDA) — BÖHTLINGK S. 477–480
// =============================================================================

#let corrigenda_data = json("/data/corrigenda.json")

#heading(level: 1, numbering: none, outlined: false)[Nachträge und Verbesserungen (Corrigenda)]

#v(0.3em)
#text(8.5pt, style: "italic", fill: rgb("#334155"))[
  Otto von Böhtlingks originale Druckfehlerkorrekturen und philologische Nachträge zum Text und Kommentar (Leipzig 1887, S. 477–480).
]
#v(0.6em)

#for item in corrigenda_data [
  #block(width: 100%, breakable: false)[
    #rect(width: 100%, stroke: 0.35pt + rgb("#d8d2c6"), inset: 0.55em, radius: 2pt)[
      #text(8.5pt, fill: rgb("#1e2d37"))[#item.text]
    ]
    #v(0.30em)
  ]
]
