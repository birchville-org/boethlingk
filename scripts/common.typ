// =============================================================================
// Gemeinsame Typst-Hilfsfunktionen & Front-Matter-Komponenten (Boethlingk 1887)
// =============================================================================

#let to-deva(num) = {
  let s = str(num)
  let map = ("0": "०", "1": "१", "2": "२", "3": "३", "4": "४", "5": "५", "6": "६", "7": "७", "8": "८", "9": "९")
  s.clusters().map(c => map.at(c, default: c)).join("")
}

#let parse-len(s) = {
  if type(s) == length {
    s
  } else if s.ends-with("pt") {
    float(s.slice(0, -2)) * 1pt
  } else if s.ends-with("em") {
    float(s.slice(0, -2)) * 1em
  } else {
    float(s) * 1pt
  }
}

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

#let render-front-imprint(subtitle_line: none, edition_bullets: ()) = [
  // Seite i: Halbtitel (Bastard Title)
  #v(6cm)
  #align(center)[
    #text(16pt, weight: "bold", tracking: 0.12em)[#smallcaps[Pāṇini's Grammatik]] \
    #v(0.6cm)
    #text(9pt, style: "italic", fill: rgb("#334155"))[Otto von Böhtlingk (Leipzig 1887)]
    #if subtitle_line != none [
      \ #v(0.3cm)
      #text(8.5pt, fill: rgb("#b45309"), weight: "bold")[#subtitle_line]
    ]
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
      #for item in edition_bullets [
        #item \
      ]
      \
      *Urheberrecht & Lizenzen:* \
      Historisches Originalwerk: Gemeinfrei (Public Domain worldwide) \
      Digitale Ausgabe, Typst-Code & TEI-Encoding: MIT License / CC-BY-SA 4.0
    ]
  ]

  #pagebreak()
]

#let render-main-title(edition_note) = [
  // Seite iii: Haupttitel (Leipzig 1887)
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
    #text(11pt, style: "italic")[#edition_note]

    #v(0.6cm)
    #line(length: 25%, stroke: 0.5pt)
    #v(0.6cm)

    #text(10.5pt)[LEIPZIG \ VERLAG VON H. HAESSEL \ 1887]
  ]

  #pagebreak()
]
