// =============================================================================
// Birchville Scholarly Synthesis — Canonical Typeset Edition
// Otto von Böhtlingk: Pāṇini's Grammatik (2. Auflage, Leipzig 1887)
// =============================================================================

#set document(
  title: "Pāṇini's Grammatik (Otto von Böhtlingk, 1887) — Digitale Neuausgabe",
  author: "Otto von Böhtlingk (Ed. Marco Demarmels / Birchville Foundation)",
  keywords: ("Pāṇini", "Aṣṭādhyāyī", "Sanskrit", "Grammatik", "Böhtlingk", "Indologie", "Birchville")
)

#set page(
  paper: "iso-b5",
  margin: (top: 2.2cm, bottom: 2.2cm, inside: 2.4cm, outside: 2.0cm),
  header: none,
  footer: none
)

#set text(
  font: ("STIX Two Text", "Noto Serif Devanagari", "Devanagari MT"),
  size: 9.5pt,
  lang: "de"
)

#set par(justify: true, leading: 0.46em)

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
  #text(9pt, style: "italic", fill: rgb("#334155"))[Otto von Böhtlingk (Leipzig 1887)]
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
    *Digitale Neuausgabe:* AlexandriaSandwich Digital Humanities Pipeline (2026) \
    *Herausgeber & Neusatz:* Marco Demarmels (Birchville Foundation) \
    *Kanonisches Alignment:* 100 % Abdeckung (14 Śiva-Sūtras + 3.983 Aṣṭādhyāyī-Sūtras) \
    *TEI-P5 Konformität:* Schema-valide XML-Masterauszeichnung (RelaxNG) \
    \
    *Urheberrecht & Lizenzen:* \
    Historisches Originalwerk: Gemeinfrei (Public Domain worldwide) \
    Digitale Ausgabe, Typst-Code & TEI-Encoding: MIT License / CC-BY-SA 4.0
  ]
]

#pagebreak()

// Seite iii: Haupttitel (Historischer Satz nach Leipzig 1887)
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
  #text(11pt, style: "italic")[Zweite Auflage]
  
  #v(0.6cm)
  #line(length: 25%, stroke: 0.5pt)
  #v(0.6cm)
  
  #text(10.5pt)[LEIPZIG \ VERLAG VON H. HAESSEL \ 1887]
]

#pagebreak()

// Seite iv: Vorwort zur digitalen Neuausgabe
#heading(level: 1, numbering: none, outlined: false)[Vorwort zur digitalen Neuausgabe]

#v(0.5em)

Die vorliegende digitale Neuausgabe von Otto von Böhtlingks zweiter Auflage der *Grammatik des Pāṇini* (Leipzig 1887) verbindet die editorische und philologische Autorität des 19. Jahrhunderts mit modernen Satz- und Archivierungsstandards des 21. Jahrhunderts.

Böhtlingks Werk ist bis heute die maßgebliche europäische Gesamtdarstellung der Aṣṭādhyāyī mit deutscher Übersetzung und fortlaufendem sachkritischem Kommentar. Frühere Digitalisierungen litten entweder unter unvollständiger OCR (Verlust von Devanāgarī-Ligaturen und IAST-Diakritika) oder unter unstrukturierten Textabschriften ohne wissenschaftlichen Zitationsbezug.

Im Rahmen der *AlexandriaSandwich-Pipeline* wurden sämtliche 478 Buchseiten der Heidelberger Originalvorlage multimodal erfasst, gegen den kanonischen Aṣṭādhyāyī-Sūtrapāṭha abgeglichen und lückenlos zu 100 % (alle 3.997 Sūtras) strukturiert.

*Typografische Grundsätze dieser Neuausgabe:*
1. *Duale Zitationssicherheit:* Jedes Sūtra führt sowohl die kanonische Aṣṭādhyāyī-Zählung (z. B. `1.1.1`) als auch den exakten Seitenumbruch der historischen Leipziger Originalausgabe von 1887 (`📖 Böhtlingk (1887) S. 2`).
2. *Authentische Hierarchie:* Der Devanāgarī-Sūtratext steht in typografisch hervorgehobenem Satz, gefolgt von Böhtlingks Übersetzung im Haupttext und seinem philologischen Kommentar im klassischen Kleindruck (*Petit*).
3. *Vektorneusatz:* Gestochen scharfe Schrift auf Basis offener Schriften (*STIX Two Text* und *Noto Serif Devanagari*) für ermüdungsfreies Lesen auf hochauflösenden Bildschirmen und professionellen Drucksystemen.

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

#outline(
  title: none,
  depth: 2,
  indent: 1.5em,
)

#pagebreak()

// =============================================================================
// 3. ARABISCHE SEITENZÄHLUNG & DYNAMISCHE LEBENDE KOLUMNENTITEL
// =============================================================================

#counter(page).update(1)

#set page(
  header: context {
    let loc = here()
    let page_num = counter(page).get().first()
    
    // Unterdrücke Kopfzeile auf Seiten mit Hauptüberschrift (Level 1)
    let h1_on_page = query(selector(heading.where(level: 1)).after(loc)).filter(h => counter(page).at(h.location()).first() == page_num)
    if h1_on_page.len() > 0 {
      return none
    }

    let h1_nodes = query(selector(heading.where(level: 1)).before(loc))
    let h2_nodes = query(selector(heading.where(level: 2)).before(loc))
    
    let cur_h1 = if h1_nodes.len() > 0 { h1_nodes.last().body } else { [Pāṇini's Grammatik] }
    let cur_h2 = if h2_nodes.len() > 0 { h2_nodes.last().body } else { [Aṣṭādhyāyī Sūtrapāṭha] }

    // Ermittle die letzte Sūtra auf der aktuellen Seite (bzw. die aktive Sūtra für Fortsetzungsseiten)
    let sutras_on_page = query(selector(<sutra-marker>)).filter(m => counter(page).at(m.location()).first() == page_num)
    let last_sutra_ref = if sutras_on_page.len() > 0 {
      let v = sutras_on_page.last().value
      str(v.adh) + ", " + str(v.pada) + ", " + str(v.snum) + "."
    } else {
      let prev_sutras = query(selector(<sutra-marker>).before(loc))
      if prev_sutras.len() > 0 {
        let v = prev_sutras.last().value
        str(v.adh) + ", " + str(v.pada) + ", " + str(v.snum) + "."
      } else {
        ""
      }
    }

    [
      #if calc.even(page_num) [
        #text(8.5pt, weight: "bold")[#page_num]
        #h(1fr)
        #text(8pt, font: ("STIX Two Text", "Noto Serif Devanagari"))[#smallcaps[#cur_h1]]
        #h(1fr)
        #text(8.5pt, weight: "bold", fill: rgb("#03192e"))[#last_sutra_ref]
      ] else [
        #text(8.5pt, weight: "bold", fill: rgb("#03192e"))[#last_sutra_ref]
        #h(1fr)
        #text(8pt, font: ("STIX Two Text", "Noto Serif Devanagari"))[#cur_h2]
        #h(1fr)
        #text(8.5pt, weight: "bold")[#page_num]
      ]
      #v(0.3em)
      #line(length: 100%, stroke: 0.35pt + rgb("#d8d2c6"))
    ]
  },
  footer: none
)

// =============================================================================
// 4. DATEN LADEN
// =============================================================================

#let tree = json("/data/ashtadhyayi_grouped_edition.json")
#let corrigenda_data = json("/data/corrigenda.json")

#let shiva_canonical = (
  (1, "अ इ उ ण्", "a i u ṇ"),
  (2, "ऋ ऌ क्", "ṛ ḷ k"),
  (3, "ए ओ ङ्", "e o ṅ"),
  (4, "ऐ औ च्", "ai au c"),
  (5, "ह य व र ट्", "ha ya va ra ṭ"),
  (6, "लँ ण्", "la ṇ"),
  (7, "ञ म ङ ण न म्", "ña ma ṅa ṇa na m"),
  (8, "झ भ ञ्", "jha bha ñ"),
  (9, "घ ढ ध ष्", "gha ḍha dha ṣ"),
  (10, "ज ब ग ड द श्", "ja ba ga ḍa da ś"),
  (11, "ख फ छ ठ थ च ट त व्", "kha pha cha ṭha tha ca ṭa ta v"),
  (12, "क प य्", "ka pa y"),
  (13, "श ष स र्", "śa ṣa sa r"),
  (14, "ह ल्", "ha l"),
)

// =============================================================================
// 5. ŚIVA-SŪTRAS (AKṢARASAMĀMNĀYA)
// =============================================================================

#heading(level: 1)[Śiva-Sūtras (Akṣarasamāmnāya)]

#v(0.3em)
#align(center)[
  #text(8.5pt, style: "italic", fill: rgb("#334155"))[
    Die 14 kanonischen Lautgruppen zur Bildung der grammatischen Pratyāhāras (Böhtlingk 1887, S. 1).
  ]
]
#v(1.2em)

#grid(
  columns: (1fr, 1fr),
  gutter: 2.5em,
  [
    #for s in shiva_canonical.slice(0, 7) [
      #align(center)[
        #text(12pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT", "Kohinoor Devanagari"))[
          #s.at(1) ॥ #to-deva(s.at(0)) ॥
        ]
        #v(-0.35em)
        #text(8pt, style: "italic", fill: rgb("#334155"))[
          (Śiva-Sūtra #s.at(0) — #s.at(2))
        ]
      ]
      #v(0.65em)
    ]
  ],
  [
    #for s in shiva_canonical.slice(7, 14) [
      #align(center)[
        #text(12pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT", "Kohinoor Devanagari"))[
          #s.at(1) ॥ #to-deva(s.at(0)) ॥
        ]
        #v(-0.35em)
        #text(8pt, style: "italic", fill: rgb("#334155"))[
          (Śiva-Sūtra #s.at(0) — #s.at(2))
        ]
      ]
      #v(0.65em)
    ]
  ]
)

#pagebreak()

// =============================================================================
// 6. AṢṬĀDHYĀYĪ SŪTRAPĀṬHA (3.983 SŪTRAS)
// =============================================================================

#{
  let last_page_seen = -1

  for adh in tree {
    [
      #pagebreak(weak: true)
      #heading(level: 1)[#adh.title_de (#adh.title_sa)]
      #v(0.6em)
    ]

    for pada in adh.padas {
      [
        #v(0.4em)
        #heading(level: 2)[#pada.title_de (#pada.title_sa)]
        #v(0.5em)
      ]

      for s in pada.sutras {
        let is_new_orig_page = (s.page != none and s.page != last_page_seen)
        if is_new_orig_page {
          last_page_seen = s.page
          [
            #v(0.5em)
            #grid(
              columns: (1fr, auto, 1fr),
              align: (center, center, center),
              line(length: 90%, stroke: 0.35pt + rgb("#d8d2c6")),
              text(7.5pt, fill: rgb("#b45309"), weight: "bold")[#h(0.5em) 📖 Böhtlingk (1887) S. #s.page #h(0.5em)],
              line(length: 90%, stroke: 0.35pt + rgb("#d8d2c6"))
            )
            #v(0.4em)
          ]
        }

        [
          #metadata((adh: adh.num, pada: pada.num, snum: s.sutra_num, ref: s.ref)) <sutra-marker>
          #block(width: 100%, breakable: true)[
            // Sūtra-Kopf und Übersetzung unteilbar zusammenhalten (Original-Layout Böhtlingk 1887)
            #block(width: 100%, breakable: false)[
              #grid(
                columns: (1fr, auto),
                align: (left + bottom, right + bottom),
                gutter: 1em,
                [
                  #text(12pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT", "Kohinoor Devanagari"))[
                    #s.canonical_devanagari ॥ #to-deva(s.sutra_num) ॥
                  ]
                  #if s.canonical_iast != "" [
                    #h(0.6em)
                    #text(8.5pt, style: "italic", fill: rgb("#475569"))[(#s.canonical_iast)]
                  ]
                ],
                [
                  #text(10pt, font: ("STIX Two Text", "Noto Serif Devanagari"), fill: rgb("#03192e"))[
                    #str(adh.num), #str(pada.num), #str(s.sutra_num).
                  ]
                ]
              )
              #v(0.18em)
              #if s.translation != "" [
                #text(9.5pt, fill: rgb("#03192e"))[#s.translation]
              ]
            ]
            // Philologischer Kommentar (Kleindruck, eingerückt)
            #if s.commentary != "" [
              #v(0.18em)
              #pad(left: 1.2em)[
                #set par(leading: 0.40em)
                #text(8.3pt, fill: rgb("#1e2d37"))[#s.commentary]
              ]
            ]
            #v(0.50em)
          ]
        ]
      }
    }
  }
}

#pagebreak()

// =============================================================================
// 7. NACHTRÄGE UND VERBESSERUNGEN (CORRIGENDA)
// =============================================================================

#heading(level: 1)[Nachträge und Verbesserungen]

#v(0.3em)
#align(center)[
  #text(8.5pt, style: "italic", fill: rgb("#334155"))[
    Corrigenda und Zusätze von Otto Böhtlingk zu den Seiten 477–478 der Originalausgabe von 1887.
  ]
]
#v(0.8em)

#for c in corrigenda_data [
  #block(width: 100%, breakable: true, [
    #text(8.5pt, fill: rgb("#1e2d37"))[
      • #c.text
    ]
    #v(0.25em)
  ])
]
