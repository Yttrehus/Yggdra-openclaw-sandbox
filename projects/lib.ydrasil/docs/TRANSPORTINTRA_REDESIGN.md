# TransportIntra App — Redesign Plan

**Dato:** 17. februar 2026
**Formål:** Komplet designdokumentation til brug som Nano Banana Pro prompt for visuel mockup-generering.

---

## 1. NUVÆRENDE TILSTAND

### 1.1 Teknologi
- jQuery Mobile 1.4.5 (fra 2014) — standardknapper, headers, pages
- Appen er en klon af TransportIntra's officielle webapp
- Dark mode tilføjet ovenpå original lys CSS
- Hamburger-menu med ~10 punkter
- Primært brugt på Android telefon i **vertikal** og **horisontal** orientering

### 1.2 Skærme (Pages) — Nuværende

| # | Skærm | Hvad den gør | Problem |
|---|--------|-------------|---------|
| 1 | **Login** | Brugernavn + password | Fungerer, men kedelig. Ingen branding. |
| 2 | **Menu** | 7 knapper lodret (Kørelister, Manuel ordre, Tidsreg, Info, Chat, Opsætning, Log ud) | Alt for mange valgmuligheder. Kris bruger kun 2-3 dagligt. |
| 3 | **Køreliste** | Dato-navigation (←kalender→), liste af ruter for dagen | OK men knapperne er små |
| 4 | **Rute-oversigt** | Det aktive stop + kort + stopknapper | **Hovedskærmen** — her tilbringer Kris 90% af tiden. For mange knapper, ujævn layout. |
| 5 | **Rute fuld liste** | Alle stops i rækkefølge | Simpel, virker |
| 6 | **Tidsregistrering** | Forvogn/påhæng valg + start/pause/slut/godkend | Brugt dagligt morgen+aften. Mange knapper gemt i collapsed sektioner. |
| 7 | **Besked (fejlmelding)** | Textarea + billede + signatur + GPS | Bruges ved containerfejl |
| 8 | **Kvittering** | Signatur-capture + bemærkninger | Sjældent brugt |
| 9 | **Chat** | Intern chat med chauffører/kontor | Sjældent brugt |
| 10 | **Opsætning** | Font-størrelse slider + privatlivspolitik | Næsten aldrig brugt |

### 1.3 Vigtigste UI-problemer nu

1. **jQuery Mobile æstetik** — ser ud som 2014. Runde grå knapper, grå gradients, ingen visuel identitet.
2. **Ingen hierarki** — alle knapper er lige store/vigtige. Kris' 3 daglige handlinger (start vagt, åbn rute, afslut stop) drukner i 20 andre knapper.
3. **Vægt-bar** er gemt i header (↩ 0 kg ↪ 🚛) — svær at se og bruge.
4. **Kortet** tager 50% af skærmen i rutevisning men kontrolknapperne (Vis alle, Centrér, Følg, Mørk, +Pin) er små og utydeligt placeret.
5. **Sorteringsknappen** (Kris' kerneproblem) er gemt som en lille tekst-knap "Sortering" mellem andre knapper.
6. **Ingen dashboard/overblik** — man hopper direkte fra login til menu til rute.

---

## 2. DESIGN VISION

### 2.1 Designfilosofi

**"Cockpit for en chauffør"** — Kris sidder i en lastbil og kigger hurtigt på sin telefon. Hvert visuelt element skal være:
- Stort nok til at ramme med tommelfingeren mens man kører
- Kontrastfuldt nok til at læse i sollys og mørke
- Organiseret efter **frekvens af brug**, ikke logisk kategori

### 2.2 Farvepalette

| Rolle | Farve | Hex | Brug |
|-------|-------|-----|------|
| Baggrund | Dyb natblå | `#0d1117` | Alle skærme |
| Surface | Mørk grå | `#161b22` | Kort, paneler, sektioner |
| Primary | Ydrasil-grøn | `#34A853` | Primære handlinger (Afslut, Start, OK) |
| Secondary | Amber/guld | `#F5A623` | Sortering, advarsler, "næste stop" |
| Danger | Rød | `#E54D42` | Afvis, fejl, slet |
| Info | Blå | `#4FC3F7` | Afstande, info, links |
| Text primary | Hvid | `#E6EDF3` | Al tekst |
| Text muted | Grå | `#8B949E` | Sekundær info |
| Border | Kant-grå | `#30363D` | Separatorer |

### 2.3 Typografi

- **Font:** Inter eller system-default sans-serif
- **Overskrifter:** 18-22px, bold, hvid
- **Body:** 16px, regular, lys grå
- **Knapper:** 16-18px, bold, VERSALER på primære handlinger
- **Afstande/data:** 14px, monospace eller tabular

---

## 3. SKÆRM-FOR-SKÆRM REDESIGN

### 3.1 LOGIN

**Nu:** Simpel form med to felter, "Log ind"-knap og "Glemt kode"-link. Ingen branding.

**Nyt design:**
- Centered layout med Ydrasil-logo (Y-træ ikon) øverst
- Undertekst: "Rute 256 — Organisk Affald"
- Input-felter med afrundede hjørner, mørk baggrund, hvid tekst
- Stor grøn "LOG IND" knap (fuld bredde)
- Subtil gradient fra `#0d1117` til `#161b22`
- Ingen "Glemt kode" (bruges aldrig)

**Prompt til billede:**
> Dark mobile login screen. Deep navy background (#0d1117). Centered white tree logo (Y shape) at top. Below: "Ydrasil" in elegant white serif text, smaller "Rute 256" subtitle. Two rounded input fields with dark gray background and white text: "Brugernavn" and "Adgangskode". Large green (#34A853) rounded button "LOG IND" full width below. Minimal, clean, modern. Mobile portrait 390x844px.

---

### 3.2 DASHBOARD (erstatter den gamle Menu-side)

**Nu:** 7 jQuery Mobile-knapper lodret stablet. Ingen kontekst, ingen data.

**Nyt design — "Morgenbriefing":**
- **Top-bar:** Dato + ugedag + klokkeslæt, vognregistrering
- **Status-kort:** Stort kort med:
  - "Rute 256 — Tirsdag" som overskrift
  - Status: "Ikke startet" / "I gang — 12/47 stops"
  - Progressbar (grøn)
  - Estimeret sluttid
- **Quick Actions** (3 store knapper i en række):
  - 🚛 **START VAGT** (grøn, primær)
  - 📋 **ÅBEN RUTE** (blå)
  - ⚖️ **VEJNING** (amber)
- **Sekundære handlinger** (mindre, under):
  - Manuel ordre | Chat | Opsætning
- **Bund:** Vægt-status som altid-synlig footer: "Affald: 0 kg | Total: 12.340 kg"

**Prompt til billede:**
> Dark mobile dashboard screen. Navy background (#0d1117). Top bar shows "Tirsdag 17. feb" and time. Large status card with dark gray background (#161b22): "Rute 256 — Tirsdag" header, green progress bar at 25%, text "12/47 stops afsluttet", "ETA: 14:30". Below: three large rounded action buttons in a row: green "START VAGT" with truck icon, blue "ÅBEN RUTE" with list icon, amber "VEJNING" with scale icon. Smaller secondary buttons below. Bottom sticky footer showing weight "Affald: 0 kg". Clean, modern, mobile-first. 390x844px.

---

### 3.3 RUTE-OVERSIGT (Hovedskærmen)

**Nu:** Lille info-boks med adresse + 6 handlingsknapper (Besked, Afvis, Fejl, Kvittering, Delvis afslut, Afslut) + navigationsknapper + kort under.

**Nyt design — Split view:**

#### Vertikal (portræt):
- **Header:** Rutenavn + stop-nummer "Stop 12/47"
- **Aktiv stop-kort:** Stort kort med:
  - Kunde-navn (stor, fed)
  - Adresse (medium)
  - Afstand + køretid badge: "3,2 km · 8 min" (blå)
  - Ordrelinjer: "1× 240L Organisk" med kg-felt
  - **Stor grøn AFSLUT-knap** (fuld bredde, 60px høj)
  - Sekundære: Fejl | Besked | Spring over (mindre, under)
- **Swipe-zone:** Swipe op → kort. Swipe ned → næste stop.
- **Mini-kort** i bunden (1/3 af skærmen) med pin for aktiv stop
- **Sortering-badge:** Amber-farvet "⚡ Sortering" knap synlig i øverste højre hjørne — ALTID tilgængelig

#### Horisontal (landskab):
- **Venstre 40%:** Stop-liste (scrollbar) med aktiv stop highlighted
- **Højre 60%:** Google Maps kort med alle pins
- **Bund-bar:** Vægt + Afslut-knap + sortering

**Prompt til billede (portræt):**
> Dark mobile route screen, portrait orientation. Navy background. Header bar: "Rute 256" left, "Stop 12/47" right, orange. Large white card (#161b22 bg): bold "Andersen Boligforening" name, "Rydevænget 42, 8210 Aarhus V" address below. Blue badge "3.2 km · 8 min". Order line "1× 240L Organisk" with weight input field. Very large green (#34A853) rounded button "AFSLUT" full width, 60px height. Below: three small gray buttons "Fejl" "Besked" "Spring over". Small map preview at bottom showing one blue pin. Amber badge "Sortering" top right corner. Modern, clean, high contrast. 390x844px.

**Prompt til billede (landskab):**
> Dark mobile route screen, landscape orientation. Navy background. Left panel (40% width): scrollable stop list with items showing number, street name, and status dots (green=done, blue=current, gray=pending). Right panel (60%): Google Maps dark mode with numbered pin markers. Blue pin highlighted for current stop. Bottom bar spanning full width: weight display "4.230 kg", green "AFSLUT" button, amber "Sortering" button. 844x390px.

---

### 3.4 SORTERINGSVISNING

**Nu:** Gemt bag "Sortering"-knap. Åbner en modal.

**Nyt design:**
- Slide-in panel fra højre (animeret)
- **Drag-and-drop liste** med alle stops
- Hver stop viser: nummer + adresse + afstand
- Grøn checkmark for sorterede, grå for usorterede
- **"Anvend profil"** dropdown i toppen (mandag-profil, tirsdag-profil, etc.)
- **"Gem som profil"** knap i bunden
- Store touch-targets for at flytte stops op/ned

**Prompt til billede:**
> Dark mobile panel sliding from right. Navy background (#0d1117). Header "Sortering" with close X button. Dropdown at top "Vælg profil: Tirsdag standard". Below: reorderable list of stops. Each item has drag handle (three horizontal lines), number badge, street name, and distance. Item 1: "1. Rydevænget 42 — 0.3 km" with green checkmark. Item 5: "5. Skanderborgvej 100 — 2.1 km" with gray circle. Touch-friendly items, 56px height each. Bottom button: green "Gem som profil". Modern, clean. 390x844px.

---

### 3.5 TIDSREGISTRERING

**Nu:** Collapsed sektioner for forvogn/påhæng + mange små knapper. Uoverskuelig.

**Nyt design:**
- **Tidslinje** (vertikal) der viser dagens registreringer visuelt
  - Grøn blok = arbejde
  - Gul blok = pause
  - Grå blok = andet
- **Aktuel status** stort vist: "I gang siden 06:15 — 4t 32m"
- **Store action-knapper:** PAUSE | ANDET | SLUT (i en række)
- Vognregistrering i **kompakt** kort øverst (ikke collapsed sektion)

**Prompt til billede:**
> Dark mobile time registration screen. Navy background. Top card: "Forvogn: 8721" and "Påhæng: 3019" in compact row with gray badges. Below: vertical timeline showing colored blocks: green block "06:15-10:47 Arbejde" (4h32m), yellow block "10:47-11:15 Pause" (28m), green block "11:15-now Arbejde". Current status highlighted: "I gang siden 11:15 — 2t 14m" in large white text. Three large buttons at bottom: blue "PAUSE", amber "ANDET", red "SLUT". Clean, modern. 390x844px.

---

### 3.6 VÆGT-TRACKER

**Nu:** Gemt i header som "↩ 0 ↪ 🚛". Næsten usynlig.

**Nyt design:**
- **Altid-synlig footer** på rute-skærmen (sticky bottom)
- Stor talangivelse: **"4.230 kg"** i hvid bold
- Bagvedliggende grå bar med fill-level (visuelt som batteri)
- Tryk → åbn vægt-popup med:
  - Tastatur til hurtig indtastning
  - Seneste dumps (historik)
  - Kalibreringsfaktor
  - "DUMP" knap (rød, med bekræftelse)

**Prompt til billede:**
> Dark mobile weight tracker footer bar. Navy background (#161b22). Large bold white text "4.230 kg" centered. Thin green progress bar underneath showing fill level (60%). Left: undo arrow button. Right: dump truck icon button. When expanded (popup): dark modal with large number display, numeric keypad for quick entry, list of recent dumps "10:30 — 1.240 kg dumped at Lisbjerg", red "DUMP" button. Clean, modern. 390x200px for footer, 390x500px for popup.

---

### 3.7 KORT-KONTROLLER

**Nu:** Små tekst-knapper "Vis alle | Centrér | Følg | Mørk | +Pin" under kortet.

**Nyt design:**
- **Floating action buttons** (FAB) ovenpå kortet:
  - 📍 Centrér (blå cirkel, nederst højre)
  - 🗺 Vis alle (over centrér)
  - 👁 Følg mig (toggle, grøn når aktiv)
- Mørk mode er default (ingen knap nødvendig)
- Waypoint-knapper som chips langs bunden af kortet

**Prompt til billede:**
> Dark Google Maps view with numbered blue pin markers (1-47). Current stop pin is larger, amber colored. Blue dot shows user location. Floating action buttons on right side: blue circle "center" button at bottom right, "show all" button above it, green "follow me" toggle above that. Route line connecting pins in order (dotted blue line). Waypoint chips at bottom of map: "Tank" "Depot" "Hjem" as small rounded pills. Clean, modern. 390x400px.

---

## 4. NYE FUNKTIONER (med begrundelse)

### 4.1 Sorteringsprofiler (KERNEFUNKTION)
**Hvad:** Gem og genindlæs rækkefølgen af stops per ugedag.
**Hvorfor:** TransportIntra nulstiller sorteringen ugentligt. Kris' #1 problem. Sparer 15-20 min mandag morgen.
**Hvordan:** Amber-farvet knap, altid synlig. Dropdown med profiler. One-tap apply.

### 4.2 Dashboard med dagsstatus
**Hvad:** Overblik over dagen: stops, progress, ETA, vægt.
**Hvorfor:** Nu hopper man direkte ind i ruten uden kontekst. Et dashboard giver overblik og ro.
**Hvordan:** Stort status-kort med progressbar og nøgletal.

### 4.3 Visuel tidslinje for tidsregistrering
**Hvad:** Farvede blokke der viser arbejde/pause/andet på en tidslinje.
**Hvorfor:** Nu er det bare tekst-lister med timestamps. En tidslinje giver overblik med ét blik.
**Hvordan:** Vertikal tidslinje med farvekodede segmenter.

### 4.4 Quick-weight input
**Hvad:** Stort, altid synligt vægt-display med one-tap dump.
**Hvorfor:** Vægten er central for Kris' job men er gemt i en 20px header. Skal fylde mere.
**Hvordan:** Sticky footer + popup med numpad.

### 4.5 Swipe-navigation mellem stops
**Hvad:** Swipe venstre/højre for at bladre mellem stops.
**Hvorfor:** Nu kræver det klik på "næste" — swipe er hurtigere i bilen.
**Hvordan:** Touch gesture handler med animation.

---

## 5. NAVIGATION FLOW

```
Login → Dashboard → Rute-oversigt ↔ Fuld liste
                  → Tidsregistrering
                  → Sortering (panel)
                  → Opsætning (sjælden)
```

**Hovedregel:** Max 2 tryk fra login til aktiv rute.

---

## 6. SAMLET NANO BANANA PRO PROMPT (Komplet)

Brug denne prompt til at generere det fulde design:

```
Design a complete mobile app UI for a waste management route driver app called "Ydrasil".
Dark theme, navy background (#0d1117), with green (#34A853), amber (#F5A623), blue (#4FC3F7), and red (#E54D42) accent colors. White text on dark backgrounds.

Show 4 screens side by side:

Screen 1 - LOGIN: Centered Y-tree logo, "Ydrasil" title, "Rute 256" subtitle, two dark input fields (username, password), large green "LOG IND" button.

Screen 2 - DASHBOARD: Top bar with date "Tirsdag 17. feb". Status card showing "Rute 256 — 12/47 stops" with green progress bar at 25%. Three action buttons: green "START VAGT", blue "ÅBEN RUTE", amber "VEJNING". Sticky weight footer "4.230 kg".

Screen 3 - ROUTE VIEW (portrait): Header "Stop 12/47". Active stop card: "Andersen Boligforening", "Rydevænget 42, 8210 Aarhus V", blue "3.2 km · 8 min" badge, order line "1× 240L Organisk". Very large green "AFSLUT" button. Small map preview below. Amber "Sortering" badge top-right.

Screen 4 - SORTING PANEL: Slide-in from right. Profile dropdown at top. Reorderable list with drag handles: numbered stops with addresses and distances. Green checkmarks for sorted, gray circles for unsorted. Green "Gem profil" button at bottom.

Style: Modern, clean, high contrast, mobile-first (390x844px per screen). Sans-serif font (Inter). Rounded corners on all cards and buttons. Subtle shadows. No gradients on buttons - flat with slight depth. Touch-friendly targets (min 48px).
```

---

## 7. ITERATION

Kris kigger på de genererede billeder og giver feedback:
- "Den knap er for lille"
- "Flyt det her op"
- "Farven er forkert"
- "Tilføj X"

Vi opdaterer prompten og genererer igen. Gentag til det er rigtigt.

Når designet er godkendt → implementer i kode.
