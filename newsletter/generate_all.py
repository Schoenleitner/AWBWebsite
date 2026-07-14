#!/usr/bin/env python3
"""Generates all 48 newsletter HTML files for AWB."""

import os

def ent(text):
    """Convert special chars to HTML entities for safe copy-paste."""
    return (text
        .replace('ä', '&auml;').replace('ö', '&ouml;').replace('ü', '&uuml;')
        .replace('Ä', '&Auml;').replace('Ö', '&Ouml;').replace('Ü', '&Uuml;')
        .replace('ß', '&szlig;')
        .replace('—', '&mdash;').replace('–', '&ndash;')
        .replace('→', '&rarr;').replace('…', '&hellip;')
        .replace('²', '&sup2;').replace('·', '&middot;')
        .replace('"', '&ldquo;').replace('"', '&rdquo;')
        .replace('„', '&bdquo;')
    )

BASE = "/Users/michael/Documents/Claude/AWBWebsite/newsletter"
IMG_N = "https://www.attergauer-wohnbau.at/images/seeblick/"
IMG_W = "https://www.attergauer-wohnbau.at/images/reihenhaeuser/"
URL_N = "https://www.attergauer-wohnbau.at/eigenprojekte/seeblick-nussdorf/"
URL_W = "https://www.attergauer-wohnbau.at/eigenprojekte/reihenhaeuser-weissenkirchen/"

CTAS_N = [
    {"text": "Besichtigungstermin anfragen →",
     "href": "mailto:office@attergauer-wohnbau.at?subject=Besichtigungstermin%20Seeblick%20H%C3%A4user%20Nu%C3%9Fdorf",
     "intro": "Möchten Sie Ihr neues Zuhause persönlich erleben? Wir zeigen Ihnen alles vor Ort — unverbindlich und in aller Ruhe."},
    {"text": "Zur Projektseite →",
     "href": URL_N,
     "intro": "Alle Details, Grundrisse und Ausstattungsmerkmale finden Sie auf unserer Projektseite."},
    {"text": "Jetzt anrufen: +43 664 82 49 411",
     "href": "tel:+436648249411",
     "intro": "Fragen? Wir sind persönlich für Sie da — rufen Sie einfach an."},
    {"text": "Rückruf anfordern →",
     "href": "mailto:office@attergauer-wohnbau.at?subject=R%C3%BCckruf%20Seeblick%20H%C3%A4user%20Nu%C3%9Fdorf",
     "intro": "Kein guter Moment zum Telefonieren? Wir rufen Sie gerne zurück — zu Ihrer Wunschzeit."},
]

CTAS_W = [
    {"text": "Besichtigungstermin anfragen →",
     "href": "mailto:office@attergauer-wohnbau.at?subject=Besichtigungstermin%20Reihenhäuser%20Weißenkirchen",
     "intro": "Kommen Sie vorbei und erleben Sie Ihr zukünftiges Zuhause — unverbindlich und in aller Ruhe."},
    {"text": "Zur Projektseite →",
     "href": URL_W,
     "intro": "Grundrisse, Ausstattung und alle Details zu Mietkauf und Festpreis finden Sie auf unserer Projektseite."},
    {"text": "Jetzt anrufen: +43 664 82 49 411",
     "href": "tel:+436648249411",
     "intro": "Wir beantworten Ihre Fragen gerne persönlich — rufen Sie uns an."},
    {"text": "Rückruf anfordern →",
     "href": "mailto:office@attergauer-wohnbau.at?subject=R%C3%BCckruf%20Reihenhäuser%20Weißenkirchen",
     "intro": "Soll ich Sie zurückrufen? Schreiben Sie uns kurz — wir melden uns bei Ihnen."},
]

# Nußdorf mails: (nr, betreff, preheader, versand, headline, body_paragraphs, hero_img, hero_alt, extra_img, extra_alt, extra_caption)
NUSSDORF = [
    (1, "Stellen Sie sich vor … ein Morgen am Attersee",
     "Panorama-Seeblick, ~180 m², Übergabe Sommer 2026 – könnte das Ihr Zuhause sein?",
     "Dienstag, Woche 1",
     "Stellen Sie sich vor …",
     ["Sie wachen morgens auf. Sie gehen ins Wohnzimmer — und der Blick fällt über die Dächer von Nußdorf direkt auf den Attersee. Glitzernd im frühen Licht.",
      "Kein Urlaubshotel. Kein Ferienhaus. Einfach Ihr Zuhause.",
      "Genau dieses Gefühl hatten wir im Kopf, als wir die Seeblick Häuser in Nußdorf am Attersee geplant haben. Ein Zuhause, in dem der See nicht Kulisse ist — sondern täglich gelebtes Leben. Mit großzügiger Terrasse, Wärmepumpe, PV-Anlage und Loxone Smarthome.",
      "In den nächsten Wochen nehmen wir Sie mit — durch Räume, Ausblicke und alle Details. Damit Sie sich schon vor der Besichtigung vorstellen können, wie es sich anfühlt, hier zu Hause zu sein."],
     "visualisierung.jpg", "Seeblick Häuser Nußdorf am Attersee",
     "drohne-1.jpg", "Nußdorf am Attersee aus der Vogelperspektive", "Nußdorf am Attersee — mitten in der Natur, direkt am See."),

    (2, "Der See gehört einfach dazu.",
     "Jeden Morgen dieser Ausblick – von Ihrer Terrasse und aus Ihrem Wohnzimmer.",
     "Freitag, Woche 1",
     "Der See gehört einfach dazu.",
     ["Es gibt Orte, an die man jedes Jahr wieder zurückwill. Nußdorf am Attersee ist so ein Ort — das wissen alle, die einmal dort waren.",
      "Was wäre es, wenn dieser Ort nicht nur Ihr Urlaubsziel wäre, sondern Ihr Zuhause?",
      "Von Ihrer Terrasse aus sehen Sie das Wasser. Im Winter liegt der See im Nebel. Im Frühling glitzert er türkis. Im Sommer hören Sie die Boote. Und im Herbst leuchtet das Höllengebirge drüben in einem satten Rosa.",
      "Vier Jahreszeiten. Ein Zuhause. Immer am See."],
     "drohne-1.jpg", "Attersee aus der Vogelperspektive",
     "terrasse2.jpg", "Terrasse mit Seeblick", "Ihre Terrasse — mit dem See immer im Blick."),

    (3, "Wo andere Urlaub machen, kommen Sie heim.",
     "Das Salzkammergut vor der Haustür — und trotzdem alles, was Sie für den Alltag brauchen.",
     "Dienstag, Woche 2",
     "Wo andere Urlaub machen, kommen Sie heim.",
     ["Nußdorf am Attersee. Ein Name, den Österreicher kennen — und der bei vielen ein Lächeln auslöst. Der See. Die Berge. Die Ruhe.",
      "Für die meisten ist das ein Urlaubsgefühl. Für Sie könnte es Alltag sein.",
      "Die Seeblick Häuser liegen in einer der schönsten Lagen des Attersees — und trotzdem nah genug an allem Wichtigen. Nahversorger, Schulen, Arzt — alles erreichbar. Autobahn und Bahn in wenigen Minuten.",
      "Das Beste aus beiden Welten: die Ruhe des Landes, die Anbindung der Region."],
     "aussen.jpg", "Seeblick Häuser Nußdorf Außenansicht",
     "terrasse3.jpg", "Terrasse mit Bergblick", "Ihre neue Heimat — Nußdorf am Attersee."),

    (4, "Abends nach Hause kommen.",
     "Wenn andere im Stau stehen, sitzen Sie schon auf Ihrer Terrasse.",
     "Freitag, Woche 2",
     "Abends nach Hause kommen.",
     ["Der Arbeitstag ist lang. Das Pendeln zehrt. Und dann — endlich — Feierabend.",
      "Wie fühlt es sich an, nach Hause zu kommen? In ein Haus, das nach Ihnen riecht. In eine Küche, die nach Essen duftet. Auf eine Terrasse, von der aus Sie den See sehen.",
      "Diese kleine Abendroutine — Schlüssel ins Schloss, Schuhe aus, kurz auf die Terrasse — kann sich für Sie völlig anders anfühlen als heute.",
      "Wir würden Ihnen gerne zeigen, wie."],
     "esszimmer.jpg", "Helles Esszimmer mit Seeblick",
     "galerie.jpg", "Innenansicht Seeblick Haus", "Hell, offen, einladend — Ihr neues Zuhause."),

    (5, "Ihre Küche. Ihr Morgen.",
     "Kaffee kochen, aus dem Fenster schauen — und der See ist da.",
     "Dienstag, Woche 3",
     "Kaffee. Stille. Seeblick.",
     ["Morgens, bevor der Tag richtig beginnt. Der Kaffee kocht. Sie stehen am Fenster. Draußen liegt der Attersee — ruhig, glatt, still.",
      "Dieser Moment. Jeden Tag.",
      "Die Seeblick Häuser haben große Fensterfronten, die genau auf diesen Moment ausgerichtet sind. Offene Wohnküchen, die Kochen und Genießen verbinden. Licht, das den ganzen Tag bleibt.",
      "Ein Zuhause ist nicht nur ein Gebäude — es ist eine Sammlung von Momenten. Wir helfen Ihnen, die richtigen zu sammeln."],
     "esszimmer.jpg", "Offener Wohn- und Essbereich",
     "terrasse.jpg", "Wohnzimmer mit Panorama-Seeblick", "Seeblick vom Wohnzimmer — jeden Tag."),

    (6, "Die Terrasse — Ihr zweites Wohnzimmer.",
     "Im Sommer draußen leben. Frühstücken mit Seeblick. Abende, die man nicht mehr missen möchte.",
     "Freitag, Woche 3",
     "Draußen sein. Ankommen.",
     ["Was ist eine gute Terrasse? Nicht einfach nur ein paar Quadratmeter vor dem Haus. Eine gute Terrasse ist ein Raum — ein Ort, an dem man isst, liest, redet, sitzt.",
      "Die Terrassen der Seeblick Häuser sind großzügig geplant. Mit Blick auf den Attersee. Mit Platz für einen Tisch, Sessel, eine Hollywoodschaukel — was auch immer Ihr Sommer braucht.",
      "Im Sommer verbringen die meisten mehr Zeit draußen als drinnen. Warum also nicht einen Außenbereich gestalten, der das verdient?",
      "Wir laden Sie ein, sich das vor Ort anzusehen."],
     "terrasse2.jpg", "Terrasse mit Seeblick",
     "terrasse3.jpg", "Außenbereich Seeblick Haus", "Großzügige Terrasse — Ihr Außenwohnzimmer."),

    (7, "Der Morgen gehört Ihnen.",
     "Erster Kaffee, große Fenster, Seeblick — das ist Ihr neuer Alltag.",
     "Dienstag, Woche 4",
     "Morgens aufwachen. Ankommen.",
     ["Es ist 7 Uhr. Der Kaffee kocht. Sie treten ins Wohnzimmer — und der Attersee liegt vor Ihnen. Ruhig, hell, weit.",
      "Kein Wecker, der daran erinnert, dass das nur Urlaub ist. Kein Check-out. Kein Abreise-Gefühl.",
      "Die großen Panoramafenster der Seeblick Häuser sind genau auf diesen Moment ausgerichtet. Das Wohnzimmer öffnet sich zum See hin — Licht und Weite von morgens bis abends.",
      "Dieser Morgen. Jeden Tag. In Ihrem Zuhause."],
     "terrasse.jpg", "Seeblick vom Wohnzimmer — Panoramafenster",
     "badezimmer-2.jpg", "Modernes Badezimmer", "Hochwertige Ausstattung in jedem Raum."),

    (8, "Raum für alles, was zählt.",
     "~180 m² für Ihre Familie, Ihre Hobbys, Ihr Leben.",
     "Freitag, Woche 4",
     "Platz. Echter Platz.",
     ["Kennen Sie das Gefühl, dass die Wohnung irgendwie nie ganz reicht? Dass man immer zwischen Dingen abwägen muss — Gästezimmer oder Büro? Abstellraum oder Hobbyraum?",
      "Mit ~180 m² stellen Sie sich diese Fragen nicht mehr. Es gibt Platz für Gäste und Büro. Für die Fahrräder und die Skiausrüstung. Für Kinder und Ruhe.",
      "Die Seeblick Häuser bieten nicht nur Fläche — sondern durchdachte Raumaufteilung. Großzügige Wohnbereiche, funktionale Nebenräume, ein Doppelcarport für zwei Autos.",
      "Endlich ein Zuhause, das zu Ihrem Leben passt — und nicht umgekehrt."],
     "galerie.jpg", "Innenansicht Seeblick Haus",
     "esszimmer.jpg", "Heller Wohn-Essbereich", "Großzügig, hell, durchdacht."),

    (9, "Heizen ohne Sorgen — und ohne Überraschungen.",
     "Wärmepumpe + PV-Anlage: Ihre Energiekosten bleiben planbar.",
     "Dienstag, Woche 5",
     "Warm sein. Ohne Rechnung zu fürchten.",
     ["Die Energiepreise der letzten Jahre haben vielen gezeigt: Wer auf fossile Energie setzt, ist abhängig. Wer vorausdenkt, wohnt besser.",
      "Die Seeblick Häuser sind mit modernen Wärmepumpen und PV-Anlage ausgestattet. Heizung und Warmwasser werden mit Strom betrieben — günstig, sauber, planbar.",
      "Im Sommer produziert Ihre Anlage mehr, als Sie verbrauchen. Im Winter zehren Sie davon. Und der Rest? Den speisen Sie ins Netz ein.",
      "Unabhängigkeit. Das ist auch ein Zuhause-Gefühl."],
     "visualisierung.jpg", "Seeblick Häuser Nußdorf Visualisierung",
     "terrasse3.jpg", "Außenansicht mit Garten", "Nachhaltig gebaut — für die nächste Generation."),

    (10, "Ihr Haus denkt mit.",
     "Loxone Smarthome: Licht, Heizung, Beschattung — alles aus einer Hand.",
     "Freitag, Woche 5",
     "Smart leben. Echt smart.",
     ["Smarthome — das klingt für viele nach Spielerei. Bis man es erlebt hat.",
      "Loxone ist das führende Smarthome-System aus Österreich. In den Seeblick Häusern ist es serienmäßig verbaut. Das bedeutet: Licht, Heizung, Beschattung, Alarmanlage und Türöffner — alles über eine App steuerbar.",
      "Sie kommen nach Hause: Das Licht geht an, die Heizung hat schon vorgeheizt, die Jalousien fahren hoch. Oder Sie liegen im Bett: Alles ausschalten — ein Tippen.",
      "Das ist kein Luxus. Das ist der Standard, den wir für Sie geplant haben."],
     "terrasse.jpg", "Panorama-Wohnzimmer Seeblick",
     "esszimmer.jpg", "Moderner Wohnbereich", "Loxone Smarthome — serienmäßig inklusive."),

    (11, "Schlüsselfertig. Wirklich.",
     "Einziehen und wohlfühlen — ohne Baustelle danach.",
     "Dienstag, Woche 6",
     "Einziehen. Fertig.",
     ["\"Schlüsselfertig\" — ein Wort, das viele Bauträger verwenden. Aber was steckt dahinter?",
      "Bei uns bedeutet es: Sie ziehen ein und wohnen. Keine offenen Gewerke, keine Nachbesserungsliste, keine halbfertigen Räume. Küche kann eingebaut werden, Böden sind verlegt, Bäder sind gefliest und ausgestattet.",
      "Wir bauen seit 1970. In dieser Zeit haben wir gelernt, was Familien wirklich brauchen — und was sie nicht brauchen: Stress nach dem Einzug.",
      "Ihr neues Zuhause wartet auf Sie. Schlüsselfertig."],
     "terrasse2.jpg", "Terrasse mit Blick",
     "galerie.jpg", "Fertig ausgebautes Haus", "Schlüsselfertig — bereit für Ihren Einzug."),

    (12, "Alles inklusive. Wirklich alles.",
     "Wärmepumpe, PV, Loxone, Doppelcarport — kein verstecktes Extra.",
     "Freitag, Woche 6",
     "Keine Überraschungen.",
     ["Beim Hauskauf gibt es oft eine böse Überraschung: Der Preis war günstig — aber dann kommen Extras. Carport extra. PV-Anlage extra. Böden extra.",
      "Bei den Seeblick Häusern ist das anders. Der Festpreis enthält alles: Wärmepumpe mit Fußbodenheizung, PV-Anlage, Loxone Smarthome, Doppelcarport, Gartenpflasterung, hochwertige Innenausstattung.",
      "Kein Kleingedrucktes. Kein Nachverhandeln. Ein Preis — ein Zuhause.",
      "Fragen Sie uns nach den Details. Wir erklären Ihnen alles, was drin ist."],
     "badezimmer-2.jpg", "Hochwertiges Badezimmer",
     "terrasse2.jpg", "Terrasse und Außenanlage", "Alles inklusive — ohne Ausnahme."),

    (13, "Seit 1970 bauen wir Zuhause.",
     "Über 50 Jahre Erfahrung, Hunderte realisierte Projekte — im Attergau.",
     "Dienstag, Woche 7",
     "Vertrauen, das gewachsen ist.",
     ["1970. Damals, als die Attergauer Wohnbau GmbH gegründet wurde, sah die Welt noch ganz anders aus. Seitdem haben wir Hunderte von Familien in ihr neues Zuhause begleitet.",
      "Viele dieser Familien wohnen noch heute in unseren Häusern. Manche Kinder sind inzwischen erwachsen — und kaufen selbst bei uns.",
      "Das ist kein Zufall. Das ist das Ergebnis von mehr als 50 Jahren Arbeit, Qualität und Verlässlichkeit — im Attergau, für den Attergau.",
      "Wir kennen diese Region wie unsere Westentasche. Und wir bauen hier, weil wir hier zuhause sind."],
     "visualisierung.jpg", "Seeblick Häuser Nußdorf",
     "drohne-1.jpg", "Luftbild Nußdorf am Attersee", "Nußdorf am Attersee — unsere Heimat."),

    (14, "Unser Versprechen an Sie.",
     "Persönliche Betreuung, direkter Ansprechpartner, transparente Abwicklung — von Anfang bis Schlüsselübergabe.",
     "Freitag, Woche 7",
     "Ein Ansprechpartner. Immer.",
     ["Beim Hauskauf hat man viele Fragen — und oft niemanden, der sie beantwortet. Man telefoniert sich durch, wartet auf Rückrufe, bekommt unterschiedliche Aussagen.",
      "Bei uns ist das anders. Sie haben einen direkten Ansprechpartner, der Ihr Projekt kennt und für Sie da ist — von der ersten Anfrage bis zur Schlüsselübergabe.",
      "Wir sind ein regionales Unternehmen. Kein Konzern, keine anonyme Hotline. Wenn Sie anrufen, sprechen Sie mit jemandem, der Ihr Haus kennt.",
      "Das ist unser Versprechen."],
     "terrasse3.jpg", "Terrasse und Außenbereich",
     "galerie.jpg", "Innenansicht fertiggestelltes Haus", "Persönlich, regional, verlässlich."),

    (15, "Qualität in jedem Detail.",
     "Was in Ihrem neuen Zuhause verbaut wird — und warum es einen Unterschied macht.",
     "Dienstag, Woche 8",
     "Details, die bleiben.",
     ["Ein Haus ist nur so gut wie das, was man nicht sieht. Die Leitungen hinter der Wand. Die Dämmung unter dem Boden. Die Verbindungen, die halten.",
      "Wir arbeiten seit Jahrzehnten mit denselben regionalen Handwerksbetrieben zusammen. Wir kennen ihre Arbeit. Wir vertrauen ihr.",
      "Sichtbar hochwertig: Dreifachverglasung, ebenerdige Duschen, Fliesen von Boden bis Decke, Böden mit echtem Holzdekor. Unsichtbar verlässlich: alles, was dahintersteckt.",
      "Das Ergebnis: Ein Haus, das nach 20 Jahren noch genauso gut ist wie am ersten Tag."],
     "galerie.jpg", "Innenausbau Seeblick Haus",
     "badezimmer-2.jpg", "Hochwertiges Badezimmer mit ebenerdigem Duschbereich", "Qualität, die man spürt."),

    (16, "Ihr Haus entsteht gerade.",
     "Sommer 2026 kommt schneller als man denkt.",
     "Freitag, Woche 8",
     "Es wird gebaut. Für Sie.",
     ["Während Sie diese E-Mail lesen, sind unsere Handwerker in Nußdorf. Es wird gemauert, gedämmt, verputzt.",
      "Was heute noch eine Baustelle ist, wird im Sommer 2026 Ihr Zuhause sein. Mit Ihrer Terrasse. Ihrem Seeblick. Ihrem Eingangsbereich.",
      "Das Schöne an einem Neubau: Sie können noch mitgestalten. Fliesen auswählen. Bodenfarbe bestimmen. Kleine Wünsche einbringen — solange das Haus noch entsteht.",
      "Wann möchten Sie das erste Mal draufschauen?"],
     "aussen.jpg", "Außenansicht Seeblick Häuser",
     "terrasse3.jpg", "Gartenbereich und Außenanlage", "Im Entstehen — bereit für Sie."),

    (17, "Noch wenige Häuser verfügbar.",
     "Die Seeblick Häuser sind gefragt — schauen Sie bald vorbei.",
     "Dienstag, Woche 9",
     "Warten kostet manchmal mehr.",
     ["\"Wir schauen uns das noch an\" — dieser Satz kostet manchmal mehr als man denkt.",
      "Die Seeblick Häuser sind ein kleines, exklusives Projekt in einer der begehrtesten Lagen am Attersee. Die Nachfrage ist da. Und die Anzahl der Häuser ist endlich.",
      "Wir sagen das nicht, um Druck zu machen. Wir sagen es, weil wir es ehrlich meinen: Wer sich zu lange Zeit lässt, hat am Ende vielleicht keine Wahl mehr.",
      "Wann dürfen wir Sie einladen, sich das vor Ort anzusehen?"],
     "uebersicht.jpg", "Übersicht Seeblick Häuser Nußdorf",
     "terrasse.jpg", "Wohnzimmer mit Seeblick-Panorama", "Exklusiv. Limitiert. Am Attersee."),

    (18, "Was kostet ein Leben am See?",
     "Weniger als Sie vielleicht denken. Mehr als Sie sich erhoffen.",
     "Freitag, Woche 9",
     "Der Preis für ein Leben am Attersee.",
     ["\"Das kann ich mir nicht leisten\" — ein Gedanke, den viele haben, bevor sie die Zahlen kennen.",
      "Wir laden Sie ein, uns zu fragen. Nicht für ein Angebot, das Sie verpflichtet — sondern für ein ehrliches Gespräch über Finanzierung, Fördermöglichkeiten und was wirklich auf Sie zukommt.",
      "Viele unserer Käufer haben vorher gedacht, es sei zu teuer. Dann haben sie gerechnet — und gemerkt: Mit der richtigen Finanzierung ist der Schritt kleiner als gedacht.",
      "Lassen Sie uns rechnen. Unverbindlich."],
     "drohne-1.jpg", "Attersee Luftbild Nußdorf",
     "esszimmer.jpg", "Wohn-Essbereich Seeblick Haus", "Ihr Traum — näher als Sie denken."),

    (19, "Wann dürfen wir Sie einladen?",
     "Eine Besichtigung sagt mehr als tausend Fotos.",
     "Dienstag, Woche 10",
     "Kommen Sie vorbei.",
     ["Fotos sind schön. Grundrisse sind hilfreich. Aber das Gefühl — das Gefühl, wenn Sie durch die Tür gehen und die Decke hoch ist und der See durch die Fenster leuchtet — das können wir nicht fotografieren.",
      "Das müssen Sie selbst erleben.",
      "Wir zeigen Ihnen alles vor Ort: den Rohbau, die Ausblicke, die geplante Raumaufteilung. Wir nehmen uns Zeit für Ihre Fragen — so viel, wie Sie brauchen.",
      "Schreiben Sie uns kurz oder rufen Sie an. Wir finden einen Termin, der passt."],
     "terrasse2.jpg", "Terrasse Seeblick Haus",
     "visualisierung.jpg", "Visualisierung Seeblick Häuser", "Erleben Sie es selbst."),

    (20, "Ihre Fragen — unsere Antworten.",
     "Was Menschen häufig fragen, bevor sie sich entscheiden.",
     "Freitag, Woche 10",
     "Wir hören zu.",
     ["Im Laufe der letzten Wochen haben wir Ihnen viel geschrieben. Heute möchten wir einfach fragen: Haben Sie Fragen?",
      "Was ist noch unklar? Was würden Sie gerne wissen? Finanzierung, Ausstattung, Zeitplan, Nachbarschaft — nichts ist zu klein oder zu groß.",
      "Wir antworten persönlich. Nicht mit einem Formular, nicht mit einer automatischen Antwort. Sondern mit einer echten Antwort von einem echten Menschen.",
      "Schreiben Sie uns einfach zurück."],
     "esszimmer.jpg", "Heller Wohnbereich",
     "drohne-1.jpg", "Luftbild Nußdorf Attersee", "Wir sind für Sie da — persönlich."),

    (21, "Sommer 2026 kommt.",
     "Und mit ihm die Schlüsselübergabe — sind Sie dabei?",
     "Dienstag, Woche 11",
     "Der Sommer Ihres Lebens.",
     ["Sommer 2026. Das klingt noch weit. Aber wer einmal ein Haus gebaut oder gekauft hat, weiß: Es geht schneller als man denkt.",
      "Die Entscheidung treffen. Den Vertrag unterschreiben. Materialien auswählen. Den Fortschritt beobachten. Und dann — irgendwann im Sommer — der erste Morgen am See. In Ihrem Zuhause.",
      "Wer jetzt entscheidet, kann diesen Sommer noch mitgestalten. Wer wartet, schaut vielleicht zu.",
      "Wann starten wir?"],
     "terrasse3.jpg", "Terrasse mit Bergpanorama",
     "uebersicht.jpg", "Übersicht Seeblick Häuser", "Sommer 2026 — Ihr erster Sommer am See."),

    (22, "Das erste Haus ist vergeben.",
     "Die Seeblick Häuser finden ihre Besitzer — eines nach dem anderen.",
     "Freitag, Woche 11",
     "Es geht los.",
     ["Wir können es nun offiziell sagen: Das erste der Seeblick Häuser ist reserviert.",
      "Eine Familie aus der Region hat sich entschieden. Sie haben das Haus gesehen, sich die Lage angeschaut, die Zahlen geprüft — und ja gesagt.",
      "Wir freuen uns für sie. Und wir freuen uns auf die nächste Familie, die diesen Schritt geht.",
      "Wenn Sie überlegen — jetzt wäre ein guter Zeitpunkt, den nächsten Schritt zu machen."],
     "uebersicht.jpg", "Übersicht Seeblick Häuser Nußdorf",
     "drohne-1.jpg", "Luftbild Nußdorf am Attersee", "Nußdorf am Attersee — Ihr neues Zuhause wartet."),

    (23, "Herzlich willkommen — als Nachbar.",
     "Wir freuen uns auf Sie.",
     "Dienstag, Woche 12",
     "Bald Nachbarn?",
     ["Wir schreiben Ihnen jetzt schon seit einigen Wochen. Wir haben Ihnen Bilder gezeigt, Ausblicke beschrieben, Details erklärt.",
      "Was wir Ihnen noch nicht gesagt haben: Wir würden uns wirklich freuen, Sie als Nachbarn zu begrüßen.",
      "Die Seeblick Häuser sind kein anonymes Projekt. Es sind wenige Häuser, an einem besonderen Ort. Die Menschen, die hier einziehen, werden sich kennen. Werden sich im Garten grüßen. Werden gemeinsam am See sein.",
      "Werden Sie ein Teil davon?"],
     "visualisierung.jpg", "Seeblick Häuser Nußdorf Visualisierung",
     "terrasse.jpg", "Panorama-Seeblick vom Wohnzimmer", "Nußdorf am Attersee — Gemeinschaft am See."),

    (24, "Die letzte Gelegenheit.",
     "Wer jetzt noch warten möchte — wir verstehen es. Aber wir möchten ehrlich sein.",
     "Freitag, Woche 12",
     "Letzte Chance — oder erster Schritt?",
     ["Dies ist unsere letzte E-Mail in dieser Reihe. Wir haben Ihnen in den vergangenen Wochen vieles gezeigt und erklärt. Jetzt liegt die Entscheidung bei Ihnen.",
      "Wenn etwas dagegen spricht — sagen Sie es uns. Vielleicht können wir helfen. Wenn die Zeit noch nicht reif ist — kein Problem. Wir sind weiterhin für Sie da.",
      "Und wenn ein Teil von Ihnen schon die ganze Zeit ja sagen wollte — dann ist jetzt der Moment.",
      "Wir freuen uns auf Ihren Anruf. Oder Ihre E-Mail. Oder einfach Ihren Besuch vor Ort."],
     "terrasse.jpg", "Panorama-Seeblick Wohnzimmer",
     "terrasse2.jpg", "Terrasse mit Seeblick", "Ihr Zuhause am Attersee — jetzt entscheiden."),
]

# Weißenkirchen mails
WEISSENKIRCHEN = [
    (1, "Willkommen in Weißenkirchen im Attergau.",
     "Familienfreundlich, erschwinglich, naturnah — Ihre neue Heimat wartet.",
     "Dienstag, Woche 1",
     "Ankommen. Bleiben. Zuhause sein.",
     ["Es gibt Orte, die man sucht — und Orte, die man findet. Weißenkirchen im Attergau ist ein solcher Ort.",
      "Ruhige Lage, grüne Umgebung, kurze Wege in alle Richtungen. Und jetzt: neue Reihenhäuser, die genau dazu passen.",
      "Die Reihenhäuser Weißenkirchen bieten Ihnen modernes Wohnen auf ~140 m² — mit Garten, zwei Stellplätzen, hochwertiger Ausstattung und einem Festpreis, der keine Überraschungen kennt.",
      "In den nächsten Wochen nehmen wir Sie mit — durch Räume, Details und alles, was Ihr neues Zuhause ausmacht."],
     "droneumgebung.jpg", "Weißenkirchen im Attergau Luftbild",
     "fassade.jpg", "Reihenhäuser Weißenkirchen Fassade", "Weißenkirchen im Attergau — Ihr neues Zuhause."),

    (2, "Einziehen heute. Kaufpreis heute fixiert.",
     "Mietkauf: Der Preis steht fest — egal was der Markt in 10 Jahren macht.",
     "Freitag, Woche 1",
     "Einziehen. Kaufpreis fixieren. Sicher sein.",
     ["\"Wir würden gerne kaufen — aber der Zeitpunkt ist noch nicht ideal.\" Das hören wir oft. Und genau dafür haben wir etwas, das es so kaum gibt.",
      "Unser Mietkauf funktioniert so: Sie ziehen ein, zahlen monatlich Miete — und der Kaufpreis Ihres Hauses wird vertraglich heute festgeschrieben. Nicht irgendwann. Heute. Egal wie sich Immobilienpreise oder Zinsen entwickeln.",
      "Nach 10 Jahren können Sie kaufen — zu genau diesem Preis. Ihr Grundanteil, den Sie zu Beginn leisten, wird dabei voll angerechnet. Wer früher kaufen möchte: auch das ist jederzeit möglich.",
      "Oder Sie kaufen gleich direkt — auch das geht. Sprechen Sie uns an, wir finden gemeinsam den richtigen Weg für Sie."],
     "fassade.jpg", "Reihenhäuser Weißenkirchen",
     "wohnzimmer3.jpg", "Heller Wohnbereich", "Ihr Preis. Heute fixiert. Für immer sicher."),

    (3, "Wo Kinder draußen spielen.",
     "Garten, Ruhe, sichere Nachbarschaft — ideal für Familien.",
     "Dienstag, Woche 2",
     "Für Familien gemacht.",
     ["Was braucht eine Familie wirklich? Platz. Einen Garten. Ruhige Straßen. Nachbarn, die man kennt.",
      "Die Reihenhäuser Weißenkirchen liegen in einer ruhigen, familienfreundlichen Lage — mit Garten für die Kinder, zwei Stellplätzen fürs Auto und genug Platz für alle.",
      "Schule und Kindergarten gleich in der Nähe, der nächste Einkauf in wenigen Autominuten. Und ringsum: Natur, Stille, Luft.",
      "Ein Zuhause, in dem Kinder aufwachsen können. Und Eltern durchatmen."],
     "fassade.jpg", "Garten mit Terrasse und Sandkasten in Weißenkirchen",
     "kinderzimmer.jpg", "Kinderzimmer mit viel Licht", "Familienwohnen wie es sein soll."),

    (4, "Ankommen nach einem langen Tag.",
     "Schuh aus. Tür zu. Zuhause.",
     "Freitag, Woche 2",
     "Das Gefühl des Ankommens.",
     ["Der Arbeitstag war lang. Die Kinder warten. Und dann — die Tür geht auf, der Geruch von Zuhause empfängt Sie, jemand ruft Ihren Namen.",
      "Das ist kein Film. Das kann Ihr Alltag sein.",
      "Eine großzügige Garderobe, ein offener Wohnbereich, ein Garten dahinter — die Reihenhäuser Weißenkirchen sind so geplant, dass Ankommen leichtfällt.",
      "Nicht mehr lange. Nur noch der nächste Schritt fehlt."],
     "garderobe.jpg", "Geräumige Garderobe",
     "wohnzimmer.jpg", "Heller Wohnbereich", "Ankommen — in Ihrem Zuhause."),

    (5, "Kochen, Essen, Leben.",
     "Eine Küche, die zum Mittelpunkt Ihres Zuhauses wird.",
     "Dienstag, Woche 3",
     "Die Küche — Herz des Hauses.",
     ["In keinem Raum verbringt eine Familie mehr Zeit als in der Küche. Frühstück, Mittagessen, Abendessen — aber auch Gespräche, Hausaufgaben, Planung.",
      "Die Küchen der Reihenhäuser Weißenkirchen sind offen und großzügig geplant — mit einer fließenden Verbindung zum Wohnbereich, die das Leben leichter macht. Und das Beste: Die Ausstattung wählen Sie selbst. Der Raum lässt Ihnen alle Möglichkeiten, Ihre Traumküche genau nach Ihren Wünschen zu gestalten.",
      "Kochen und dabei die Kinder im Blick haben. Gäste bewirten, ohne in der Küche zu verschwinden. Den Abend gemeinsam ausklingen lassen.",
      "Alles an einem Ort. Ihrem."],
     "kueche-vis.jpg", "Moderne Küche Reihenhäuser Weißenkirchen",
     "wohnzimmer3.jpg", "Offener Wohnbereich", "Offen, modern, einladend."),

    (6, "Der Garten gehört Ihnen.",
     "Kein Balkon, kein geteilter Hof — Ihr eigener Garten.",
     "Freitag, Woche 3",
     "Ihr eigenes Grün.",
     ["Ein Balkon ist schön. Ein Garten ist mehr.",
      "Jedes der Reihenhäuser Weißenkirchen hat einen eigenen Garten — nicht groß genug, um sich darin zu verlieren, aber groß genug für das, was zählt: Ein Tisch für den Sommer. Ein Sandkasten für die Kinder. Ein Bereich zum Grillen.",
      "Und das alles gehört Ihnen. Nicht der Hausgemeinschaft. Nicht dem Vermieter. Ihnen.",
      "Was würden Sie in Ihrem Garten als Erstes machen?"],
     "fassade.jpg", "Reihenhäuser Weißenkirchen mit Garten",
     "kinderzimmer.jpg", "Kinderzimmer", "Ihr Garten — Ihr Freiraum."),

    (7, "Schlafen wie zuhause — weil es Ihr Zuhause ist.",
     "Ruhig, dunkel, Ihres. Das Schlafzimmer in Weißenkirchen.",
     "Dienstag, Woche 4",
     "Guter Schlaf. Gutes Leben.",
     ["Schlafen ist unterschätzt. Wir verbringen ein Drittel unseres Lebens damit — und trotzdem opfern wir dem Schlafzimmer oft das wenigste.",
      "Die Schlafzimmer in den Reihenhäusern Weißenkirchen sind ruhig gelegen, mit ausreichend Platz für ein echtes Bett, Kasten, Nachttische.",
      "Kein Straßenlärm. Kein enger Raum. Nur guter Schlaf — in Ihrem eigenen Haus.",
      "Das ist kein Luxus. Das ist das, was Sie verdienen."],
     "schlafzimmer.jpg", "Helles Schlafzimmer Reihenhäuser Weißenkirchen",
     "badezimmer.jpg", "Modernes Badezimmer", "Erholung pur — in Ihrem Zuhause."),

    (8, "~140 m² für Ihr Leben.",
     "Platz für Familie, Gäste, Hobbys — und endlich genug Abstellraum.",
     "Freitag, Woche 4",
     "Endlich: echter Platz.",
     ["~140 m² klingen zunächst nach einer Zahl. Aber hinter dieser Zahl steckt: ein Wohnzimmer, das atmet. Eine Küche, die Platz lässt. Schlafzimmer, die mehr sind als Durchgangsräume. Ein Bad, das Sie morgens nicht stresst.",
      "Dazu: zwei Stellplätze, durchdachter Stauraum und ein eigener Garten. Alles, was eine Familie wirklich braucht.",
      "Die Reihenhäuser Weißenkirchen sind nicht überdimensioniert — aber sie sind durchdacht. Jeder Quadratmeter hat einen Zweck.",
      "Das merkt man beim Einziehen. Und noch mehr beim Wohnen."],
     "wohnzimmer3.jpg", "Großzügiger Wohnbereich",
     "garderobe.jpg", "Eingangsbereich und Garderobe", "Durchdacht bis in den letzten Winkel."),

    (9, "Wärme ohne Rechnung-Schock.",
     "Erdwärmepumpe, eigene PV-Anlage und Wohnraumlüftung — Ihre Energiekosten bleiben planbar.",
     "Dienstag, Woche 5",
     "Günstig heizen. Wirklich.",
     ["Die Energiekosten sind ein Thema, das bleibt. Wer jetzt ein Haus kauft oder mietet, denkt zwangsläufig daran.",
      "Die Reihenhäuser Weißenkirchen sind mit moderner Erdwärmepumpe ausgestattet — kein Gas, kein Öl, keine Abhängigkeit von schwankenden Preisen. Und auf jedem Dach erzeugt eine eigene Photovoltaik-Anlage Ihren Strom gleich selbst. Einen Hausspeicher können Sie auf Wunsch ergänzen.",
      "Dazu hochwertige Dämmung und Fußbodenheizung für gleichmäßige, günstige Wärme. Und eine zentrale Wohnraumlüftung mit Wärmerückgewinnung, die im Winter die Wärme im Haus hält — für frische Luft und niedrige Betriebskosten.",
      "Planbar warm. Planbar günstig. Das ist der Standard, den Sie verdienen."],
     "wohnzimmer.jpg", "Gemütlicher Wohnbereich mit Fußbodenheizung",
     "droneumgebung.jpg", "Reihenhäuser Weißenkirchen im Attergau von oben", "Modern, effizient, nachhaltig gebaut."),

    (10, "Ihr Kaufpreis steht — was auch immer kommt.",
     "Festpreis-Garantie: Heute fixiert, in 10 Jahren noch gültig. So schützen Sie sich vor dem Markt.",
     "Freitag, Woche 5",
     "Heute fixiert. Für immer sicher.",
     ["Immobilienpreise steigen, Zinsen schwanken, Baukosten entwickeln sich unvorhersehbar. Wer heute wartet, zahlt morgen mehr — das haben die vergangenen Jahre deutlich gezeigt.",
      "Unser Mietkauf-Modell schafft hier Sicherheit: Zu Beginn leisten Sie einen Grundanteil, anschließend zahlen Sie eine monatliche Miete — die fix bleibt und nicht an den Index angepasst wird. Und der Kaufpreis wird bereits heute vertraglich festgelegt, unabhängig von der späteren Marktentwicklung.",
      "Das ist kein Werbeversprechen, sondern eine vertraglich garantierte Festpreiszusage — ein Modell, das in dieser Form die wenigsten Bauträger sowie gemeinnützige Wohnbaugenossenschaften anbieten. Bei uns ist es fester Bestandteil. Je nach Preisentwicklung kann sich daraus für Sie ein erheblicher finanzieller Vorteil ergeben.",
      "Selbstverständlich können Sie sich auch für den sofortigen Direktkauf entscheiden — ebenfalls zum garantierten Festpreis, ohne Nachforderungen und ohne Kleingedrucktes."],
     "fassade.jpg", "Reihenhäuser Weißenkirchen Fassade",
     "wohnzimmer3.jpg", "Heller Wohnbereich", "Festpreis — heute, morgen, in 10 Jahren."),

    (11, "Schlüsselfertig — oder nach Ihren Wünschen.",
     "Standardausstattung oder eigene Akzente setzen — beides ist möglich.",
     "Dienstag, Woche 6",
     "So wie Sie wollen.",
     ["Schlüsselfertig — das klingt manchmal nach: keine Mitsprache. Aber das muss nicht so sein.",
      "Solange Ihr Haus noch im Bau ist, können Sie mitgestalten. Fliesenfarbe, Bodenbelag, kleine Extras — reden Sie mit uns. Wir schauen, was möglich ist.",
      "Das Grundpaket ist bereits hochwertig. Aber ein Zuhause wird wirklich Ihres, wenn Ihre Handschrift drin steckt.",
      "Was wünschen Sie sich?"],
     "wohnzimmer.jpg", "Wohnzimmer Reihenhäuser Weißenkirchen",
     "kueche-vis.jpg", "Moderne Küche", "Ihr Haus. Ihre Entscheidungen."),

    (12, "So funktioniert unser Mietkauf — und warum er anders ist.",
     "Kein gewöhnlicher Mietkauf: Ihr Kaufpreis wird heute vertraglich fixiert — mit allen Vorteilen.",
     "Freitag, Woche 6",
     "Mietkauf — aber richtig.",
     ["Viele kennen Mietkauf nur vom Hörensagen. Was die meisten nicht wissen: Es gibt große Unterschiede — und unser Modell gehört zu den käuferfreundlichsten überhaupt.",
      "So funktioniert es: Sie leisten zu Beginn einen Grundanteil, der am Ende voll auf den Kaufpreis angerechnet wird. Sie ziehen ein und zahlen eine monatliche Miete — die über die gesamte Laufzeit fix bleibt und nicht an den Index angepasst wird. Der Kaufpreis wird heute vertraglich festgeschrieben — für 10 Jahre. Kein Zinsrisiko. Keine Preissteigerung. Keine bösen Überraschungen.",
      "Nach 10 Jahren kaufen Sie zum vereinbarten Preis — Grundanteil bereits abgezogen. Wer früher kaufen möchte: auch das ist jederzeit nach Absprache möglich.",
      "Das Ergebnis: Sie wohnen sofort in Ihrem Haus, gewinnen Zeit für die Finanzierung — und sind trotzdem vor dem Markt geschützt. Das ist kein Kompromiss. Das ist eine kluge Entscheidung."],
     "garderobe.jpg", "Eingangsbereich Reihenhäuser",
     "fassade.jpg", "Außenansicht Reihenhäuser Weißenkirchen", "Mietkauf — käuferfreundlich wie kaum woanders."),

    (13, "Seit 1970 bauen wir Zuhause.",
     "Im Attergau kennt man uns — seit über 50 Jahren.",
     "Dienstag, Woche 7",
     "Erfahrung, die trägt.",
     ["Bauträger gibt es viele. Bauträger, die seit 1970 im Attergau bauen — einen.",
      "In dieser Zeit haben wir hunderte Familien begleitet. Vom ersten Gespräch bis zum Schlüssel. Vom Traum bis zur Wirklichkeit.",
      "Wir kennen die Region. Wir kennen die Handwerker. Wir kennen die Behörden. Und wir wissen: Was beim Bauen zählt, ist nicht nur das Gebäude — sondern das Vertrauen.",
      "Das haben wir uns aufgebaut. Über Generationen."],
     "droneumgebung.jpg", "Attergau Luftbild",
     "fassade.jpg", "Reihenhäuser Weißenkirchen", "Über 50 Jahre Erfahrung im Attergau."),

    (14, "Was Menschen bei uns schätzen.",
     "Persönliche Betreuung, direkte Kommunikation, regionale Verwurzelung.",
     "Freitag, Woche 7",
     "Was unsere Käufer sagen.",
     ["\"Man merkt, dass es ein Familienunternehmen ist.\" Das hören wir oft. Und wir freuen uns darüber.",
      "Kein Konzern, keine anonyme Hotline, kein Durchverbinden. Wenn Sie uns anrufen, sprechen Sie mit jemandem, der Ihr Projekt kennt und für Sie da ist.",
      "Das klingt selbstverständlich — ist es aber nicht. In einer Branche, die oft von großen Investoren und anonymen Strukturen geprägt ist, sind wir bewusst anders.",
      "Regional. Persönlich. Verlässlich. Seit 1970."],
     "fassade.jpg", "Reihenhäuser Weißenkirchen",
     "wohnzimmer3.jpg", "Heller Wohnbereich", "Persönlich betreut — von Anfang bis Ende."),

    (15, "Qualität, die man anfassen kann.",
     "Was in Ihren Wänden steckt — und warum es einen Unterschied macht.",
     "Dienstag, Woche 8",
     "Gut gemacht. Wirklich.",
     ["Hochwertig — das sagen viele. Was steckt bei uns dahinter?",
      "Markenfliesen, ebenerdige Duschen, dreifachverglaste Fenster, Fußbodenheizung, hochwertige Türen und Böden. Und dahinter: ordentlich ausgeführte Installationen, gute Dämmung, sorgfältige Verarbeitung.",
      "Wir arbeiten mit denselben regionalen Handwerksbetrieben seit Jahrzehnten. Weil Qualität auch eine Frage des Vertrauens ist.",
      "Das Ergebnis sehen — und spüren — Sie, wenn Sie durch die Tür gehen."],
     "badezimmer.jpg", "Hochwertiges Badezimmer",
     "schlafzimmer.jpg", "Helles Schlafzimmer", "Qualität, die langfristig trägt."),

    (16, "Kommen Sie vorbei — es steht bereits.",
     "Die Reihenhäuser in Weißenkirchen können Sie sich jetzt ansehen.",
     "Freitag, Woche 8",
     "Überzeugen Sie sich selbst.",
     ["Fotos können nur zeigen, wie etwas aussieht. Nicht, wie es sich anfühlt.",
      "Kommen Sie vorbei. Gehen Sie durch die Räume. Stehen Sie im Garten. Schauen Sie nach draußen.",
      "Wir zeigen Ihnen alles — ohne Druck, ohne Verkaufsgespräch. Einfach das Haus, die Lage, die Atmosphäre.",
      "Ein Termin genügt. Und oft genügt er, um zu wissen."],
     "fassade.jpg", "Reihenhäuser Weißenkirchen",
     "garderobe.jpg", "Eingangsbereich", "Sehen ist glauben — kommen Sie vorbei."),

    (17, "Noch Häuser verfügbar — aber nicht mehr lange.",
     "Die Reihenhäuser Weißenkirchen finden ihre Besitzer.",
     "Dienstag, Woche 9",
     "Jetzt ist der richtige Zeitpunkt.",
     ["Wir möchten ehrlich mit Ihnen sein: Die Reihenhäuser Weißenkirchen stoßen auf echtes Interesse.",
      "Familien suchen genau das: Ein Haus mit Garten, ruhige Lage, faire Konditionen. Das passt.",
      "Wer heute konkret nachfragt, hat noch die Wahl — Haus, Lage innerhalb der Anlage, Ausstattungsdetails.",
      "Wer wartet, hat vielleicht bald weniger davon. Das ist keine Drohung — das ist einfach die Realität."],
     "fassade.jpg", "Reihenhäuser Weißenkirchen Übersicht",
     "droneumgebung.jpg", "Weißenkirchen im Attergau", "Jetzt entscheiden — solange die Wahl noch groß ist."),

    (18, "Sofort kaufen oder Mietkauf — was ist besser für Sie?",
     "Beide Wege führen ins Eigenheim. Welcher der richtige ist, finden wir gemeinsam heraus.",
     "Freitag, Woche 9",
     "Zwei Wege. Ein Ziel.",
     ["Manche sind bereit und wollen sofort kaufen — Direktkauf zum Festpreis, schlüsselfertig, fertig. Andere schätzen die Flexibilität: einziehen, Kaufpreis heute sichern, Zeit für die Finanzierung gewinnen. Beides ist möglich.",
      "Was viele beim Mietkauf nicht sofort sehen: Es ist kein Kompromiss. Es ist eine strategische Entscheidung. Wer heute seinen Kaufpreis festschreibt, schützt sich vor allem, was der Markt in den nächsten Jahren tun könnte.",
      "Ob Zinsen steigen, Baupreise anziehen oder Immobilien teurer werden — Ihr Preis steht. Vertraglich. Unveränderlich.",
      "In welcher Situation stecken Sie gerade? Rufen Sie uns an. Kein Verkaufsgespräch, kein Druck — einfach ein ehrliches Gespräch darüber, welcher Weg für Sie Sinn macht."],
     "wohnzimmer3.jpg", "Wohnzimmer Reihenhäuser",
     "kueche-vis.jpg", "Moderne Küche", "Ihr Weg ins Eigenheim — wir begleiten Sie."),

    (19, "Wir laden Sie ein.",
     "Eine Besichtigung ist der einfachste Weg zur Entscheidung.",
     "Dienstag, Woche 10",
     "Lernen Sie Ihr neues Zuhause kennen.",
     ["In den letzten Wochen haben Sie viel gelesen. Jetzt ist es Zeit, etwas zu erleben.",
      "Wir laden Sie herzlich zu einer persönlichen Besichtigung ein. Sie sehen das Haus, den Garten, die Lage. Wir erklären, zeigen, beantworten.",
      "Keine Verpflichtung. Kein Druck. Einfach ein ehrliches Gespräch über ein Haus, das gut zu Ihnen passen könnte.",
      "Wann haben Sie Zeit?"],
     "garderobe.jpg", "Eingangsbereich und Garderobe",
     "fassade.jpg", "Reihenhäuser Weißenkirchen", "Persönlich. Vor Ort. Unverbindlich."),

    (20, "Haben Sie noch Fragen?",
     "Wir sind für Sie da — schreiben oder rufen Sie einfach an.",
     "Freitag, Woche 10",
     "Einfach fragen.",
     ["In diesen Wochen haben wir viel geschrieben. Heute halten wir inne und fragen: Was beschäftigt Sie noch?",
      "Manchmal ist es eine konkrete Frage zur Ausstattung. Manchmal ein Zweifel zur Finanzierung. Manchmal einfach: \"Ich bin noch nicht sicher.\"",
      "All das dürfen Sie uns sagen. Wir hören zu — ohne Verkaufsdruck, ohne vorgefertigte Antworten.",
      "Schreiben Sie uns. Oder rufen Sie einfach an."],
     "droneumgebung.jpg", "Weißenkirchen im Attergau Luftbild",
     "wohnzimmer.jpg", "Heller Wohnbereich", "Wir hören zu — immer."),

    (21, "Ihr neues Zuhause ist bereit.",
     "Die Reihenhäuser stehen — Sie können jederzeit einziehen.",
     "Dienstag, Woche 11",
     "Bereit, wenn Sie es sind.",
     ["Das Schöne ist: Sie müssen auf nichts mehr warten. Ihr neues Zuhause in Weißenkirchen steht bereit — der Einzug ist jederzeit möglich.",
      "Und stellen Sie sich vor, wie nah das alles auf einmal ist: der erste Abend im eigenen Garten. Die Kinder, die zum ersten Mal draußen spielen. Das erste Frühstück im eigenen Zuhause. Kein ferner Traum mehr — sondern zum Greifen nah.",
      "Sie entscheiden, wann es losgeht. Ob in wenigen Wochen oder wann immer es für Sie passt — Ihr Haus wartet auf Sie.",
      "Wie schön wäre es, wenn dieser Sommer schon Ihr erster Sommer im neuen Zuhause wird?"],
     "fassade.jpg", "Reihenhäuser Weißenkirchen mit Garten",
     "droneumgebung.jpg", "Weißenkirchen Umgebung", "Ihr neues Zuhause — bereit, wenn Sie es sind."),

    (22, "Das erste Haus ist reserviert.",
     "Die Reihenhäuser Weißenkirchen finden ihre Familien.",
     "Freitag, Woche 11",
     "Es geht los.",
     ["Eine Familie hat sich entschieden. Das erste der Reihenhäuser Weißenkirchen ist reserviert.",
      "Wir freuen uns für sie — und wir freuen uns auf alle weiteren Familien, die diesen Schritt gehen.",
      "Die Häuser, die noch verfügbar sind, warten auf die richtigen Menschen. Vielleicht sind das Sie.",
      "Wann machen Sie den nächsten Schritt?"],
     "fassade.jpg", "Reihenhäuser Weißenkirchen",
     "kinderzimmer.jpg", "Kinderzimmer", "Weißenkirchen — eine Gemeinschaft entsteht."),

    (23, "Wir freuen uns auf Sie als Nachbarn.",
     "Willkommen in Weißenkirchen — bald.",
     "Dienstag, Woche 12",
     "Bald Nachbarn?",
     ["Wir haben Ihnen jetzt einige Wochen lang geschrieben. Wir haben Räume beschrieben, Zahlen erklärt, Gefühle skizziert.",
      "Was wir nicht so leicht in Worte fassen können: Wie es sich anfühlt, zum ersten Mal die Haustür aufzumachen — und zu wissen, dass sie Ihre ist.",
      "Wir bauen Häuser. Aber was wirklich entsteht, sind Zuhause. Für echte Menschen. Für Familien, die ankommen wollen.",
      "Seien Sie dabei."],
     "wohnzimmer3.jpg", "Heller Wohnbereich Reihenhäuser",
     "fassade.jpg", "Reihenhäuser Weißenkirchen", "Ihr neues Zuhause — in Weißenkirchen."),

    (24, "Letzte Möglichkeit.",
     "Dies ist unsere letzte E-Mail — aber nicht das letzte Angebot.",
     "Freitag, Woche 12",
     "Das Ende dieser Reihe. Nicht das Ende der Möglichkeit.",
     ["Das ist unsere letzte E-Mail in dieser Serie. Wir haben Ihnen viel erzählt — und wir hoffen, dass davon etwas hängengeblieben ist.",
      "Wenn Sie sich vorstellen konnten, in Weißenkirchen zu wohnen — dann nehmen Sie sich diesen Gedanken ernst. Nicht jedes Mal kommt eine neue Gelegenheit.",
      "Und wenn der Zeitpunkt noch nicht stimmt — kein Problem. Melden Sie sich, wenn er es tut. Wir sind da.",
      "Bis dahin: Alles Gute. Und danke, dass Sie dabei waren."],
     "droneumgebung.jpg", "Weißenkirchen im Attergau",
     "fassade.jpg", "Reihenhäuser Weißenkirchen", "Weißenkirchen wartet auf Sie."),
]


def make_html(nr, series, betreff, preheader, versand, headline, body_paras,
              hero_img, hero_alt, extra_img, extra_alt, extra_caption,
              img_base, ctas, url, subtitle, kennzahlen):
    cta = ctas[(nr - 1) % 4]
    paras_html = "\n".join(
        f'<p style="margin:0 0 16px 0; font-size:16px; color:#4a6070; line-height:1.8;">{ent(p)}</p>'
        for p in body_paras
    )
    kenn = kennzahlen
    e_betreff    = ent(betreff)
    e_preheader  = ent(preheader)
    e_headline   = ent(headline)
    e_subtitle   = ent(subtitle)
    e_cta_intro  = ent(cta["intro"])
    e_cta_text   = ent(cta["text"])
    e_hero_alt   = ent(hero_alt)
    e_extra_alt  = ent(extra_alt)
    e_extra_cap  = ent(extra_caption)
    e_k0v = ent(kenn[0][0]); e_k0l = ent(kenn[0][1])
    e_k1v = ent(kenn[1][0]); e_k1l = ent(kenn[1][1])
    e_k2v = ent(kenn[2][0]); e_k2l = ent(kenn[2][1])
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!--
    BETREFF:   {betreff}
    PREHEADER: {preheader}
    VERSAND:   {versand}
  -->
  <title>{ent(series)} &ndash; Newsletter {nr:02d}</title>
  <style>@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');</style>
</head>
<body style="margin:0; padding:0; background-color:#f4f7fb; font-family:Arial,Helvetica,sans-serif;">

  <div style="display:none; max-height:0; overflow:hidden; mso-hide:all;">
    {e_preheader}&nbsp;&#8204;&nbsp;&#8204;&nbsp;&#8204;&nbsp;&#8204;&nbsp;&#8204;
  </div>

  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f4f7fb;">
    <tr>
      <td align="center" style="padding:32px 16px;">
        <table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px; width:100%; background-color:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 4px 24px rgba(103,153,204,0.12);">

          <!-- HEADER -->
          <tr>
            <td style="background-color:#6799CC; padding:28px 40px 24px 40px; text-align:center;">
              <p style="margin:0; font-family:'Pacifico',Georgia,serif; font-size:28px; color:#ffffff; font-weight:400; line-height:1.2;">
                Attergauer Wohnbau
              </p>
              <p style="margin:8px 0 0 0; font-size:11px; color:rgba(255,255,255,0.8); letter-spacing:2.5px; text-transform:uppercase;">
                {e_subtitle}
              </p>
            </td>
          </tr>

          <!-- HERO -->
          <tr>
            <td style="padding:0; line-height:0; background-color:#dce8f4; min-height:260px; font-size:0;">
              <img src="{img_base}{hero_img}" alt="{e_hero_alt}" width="600"
                   style="width:100%; max-width:600px; height:auto; display:block; border:0;">
            </td>
          </tr>

          <!-- INHALT -->
          <tr>
            <td style="padding:40px 40px 36px 40px;">
              <h1 style="margin:0 0 20px 0; font-size:28px; color:#1a2a3a; line-height:1.3; font-family:Georgia,serif; font-weight:400;">
                {e_headline}
              </h1>
              <p style="margin:0 0 16px 0; font-size:16px; color:#4a6070; line-height:1.8;">
                Guten Tag,
              </p>

{paras_html}

              <hr style="border:none; border-top:1px solid #e8f0f8; margin:32px 0 28px 0;">
              <p style="margin:0 0 20px 0; font-size:15px; color:#4a6070; line-height:1.7;">{e_cta_intro}</p>
              <table cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="border-radius:50px; background-color:#6799CC;">
                    <a href="{cta["href"]}"
                       style="display:inline-block; padding:14px 32px; font-size:15px; font-weight:600; color:#ffffff; text-decoration:none !important; border-bottom:none !important; border-radius:50px; letter-spacing:0.3px;">
                      {e_cta_text}
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- EXTRA BILD -->
          <tr>
            <td style="padding:0 40px 32px 40px; background-color:#ffffff;">
              <div style="border-radius:12px; overflow:hidden; background-color:#dce8f4; line-height:0; min-height:180px;">
                <img src="{img_base}{extra_img}" alt="{e_extra_alt}" width="520"
                     style="width:100%; height:auto; display:block; border:0; border-radius:12px;">
              </div>
              <p style="margin:10px 0 0 0; font-size:12px; color:#aabccc; text-align:center; font-style:italic;">{e_extra_cap}</p>
            </td>
          </tr>

          <!-- KENNZAHLEN -->
          <tr>
            <td style="background-color:#f4f7fb; padding:24px 40px; border-top:1px solid #e8f0f8;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td width="33%" style="text-align:center; padding:8px;">
                    <p style="margin:0; font-size:15px; font-weight:700; color:#6799CC; line-height:1.2;">{e_k0v}</p>
                    <p style="margin:4px 0 0 0; font-size:11px; color:#7a9ab0; text-transform:uppercase; letter-spacing:1.5px;">{e_k0l}</p>
                  </td>
                  <td width="1px" style="background:#dde8f2;">&nbsp;</td>
                  <td width="33%" style="text-align:center; padding:8px;">
                    <p style="margin:0; font-size:22px; font-weight:700; color:#6799CC; line-height:1;">{e_k1v}</p>
                    <p style="margin:4px 0 0 0; font-size:11px; color:#7a9ab0; text-transform:uppercase; letter-spacing:1.5px;">{e_k1l}</p>
                  </td>
                  <td width="1px" style="background:#dde8f2;">&nbsp;</td>
                  <td width="33%" style="text-align:center; padding:8px;">
                    <p style="margin:0; font-size:15px; font-weight:700; color:#6799CC; line-height:1.2;">{e_k2v}</p>
                    <p style="margin:4px 0 0 0; font-size:11px; color:#7a9ab0; text-transform:uppercase; letter-spacing:1.5px;">{e_k2l}</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- FOOTER -->
          <tr>
            <td style="background-color:#1a2a3a; padding:32px 40px; border-radius:0 0 16px 16px;">
              <p style="margin:0 0 2px 0; font-family:'Pacifico',Georgia,serif; font-size:18px; color:#ffffff; font-weight:400; line-height:1.4;">
                Attergauer Wohnbau GmbH
              </p>
              <p style="margin:0 0 16px 0; font-size:13px; color:#7a9ab0; line-height:1.8;">
                Ihr regionaler Bauträger seit 1970<br>
                4880 St. Georgen im Attergau · Österreich<br>
                <a href="tel:+436648249411" style="color:#6799CC; text-decoration:none;">+43 664 82 49 411</a>
                &nbsp;·&nbsp;
                <a href="mailto:office@attergauer-wohnbau.at" style="color:#6799CC; text-decoration:none;">office@attergauer-wohnbau.at</a>
              </p>
              <hr style="border:none; border-top:1px solid #2a3d52; margin:0 0 16px 0;">
              <p style="margin:0; font-size:12px; color:#4a6070; line-height:1.7;">
                Sie erhalten diese E-Mail, weil Sie Interesse an unseren Projekten bekundet haben.<br>
                <a href="{{{{ unsubscribe }}}}" style="color:#6799CC; text-decoration:underline;">Vom Newsletter abmelden</a>
                &nbsp;·&nbsp;
                <a href="https://www.attergauer-wohnbau.at/datenschutz/" style="color:#6799CC; text-decoration:underline;">Datenschutz</a>
                &nbsp;·&nbsp;
                <a href="https://www.attergauer-wohnbau.at/impressum/" style="color:#6799CC; text-decoration:underline;">Impressum</a>
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


KENN_N = [
    ("Panorama-Seeblick", "aus jedem Stockwerk"),
    ("~180 m²", "Wohnfläche"),
    ("Sommer 2026", "Übergabe"),
]
KENN_W = [
    ("Festpreis", "keine Überraschungen"),
    ("~140 m²", "Wohnfläche"),
    ("Mietkauf", "möglich"),
]

# Generate Nußdorf
os.makedirs(f"{BASE}/nussdorf", exist_ok=True)
for row in NUSSDORF:
    nr, betreff, preheader, versand, headline, body, hero, hero_alt, extra, extra_alt, extra_cap = row
    html = make_html(nr, "Seeblick Häuser Nußdorf", betreff, preheader, versand,
                     headline, body, hero, hero_alt, extra, extra_alt, extra_cap,
                     IMG_N, CTAS_N, URL_N,
                     "Seeblick Häuser · Nußdorf am Attersee", KENN_N)
    path = f"{BASE}/nussdorf/nussdorf-{nr:02d}.html"
    with open(path, "w") as f:
        f.write(html)
print(f"✓ {len(NUSSDORF)} Nußdorf Mails generiert")

# Generate Weißenkirchen
os.makedirs(f"{BASE}/weissenkirchen", exist_ok=True)
for row in WEISSENKIRCHEN:
    nr, betreff, preheader, versand, headline, body, hero, hero_alt, extra, extra_alt, extra_cap = row
    html = make_html(nr, "Reihenhäuser Weißenkirchen", betreff, preheader, versand,
                     headline, body, hero, hero_alt, extra, extra_alt, extra_cap,
                     IMG_W, CTAS_W, URL_W,
                     "Reihenhäuser · Weißenkirchen im Attergau", KENN_W)
    path = f"{BASE}/weissenkirchen/weissenkirchen-{nr:02d}.html"
    with open(path, "w") as f:
        f.write(html)
print(f"✓ {len(WEISSENKIRCHEN)} Weißenkirchen Mails generiert")
print("\nAlle 48 Mails fertig!")
