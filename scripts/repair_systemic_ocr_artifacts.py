"""
Repair systemic OCR artifacts on pages 9, 10, and 149 of Böhtlingk 1887.
Mistral OCR misrecognized isolated Devanagari types as Hebrew characters on these pages,
which downstream regexes replaced with [Sanskrit] or stripped.
This script restores the exact historical reading verified against original scan plates.
"""

import json
from pathlib import Path

RESTORATIONS = {
    "1.1.58": {
        "commentary": (
            "Zu 1) Der Anlaut von अस् ist in सन्ति abgefallen; wenn diesem कानि vorangeht, "
            "so ist dieses abgefallene अ wirkungslos in Bezug auf das vorangehende इ, "
            "da dieses vor सन्ति nicht in य् übergeht. "
            "Zu 2) सुधी und उपास्य giebt सुध्युपास्य; hier ist das ursprüngliche ई in Bezug auf die "
            "Verdoppelung von ध् als nicht mehr vorhanden zu betrachten, da nach 8, 4, 47 wohl vor य्, "
            "aber nicht vor einem Vocal, ध् zu द्ध werden kann. Man darf also सुद्ध्युपास्य schreiben. "
            "Zu 3) Nach 3, 2, 176 bildet man vom Intensivum von या ein Adjectiv auf वर; "
            "nach 6, 4, 48 muss das अ des Intensiv-Charakters vor व् abfallen. Wenn dieser Abfall "
            "in Bezug auf die Behandlung des nachbleibenden य् als nicht geschehen betrachtet würde, "
            "dann dürfte dieses nicht nach 6, 1, 66 ausfallen, und wir erhielten nicht यायावर. "
            "Zu 4) Der mit dem Suffix सन् von कृ gebildete Desiderativstamm चिकीर्ष verliert nach 6, 4, 48 "
            "vor dem Suffix अक (वुल्) das schliessende अ. Wenn dieser Abfall nicht als definitiv erfolgt "
            "angesehen würde, könnte der Acut in चिकीर्षक, der in Folge des stummen ल् im Suffix वुल् auf der "
            "diesem Suffix unmittelbar vorangehenden Silbe ruhen muss, nicht auf das ई bezogen werden. "
            "Zu 5) und 6) Von der Wurzel शिष् wird der Präsensstamm शिन्ष् gebildet. Vor gewissen Personalendungen "
            "fällt nach 6, 4, 111 das अ des Suffixes न aus; wenn nun dieser Ausfall in Bezug auf das vorangehende न् "
            "als nicht erfolgt betrachtet würde, könnte nicht शिंषन्ति nach 8, 3, 24 und nicht शिंशिष्ठ nach 8, 4, 58 "
            "gebildet werden. "
            "Zu 7) In प्रतिदिवन् fällt nach 6, 4, 134 vor vocalisch anlautenden Casusendungen das अ aus. "
            "Wenn dieser Ausfall in Bezug auf die Verlängerung des इ in der vorangehenden Silbe als nicht erfolgt "
            "betrachtet würde, könnte dieses nicht nach 8, 2, 77 verlängert werden, es bliebe प्रतिदीव्नः unerklärt. "
            "Zu 8) In der Wurzel घस् fällt vor dem Suffix ति nach 6, 4, 100 der Vocal aus und in Folge dessen auch "
            "der Auslaut nach 8, 2, 26. Das त् des Suffixes geht wegen घ् nach 8, 2, 40 in ध् über. Wenn nun der "
            "Wurzelvocal als nicht ausgefallen betrachtet würde in Bezug auf das vorangehende घ्, dann könnte dieses "
            "nicht nach 8, 4, 53 in ग् übergehen, und die Form जग्ध bliebe unerklärt. "
            "Zu 9) Dieselbe Wurzel घस् verliert vor den Personalendungen अतुस् und उस् des Perfects nach 6, 4, 98 "
            "ihren Vocal. Mit diesem Ausfall hört auch der Einfluss des ausgefallenen Vocals auf das vorangehende घ् "
            "auf, dieses geht in Folge dessen nach 8, 4, 55 in क् über, worauf nach 8, 3, 60 स् zu ष् wird. "
            "Auf diese Weise erhalten wir die Formen जक्षतुः und जक्षुः."
        )
    },
    "1.1.59": {
        "commentary": (
            "Der Wurzelvocal von पा fällt vor den Personalendungen अतुस् und उस् nach 6, 4, 64 ab. "
            "Die Reduplication wird nach 6, 1, 1 und 7, 4, 59 gebildet, als wenn das आ nicht abgefallen wäre."
        )
    },
    "1.1.61": {
        "translation": "Das nicht zur Erscheinung Kommen eines Suffixes wird durch लुक्, श्लु und लुप् bezeichnet."
    },
    "1.1.62": {
        "translation": "Wenn ein Suffix auch schwindet, so tritt doch Alles ein, was durch dasselbe bedingt ist.",
        "commentary": (
            "Nach 1, 4, 14 heisst das, was mit einer Casus- oder Personalendung versehen ist, "
            "पद „fertiges Wort“. Obgleich nun im Nomin. अग्निचित् die Casusendung und im Verbum finitum "
            "अहन् die Personalendung abgefallen ist, so heissen diese dennoch पद."
        )
    },
    "1.1.63": {
        "translation": "Wenn ein Suffix aber durch लुक्, श्लु oder लुप् schwindet, so tritt das durch das Suffix in Bezug auf den Stamm Bedingte nicht ein.",
        "commentary": (
            "Nach 4, 1, 105 wird das Patronymicum von गर्ग mit dem Suffix यञ् gebildet, das aber im Plural "
            "nach 2, 4, 64 verschwindet. Das ञ् in यञ् erfordert die Substitution von Vṛddhi für den ersten "
            "Vocal des Stammes und auch Betonung desselben (गौर्ग्य). Da das Suffix durch die Bezeichnung लुक् "
            "verschwindet, geht die Wirkung des stummen ञ् im Plural verloren (गार्गाः). Nach den Wurzeln der "
            "dritten Klasse verschwindet der Präsens-Charakter शप् (शप्) nach 2, 4, 75 durch श्लु. शप् erfordert "
            "nach 7, 3, 84 Substitution von Guṇa für den Wurzelvocal, diese unterbleibt aber nach unserm Sūtra in "
            "जुहुतः (in जुहोति ist Guṇa durch die Personalendung hervorgerufen). Zu लुप् s. 1, 2, 51."
        )
    },
    "1.1.66": {
        "translation": "Wenn Etwas im Locativ angegeben wird, so heisst dieses, dass an dem diesem unmittelbar Vorangehenden Etwas vorzunehmen ist.",
        "commentary": "इको यणचि 6, 1, 77 bedeutet: an die Stelle von इक् tritt यण् vor einem Vocal."
    },
    "1.1.67": {
        "translation": "Wenn Etwas im Ablativ angegeben wird, so heisst dieses, dass an dem auf diesen unmittelbar Folgenden Etwas vorzunehmen ist.",
        "commentary": "तिङ्ङतिङः 8, 1, 28 bedeutet: ein तिङ् (ein Verbum finitum) nach einem अतिङ् (nicht Verbum finitum); zu ergänzen: ist unbetont."
    },
    "1.1.69": {
        "translation": "Die Vocale, die Halbvocale und ein Consonant mit stummem उ (wie कु, चु, टु, तु, पु) bezeichnen, wenn sie nicht Suffixe sind, zugleich ihre homogenenen Laute."
    },
    "1.1.70": {
        "translation": "Ein Vocal mit folgendem त् bezeichnet nur den Vocal seiner Quantität.",
        "commentary": "अत् nur das kurze अ, इत् nur das kurze इ u. s. w."
    },
    "4.1.1": {
        "translation": "Die nun folgenden Suffixe treten an die mit ङी oder आप् gebildeten Feminina und an Nominalstämme.",
        "commentary": "Da die Femininsuffixe ङी und आप् weder kṛt noch taddhita sind, ist der darauf ausgehende Lautcomplex kein Nominalstamm (Prātipadika); vgl. 1, 2, 45. 46."
    },
    "4.1.5": {
        "translation": "An auf ऋ und न auslautende Nominalstämme tritt ङी.",
        "commentary": "कर्त्री, दण्डिनी."
    }
}

def main():
    db_path = Path("data/ashtadhyayi_complete_boethlingk1887.json")
    with open(db_path, encoding="utf-8") as f:
        data = json.load(f)

    repaired_count = 0
    for s in data["sutras"]:
        ref = s["ref"]
        if ref in RESTORATIONS:
            patch = RESTORATIONS[ref]
            for key, val in patch.items():
                s[key] = val
            repaired_count += 1
            print(f"Repaired {ref}")

    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Successfully repaired {repaired_count} sutras in {db_path}.")

if __name__ == "__main__":
    main()
