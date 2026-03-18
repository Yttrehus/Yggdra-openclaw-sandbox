# getRute API Response Schema

Dette dokument beskriver JSON-strukturen fra TransportIntra's `getRute` API endpoint.

---

## Overblik

```
{
  "rute": { ... },      // Route metadata
  "disps": [ ... ]      // Array af stops/dispatches
}
```

---

## RUTE (Rod-niveau)

| Felt | Type | Betydning |
|------|------|-----------|
| `id` | int | Unik instance-ID for denne kørselsdag |
| `rute_id` | int | Internt ID (negativt i response: -231) |
| `headline` | string | **Rutenavn**: "256 ORG2ÅRH MANDAG" |
| `details` | string | Chauffør(er) - kan være flere navne adskilt af newline |
| `status` | int | 4=ikke startet, 5=i gang, 6=færdig |
| `err_list` | int | 0=ok, 3=normal, 6=fejl |
| `plan_strt` | timestamp | Planlagt start (Unix) |
| `plan_slut` | timestamp | Planlagt slut (Unix) |
| `aktl_strt` | timestamp | Altid 0 på ruteniveau |
| `aktl_slut` | timestamp | Altid 0 på ruteniveau |
| `totl` | string | Total antal stops |
| `fins` | string | Antal færdige stops |
| `disp_ids` | string | Kommasepareret liste af dispatch-IDs |
| `remarks` | string | Bemærkninger (sjældent brugt) |
| `impremrks` | string | Vigtige bemærkninger (sjældent brugt) |
| `tids_type` | int | Altid 0 på ruteniveau |
| `updated` | timestamp | Altid 0 på ruteniveau |
| `items` | array | Altid tom |
| `freight` | array | Altid tom |
| `comments` | array | Altid tom |
| `atchmnts` | array | Altid tom (attachments) |
| `adresser` | array | Altid tom |

### Headline Format
```
[Rutenr] [Type][Område] [Dag]
Eksempel: "256 ORG2ÅRH MANDAG"
```

Type-koder:
- **ORG** = Organisk/Madaffald
- **BB** = Brændbart
- **PAP** = Pap
- **MDK** = Madaffald (variant)
- **BBF** = Brændbart Foder?

---

## DISPS (Stops/Dispatches)

Hvert element i `disps` array er et stop på ruten.

### Kernefelter

| Felt | Type | Betydning |
|------|------|-----------|
| `id` | int | Unik dispatch-ID |
| `rute_id` | int | Rutenummer (positivt: 231) |
| `sorter` | int | **Sorteringsposition** (0 = ikke manuelt sorteret) |
| `status` | int | Se status-koder nedenfor |
| `headline` | string | Opgavetype: "Tømning 660L t/madaffald" |
| `details` | string | Ekstra detaljer (ofte tom) |
| `chf_rmrks` | string | **Chauffør-instruktioner** (koder, tider, kontakter) |
| `impremrks` | string | Vigtige bemærkninger (sjældent brugt) |
| `chauf` | string | Altid tom |

### Tidsfelter

| Felt | Type | Betydning |
|------|------|-----------|
| `plan_strt` | timestamp | Planlagt start |
| `plan_slut` | timestamp | Planlagt slut |
| `aktl_strt` | timestamp | Faktisk start (når chauffør starter) |
| `aktl_slut` | timestamp | Faktisk slut (når chauffør markerer done) |
| `updated` | timestamp | Sidste ændring i systemet |
| `tids_type` | int | 0=sjælden, 2=normal |
| `err_list` | int | 0=ok, 3=normal, 6=fejl/annulleret |

**Note:** `aktl_strt` og `aktl_slut` er ofte identiske (66% af tilfælde) - chauffør trykker bare "done".

### Status-koder (dispatch)

| Status | Betydning | Andel |
|--------|-----------|-------|
| **50** | Fuldført normalt | 93.8% |
| **20** | Fuldført (variant) | 2.3% |
| **10** | Fuldført (inkl. service) | 2.2% |
| **8** | Fuldført (variant) | 0.4% |
| **6** | Fuldført (variant) | 1.0% |
| **7** | Fuldført (variant) | <0.1% |
| **4** | Ikke fuldført | <0.1% |
| **62** | Annulleret/slettet | 0.1% |
| **63** | Annulleret/slettet | 0.1% |

---

## ADRESSER

```json
"adresser": {
  "kunde": { ... },   // Fakturering/hovedkontor - IKKE for chauffør
  "work": { ... }     // ARBEJDSSTED - brug denne!
}
```

### kunde (bagvedliggende kunde)
Bruges til fakturering. Kan være hovedkontor eller administrativ adresse.

| Felt | Type | Betydning |
|------|------|-----------|
| `navn` | string | Firmanavn |
| `adresse` | string | Adresse |
| `postnr` | string | Postnummer |
| `bynavn` | string | By |
| `kontakt` | string | Kontaktperson |
| `tlf` | string | Telefon |
| `mbl` | string | Mobil |
| `email` | string | Email |
| `kvit` | string | Kvittering (ofte tom) |
| `remarks` | string | Bemærkninger |

### work (arbejdssted) - BRUG DENNE!
Den faktiske lokation hvor affaldet står og chaufføren skal hen.

| Felt | Type | Betydning |
|------|------|-----------|
| `navn` | string | Stednavn (ofte mere beskrivende) |
| `adresse` | string | Faktisk adresse |
| `postnr` | string | Postnummer |
| `bynavn` | string | By |
| `kontakt` | string | Kontaktperson |
| `tlf` | string | Telefon |
| `mbl` | string | Mobil |
| `email` | string | Email |
| `kvit` | string | Kvittering |
| `lat` | string | **GPS latitude** (100% dækning!) |
| `lng` | string | **GPS longitude** (100% dækning!) |

**Vigtigt:** 48% af stops har forskellig kunde/work adresse. Altid brug `work` for routing!

---

## CHF_RMRKS (Chauffør-bemærkninger)

Indeholder kritisk information for chaufføren:

| Indhold | Antal stops | Eksempel |
|---------|-------------|----------|
| Portkoder | ~1.750 | "kode 2610", "Portkode 3712" |
| Tidskrav | ~6.900 | "må ikke tømmes før kl. 7", "mellem 7-23" |
| Nøgleinfo | ~5.800 | "nøgleboks", "Nøgle nr 8", "brik" |
| Telefonnumre | ~5.400 | 8-cifrede numre |

Eksempler:
```
"Portkode 2830#"
"Absolut ingen tømning før 07:00!"
"MasterLock nøgleboks kode 7153"
"Ved problemer kontakt: Victoria: 24224516"
```

---

## COMMENTS (Fejlrapporter)

Array af kommentarer, typisk fejlrapporter med GPS.

```json
{
  "orig_id": 1455746,
  "disp_id": 4406575,
  "status": 0,
  "err_code": 38,
  "mod": 1730949398,
  "txt": "Information til kontoret...",
  "imgType": "",
  "cmtType": 0,
  "lat": 56.1433201,
  "long": 10.1504833
}
```

### err_code værdier

| Kode | Betydning | Antal |
|------|-----------|-------|
| **38** | Standard afslutning | 3.160 |
| **39** | Info til kontoret | 433 |
| **42** | Ukendt | 428 |
| **110** | Adgangsvej spærret | 388 |
| **0** | Generel (fx "Ingen brik") | 307 |
| **112** | Ingen åbner adgangen | 242 |
| **58** | Forgæves kørsel / tom spand | 211 |
| **118** | Ferielukket | 137 |
| **37** | Ekstra affald/håndlæsning | 47 |
| **60** | Adgangsveje spærret (variant) | 46 |
| **40** | Bilspærret | 16 |
| **114** | Fejlsorteret affald | 12 |
| **122** | Dobbelt ordre | 11 |
| **116** | Kunden ønsker ingen tømning | 8 |
| **120** | Sne og isglat | 2 |

---

## LINES (Faktureringslinjer)

Array af linjer til fakturering.

```json
{
  "id": 17976968,
  "amount": 2,
  "units": "Stk",
  "text": "Tømning af 770 l. t/affald",
  "editable": true,
  "matnr": "",
  "matnr_req": false,
  "sum_type": 0,
  "sum_ref": 0,
  "sum_lines": []
}
```

### Enheder (units)

| Unit | Betydning | Antal |
|------|-----------|-------|
| **Kg.** | Vægt (afgifter) | 39.811 |
| **Stk** | Antal tømninger | 37.721 |
| **stk.** | Antal (variant) | 8.155 |
| **Tim.** | Timer | 8 |
| **Ton** | Tons | 6 |

### Mest almindelige services

| Antal | Tekst |
|-------|-------|
| 19.548 | Behandlingsafg. emb.org. |
| 15.075 | Behandlingsafg. emb. organisk |
| 6.232 | Tømning af 240 l. t/organisk |
| 5.534 | Tømn. 770 l. emb. org. |
| 5.372 | Tømn. 660 L, Emb. organisk |

---

## CONTAINER STØRRELSER

Fra headline-analyse:

| Størrelse | Antal |
|-----------|-------|
| 240L | 8.007 |
| 660L | ~18.674 (varierende skrivemåder) |
| 770L | ~7.677 |
| 1100L | ~1.347 |
| 120L | 327 |
| 8 m³ | 310 (frontlæsser) |

---

## ROUTE ID MAPPING

Route 256 (Kris's rute) har forskellige `rute_id` per dag:

| rute_id | Headline |
|---------|----------|
| 228 | 256 ORG2ÅRH ONSDAG |
| 231 | 256 ORG2ÅRH MANDAG |
| 232 | 256 ORG2ÅRH TIRSDAG |
| 233 | 256 ORG2ÅRH TORSDAG |
| 234 | 256 ORG2ÅRH FREDAG |

---

## VIGTIGE INDSIGTER

1. **Brug altid `adresser.work`** - ikke `kunde` - for chauffør-relevante data
2. **100% GPS dækning** på `work.lat/lng`
3. **`sorter=0`** betyder ikke manuelt sorteret
4. **`aktl_strt = aktl_slut`** i 66% af tilfælde
5. **Status 50** = normal fuldførelse (93.8%)
6. **`rute_id` er negativt** i API response, positivt i dispatch
7. **Headline indeholder rutenummer** - brug regex: `^(\d+)\s+(\w+)\s+(\w+)$`

---

## EKSEMPEL: Udtræk chauffør-relevant data

```python
for disp in data['disps']:
    work = disp['adresser']['work']
    print(f"""
    Stop: {work['navn']}
    Adresse: {work['adresse']}, {work['postnr']} {work['bynavn']}
    GPS: ({work['lat']}, {work['lng']})
    Opgave: {disp['headline']}
    Instruktioner: {disp['chf_rmrks']}
    Sortering: {disp['sorter']}
    """)
```

---

*Sidst opdateret: 2026-01-25*
*Baseret på analyse af 577 rutefiler, 40.053 dispatches*
