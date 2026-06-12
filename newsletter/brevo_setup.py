#!/usr/bin/env python3
"""
AWB Brevo Template Upload
=========================
Lädt alle 48 Newsletter-Templates in Brevo hoch.
Danach bauen Sie 2 Automations in der Brevo-UI.

AUSFÜHREN:
  export BREVO_KEY="dein-api-key-hier"
  python3 brevo_setup.py

OPTIONEN:
  python3 brevo_setup.py --test    # Nur die ersten 2 pro Serie testen
"""

import os, sys, json, time, re
from pathlib import Path
import urllib.request, urllib.error

API = "https://api.brevo.com/v3"
BASE = Path(__file__).parent


def get_key():
    key = os.environ.get("BREVO_KEY", "").strip()
    if not key:
        print("FEHLER: BREVO_KEY nicht gesetzt.")
        print('  export BREVO_KEY="dein-api-key"')
        sys.exit(1)
    return key


def api(method, path, data=None, key=None):
    url = f"{API}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("api-key", key)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode()
        print(f"\n  HTTP {e.code}: {body_txt[:300]}")
        raise


def read_html_meta(path):
    content = Path(path).read_text()
    subject   = re.search(r"BETREFF:\s+(.+)",   content)
    preheader = re.search(r"PREHEADER:\s+(.+)", content)
    return (
        subject.group(1).strip()   if subject   else "Newsletter",
        preheader.group(1).strip() if preheader else "",
    )


def create_template(name, subject, html, key):
    """Erstellt ein E-Mail-Template. Gibt die ID zurück."""
    data = {
        "templateName": name,
        "subject":      subject,
        "htmlContent":  html,
        "sender":       {"name": "Attergauer Wohnbau GmbH",
                         "email": "news@attergauer-wohnbau.at"},
        "isActive":     True,
    }
    result = api("POST", "/smtp/templates", data, key=key)
    return result["id"]


def main():
    test_mode = "--test" in sys.argv
    key = get_key()
    print("✓ API-Key gefunden\n")

    series = [
        {"folder": BASE / "nussdorf",       "prefix": "nussdorf",
         "label": "Nußdorf",       "count": 24},
        {"folder": BASE / "weissenkirchen", "prefix": "weissenkirchen",
         "label": "Weißenkirchen", "count": 24},
    ]

    created   = []
    errors    = []

    for s in series:
        print(f"━━━ Serie: {s['label']} ━━━")
        limit = 2 if test_mode else s["count"]
        for i in range(1, limit + 1):
            filename = s["folder"] / f"{s['prefix']}-{i:02d}.html"
            if not filename.exists():
                print(f"  [{i:02d}] FEHLER: Datei fehlt: {filename}")
                errors.append(str(filename))
                continue

            subject, _ = read_html_meta(filename)
            html = filename.read_text()
            tpl_name = f"AWB {s['label']} {i:02d} – {subject[:55]}"

            print(f"  [{i:02d}] {subject[:50]}…", end=" ", flush=True)
            try:
                tid = create_template(tpl_name, subject, html, key)
                print(f"→ Template-ID {tid}")
                created.append({"id": tid, "series": s["label"],
                                 "nr": i, "name": tpl_name, "subject": subject})
                time.sleep(0.3)
            except Exception as e:
                print(f"FEHLER: {e}")
                errors.append(tpl_name)
        print()

    # IDs speichern
    ids_file = BASE / "brevo_template_ids.json"
    with open(ids_file, "w") as f:
        json.dump(created, f, indent=2, ensure_ascii=False)

    print("=" * 60)
    print(f"✓ {len(created)} Templates hochgeladen")
    if errors:
        print(f"✗ {len(errors)} Fehler: {errors}")
    print(f"\nTemplate-IDs gespeichert in: {ids_file.name}")

    # Anleitung ausgeben
    n_ids = [c for c in created if c["series"] == "Nußdorf"]
    w_ids = [c for c in created if c["series"] == "Weißenkirchen"]

    print("""
╔══════════════════════════════════════════════════════════════╗
║           NÄCHSTE SCHRITTE — AUTOMATION IN BREVO             ║
╚══════════════════════════════════════════════════════════════╝

1. Brevo öffnen → Automations → "Neue Automation erstellen"

2. SERIE NUSSDORF:
   Trigger: "Kontakt einer Liste hinzugefügt"
            Liste: AWB Nußdorf 8

   Dann für jede Mail:
   → Aktion:  "E-Mail senden" → Template auswählen (siehe unten)
   → Warten:  1 Minute  (Testlauf — später auf 3–4 Tage ändern)
""")

    for c in n_ids:
        print(f"   Mail {c['nr']:02d}: ID {c['id']:6d}  {c['subject'][:50]}")

    print("""
3. SERIE WEISSENKIRCHEN:
   Trigger: "Kontakt einer Liste hinzugefügt"
            Liste: AWB Weißenkirchen
""")
    for c in w_ids:
        print(f"   Mail {c['nr']:02d}: ID {c['id']:6d}  {c['subject'][:50]}")

    print("""
4. Automation aktivieren → Test: sich selbst zur Liste hinzufügen
   → Die Mails kommen dann im 1-Minuten-Takt

5. Vor dem echten Start:
   → Wartezeiten auf Di/Fr-Rhythmus ändern:
     Mail 1 → 3 Tage → Mail 2 → 4 Tage → Mail 3 → 3 Tage → …
     (Di nach Fr = 3 Tage, Fr nach Di = 4 Tage)
""")


if __name__ == "__main__":
    main()
