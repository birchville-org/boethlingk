// =============================================================================
// Birchville Scholarly Synthesis — Page-Aligned Test Edition (Böhtlingk 1887)
// Jede Seite beginnt exakt an derselben Stelle wie im historischen Originaldruck.
// Überläufe fließen auf die Folgeseite, bevor die nächste Originalseite beginnt.
// =============================================================================

#set document(
  title: "Pāṇini's Grammatik (Otto von Böhtlingk, 1887) — Seitengetreue Neuausgabe",
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
  font: ("Libertinus Serif", "Linux Libertine O", "Noto Serif Devanagari", "Devanagari MT", "Times New Roman"),
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
  #text(9pt, style: "italic", fill: rgb("#334155"))[Otto von Böhtlingk (Leipzig 1887)] \
  #v(0.3cm)
  #text(8.5pt, fill: rgb("#b45309"), weight: "bold")[Seitengetreue Synchronausgabe (Original-Seitenstarts)]
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
    *Seitengetreue Neuausgabe:* AlexandriaSandwich Digital Humanities Pipeline (2026) \
    *Herausgeber & Neusatz:* Marco Demarmels (Birchville Foundation) \
    *Seitenparität:* Jeder Seitenanfang entspricht exakt dem Beginn der jeweiligen Originalseite (S. 1–476). \
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
  #text(22pt, weight: "bold", font: ("Baskerville", "Libertinus Serif", "Times New Roman"))[PĀṆINI'S GRAMMATIK]
  
  #v(0.8cm)
  #text(11pt, style: "italic")[herausgegeben, übersetzt, erläutert und mit verschiedenen Indices versehen]
  
  #v(0.4cm)
  #text(10pt)[von]
  
  #v(0.4cm)
  #text(16pt, weight: "bold")[OTTO BÖHTLINGK]
  
  #v(0.8cm)
  #text(11pt, style: "italic")[Zweite Auflage · Seitengetreuer Neusatz]
  
  #v(0.6cm)
  #line(length: 25%, stroke: 0.5pt)
  #v(0.6cm)
  
  #text(10.5pt)[LEIPZIG \ VERLAG VON H. HAESSEL \ 1887]
]

#pagebreak()

// Seite iv: Vorwort zur seitengetreuen Synchronausgabe
#heading(level: 1, numbering: none, outlined: false)[Vorwort zur seitengetreuen Ausgabe]

#v(0.5em)

Die vorliegende Ausgabe von Otto von Böhtlingks *Grammatik des Pāṇini* (Leipzig 1887) ist eine *seitengetreue Synchronausgabe*:

Jede Seite dieser Neuausgabe beginnt exakt mit demjenigen Sūtra, mit welchem die entsprechende Seite im Heidelberger Originaldruck von 1887 beginnt (Originalseiten 1 bis 476).

*Besonderheiten dieses Satzes:*
1. *Identischer Seitenstart:* Die Sūtra-Folge jeder Seite setzt an exakt denselben Stellen an wie im historischen Buch. Zitate nach der Seitenzahl von 1887 lassen sich so unmittelbar aufschlagen.
2. *Überlauf-Handling:* Beansprucht der Text einer Originalseite im großzügigen modernen Neusatz mehr Raum als eine einzelne ISO-B5-Seite bietet, fließt der Text natürlich auf die Folgeseite weiter. Die darauffolgende Originalseite beginnt wieder am Kopf einer frischen Seite.
3. *Klassische Leipziger Kopfzeile:* Der lebende Kolumnentitel zeigt die Seitenzahl, den Adhyāya/Pāda, die letzte Sūtra der Seite sowie die Referenz auf die historische Originalseite (`[Böhtl. S. X]`).

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

    let orig_p = if sutras_on_page.len() > 0 {
      str(sutras_on_page.first().value.orig_page)
    } else {
      let prev = query(selector(<sutra-marker>).before(loc))
      if prev.len() > 0 { str(prev.last().value.orig_page) } else { "" }
    }

    [
      #if calc.even(page_num) [
        #text(8.5pt, weight: "bold")[#page_num]
        #if orig_p != "" [
          #h(0.4em)
          #text(7.5pt, fill: rgb("#b45309"))[[Orig. S. #orig_p]]
        ]
        #h(1fr)
        #text(8pt, font: ("Libertinus Serif", "Linux Libertine O", "Times New Roman"))[#smallcaps[#cur_h1]]
        #h(1fr)
        #text(8.5pt, weight: "bold", fill: rgb("#03192e"))[#last_sutra_ref]
      ] else [
        #text(8.5pt, weight: "bold", fill: rgb("#03192e"))[#last_sutra_ref]
        #h(1fr)
        #text(8pt, style: "italic", fill: rgb("#334155"))[#cur_h2]
        #h(1fr)
        #if orig_p != "" [
          #text(7.5pt, fill: rgb("#b45309"))[[Orig. S. #orig_p]]
          #h(0.4em)
        ]
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
// 5. ŚIVA-SŪTRAS (AKṢARASAMĀMNĀYA) — BÖHTLINGK S. 1
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
// 6. AṢṬĀDHYĀYĪ SŪTRAPĀṬHA (3.983 SŪTRAS) — SEITENGETREUER ANFANG
// =============================================================================

#{
  let last_page_seen = -1

  for adh in tree {
    // Adhyāya-Überschrift
    [
      #heading(level: 1)[#adh.title_de (#adh.title_sa)]
      #v(0.6em)
    ]

    for pada in adh.padas {
      // Pāda-Überschrift
      [
        #v(0.4em)
        #heading(level: 2)[#pada.title_de (#pada.title_sa)]
        #v(0.5em)
      ]

      for s in pada.sutras {
        let is_new_orig_page = (s.page != none and s.page != last_page_seen)
        if is_new_orig_page {
          // Erster Seitenstart: S. 2 nach den Śiva-Sūtras braucht keinen doppelten Umbruch
          if last_page_seen != -1 {
            [ #pagebreak() ]
          }
          last_page_seen = s.page
          [
            #v(0.2em)
            #align(center)[
              #text(7.5pt, fill: rgb("#b45309"), weight: "bold")[📖 Böhtlingk (1887) S. #s.page]
            ]
            #v(0.3em)
          ]
        }

        [
          #metadata((adh: adh.num, pada: pada.num, snum: s.sutra_num, ref: s.ref, orig_page: s.page)) <sutra-marker>
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
                  #text(10pt, font: ("Libertinus Serif", "Linux Libertine O"), fill: rgb("#03192e"))[
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

#heading(level: 1)[Nachträge und Verbesserungen (Corrigenda)]

#v(0.4em)
#text(8.5pt, style: "italic", fill: rgb("#334155"))[
  Otto von Böhtlingks originale Druckfehlerkorrekturen und philologische Nachträge zum Text und Kommentar (Leipzig 1887, S. 477–480).
]
#v(0.8em)

#for item in corrigenda_data [
  #block(width: 100%, breakable: false)[
    #rect(width: 100%, stroke: 0.35pt + rgb("#d8d2c6"), inset: 0.6em, radius: 2pt)[
      #text(8.5pt, fill: rgb("#1e2d37"))[#item.text]
    ]
    #v(0.35em)
  ]
]
