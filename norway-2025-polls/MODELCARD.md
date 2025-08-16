# MODELCARD.md

## Modellnavn
`Norway2025Polls` – enkel vektings- og simuleringsmodell for nasjonal oppslutning og blokkflertall.

## Formål
- Aggregere meningsmålinger (nasjonalt nivå).
- Estimere dagens oppslutning for partier.
- Estimere flertallssannsynlighet for blokker/koalisjoner.

## Datasett
- Wikipedia-tabeller over nasjonale målinger.
- (Valgfritt) Pollofpolls/PolitPro som validering/kryssjekk.
- Historiske valgresultater for enkel setemodell (senere).

## Forutsetninger og begrensninger
- Ingen velgeroverganger eller distriktseffekter modelleres eksplisitt i første versjon.
- Forenklet setemodell (proporsjonal allokering med 4 % sperre) – forbedres senere.
- Hus-effekter brukes først når det finnes nok observasjoner per byrå.

## Etiske hensyn
Se `ETHICS.md`.

## Evalueringsplan
- Etter 8. september 2025: sammenligne predikert oppslutning og blokkutfall med faktisk resultat (MAE, RMSE, Brier).
