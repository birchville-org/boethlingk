#set page(
  paper: "iso-b5",
  margin: (top: 2.2cm, bottom: 2.2cm, inside: 2.5cm, outside: 2cm),
  header: none,
  footer: none
)

#set text(
  font: ("Baskerville", "Times New Roman", "Devanagari MT", "Kohinoor Devanagari"),
  size: 10pt,
  lang: "de"
)

#set par(justify: true, leading: 0.65em)

// =============================================================================
// Helper: Convert ASCII digits to Devanāgarī numerals
#let to-deva(num) = {
  let s = str(num)
  let map = ("0": "०", "1": "१", "2": "२", "3": "३", "4": "४", "5": "५", "6": "६", "7": "७", "8": "८", "9": "९")
  s.clusters().map(c => map.at(c, default: c)).join("")
}

// 1. TITELSEITE & IMPRESSUM
// =============================================================================

#align(center)[
  #v(2.5cm)
  #text(22pt, weight: "bold", font: ("Baskerville", "Times New Roman"))[PĀṆINI'S GRAMMATIK]
  
  #v(0.8cm)
  #text(12pt, style: "italic")[herausgegeben, übersetzt, erläutert und mit verschiedenen Indices versehen]
  
  #v(0.4cm)
  #text(11pt)[von]
  
  #v(0.4cm)
  #text(16pt, weight: "bold")[OTTO BÖHTLINGK]
  
  #v(0.8cm)
  #text(11pt, style: "italic")[Zweite Auflage]
  
  #v(0.5cm)
  #line(length: 30%, stroke: 0.5pt)
  #v(0.5cm)
  
  #text(11pt)[LEIPZIG \ VERLAG VON H. HAESSEL \ 1887]

  #v(3.2cm)
  #line(length: 60%, stroke: 0.4pt)
  #v(0.4cm)
  #text(8pt, fill: luma(70))[
    Digitale typografische Neuausgabe (2026) auf Basis der Originalscans der \
    Universitätsbibliothek Heidelberg (Bibliotheca Palatina) \
    Kanonisch konsolidierter Master-Datensatz (100% Abdeckung, 3.997 Sūtras) \
    AlexandriaSandwich Digital Humanities Edition \
    Lizenziert unter Public Domain (Werk) / CC-BY-SA 4.0 / MIT (Edition)
  ]
]

#pagebreak()

// =============================================================================
// 2. INHALTSÜBERSICHT
// =============================================================================

#outline(
  title: [Inhaltsübersicht],
  depth: 2,
  indent: 1.5em,
)

#pagebreak()

// =============================================================================
// 3. AB HIER ARABISCHE SEITENZÄHLUNG & DYNAMISCHE LEBENDE KOLUMNENTITEL
// =============================================================================

#counter(page).update(1)

#set page(
  header: context {
    let page_num = counter(page).get().first()
    let headings = query(selector(heading).before(here()))
    let current_title = if headings.len() > 0 { headings.last().body } else { [Pāṇini's Grammatik] }
    
    if calc.even(page_num) [
      #text(8.5pt, weight: "bold")[#page_num]
      #h(1fr)
      #text(8pt, font: ("Baskerville", "Times New Roman"), style: "italic")[Pāṇini's Grammatik (Otto von Böhtlingk, 1887)]
    ] else [
      #text(8pt, font: ("Baskerville", "Times New Roman"), style: "italic")[#current_title]
      #h(1fr)
      #text(8.5pt, weight: "bold")[#page_num]
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

#v(0.5em)
#align(center)[
  #text(9pt, style: "italic")[
    Die 14 kanonischen Lautgruppen zur Bildung der grammatischen Pratyāhāras (Böhtlingk 1887, S. 1).
  ]
]
#v(1em)

#for s in shiva_canonical [
  #block(width: 100%, breakable: false, [
    #align(center)[
      #text(13pt, weight: "bold", font: ("Devanagari MT", "Kohinoor Devanagari"))[
        #s.at(1) ॥ #to-deva(s.at(0)) ॥
      ]
      #v(-0.25em)
      #text(8.5pt, style: "italic")[
        (Śiva-Sūtra #s.at(0) — #s.at(2))
      ]
    ]
    #v(0.35em)
  ])
]

#pagebreak()

// =============================================================================
// 6. AṢṬĀDHYĀYĪ SŪTRAPĀṬHA (3.983 SŪTRAS)
// =============================================================================

#for adh in tree [
  #pagebreak(weak: true)
  #heading(level: 1)[#adh.title_de (#adh.title_sa)]
  #v(0.8em)

  #for pada in adh.padas [
    #v(0.5em)
    #heading(level: 2)[#pada.title_de (#pada.title_sa)]
    #v(0.6em)

    #for s in pada.sutras [
      #block(width: 100%, breakable: true, [
        // 1. Devanāgarī Sūtra-Kopf (fett zentriert)
        #align(center)[
          #text(12.5pt, weight: "bold", font: ("Devanagari MT", "Kohinoor Devanagari"))[
            #s.canonical_devanagari ॥ #to-deva(s.sutra_num) ॥
          ]
          #v(-0.25em)
          #text(8.5pt, style: "italic")[
            (#s.ref — #s.canonical_iast)
          ]
        ]

        // 2. Deutsche Übersetzung (Böhtlingk 1887)
        #if s.translation != "" [
          #v(0.15em)
          #text(9.5pt)[#s.translation]
        ]

        // 3. Philologischer Kommentar (Böhtlingks Kleindruck, leicht eingerückt)
        #if s.commentary != "" [
          #v(0.15em)
          #pad(left: 1.2em)[
            #text(8.2pt, fill: luma(35))[#s.commentary]
          ]
        ]
        #v(0.65em)
      ])
    ]
  ]
]

#pagebreak()

// =============================================================================
// 7. NACHTRÄGE UND VERBESSERUNGEN (CORRIGENDA)
// =============================================================================

#heading(level: 1)[Nachträge und Verbesserungen]

#v(0.5em)
#align(center)[
  #text(9pt, style: "italic")[
    Corrigenda und Zusätze von Otto Böhtlingk zu den Seiten 477–478 der Originalausgabe von 1887.
  ]
]
#v(1em)

#for c in corrigenda_data [
  #block(width: 100%, breakable: true, [
    #text(8.5pt)[
      • #c.text
    ]
    #v(0.3em)
  ])
]
