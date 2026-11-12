# Training Station Fitness – βελτιωμένο site (SEO + AI)

Στατική προεπισκόπηση του trainingstationfitness.com με όλες τις διορθώσεις από τον έλεγχο SEO/AI.
Το περιεχόμενο, οι φωτογραφίες, τα χρώματα και η γραμματοσειρά είναι του υπάρχοντος site.

```bash
python3 build.py               # προεπισκόπηση (κίτρινα σημεία = στοιχεία που λείπουν)
python3 build.py --final       # χωρίς τις σημάνσεις
cd site && python3 -m http.server 8080
```

Τιμές, ωράριο, ΤΚ, link Google Business και Facebook Pixel συμπληρώνονται στην αρχή του `build.py` (`BUSINESS`, `PRICES`).

## Τι άλλαξε

| Θέμα | Πριν | Τώρα |
|---|---|---|
| Schema | Μόνο `Organization` | `ExerciseGym` με διεύθυνση, geo, τηλέφωνα, περιοχές, `Person` (Μάνος, Μελίνα), `Service` ανά υπηρεσία, `FAQPage`, `BreadcrumbList`, `OfferCatalog` |
| H1 | 2 στην αρχική, 0 στις υπηρεσίες | Ακριβώς 1 σε κάθε σελίδα, με «Περιστέρι» |
| Τίτλοι | «Recovery Injuries - Training Station Fitness» | Απλοί και φυσικοί: «Pilates Reformer \| Training Station Fitness». Χωρίς λέξεις-κλειδιά που μοιάζουν με διαφήμιση |
| Τοπικό SEO | Πουθενά | Στα δομημένα δεδομένα (διεύθυνση, συντεταγμένες, περιοχές), στις περιγραφές για τη Google, στο llms.txt και στη διεύθυνση της σελίδας – όχι στους τίτλους |
| Κεφαλαία | Τόνοι σε κεφαλαία σε κάποιους browsers | Χωρίς τόνους στα κεφαλαία (με διαλυτικά όπου χρειάζεται) |
| Τιμές | Δεν υπήρχαν | Νέα σελίδα `/pricing/` |
| FAQ | Δεν υπήρχαν | Σε κάθε υπηρεσία + `/faq/` |
| E-E-A-T | Βιογραφικό μόνο στο About | Προσόντα παντού, `Person` schema, ενότητα Forces με αναφορά στη ΣΑΕΑ |
| Εικόνες | PNG έως ~770KB | WebP ~20–60KB, περιγραφικά ονόματα και alt, lazy loading |
| Cookies | «Αν συνεχίσετε…», Pixel πριν τη συγκατάθεση | Αποδοχή / Μόνο απαραίτητα, Consent Mode v2, Pixel μόνο μετά από αποδοχή |
| Χάρτης | iframe Google σε κάθε σελίδα | Φορτώνει με κλικ (ταχύτητα + GDPR) |
| Gift cards | Άδεια σελίδα | Περιεχόμενο + description |
| Τηλέφωνα | `tel:%C2%A0+30.69…` | `tel:+30…` |
| Login form στο footer | Σε κάθε σελίδα | Αφαιρέθηκε |
| llms.txt | 404 | Υπάρχει |
| robots.txt | Γενικό | Ρητή άδεια για AI crawlers |

## Πώς περνάει στο WordPress

Το site σήμερα είναι WordPress (Astra + Elementor + AIOSEO + Booknetic). Δύο δρόμοι:

**Α. Μένεις στο WordPress (προτείνεται)** – αντιγράφεις τις αλλαγές:
1. AIOSEO → Search Appearance → Local Business: τύπος *ExerciseGym*, στοιχεία όπως στο `BUSINESS`. Αλλιώς επικόλλησε το JSON-LD από τον κώδικα της `site/index.html`.
2. AIOSEO → κάθε σελίδα: τίτλος «Όνομα σελίδας | Training Station Fitness» και description από το `build.py` (`desc`).
3. Elementor: ο πρώτος τίτλος κάθε σελίδας → H1· το «Είπαν για εμάς» → H2.
4. Νέες σελίδες «Τιμές» και «Συχνές ερωτήσεις» (κείμενο από το preview). FAQ με το AIOSEO FAQ block για αυτόματο schema.
5. SiteGround Optimizer: WebP, lazy load· το Facebook Pixel να μπαίνει μόνο client-side ώστε η cache να γίνει `HIT`.
6. Complianz ή CookieYes με Google Consent Mode v2· αφαίρεση του υπάρχοντος banner.
7. Ανέβασε το `site/llms.txt` στη ρίζα (File Manager του SiteGround).
8. Search Console + Bing Webmaster Tools: υποβολή sitemap.

**Β. Στατικό site** – τα αρχεία του `site/` ανεβαίνουν όπως είναι. Χρειάζεται εξωτερικό σύστημα κρατήσεων στη θέση του Booknetic και υπηρεσία για τη φόρμα επικοινωνίας.

## Πριν ανέβει
- Σημεία σημειωμένα κίτρινα: ΤΚ, ωράριο, τιμές, link Google Business, διάρκεια gift card, οδηγίες πρόσβασης.
- Οι απαντήσεις των FAQ γράφτηκαν με βάση τα κείμενα του site – διάβασέ τες και διόρθωσε ό,τι δεν ισχύει.
- Το πλήρες κείμενο όρων/απορρήτου μπαίνει αυτούσιο από το υπάρχον site.
