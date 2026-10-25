
#let font_name = sys.inputs.at("font", default: "Charis SIL")

#set page(
  paper: "iso-b5",
  margin: (top: 2.0cm, bottom: 2.0cm, left: 2.2cm, right: 2.2cm),
  header: none,
  footer: none
)

#set text(
  font: (font_name, "Noto Serif Devanagari", "Devanagari MT"),
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
// Seite 0: Probe Halbtitel & Titelei
// =============================================================================
#align(center)[
  #v(2cm)
  #text(11pt, fill: rgb("#b45309"), weight: "bold")[SCHRIFTPROBE: #font_name]   #v(1.5cm)
  #text(20pt, weight: "bold", tracking: 0.12em)[#smallcaps[Pāṇini's Grammatik]]   #v(0.6cm)
  #text(11pt, style: "italic", fill: rgb("#334155"))[Herausgegeben, übersetzt, erläutert und mit verschiedenen Indices versehen]   #v(0.3cm)
  #text(12pt, weight: "bold")[von #smallcaps[Otto Böhtlingk]]   #v(0.8cm)
  #text(10.5pt)[#smallcaps[Mit Vārttika des Kātyāyana und Mahābhāṣya des Patañjali]]   #v(0.4cm)
  #text(9.5pt, fill: rgb("#6b6257"))[Referenzen: Bhaṭṭoji Dīkṣita's Siddhāntakaumudī, Kāśikāvṛtti, Śākaṭāyana, Ṛgveda]   #v(1.5cm)
  #line(length: 60%, stroke: 0.5pt + rgb("#d8d2c6"))
  #v(0.8cm)
  #text(9pt, style: "italic")[Leipzig 1887 — Verlag von H. Haessel]
]

#pagebreak()

// =============================================================================
// Seite 1: Śiva-Sūtras & Einführung
// =============================================================================
#v(1.6cm)
#grid(
  columns: (1fr, auto, 1fr),
  align: (left, center, right),
  [#text(10pt, weight: "bold")[1]],
  [#text(15pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[॥ अथ शब्दानुशासनम् ॥]],
  none
)
#v(0.8cm)

#align(center)[
  #table(
    columns: (auto, auto, auto, auto),
    column-gutter: 2.2em,
    row-gutter: 1.5em,
    stroke: none,
    align: (left, left, left, left),
    [#text(12.5pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[अ इ उ ण् । १ ।]],
    [#text(12.5pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[ऋ ऌ क् । २ ।]],
    [#text(12.5pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[ए ओ ङ् । ३ ।]],
    [#text(12.5pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[ऐ औ च् । ४ ।]],
    [#text(12.5pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[ह य व र ट् । ५ ।]],
    [#text(12.5pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[लँ ण् । ६ ।]],
    [#text(12.5pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[ञ म ङ ण न म् । ७ ।]],
    [#text(12.5pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[झ भ ञ् । ८ ।]],
    [#text(12.5pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[घ ढ ध ष् । ९ ।]],
    [#text(12.5pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[ज ब ग ड द श् । १० ।]],
    [#text(12.5pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[ख फ छ ठ थ च ट त व् । ११ ।]],
    [#text(12.5pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[क प य् । १२ ।]],
    [#text(12.5pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[श ष स र् । १३ ।]],
    [#text(12.5pt, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[ह ल् । १४ ।]],
    [], []
  )
]

#v(1.6cm)

#set text(size: 10.0pt)
#set par(leading: 0.52em)

Die vorstehenden, das Alphabet enthaltenden Sūtra führen den Namen #text(font: ("Noto Serif Devanagari"))[अक्षरसमानाय] oder #text(font: ("Noto Serif Devanagari"))[शिवसूत्राणि] und werden der Gottheit zugeschrieben. Die Vocale sind mit Ausnahme von #text(font: ("Noto Serif Devanagari"))[ऌ] sowohl kurz als lang und überdies noch nasalirt oder nicht nasalirt, circumflectirt oder nicht circumflectirt (1, 2, 27–32). Der nach #text(font: ("Noto Serif Devanagari"))[लँ] gesetzte Nasalstrich deutet an, dass der Vocal nasalirt ist (1, 3, 2). Die Consonanten haben mit Ausnahme des letzten jedes Sūtra einen inhärirenden unbetonten Vocal #text(font: ("Noto Serif Devanagari"))[अ] zur Erleichterung der Aussprache (1, 3, 3); die letzten Consonanten heissen #text(font: ("Noto Serif Devanagari"))[इत्] (stumm) und dienen in Verbindung mit einem vorhergehenden Laute zur Bildung von Sigla (1, 1, 71). Ein Vocal mit angefügtem #text(font: ("Noto Serif Devanagari"))[त्] bezeichnet eine ganze Classe von Lauten, z. B. #text(font: ("Noto Serif Devanagari"))[कु] die Gutturale, #text(font: ("Noto Serif Devanagari"))[चु] die Palatale u. s. w. (1, 1, 69). Die langen Vocale fehlen im Alphabet, weil in Pāṇini's Grammatik der kurze Vocal auch die entsprechende Länge in sich begreift; soll diese ausgeschlossen werden, so wird dem kurzen Vocal #text(font: ("Noto Serif Devanagari"))[त्] angefügt (1, 1, 70). Pāṇini verwendet folgende 40 Sigla: #text(font: ("Noto Serif Devanagari"))[अक्, अच्, अट्, अण्] (als Bezeichnung zweier Gruppen), #text(font: ("Noto Serif Devanagari"))[अम्, अल्, अश्, इक्, इच्, इण्, उक्, एङ्, एच्, ऐच्, खय्, खर्, ङम्, चर्, छव्, जश्, झय्, झर्, झल्, झश्, झष्, बश्, भष्, मय्, यञ्, यण्, यम्, यय्, यर्, रल्, वल्, वश्, शर्, शल्, हल्] und #text(font: ("Noto Serif Devanagari"))[हश्].

#v(1fr)
#grid(
  columns: (1fr, auto),
  [#text(9pt, style: "italic", fill: rgb("#334155"))[Pāṇini's Grammatik.]],
  [#text(9pt, weight: "bold")[1]]
)

#pagebreak()

// =============================================================================
// Seiten 2 & 8 aus JSON
// =============================================================================
#let pages_data = json("/data/ashtadhyayi_facsimile_dense.json")

#for target_p in (2, 8) {
  let p_info = pages_data.find(p => p.page_num == target_p)
  if p_info != none {
    // Header
    grid(
      columns: (1fr, auto, 1fr),
      align: (left, center, right),
      [#text(8.5pt, weight: "bold")[#str(target_p)]],
      [#text(8pt, font: (font_name, "Noto Serif Devanagari", "Devanagari MT"))[#p_info.header_adh_str]],
      [#text(8.5pt, font: (font_name, "Noto Serif Devanagari", "Devanagari MT"), style: "italic")[#p_info.last_sutra_ref]]
    )
    line(length: 100%, stroke: 0.35pt + rgb("#d8d2c6"))
    v(0.3em)
    
    let prof = p_info.profile
    let deva_sz = eval(prof.deva_size)
    let body_sz = eval(prof.body_size)
    let body_lead = eval(prof.body_leading)
    let comm_sz = eval(prof.comm_size)
    let comm_lead = eval(prof.comm_leading)
    let sutra_sp = eval(prof.sutra_spacing)

    for s in p_info.sutras [
      #block(width: 100%, breakable: false)[
        #block(width: 100%)[
          #grid(
            columns: (1fr, auto),
            align: (left + bottom, right + bottom),
            gutter: 0.8em,
            [
              #text(deva_sz, weight: "bold", font: ("Noto Serif Devanagari", "Devanagari MT"))[
                #s.canonical_devanagari ॥ #s.sutra_num_deva ॥
              ]
              #if s.canonical_iast != "" [
                #h(0.4em)
                #text(body_sz * 0.82, style: "italic", font: (font_name, "Noto Serif Devanagari", "Devanagari MT"), fill: rgb("#475569"))[(#s.canonical_iast)]
              ]
            ],
            [
              #text(body_sz, font: (font_name, "Noto Serif Devanagari", "Devanagari MT"), fill: rgb("#03192e"))[
                #str(s.adhyaya), #str(s.pada), #str(s.sutra_num).
              ]
            ]
          )
          #v(0.12em)
          #if s.translation != "" [
            #set par(leading: body_lead)
            #text(body_sz, font: (font_name, "Noto Serif Devanagari", "Devanagari MT"), fill: rgb("#03192e"))[#s.translation]
          ]
        ]
        #if s.commentary != "" [
          #v(0.12em)
          #pad(left: 0.8em)[
            #set par(leading: comm_lead)
            #text(comm_sz, font: (font_name, "Noto Serif Devanagari", "Devanagari MT"), fill: rgb("#1e2d37"))[#s.commentary]
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
    if target_p == 2 [
      #pagebreak()
    ]
  }
}
