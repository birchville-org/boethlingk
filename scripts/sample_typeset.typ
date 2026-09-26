#set page(
  paper: "iso-b5",
  margin: (top: 2.2cm, bottom: 2.2cm, inside: 2.5cm, outside: 2cm),
  header: context {
    let page_num = counter(page).get().first()
    let is_even = calc.even(page_num)
    if is_even [
      #text(8pt, font: ("Baskerville", "Times New Roman"), style: "italic")[Pāṇini's Grammatik (Leipzig 1887)]
      #h(1fr)
      #text(9pt, weight: "bold")[#page_num]
    ] else [
      #text(9pt, weight: "bold")[#page_num]
      #h(1fr)
      #text(8pt, font: ("Baskerville", "Times New Roman"), style: "italic")[Erster Adhyāya — Erster Pāda]
    ]
  },
  footer: none
)

#set text(
  font: ("Baskerville", "Times New Roman", "Devanagari MT", "Kohinoor Devanagari"),
  size: 10pt,
  lang: "de"
)

#set par(justify: true, leading: 0.65em)

// Titel
#align(center)[
  #v(1cm)
  #text(16pt, weight: "bold", font: ("Baskerville", "Times New Roman"))[PĀṆINI'S GRAMMATIK]
  
  #v(0.3cm)
  #text(12pt, style: "italic")[herausgegeben, übersetzt, erläutert und mit verschiedenen Indices versehen]
  
  #v(0.2cm)
  #text(11pt)[von]
  
  #v(0.2cm)
  #text(13pt, weight: "bold")[OTTO BÖHTLINGK]
  
  #v(0.5cm)
  #line(length: 40%, stroke: 0.5pt)
  #v(1cm)
]

#let data = json("/data/ashtadhyayi_complete_boethlingk1887.json")
#let sutras = data.sutras.slice(0, 12)

#heading(level: 1, numbering: none)[Erster Adhyāya. Erster Pāda.]
#v(0.5em)

#for s in sutras [
  #block(
    width: 100%,
    breakable: true,
    stroke: none,
    inset: (y: 0.3em),
    [
      // Sūtra-Kopf: Devanāgarī groß & fett zentriert
      #align(center)[
        #text(13pt, weight: "bold", font: ("Devanagari MT", "Kohinoor Devanagari"))[
          #s.canonical_devanagari ॥ #s.sutra_num ॥
        ]
        
        #v(-0.2em)
        #text(9pt, style: "italic", font: ("Baskerville", "Times New Roman"))[
          (#s.ref — #s.canonical_iast)
        ]
      ]
      
      #v(0.2em)
      // Übersetzung (Böhtlingk 1887)
      #if s.translation != "" [
        #text(10pt)[#s.translation]
      ]
      
      // Philologischer Kommentar (eingerückt, kleinerer Schriftgrad wie im Original)
      #if s.commentary != "" [
        #v(0.2em)
        #pad(left: 1.2em)[
          #text(8.5pt, fill: luma(40))[
            #s.commentary
          ]
        ]
      ]
      #v(0.6em)
    ]
  )
]
