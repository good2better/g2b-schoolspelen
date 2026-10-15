# Play Store pakket — G2B Schoolspelen (TWA)

De app is al een volledige PWA (manifest + service worker + icons). Voor de
Play Store gebruiken we een **TWA (Trusted Web Activity)**: een dunne
Android-shell die de live site fullscreen toont. Updates aan de website zijn
dan automatisch ook updates van de app — geen dubbele releases.

## Twee routes

### Route A — PWABuilder (makkelijkst, aanbevolen)
1. Ga naar https://www.pwabuilder.com
2. Vul in: `https://good2better.github.io/g2b-schoolspelen/`
3. Klik "Package for stores" → Android → download het `.aab`-bestand
4. Upload in Play Console. Klaar.

### Route B — GitHub Actions (reproduceerbaar)
Workflow `.github/workflows/android-twa.yml` bouwt de AAB in CI met
Bubblewrap. Eenmalig nodig:

1. Maak een upload-keystore (op je eigen computer, `keytool` zit bij Java):
   ```
   keytool -genkeypair -v -keystore android-keystore.jks -alias schoolspelen \
     -keyalg RSA -keysize 2048 -validity 10000
   ```
   BEWAAR dit bestand + wachtwoorden goed — elke toekomstige update moet met
   dezelfde keystore getekend zijn.
2. `base64 -w0 android-keystore.jks > keystore.b64`
3. GitHub → repo → Settings → Secrets and variables → Actions:
   - `ANDROID_KEYSTORE_BASE64` = inhoud van keystore.b64
   - `ANDROID_KEYSTORE_PASSWORD` en `ANDROID_KEY_PASSWORD`
4. Actions → "Android AAB (TWA via Bubblewrap)" → Run workflow → artifact `aab`.

## Daarna (beide routes)
1. https://play.google.com/console → account aanmaken (eenmalig $25 / ±€25).
2. Nieuwe app aanmaken → upload de `.aab` bij een release (internal testing
   kan meteen; productie vraagt review).
3. **Adresbalk weghalen (Digital Asset Links):** Play Console toont de SHA-256
   fingerprint van je upload-keystore. Zet die in
   `/.well-known/assetlinks.json` van `good2better.github.io` (dat is de
   gebruikers-site-repo `good2better/good2better.github.io`, NIET deze repo).
   Zonder dit bestand werkt de app prima, maar toont Android een kleine
   URL-balk bovenaan.

`twa-manifest.json` hier is de Bubblewrap-config (packageId
`com.good2better.schoolspelen`). De gegenereerde `android-app/` en de keystore
staan in `.gitignore` — commit de keystore NOOIT.
