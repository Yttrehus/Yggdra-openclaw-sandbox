# Diesel — Subproject

## Status: THIN/IDÉ

Kun 2 svage datapunkter. Bør IKKE have eget subproject endnu.

## Hvad
Tracking af dieselforbrug og tankning per tur/rute.

## Evidens

### Eneste kilder
1. **PROFIL.md (l.291):** Visionsafsnit "6-12 mdr": "Prædiktiv logistik: Tidsestimat, tankningsforslag, fyldningsgrad." — Fremtidsvision, ikke aktivt krav.
2. **PROFIL.md (l.21):** Voice memo nævner "diesel-forbrug" som eksempel på Kris' stream-of-consciousness tankeproces. Ikke feature-krav.

### Hvad der IKKE eksisterer
- Ingen kode
- Ingen API-endpoints for diesel i TI API
- Ingen session-diskussioner om diesel-tracking
- Ingen design-mockups
- Ingen datapunkter fra TI API (getAppCache/getRute indeholder ikke diesel-felter)

## Afhængigheder
- GPS tracker (navigation subproject) som fundament
- Kræver nyt UI-modul + evt. ny API-endpoint

## Hvorfor THIN
Stubben opfinder mål (forbrug-per-km, historik) der ikke har kilde i nogen session.
"Tankningsforslag" i PROFIL er del af en langsigtet vision, ikke et aktivt projekt.
Genaktivér først når reelle datapunkter dukker op.
