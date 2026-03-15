# TransportIntra API Reference

**Kilde:** HAR-captures fra Chrome DevTools (2025-12-13/14) + response dumps
**Endpoint:** `POST https://webapp.transportintra.dk/srvr/index4.0.php`
**Content-Type:** `multipart/form-data`
**Server:** nginx, PHP 8.2.29, PleskLin

---

## Autentificering

Alle kald (undtagen `login`) kræver en `key` parameter — en base64-encodet session-nøgle.

**Key-format:** `M3wzMDI0fGpzfDE3MmY5MmQ1OTdiM2Q1ODFhZjA0MTU1ZTFmYTdjZWEy`
- Returneret af `login` action
- Base64-dekodet: `3|3024|js|172f92d597b3d581af04155e1fa7cea2`
- Format: `{user_id}|{year?}|{sys}|{hash}`

**VIGTIGT:** Alle string-values i POST-body er wrappet i JSON-quotes (f.eks. `"login"` sendes som `"\"login\""` i multipart form).

---

## 1. login

Autentificerer brugeren og returnerer session-nøgle + app-cache data.

### Request
| Param | Type | Eksempel |
|-------|------|----------|
| action | string | `"login"` |
| username | string | `"Kristoffer8093"` |
| password | string | `"kristoffer8093"` |
| version | string | `"4.0.070"` |

### Response (~98 KB)
```json
{
  "key": "NXwzMDI0fGpzfDFlMDMwZWM3MDdlNDVmYzUwNGVjOGYwNDRhMDg0NjE0",
  "navn": "Kristoffer Yttrehus",
  "sys": "js",
  "menuFlags": 0,
  "errors": [
    {
      "id": 1,
      "list_id": 1,
      "type": 1,           // 1=rest, 2=have
      "txt": "Affaldet var forkert sorteret",
      "msg_spec": 0,
      "img_spec": 0
    }
    // ... 127 fejlkoder i alt
  ],
  "chatmbrs": [
    {
      "navn": "(Mike) Bjørn   [F]",
      "id": "2335",
      "type": "1"
    }
    // ... 1558 chatmedlemmer
  ],
  "globalMsg": ""
}
```

**Vigtige felter:**
- `key` — Session-nøgle til alle efterfølgende kald
- `errors` — Alle fejlkoder chaufføren kan vælge (127 stk), brugt til fejlregistrering
- `chatmbrs` — Alle brugere i TiChat systemet (1558 stk)

---

## 2. getAppCache

Identisk response som `login` — returnerer app-cache med fejlkoder og chatmedlemmer.

### Request
| Param | Type | Eksempel |
|-------|------|----------|
| action | string | `"getAppCache"` |
| key | string | session key |

### Response
Samme som login response (~98 KB).

---

## 3. getTimeReg

Henter tidsregistreringer og lister for en given dato.

### Request
| Param | Type | Eksempel |
|-------|------|----------|
| action | string | `"getTimeReg"` |
| getLists | boolean | `true` |
| date | string | `"2025-12-14"` (ISO format) |
| key | string | session key |
| version | string | `"4.0.070"` |

### Response (~40 KB)
Indeholder lister over tidsregistreringer. Kaldt fra `Tidsreg.setState()` i `Tidsreg.js:133`.

---

## 4. getDisps4day

Henter alle dispositioner (ruter) for en given dato. Dette er "køreliste"-oversigten.

### Request
| Param | Type | Eksempel |
|-------|------|----------|
| action | string | `"getDisps4day"` |
| date | string | `"2025-12-15"` (ISO format) |
| key | string | session key |

### Response (~921 bytes)
Returnerer en liste af ruter for den dato. Kaldt fra `Lists.verifyAndBuild()` i `Lists.js:79`.

**Response-format (fra analyseret data):**
```json
[
  {
    "id": 217760,
    "rute_id": -231,
    "headline": "256 ORG2ÅRH MANDAG",
    "status": 5,
    "totl": 70,
    "fins": 0
  }
]
```

**Negative rute_id:** Negativt fortegn indikerer en "hoved"-rute (parent). Positivt = subrute.

**Rute-ID mapping (Rute 256 — Organisk, Aarhus):**
| Dag | rute_id |
|-----|---------|
| Mandag | 231 |
| Tirsdag | 232 |
| Onsdag | 228 |
| Torsdag | 233 |
| Fredag | 234 |

---

## 5. getRute

**DEN VIGTIGSTE ACTION.** Henter alle stop (dispositioner) for en specifik rute.

### Request
| Param | Type | Eksempel |
|-------|------|----------|
| action | string | `"getRute"` |
| rute_id | integer | `231` (Mandag, Rute 256) |
| timestamp | unix timestamp | `1765753200` (midnight for datoen) |
| key | string | session key |

### Response (~80 KB)
```json
{
  "rute": {
    "id": 216948,
    "rute_id": -231,
    "tids_type": 0,
    "plan_strt": 1765148400,     // planlagt start (unix)
    "plan_slut": 1765234799,     // planlagt slut (unix)
    "aktl_strt": 0,              // faktisk start
    "aktl_slut": 0,              // faktisk slut
    "status": 6,
    "err_list": 3,
    "headline": "256 ORG2ÅRH MANDAG",
    "details": "Kristoffer Yttrehus",
    "remarks": "",
    "impremrks": "",
    "updated": 0,
    "items": [],
    "freight": [],
    "comments": [],
    "atchmnts": [],
    "adresser": [],
    "disp_ids": "5797932,5797933,...",   // kommasepareret liste
    "totl": 70,                           // total antal stop
    "fins": 70                            // antal færdige
  },
  "disps": [
    // Array af 70 dispositioner (stop)
  ]
}
```

### Disp (stop) objekt — komplet struktur
```json
{
  "id": 5797933,                    // unikt disp ID
  "rute_id": 231,                   // rute (positivt = subrute)
  "tids_type": 2,                   // tidstype
  "plan_strt": 1765148400,          // planlagt start
  "plan_slut": 1765234740,          // planlagt slut
  "aktl_strt": 1765169596,          // faktisk start (unix)
  "aktl_slut": 1765169596,          // faktisk slut (unix)
  "status": 20,                     // se statuskoder nedenfor
  "err_list": 3,
  "headline": "240l t/org",         // kort beskrivelse
  "details": "",
  "chf_rmrks": "",                  // chauffør-bemærkninger
  "impremrks": "",                  // vigtige bemærkninger
  "updated": 1765169596,
  "sorter": 0,                      // sorteringsnummer (0 = usorteret)
  "lines": [                        // ordrelinjer
    {
      "id": 30678979,
      "amount": 1,
      "units": "Stk",
      "text": "Tømning af 240 l. t/organisk",
      "editable": true,
      "matnr": "",
      "matnr_req": false,
      "sum_type": 0,
      "sum_ref": 0,
      "sum_lines": []
    },
    {
      "id": 30678980,
      "amount": 25,
      "units": "Kg.",
      "text": "Behandlingsafg. emb. organisk",
      "editable": true,
      "matnr": "",
      "matnr_req": false,
      "sum_type": 0,
      "sum_ref": 0,
      "sum_lines": []
    }
  ],
  "chauf": "",
  "comments": [],
  "adresser": {                     // kunde + arbejdsadresse
    "kunde": {
      "navn": "JPS Germa A/S",
      "adresse": "Thyrasgade 4",
      "postnr": "8260",
      "bynavn": "Viby J",
      "kontakt": "Vides ikke (RENOV)",
      "tlf": "...",
      "mbl": "",
      "email": "",
      "kvit": "",
      "remarks": ""
    },
    "work": {
      "navn": "JPS Germa A/S",
      "adresse": "Thyrasgade 4",
      "postnr": "8260",
      "bynavn": "Viby",
      "kontakt": "Vides ikke (RENOV)",
      "tlf": "",
      "mbl": "",
      "email": "",
      "kvit": "",
      "lat": "56.138710021972656",  // GPS breddegrad
      "lng": "10.177816390991211"   // GPS længdegrad
    }
  },
  "freight": []
}
```

### Statuskoder
| Status | Betydning |
|--------|-----------|
| 4 | Aktiv/påbegyndt |
| 5 | Afventer |
| 6 | Afsluttet (rute-niveau) |
| 20 | Udført (disp-niveau) |

### Sorteringsnummer (`sorter`)
- `0` = usorteret (default — de fleste stop)
- Positivt heltal = manuel sorteringsrækkefølge
- **Problem:** Nulstilles hver uge. Nye stop får altid `sorter: 0`

---

## 6. updateRDisp

Opdaterer en disposition (markerer som udført, ændrer status, etc.).

### Request
| Param | Type | Eksempel |
|-------|------|----------|
| action | string | `"updateRDisp"` |
| rute_id | integer | `231` |
| timestamp | unix timestamp | `1765753200` |
| disp | JSON string | `{"id":5813610,"status":4,"sorter":1,"update":1765708069}` |
| vogn | JSON string | `{"forvogn_id":1044}` |
| key | string | session key |
| main | JSON string | `{"status":5,"id":217760,"rute_id":-231}` |

### disp objekt (JSON string)
```json
{
  "id": 5813610,       // disp_id
  "status": 4,         // ny status
  "sorter": 1,         // sorteringsnummer
  "update": 1765708069 // unix timestamp for opdatering
}
```

### main objekt (JSON string)
```json
{
  "status": 5,         // hoved-rute status
  "id": 217760,        // hoved-rute id
  "rute_id": -231      // negativt = hoved-rute
}
```

### vogn objekt (JSON string)
```json
{
  "forvogn_id": 1044   // bil/vogn ID
}
```

### Response (~80 KB)
Returnerer den fulde rute igen (samme som `getRute` response).

---

## 7. regGPSPos

Registrerer GPS-position.

### Request
| Param | Type | Eksempel |
|-------|------|----------|
| action | string | `"regGPSPos"` |
| reason | string | `"LOGIN"` eller `"TRACK"` |
| key | string | session key |
| ts | unix timestamp | `1765706645` |
| lat | float | `56.138710` (0 = ingen GPS) |
| long | float | `10.177816` |
| acc | float | accuracy i meter |
| head | float | heading i grader |
| speed | float | hastighed |

### Response (~54 bytes)
Lille acknowledgement response.

**reason typer:**
- `"LOGIN"` — Sendes ved login
- `"TRACK"` — Periodisk tracking (hvert ~30 sek via GPSTracker.js)

---

## 8. checkMail

Tjekker for nye chatbeskeder. Kører automatisk **hvert minut** via `setInterval` i `TiChat.js:81`.

### Request
| Param | Type | Eksempel |
|-------|------|----------|
| action | string | `"checkMail"` |
| key | string | session key |
| wid | JSON array | `[]` (watch IDs) |
| umid | JSON array | `[]` (unread message IDs) |

### Response (~20 bytes)
Lille response med eventuelle nye beskeder.

**Problem:** checkMail kører hvert minut men opdaterer IKKE rutedata. Nye stop på ruten opdages ikke af denne poller.

---

## App Flow (rækkefølge af kald)

```
1. login → key + errors + chatmbrs
2. getAppCache → same data (cache refresh)
3. getTimeReg → tidsregistreringer + lister
4. regGPSPos(reason="LOGIN") → GPS ved login
5. checkMail → starter 1-minut interval
6. [bruger navigerer til køreliste]
7. getDisps4day(date) → liste af ruter for dato
8. [bruger klikker på en rute]
9. getRute(rute_id, timestamp) → alle 70+ stop
10. [bruger udfører et stop]
11. updateRDisp(disp, main, vogn) → opdater status → fuld rute returneret
12. regGPSPos(reason="TRACK") → periodisk GPS
```

---

## JavaScript Kald-Funktion

Alle API-kald går via `json_post()` i `app.js:652`:

```javascript
function json_post(action, data, callback) {
    var formData = new FormData();
    formData.append("action", JSON.stringify(action));
    for (var key in data) {
        formData.append(key, typeof data[key] === 'string' ?
            JSON.stringify(data[key]) : data[key]);
    }
    $.ajax({
        url: "srvr/index4.0.php",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        dataType: "json",
        success: callback
    });
}
```

---

## Vigtige JS-filer

| Fil | Funktion |
|-----|----------|
| `app.js` | Hoved-app: login, navigation, json_post() |
| `DB.js` | Database initialisering, getAppCache |
| `Lists.js` | Køreliste-visning, getDisps4day |
| `Tidsreg.js` | Tidsregistrering |
| `TiChat.js` | Chat-system, checkMail interval |
| `GPSTracker.js` | GPS-tracking, regGPSPos |
| `jSignature` | Signatur-capture (underskrifter) |

---

## Key til vores app

### Match-nøgle for lokal sortering
For at matche stop fra API med vores sorteringsark:
```
match_key = normalize(kunde_navn + adresse + postnr + headline)
```

Eksempel:
- API: `navn="JPS Germa A/S"`, `adresse="Thyrasgade 4"`, `postnr="8260"`, `headline="240l t/org"`
- Sorteringsark: `Kunde="JPS Germa A/S"`, `Adresse="Thyrasgade 4"`, `Post nr.="8260"`
- match_key: `jps germa a/s|thyrasgade 4|8260`

### Timestamp-beregning
For `getRute` og `updateRDisp` timestamp:
```python
import datetime
# Midnight UTC for den dato
date = datetime.date(2025, 12, 15)
timestamp = int(datetime.datetime.combine(date, datetime.time()).timestamp())
# = 1765753200
```

### Sortering uden server-kald
Kris' plan: Gem sorteringsrækkefølge LOKALT (ikke via 400 updateRDisp kald).
1. Hent rute via `getRute` → får alle stop med `disp.id`
2. Match hvert stop mod lokal profil (CSV/JSON med sorteringsrækkefølge)
3. Vis i appen sorteret efter lokal profil
4. Server ser aldrig sorteringsændringerne

---

## Fejlkoder (udvalg)

| ID | Type | Tekst |
|----|------|-------|
| 1 | 1 (rest) | Affaldet var forkert sorteret |
| 5 | 1 (rest) | Beholderen er for tung |
| 7 | 1 (rest) | Beholderen var tom |
| 9 | 1 (rest) | Affaldet sidder fast |
| 13 | 1 (rest) | Beholderen var ikke at finde |
| 17 | 1 (rest) | Vi kan ikke komme til |
| 19 | 1 (rest) | Låst, ingen adgang til beholderen |
| 2 | 2 (have) | Haveaffaldet var forkert sorteret |
| 4 | 2 (have) | Haveaffald var emballeret |
| 16 | 2 (have) | Var ikke stillet frem til skel |

---

## Python Eksempel: Hent en rute

```python
import requests

URL = "https://webapp.transportintra.dk/srvr/index4.0.php"

def ti_post(action, **params):
    """Send POST til TransportIntra API."""
    data = {"action": f'"{action}"'}
    for k, v in params.items():
        if isinstance(v, str):
            data[k] = f'"{v}"'
        elif isinstance(v, (dict, list)):
            data[k] = json.dumps(v)
        else:
            data[k] = str(v)

    resp = requests.post(URL, data=data)
    return resp.json()

# Login
result = ti_post("login",
    username="Kristoffer8093",
    password="kristoffer8093",
    version="4.0.070")
key = result["key"]

# Hent mandagens rute
rute = ti_post("getRute",
    rute_id=231,
    timestamp=1765753200,
    key=key)

for disp in rute["disps"]:
    addr = disp["adresser"]["work"]
    print(f'{disp["sorter"]:4d} | {addr["navn"]:30s} | {addr["adresse"]} | {disp["headline"]}')
```
