// =============================================================================
// Birchville Scholarly Synthesis — Dichte Faksimile-Ausgabe (Böhtlingk 1887)
// Exakte 1:1-Seitenparität mit adaptivem Satzspiegel & maximaler Raumausnutzung
// =============================================================================

#set document(
  title: "Pāṇini's Grammatik (Otto von Böhtlingk, 1887) — Dichte Faksimile-Ausgabe",
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

#import "common.typ": to-deva, parse-len, shiva_canonical, render-front-imprint, render-main-title

#let structure = json("/data/edition_structure.json")
#let pages_data = json("/data/ashtadhyayi_facsimile_dense.json")

// =============================================================================
// 1. TITELEI & IMPRESSUM (BIRCHVILLE SCHOLARLY SYNTHESIS)
// =============================================================================

#render-front-imprint(
  subtitle_line: "Dichte Faksimile-Ausgabe (1:1-Seitenparität mit dem Originaldruck)",
  edition_bullets: (
    [*Dichte Faksimile-Neuausgabe:* AlexandriaSandwich Digital Humanities Pipeline (2026)],
    [*Herausgeber & Neusatz:* Marco Demarmels (Birchville Foundation)],
    [*1:1-Seitenparität:* Jede Seite dieser Ausgabe entspricht exakt der entsprechenden Seite des Originaldrucks (S. 1–476).],
    [*Satzspiegel & Typografie:* Rekonstruktion des Leipziger Originalspiegels in STIX Two Text und Noto Serif Devanagari mit adaptiver Durchschuss- und Grad-Optimierung.],
    [*Alignment:* 100 % Abdeckung (14 Śiva-Sūtras + 3.983 Aṣṭādhyāyī-Sūtras)],
  ),
)

#render-main-title("Zweite Auflage · Faksimile-Neusatz mit 1:1-Seitenparität")

// Seite iv: Vorwort zur dichten Faksimile-Ausgabe
#heading(level: 1, numbering: none, outlined: false)[Vorwort zur dichten Faksimile-Ausgabe]

#v(0.5em)

Die vorliegende Edition von Otto von Böhtlingks *Grammatik des Pāṇini* (Leipzig 1887) rekonstruiert den historischen Originaldruck in einer *strikten 1:1-Seitenparität*:

*Jede Textseite dieser Neuausgabe entspricht exakt einer Seite des Leipziger Originalbandes (Seiten 1 bis 476).*

*Typografische Rekonstruktion des Originals:*
1. *Exakte Seitenidentität:* Sūtra-Bestand und Textumfang jeder Seite sind identisch mit dem historischen Buch von 1887. Sämtliche philologischen Zitate („Böhtlingk S. X“) können direkt und ohne Seitenverschiebung aufgeschlagen werden.
2. *Harmonische Raumausnutzung (Adaptive Typografie):* Statt einer pauschalen Verkleinerung aller Seiten passt sich die typografische Dichte (Schriftgrad von 8,1 bis 9,6 pt, Durchschuss 0,26 bis 0,45 em, Spatium 0,06 bis 0,95 em) dem jeweiligen Textumfang an. Leicht besetzte Seiten füllen den Satzspiegel gleichmäßig aus, während textstarke Seiten ohne Überlauf auf genau einer Seite stehen.
3. *Eröffnungs-Tableau auf Seite 1:* Die 14 kanonischen Māheśvara-Sūtras sind auf der Eröffnungsseite zweispaltig im Zweiklang mit Böhtlingks historischer Einleitung gesetzt.
4. *Authentische Kolophone:* Am Ende jedes Pāda ist der überlieferte Sanskrit-Abschlussvermerk (z. B. #text(font: ("Noto Serif Devanagari"))[॥ इति प्रथमस्याध्यायस्य प्रथमः पादः ॥]) gesetzt.
5. *Originale Randverweise:* Die Sūtra-Nummern am Außenrand (#text(style: "italic")[1, 1, 1.]) und die lebenden Kolumnentitel führen wie bei Haessel 1887 durch das gesamte Werk.

#v(1.5em)
#align(right)[
  _Birchville Foundation, im Oktober 2026_ \
  *Marco Demarmels*
]

#pagebreak()

// =============================================================================
// 2. INHALTSÜBERSICHT (AUS EDITION_STRUCTURE.JSON)
// =============================================================================

#heading(level: 1, numbering: none, outlined: false)[Inhaltsübersicht]

#v(0.6em)

#{
  let toc_rows = (
    [#text(weight: "bold")[Śiva-Sūtras (Akṣarasamāmnāya)]],
    [#text(weight: "bold")[S. #structure.shiva_sutras_page]],
  )
  for adh in structure.adhyayas {
    toc_rows.push([#text(weight: "bold")[#adh.title_de] (#adh.pada_range)])
    toc_rows.push([#text(weight: "bold")[S. #adh.start_page–#adh.end_page]])
    for p in adh.padas {
      toc_rows.push([#h(1.2em) #p.num. Pāda: #p.incipit (#p.incipit_iast, #p.sutra_range)])
      toc_rows.push([S. #p.start_page])
    }
  }
  let corr_start = structure.facsimile_corrigenda_pages.at(0)
  let corr_end = structure.facsimile_corrigenda_pages.at(1)
  toc_rows.push([#text(weight: "bold")[Nachträge und Verbesserungen (Corrigenda)]])
  toc_rows.push([#text(weight: "bold")[S. #corr_start–#corr_end]])

  grid(
    columns: (1fr, auto),
    row-gutter: 0.55em,
    ..toc_rows
  )
}

#pagebreak()

// =============================================================================
// 3. ARABISCHE SEITENZÄHLUNG & DYNAMISCHE LEBENDE KOLUMNENTITEL (1:1 PARITÄT)
// =============================================================================

#counter(page).update(1)

#set page(
  header: context {
    let p_num = counter(page).get().first()

    // Keine Kopfzeile auf Seite 1 (Śiva-Sūtras Titel)
    if p_num == 1 {
      return none
    }

    // Kopfzeile für Corrigenda (ab Seite 477)
    if p_num >= structure.facsimile_corrigenda_pages.at(0) {
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
          #text(8pt, font: ("STIX Two Text", "Noto Serif Devanagari"))[#smallcaps[Nachträge und Verbesserungen (Corrigenda)]]
          #h(1fr)
          #text(8.5pt, weight: "bold")[#p_num]
        ]
        #v(0.25em)
        #line(length: 100%, stroke: 0.35pt + rgb("#d8d2c6"))
      ]
    }

    // O(1)-Direktzugriff statt O(N*P)-Markerabfrage
    let p_idx = p_num - 2
    let p_meta = if p_idx >= 0 and p_idx < pages_data.len() { pages_data.at(p_idx) } else { none }
    let adh_text = if p_meta != none { p_meta.header_adh_str } else { "" }
    let last_sutra_ref = if p_meta != none { p_meta.last_sutra_ref } else { "" }

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
        #text(8pt, font: ("STIX Two Text", "Noto Serif Devanagari"))[#adh_text]
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
// 4. ŚIVA-SŪTRAS (AKṢARASAMĀMNĀYA) — BÖHTLINGK S. 1 (KLASSISCHES 2-SPALTEN-LAYOUT MIT EINFÜHRUNG)
// =============================================================================

#v(0.2cm)

#grid(
  columns: (auto, 1fr, auto),
  [#text(9.5pt, weight: "bold")[1]],
  align(center)[#text(14.5pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[॥ अथ शब्दानुशासनम् ॥]],
  []
)

#v(-0.2em)
#align(center)[
  #text(8.2pt, style: "italic", fill: rgb("#334155"))[
    Śiva-Sūtras (Akṣarasamāmnāya) — Die 14 kanonischen Lautgruppen der Pratyāhāras (Böhtlingk 1887, S. 1).
  ]
]
#v(0.5em)

#grid(
  columns: (1fr, 1fr),
  gutter: 1.8em,
  [
    #for s in shiva_canonical.slice(0, 7) [
      #align(center)[
        #text(11.0pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[
          #s.at(1) ॥ #to-deva(s.at(0)) ॥
        ]
        #v(-0.35em)
        #text(7.8pt, style: "italic", fill: rgb("#334155"))[
          (Śiva-Sūtra #s.at(0) — #s.at(2))
        ]
      ]
      #v(0.35em)
    ]
  ],
  [
    #for s in shiva_canonical.slice(7, 14) [
      #align(center)[
        #text(11.0pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[
          #s.at(1) ॥ #to-deva(s.at(0)) ॥
        ]
        #v(-0.35em)
        #text(7.8pt, style: "italic", fill: rgb("#334155"))[
          (Śiva-Sūtra #s.at(0) — #s.at(2))
        ]
      ]
      #v(0.35em)
    ]
  ]
)

#v(0.4em)
#line(length: 100%, stroke: 0.35pt + rgb("#d8d2c6"))
#v(0.3em)

#text(8.6pt)[
#set par(justify: true, leading: 0.40em)
#h(1.2em) Die vorstehenden, das Alphabet enthaltenden Sūtra führen den Namen #text(font: ("Noto Serif Devanagari"))[प्रत्याहारसूत्राणि] oder #text(font: ("Noto Serif Devanagari"))[अक्षरसमाम्नाय], später auch #text(font: ("Noto Serif Devanagari"))[शिवसूत्राणि] oder #text(font: ("Noto Serif Devanagari"))[माहेश्वराणि सूत्राणि]. Am Ende eines jeden Sūtra steht ein Consonant mit dem Virāma, der an dieser Stelle nicht zum Alphabet gehört, sondern nur dazu dient eine Anzahl von Lauten in kürzester Form zu bezeichnen. Dieses geschieht auf die Weise, dass man den ersten Laut der zusammenzufassenden Gruppe mit dem auf den letzten Laut dieser Gruppe folgenden vocallosen Consonanten verbindet (1, 1, 71). So bezeichnet z. B. #text(font: ("Noto Serif Devanagari"))[अण्] die Vocale #text(font: ("Noto Serif Devanagari"))[अ], #text(font: ("Noto Serif Devanagari"))[इ], #text(font: ("Noto Serif Devanagari"))[उ]; #text(font: ("Noto Serif Devanagari"))[एङ्] die Diphthonge #text(font: ("Noto Serif Devanagari"))[ए], #text(font: ("Noto Serif Devanagari"))[ओ]; #text(font: ("Noto Serif Devanagari"))[एच्] alle Diphthonge; #text(font: ("Noto Serif Devanagari"))[अच्] alle Vocale, #text(font: ("Noto Serif Devanagari"))[हल्] alle Consonanten, #text(font: ("Noto Serif Devanagari"))[अल्] alle Laute. Die Consonanten sind so angeordnet, wie es die Grammatik bei der Lehre von den Lautveränderungen verlangt. #text(font: ("Noto Serif Devanagari"))[ह] erscheint zweimal, um die Sigla (प्रत्याहार) #text(font: ("Noto Serif Devanagari"))[हल्] und #text(font: ("Noto Serif Devanagari"))[हश्] bilden zu können. Um die Consonanten in der Reihenfolge, wie wir sie kennen, nach Gruppen zusammenzufassen, setzt Pāṇini an den ersten Consonanten der Gruppe den Vocal #text(font: ("Noto Serif Devanagari"))[उ]; so bezeichnet #text(font: ("Noto Serif Devanagari"))[कु] die Gutturale, #text(font: ("Noto Serif Devanagari"))[चु] die Palatale u. s. w. (1, 1, 69). Die langen Vocale fehlen im Alphabet, weil in Pāṇini's Grammatik der kurze Vocal auch die entsprechende Länge in sich begreift; soll diese ausgeschlossen werden, so wird dem kurzen Vocal #text(font: ("Noto Serif Devanagari"))[त्] angefügt (1, 1, 70). Pāṇini verwendet folgende 40 Sigla: #text(font: ("Noto Serif Devanagari"))[अक्, अच्, अट्, अण्] (als Bezeichnung zweier Gruppen), #text(font: ("Noto Serif Devanagari"))[अम्, अल्, अश्, इक्, इच्, इण्, उक्, एङ्, एच्, ऐच्, खय्, खर्, ङम्, चर्, छव्, जश्, झय्, झर्, झल्, झश्, झष्, बश्, भष्, मय्, यञ्, यण्, यम्, यय्, यर्, रल्, वल्, वश्, शर्, शल्, हल्] und #text(font: ("Noto Serif Devanagari"))[हश्].
]

#pagebreak()

// =============================================================================
// 5. AṢṬĀDHYĀYĪ SŪTRAPĀṬHA (S. 2–476) — ADAPTIVE 1:1 SEITENPARITÄT
// =============================================================================

#for p_info in pages_data {
  let prof = p_info.profile
  let deva_sz = parse-len(prof.deva_size)
  let body_sz = parse-len(prof.body_size)
  let body_lead = parse-len(prof.body_leading)
  let comm_sz = parse-len(prof.comm_size)
  let comm_lead = parse-len(prof.comm_leading)
  let sutra_sp = parse-len(prof.sutra_spacing)

  for s in p_info.sutras [
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
// 6. NACHTRÄGE UND VERBESSERUNGEN (CORRIGENDA) — BÖHTLINGK S. 477–478
// =============================================================================

#let corrigenda_data = json("/data/corrigenda.json")

#heading(level: 1, numbering: none, outlined: false)[Nachträge und Verbesserungen (Corrigenda)]

#v(0.3em)
#text(8.5pt, style: "italic", fill: rgb("#334155"))[
  Otto von Böhtlingks originale Druckfehlerkorrekturen und philologische Nachträge zum Text und Kommentar (Leipzig 1887, S. 477–478).
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
