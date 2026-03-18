# PDF Official Toolkit Skill

**Dato:** 2026-03-10
**Klar til:** Backlog (mangler: faktura-layout fra rejseselskab, weasyprint test, Tesseract installation)

## Opsummering
- Claude Code skill til PDF-generering (fakturaer, rejseplaner), tekst-udtræk, merge/split, OCR
- Poppler allerede installeret. Mangler: weasyprint (Python), Tesseract (WSL)
- MVP: faktura-generering fra JSON → HTML → PDF. Phase 2: OCR

## Origin Story
Opstod fra idé-parkering: "PDF Official Toolkit skill (professionel PDF-generering: fakturaer, rapporter, OCR — til bogføring/rejseselskab)." To konkrete use cases: (1) rejseselskabet skal lave fakturaer/tilbud som PDF, (2) bogføring modtager kvitteringer som scan der skal OCR'es.

## Rå input
**Parallel-tasks outputs:**
- ~/parallel-tasks/output-03-pdf-skill-spec.md (253 linjer) — specifikation med capabilities, værktøj-kravmatrix, arkitektur
- ~/parallel-tasks/output-03-pdf-SKILL.md (689 linjer) — komplet SKILL.md udkast med commands, templates, eksempler

**Fra PLAN.md idé-parkering:**
> PDF Official Toolkit skill (professionel PDF-generering: fakturaer, rapporter, OCR — til bogføring/rejseselskab)

## Cowork Output (2026-03-10)

### Spec (output-03-pdf-skill-spec.md)

**MVP (Phase 1):**
- Faktura-generering: JSON → HTML → PDF via weasyprint (Python)
- Tekst-udtræk: pdftotext (Poppler, allerede installeret)
- Merge/split: pdfunite/pdfseparate (Poppler)

**Phase 2 (deferred):**
- OCR via Tesseract + pytesseract + Pillow (WSL)

**Arkitektur:** Windows PATH for Poppler + Python venv for weasyprint. OCR fremtidigt via WSL.

**Krav:** weasyprint (pip install), Poppler (antaget installeret), Tesseract (deferred).

### SKILL.md udkast (output-03-pdf-SKILL.md)

Komplet SKILL.md med 5 commands:
- `pdf:generate-invoice` — JSON → PDF faktura (travel template med HTML/CSS)
- `pdf:extract-text` — PDF → plaintext (born-digital kun)
- `pdf:merge` — sammenlæg multiple PDF'er
- `pdf:split` — opdel PDF i enkeltsider
- `pdf:ocr` — OCR på scans (Phase 2, kræver Tesseract)

Inkluderer: installationsguide (Windows + WSL), HTML faktura-template med professionelt layout, workflow-eksempler, troubleshooting, og fremtidige faser (signaturer, form-udfyldning, Notion-integration).

### Action items
- [ ] Test weasyprint installation på Windows
- [ ] Verificér Poppler i PATH (pdftotext, pdfunite, pdfseparate)
- [ ] Afgør faktura-layout med rejseselskabet (logo, betalingsbetingelser, moms, bankoplysninger)
- [ ] Opret Python venv for pdf-skill
- [ ] Phase 2: Installér Tesseract i WSL
