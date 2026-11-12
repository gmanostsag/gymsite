#!/usr/bin/env python3
"""Γεννήτρια του βελτιωμένου (SEO + AI-ready) site του Training Station Fitness.

Τρέξε:  python3 build.py            -> γράφει τα HTML στο site/
        python3 build.py --final    -> χωρίς κίτρινες σημάνσεις προεπισκόπησης

Όλα τα στοιχεία που πρέπει να συμπληρώσεις είναι στο BUSINESS παρακάτω
(τιμές, ωράριο, ΤΚ, Facebook Pixel). Όσα έχουν None εμφανίζονται κίτρινα στην προεπισκόπηση.
"""
import html, json, os, re, sys, datetime

PREVIEW = "--final" not in sys.argv
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
SITE = "https://trainingstationfitness.com"
TODAY = datetime.date.today().isoformat()

# ---------------------------------------------------------------- στοιχεία επιχείρησης
BUSINESS = {
    "name": "Training Station Fitness",
    "legal_name": "ΕΜΜΑΝΟΥΗΛ ΤΣΑΓΚΑΤΑΚΗΣ",
    "slogan": "Η γυμναστική σου μόλις απέκτησε ενδιαφέρον!",
    "street": "Παρασκευοπούλου 47",
    "area": "Πλατεία Μπουρναζίου",
    "city": "Περιστέρι",
    "region": "Αττική",
    "postal": None,            # TODO: π.χ. "121 3x" – συμπλήρωσε τον σωστό ΤΚ
    "lat": 38.012443, "lng": 23.703602,
    "phone": "+302105767892", "phone_disp": "210 576 7892",
    "mobile": "+306946194809", "mobile_disp": "694 619 4809",
    "email": "info@trainingstationfitness.com",
    "gemi": "165097403000",
    # TODO: βάλε το πραγματικό ωράριο. Μορφή: (ημέρες schema.org, άνοιγμα, κλείσιμο)
    "hours": None,  # π.χ. [(["Monday","Tuesday","Wednesday","Thursday","Friday"],"07:00","22:00"),(["Saturday"],"09:00","14:00")]
    "price_range": "€€",
    "maps_url": "https://www.google.com/maps/search/?api=1&query=Training+Station+Fitness+%CE%A0%CE%B1%CF%81%CE%B1%CF%83%CE%BA%CE%B5%CF%85%CE%BF%CF%80%CE%BF%CF%8D%CE%BB%CE%BF%CF%85+47+%CE%A0%CE%B5%CF%81%CE%B9%CF%83%CF%84%CE%AD%CF%81%CE%B9",
    "maps_embed": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3143.4862165251543!2d23.70360181493293!3d38.012442906223455!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMzjCsDAwJzQ0LjgiTiAyM8KwNDInMTMuMCJF!5e0!3m2!1sel!2sgr!4v1",
    "social": {
        "Instagram": "https://www.instagram.com/training.station.fitness/",
        "Facebook": "https://www.facebook.com/training.station.fitness",
        "TikTok": "https://www.tiktok.com/@training.station.fitness",
        "Spotify Podcast": "https://open.spotify.com/show/0M0zl30MrFKcnPyTPezvxK",
    },
    "google_business": None,   # TODO: link του Google Business Profile (π.χ. https://maps.app.goo.gl/...)
    "fb_pixel_id": None,       # TODO: ID του Facebook Pixel (φορτώνει ΜΟΝΟ μετά από συγκατάθεση)
}

# Τιμές: None = άγνωστη -> κίτρινο "συμπλήρωσε" στην προεπισκόπηση
PRICES = [
    # (υπηρεσία, πακέτο, τιμή, σημείωση)
    ("Ενημερωτική συνάντηση γνωριμίας", "1 συνάντηση", "Δωρεάν", "Συζητάμε στόχους και ανάγκες"),
    ("Personal Training (ατομικό)", "1 συνεδρία", None, ""),
    ("Personal Training (ατομικό)", "Πακέτο 8 συνεδριών", None, ""),
    ("Personal Training (ατομικό)", "Πακέτο 12 συνεδριών", None, ""),
    ("Group Training (2–3 άτομα)", "Ανά άτομο / μήνα", None, ""),
    ("Pilates Reformer", "1 συνεδρία", None, ""),
    ("Pilates Reformer", "Πακέτο 8 συνεδριών", None, ""),
    ("Recovery Training", "1 συνεδρία", None, "Μετά από αρχική αξιολόγηση"),
    ("Security Forces – Army Training", "Μηνιαίο πρόγραμμα", None, ""),
    ("Digital Coaching", "Μηνιαίο πρόγραμμα", None, ""),
    ("Διατροφή (Διαιτολόγος)", "Πρώτη συνεδρία", None, "Και online"),
]

# ---------------------------------------------------------------- βοηθητικά
def esc(s): return html.escape(s, quote=True)
def md(s):
    s = esc(s)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
def todo(text, hint="συμπλήρωσε"):
    if PREVIEW: return f'<span class="todo" title="{esc(hint)}">{esc(text)}</span>'
    return esc(text)
def val(v, hint):
    return esc(v) if v else todo(hint)

def address_line():
    pc = BUSINESS["postal"]
    return f'{esc(BUSINESS["street"])}, {(esc(pc)+" ") if pc else (todo("ΤΚ","Ταχυδρομικός κώδικας")+" ")}{esc(BUSINESS["city"])} ({esc(BUSINESS["area"])})'

def hours_html():
    h = BUSINESS["hours"]
    if not h:
        return f'Κατόπιν ραντεβού · {todo("ωράριο λειτουργίας","Πρόσθεσε το ωράριο – το χρησιμοποιούν Google Maps και AI")}'
    gr = {"Monday":"Δευ","Tuesday":"Τρι","Wednesday":"Τετ","Thursday":"Πεμ","Friday":"Παρ","Saturday":"Σαβ","Sunday":"Κυρ"}
    return "<br>".join(f'{gr[d[0]]}{("–"+gr[d[-1]]) if len(d)>1 else ""}: {o}–{c}' for d,o,c in h) + "<br>Κατόπιν ραντεβού"

# ---------------------------------------------------------------- υπηρεσίες
SERVICES = [
 dict(slug="personal-training", name="Personal Training", icon="personal-training.svg",
  h1="Personal Training στο Περιστέρι",
  title="Personal Trainer στο Περιστέρι (Μπουρνάζι) | Training Station Fitness",
  desc="Ατομικό personal training στο Περιστέρι, πλ. Μπουρναζίου, με Καθηγητή Φυσικής Αγωγής: αξιολόγηση, εξατομικευμένο πρόγραμμα, διατροφικές συμβουλές. Κλείσε δωρεάν γνωριμία.",
  stype="Personal training",
  body=[("p","Το ατομικό **Personal Training** δεν είναι απλώς μια προπόνηση – είναι μια εξατομικευμένη εμπειρία που δημιουργείται αποκλειστικά για τις **ανάγκες**, τους **στόχους** και τις **δυνατότητές σου**, στον χώρο μας στην πλατεία Μπουρναζίου στο Περιστέρι."),
   ("h2","Γιατί να επιλέξεις Personal Training;"),
   ("ul",["**Εξατομίκευση**: Κάθε πρόγραμμα σχεδιάζεται αποκλειστικά για εσένα, λαμβάνοντας υπόψη το επίπεδο φυσικής κατάστασης, τυχόν τραυματισμούς και τους στόχους σου.",
          "**Αποτελεσματικότητα**: Με την καθοδήγηση ενός έμπειρου προπονητή, η προπόνησή σου γίνεται πιο αποδοτική, μεγιστοποιώντας τα αποτελέσματα στον ελάχιστο χρόνο.",
          "**Κίνητρο & Υποστήριξη**: Ο προσωπικός σου γυμναστής είναι δίπλα σου σε κάθε βήμα, παρέχοντας την απαραίτητη ενθάρρυνση για να ξεπεράσεις τα όριά σου.",
          "**Ασφάλεια**: Εκτελείς τις ασκήσεις σωστά και με ασφάλεια, αποφεύγοντας τραυματισμούς."]),
   ("h2","Τι περιλαμβάνει η υπηρεσία μας;"),
   ("ul",["Αρχική αξιολόγηση φυσικής κατάστασης και στοχοθέτηση.","Σχεδιασμός μοναδικού προγράμματος προπόνησης.","Διαρκής παρακολούθηση της προόδου σου.","Συμβουλές διατροφής και τρόπου ζωής για καλύτερα αποτελέσματα."]),
   ("p","Είτε θέλεις να **βελτιώσεις τη φυσική σου κατάσταση**, να **χτίσεις μυϊκή μάζα**, να **χάσεις βάρος**, ή απλά να αποκτήσεις περισσότερη ενέργεια και αυτοπεποίθηση, το Personal Training είναι η ιδανική επιλογή για σένα.")],
  faq=[("Ποιος κάνει την προπόνηση;","Οι προπονήσεις γίνονται από πτυχιούχους Καθηγητές Φυσικής Αγωγής (ΤΕΦΑΑ). Υπεύθυνος είναι ο Μάνος Τσαγκατάκης, που διδάσκει Σωματική Αγωγή στη Σχολή Αξιωματικών της Ελληνικής Αστυνομίας."),
       ("Είμαι εντελώς αρχάριος/α. Μπορώ να ξεκινήσω;","Ναι. Ξεκινάμε με αξιολόγηση φυσικής κατάστασης και το πρόγραμμα χτίζεται από το δικό σου επίπεδο, με έμφαση στη σωστή τεχνική και την ασφάλεια."),
       ("Πώς κλείνω ραντεβού;","Online από τη σελίδα «Κράτηση» ή τηλεφωνικά στο 210 576 7892. Μπορείς να ξεκινήσεις με μια δωρεάν ενημερωτική συνάντηση γνωριμίας."),
       ("Παρέχετε και διατροφική καθοδήγηση;","Ναι. Το personal training περιλαμβάνει συμβουλές διατροφής, ενώ για πλήρες διατροφικό πλάνο υπάρχει η υπηρεσία Διατροφής με πτυχιούχο Διαιτολόγο-Διατροφολόγο.")]),
 dict(slug="pilates", name="Pilates Reformer", icon="pilates-reformer.svg",
  h1="Pilates Reformer στο Περιστέρι",
  title="Pilates Reformer στο Περιστέρι (Μπουρνάζι) | Training Station",
  desc="Μαθήματα Pilates Reformer στο Περιστέρι, πλατεία Μπουρναζίου. Ενδυνάμωση κορμού, καλύτερη στάση σώματος, ανακούφιση από πόνους. Για αρχάριους και προχωρημένους.",
  stype="Pilates Reformer",
  body=[("p","Ανακάλυψε τη δύναμη και την ευλυγισία σου με τα μαθήματα **Pilates Reformer** στον χώρο μας στο Περιστέρι, την απόλυτη μέθοδο εκγύμνασης που προσφέρει εντυπωσιακά αποτελέσματα. Το κρεβάτι Reformer είναι ειδικά σχεδιασμένο για να υποστηρίζει κάθε κίνηση, μειώνοντας την καταπόνηση και επιτρέποντας την ασφαλή και σωστή ευθυγράμμιση του σώματος."),
   ("h2","Γιατί το Reformer είναι μοναδικό;"),
   ("ul",["Προσαρμόζεται απόλυτα στο επίπεδό σου, είτε είσαι αρχάριος είτε προχωρημένος.",
          "Προσφέρει **ενδυνάμωση ολόκληρου του σώματος**, με ιδιαίτερη έμφαση στον κορμό.",
          "Βοηθά στη **βελτίωση της στάσης του σώματος** και στην **ανακούφιση** από **μυοσκελετικούς πόνους**.",
          "Συνδυάζει **αντίσταση** και **ευλυγισία** με τη χρήση ελατηρίων, κάνοντας κάθε άσκηση αποτελεσματική και ευχάριστη."]),
   ("h2","Για ποιον είναι κατάλληλο;"),
   ("p","Για όποιον θέλει δυνατό κορμό, καλύτερη στάση σώματος και ευλυγισία: από αρχάριους και άτομα που κάθονται πολλές ώρες, μέχρι αθλητές που θέλουν συμπληρωματική προπόνηση. Αν έχεις πόνους στη μέση ή παλιό τραυματισμό, ενημέρωσέ μας στην αρχική αξιολόγηση ώστε να προσαρμόσουμε τις ασκήσεις.")],
  faq=[("Χρειάζομαι προηγούμενη εμπειρία στο Pilates;","Όχι. Το Reformer προσαρμόζεται στο επίπεδό σου και ο εκπαιδευτής σε καθοδηγεί από την πρώτη κίνηση."),
       ("Βοηθά το Pilates Reformer στον πόνο στη μέση;","Η ενδυνάμωση του κορμού και η βελτίωση της στάσης σώματος βοηθούν πολλούς ανθρώπους με μυοσκελετικούς πόνους. Για σοβαρό ή πρόσφατο τραυματισμό, συμβουλεύσου πρώτα τον γιατρό σου και δες και την υπηρεσία Recovery Training."),
       ("Τι να φορέσω;","Άνετα, εφαρμοστά ρούχα γυμναστικής και αντιολισθητικές κάλτσες."),
       ("Πόσο κοστίζει;","Δες τον τιμοκατάλογο στη σελίδα «Τιμές» ή ρώτησέ μας στο 210 576 7892.")]),
 dict(slug="group-training", name="Group Training (2–3 άτομα)", icon="group-training.svg",
  h1="Group Training για 2–3 άτομα στο Περιστέρι",
  title="Personal Training για 2–3 Άτομα στο Περιστέρι | Training Station",
  desc="Small group personal training για 2 ή 3 άτομα στο Περιστέρι. Προπονήσου με φίλους ή οικογένεια, με εξατομικευμένο πρόγραμμα και Καθηγητή Φυσικής Αγωγής.",
  stype="Small group personal training",
  body=[("p","Το **Group Training – Personal Training για 2 ή 3 άτομα** είναι η ιδανική επιλογή για όσους θέλουν να προπονούνται με φίλους ή μέλη της οικογένειάς τους, διατηρώντας παράλληλα την προσωπική καθοδήγηση και την εξατομίκευση ενός προγράμματος. Συνδυάζει τη δύναμη της ομαδικής ενέργειας με την ακρίβεια και την υποστήριξη ενός έμπειρου Καθηγητή Φυσικής Αγωγής."),
   ("h2","Γιατί να επιλέξεις Personal Training σε μικρή ομάδα;"),
   ("ul",["**Ομαδικό κίνητρο**: Η προπόνηση μαζί με φίλους ή αγαπημένα πρόσωπα ενισχύει τη δέσμευση και την ευχαρίστηση.",
          "**Εξατομίκευση**: Παρότι η προπόνηση γίνεται σε μικρή ομάδα, κάθε πρόγραμμα προσαρμόζεται στις ατομικές ανάγκες και στόχους του κάθε συμμετέχοντα.",
          "**Καλύτερη επικοινωνία**: Ο περιορισμένος αριθμός ατόμων επιτρέπει στον Καθηγητή Φυσικής Αγωγής να παρακολουθεί στενά την πρόοδο και την τεχνική του καθενός.",
          "**Αποδοτικότητα**: Μοιράζεσαι την εμπειρία με άλλους, χωρίς να θυσιάζεις την ποιότητα και την προσοχή που θα λάμβανες σε ατομικό επίπεδο.",
          "**Ευελιξία**: Ο σχεδιασμός λαμβάνει υπόψη τους κοινούς στόχους της ομάδας, όπως η απώλεια βάρους, η αύξηση δύναμης ή η γενική ευεξία."]),
   ("h2","Τι περιλαμβάνει;"),
   ("ul",["Αρχική αξιολόγηση για κάθε μέλος της ομάδας.","Πρόγραμμα που εξισορροπεί τις ανάγκες και τους στόχους όλων των συμμετεχόντων.","Συνεχής παρακολούθηση της προόδου και προσαρμογές στο πρόγραμμα, όπου χρειάζεται.","Ομαδικό πνεύμα, υποστήριξη και διασκέδαση!"])],
  faq=[("Πόσα άτομα είναι κάθε group;","Το πολύ 3 άτομα, ώστε ο Καθηγητής Φυσικής Αγωγής να προσέχει την τεχνική του καθενός."),
       ("Μπορούμε να έχουμε διαφορετικό επίπεδο;","Ναι. Κάθε συμμετέχων κάνει αρχική αξιολόγηση και οι ασκήσεις προσαρμόζονται στο δικό του επίπεδο."),
       ("Δεν έχω παρέα. Μπορώ να μπω σε group;","Επικοινώνησε μαζί μας στο 210 576 7892 και θα σε ενημερώσουμε για τη διαθεσιμότητα.")]),
 dict(slug="digital-coaching", name="Digital Coaching", icon="digital-coaching.svg",
  h1="Digital Coaching – Online Personal Training",
  title="Online Personal Training (Digital Coaching) | Training Station Fitness",
  desc="Online personal training από Καθηγητές Φυσικής Αγωγής: εξατομικευμένο πρόγραμμα με βίντεο ασκήσεων, παρακολούθηση προόδου και επικοινωνία, όπου κι αν βρίσκεσαι.",
  stype="Online personal training", online=True,
  body=[("p","Το **Digital Coaching** φέρνει την εξατομικευμένη καθοδήγηση στα χέρια σου, επιτρέποντάς σου να προπονηθείς όπου κι αν βρίσκεσαι. Με την υποστήριξη των **Καθηγητών Φυσικής Αγωγής** του γυμναστηρίου μας, δημιουργούμε προγράμματα που ταιριάζουν στις ανάγκες και τον τρόπο ζωής σου, χωρίς να χρειάζεται να έρθεις στον χώρο μας."),
   ("h2","Τι είναι το Digital Coaching;"),
   ("p","Είναι η ψηφιακή μορφή του personal training, όπου μέσω ειδικών εργαλείων και εφαρμογών:"),
   ("ul",["**Σου παρέχουμε προγράμματα προπόνησης** σχεδιασμένα αποκλειστικά για εσένα.","Παρακολουθούμε την πρόοδό σου εξ αποστάσεως.","Επικοινωνούμε μαζί σου για καθοδήγηση, κίνητρο και αναπροσαρμογή του προγράμματός σου."]),
   ("h2","Γιατί να επιλέξεις Digital Coaching;"),
   ("ul",["**Ευελιξία**: Προπονήσου οποτεδήποτε και οπουδήποτε, στο σπίτι, σε εξωτερικό χώρο ή σε άλλο γυμναστήριο.",
          "**Εξατομίκευση**: Το πρόγραμμα προσαρμόζεται στο επίπεδο, τους στόχους και τον διαθέσιμο χρόνο σου.",
          "**Υποστήριξη από ειδικούς**: Συνεχής καθοδήγηση, παρακολούθηση και προσαρμογές από Καθηγητές Φυσικής Αγωγής.",
          "**Αποτελεσματικότητα**: Αναλυτικές οδηγίες και βίντεο ασκήσεων για σωστή εκτέλεση.",
          "**Οικονομία χρόνου**: Χωρίς μετακινήσεις."]),
   ("h2","Τι περιλαμβάνει;"),
   ("ul",["**Αρχική αξιολόγηση** στόχων, επιπέδου φυσικής κατάστασης και δυνατοτήτων.","**Προσαρμοσμένο πρόγραμμα** με βίντεο και οδηγίες.","**Συνεχή επικοινωνία** μέσω email, εφαρμογών ή βιντεοκλήσεων.","**Συμβουλές ευεξίας** για διατροφή και υγιεινό τρόπο ζωής."])],
  faq=[("Χρειάζομαι εξοπλισμό;","Όχι απαραίτητα. Το πρόγραμμα σχεδιάζεται με βάση τον εξοπλισμό που έχεις: στο σπίτι, σε εξωτερικό χώρο ή σε γυμναστήριο."),
       ("Πώς επικοινωνούμε;","Μέσω email, εφαρμογών ή βιντεοκλήσεων, ανάλογα με ό,τι σε βολεύει."),
       ("Μπορώ να το κάνω αν μένω εκτός Αθήνας ή στο εξωτερικό;","Ναι, το Digital Coaching γίνεται εξ ολοκλήρου online.")]),
 dict(slug="recovery-injuries", name="Recovery Training", icon="recovery.svg",
  h1="Άσκηση για Αποκατάσταση Τραυματισμών στο Περιστέρι",
  title="Άσκηση για Αποκατάσταση Τραυματισμών Περιστέρι | Training Station",
  desc="Recovery Training στο Περιστέρι: ασφαλή, εξατομικευμένα προγράμματα άσκησης για επιστροφή μετά από τραυματισμό, ενδυνάμωση και πρόληψη. Καθηγητές Φυσικής Αγωγής.",
  stype="Exercise for injury recovery",
  body=[("p","Το **Recovery Training** είναι η εξειδικευμένη υπηρεσία μας που εστιάζει στην αποκατάσταση τραυματισμών και τη σταδιακή επανένταξή σου σε μια πλήρη και λειτουργική φυσική κατάσταση. Με την καθοδήγηση των **Καθηγητών Φυσικής Αγωγής** του γυμναστηρίου μας, δημιουργούμε ασφαλή και στοχευμένα προγράμματα που βοηθούν στην αποκατάσταση του σώματός σου, χωρίς να επιβαρύνουμε την τραυματισμένη περιοχή."),
   ("h2","Ποιος είναι ο στόχος του Recovery Training;"),
   ("ul",["**Αποκατάσταση**: Ενίσχυση της τραυματισμένης περιοχής με ασφαλείς ασκήσεις.","**Επανεκπαίδευση κινήσεων**: Βελτίωση κινητικότητας, ισορροπίας και δύναμης.","**Πρόληψη**: Μυϊκή ισορροπία και ενδυνάμωση για την αποφυγή μελλοντικών τραυματισμών.","**Υποστήριξη**: Συνεχής παρακολούθηση και αναπροσαρμογή του προγράμματος."]),
   ("h2","Τι περιλαμβάνει;"),
   ("ul",["**Αρχική αξιολόγηση**: Συζήτηση για τον τραυματισμό, το ιατρικό ιστορικό και τους στόχους σου.","**Εξατομικευμένο πρόγραμμα** με ήπιες ασκήσεις που προάγουν την αποκατάσταση.","**Ασκήσεις λειτουργικής αποκατάστασης**: Ενδυνάμωση και κινησιοθεραπεία.","**Παρακολούθηση και υποστήριξη** με προσαρμογές όποτε χρειαστεί.","**Συμβουλές ευεξίας** για στάση σώματος και εργονομία."]),
   ("p","Το Recovery Training συμπληρώνει – δεν αντικαθιστά – την ιατρική ή φυσικοθεραπευτική φροντίδα. Αν έχεις οδηγίες από γιατρό ή φυσικοθεραπευτή, φέρ' τις στην αρχική αξιολόγηση.")],
  faq=[("Πότε μπορώ να ξεκινήσω μετά από τραυματισμό;","Όταν ο γιατρός σου δώσει το ελεύθερο για άσκηση. Στην αρχική αξιολόγηση λαμβάνουμε υπόψη το ιατρικό ιστορικό και τις οδηγίες που έχεις."),
       ("Έχω χρόνιο πόνο στη μέση. Είναι για μένα;","Πολλοί ασκούμενοί μας ξεκίνησαν με προβλήματα στη μέση. Το πρόγραμμα χτίζεται σταδιακά, με έμφαση στη σωστή τεχνική και την ενδυνάμωση του κορμού."),
       ("Είναι φυσικοθεραπεία;","Όχι. Είναι στοχευμένη άσκηση από Καθηγητές Φυσικής Αγωγής, που συμπληρώνει τη φυσικοθεραπεία και βοηθά στην επιστροφή σε πλήρη δραστηριότητα.")]),
 dict(slug="army-security-forces-training", name="Security Forces – Army Training", icon="forces-training.svg",
  h1="Προετοιμασία για Αθλήματα Αστυνομίας, Στρατού & Σωμάτων Ασφαλείας",
  title="Προετοιμασία Αθλημάτων Αστυνομίας & Στρατού | Training Station",
  desc="Προετοιμασία για τις αθλητικές δοκιμασίες Αστυνομίας, Στρατιωτικών Σχολών και Σωμάτων Ασφαλείας στο Περιστέρι, από Καθηγητή Φυσικής Αγωγής που διδάσκει στη ΣΑΕΑ.",
  stype="Physical test preparation for police and armed forces",
  body=[("p","Το **Army & Security Forces Training** είναι ένα εξειδικευμένο πρόγραμμα σχεδιασμένο για τις αυξημένες απαιτήσεις φυσικής κατάστασης, δύναμης, αντοχής και ψυχικής ετοιμότητας των σωμάτων ασφαλείας και των ενόπλων δυνάμεων. Είτε ετοιμάζεσαι για εισαγωγικές δοκιμασίες, είτε θέλεις να διατηρήσεις την ετοιμότητά σου, σε υποστηρίζουμε με δομημένα προγράμματα."),
   ("p","Ο υπεύθυνος του γυμναστηρίου, **Μάνος Τσαγκατάκης**, διδάσκει από το 2020 Σωματική Αγωγή στη **Σχολή Αξιωματικών της Ελληνικής Αστυνομίας (ΣΑΕΑ)** και γνωρίζει από πρώτο χέρι τις απαιτήσεις."),
   ("h2","Στόχοι του προγράμματος"),
   ("ul",["**Φυσική αντοχή**: Ανάπτυξη καρδιοαναπνευστικής ικανότητας.","**Δύναμη**: Λειτουργική δύναμη και ευκινησία για επιχειρησιακά καθήκοντα.","**Ευκινησία και ισορροπία**: Γρήγορες αντιδράσεις και σταθερότητα.","**Ψυχική ανθεκτικότητα**: Προπόνηση που ενισχύει αυτοπεποίθηση και ψυχραιμία.","**Ετοιμότητα για εξετάσεις**: Στοχευμένη προετοιμασία για τις δοκιμασίες φυσικής κατάστασης."]),
   ("h2","Τι περιλαμβάνει"),
   ("ul",["**Αξιολόγηση** σε αντοχή, δύναμη, ευλυγισία και ταχύτητα.","**Εξατομικευμένη προπόνηση** για βελτίωση χρόνου σε τρέξιμο, push-ups, pull-ups κ.ά.","**Λειτουργική προπόνηση**: άρση βαρών, εμπόδια, sprint, μεταφορά φορτίων.","**Αερόβια και αναερόβια προπόνηση**.","**Ομαδική εργασία**: επικοινωνία και συνεργασία."])],
  faq=[("Για ποιες εξετάσεις προετοιμάζετε;","Για τις αθλητικές δοκιμασίες εισαγωγής ή αξιολόγησης σε σώματα ασφαλείας (π.χ. Αστυνομία) και ένοπλες δυνάμεις. Το πρόγραμμα στήνεται πάνω στις δοκιμασίες της σχολής που σε ενδιαφέρει."),
       ("Πόσο νωρίς πρέπει να ξεκινήσω;","Όσο νωρίτερα τόσο καλύτερα. Μετά την αρχική αξιολόγηση σου λέμε ρεαλιστικά πόσος χρόνος χρειάζεται για να πιάσεις τα όρια."),
       ("Ποιος κάνει την προπόνηση;","Ο Μάνος Τσαγκατάκης, Καθηγητής Φυσικής Αγωγής (ΤΕΦΑΑ Δ.Π.Θ.), που διδάσκει Σωματική Αγωγή στη Σχολή Αξιωματικών της Ελληνικής Αστυνομίας.")]),
 dict(slug="dietetics-and-nutrition", name="Διατροφή & Διαιτολογία", icon="diatrofi.svg",
  h1="Διαιτολόγος – Διατροφολόγος στο Περιστέρι",
  title="Διαιτολόγος στο Περιστέρι & Online | Training Station Fitness",
  desc="Εξατομικευμένα διατροφικά πλάνα από πτυχιούχο Διαιτολόγο-Διατροφολόγο (Χαροκόπειο) στο Περιστέρι ή online. Απώλεια βάρους, μυϊκή μάζα, αθλητική διατροφή.",
  stype="Dietitian / nutrition counselling", online=True,
  body=[("p","Η σωστή διατροφή είναι το θεμέλιο για τη βελτίωση της φυσικής σου κατάστασης, την αύξηση της ενέργειας και τη συνολική σου ευεξία. Η υπηρεσία μας εστιάζει σε **εξατομικευμένα διατροφικά πλάνα**, από την **πτυχιούχο Διαιτολόγο-Διατροφολόγο Μελίνα Τσαγκατάκη** (Χαροκόπειο Πανεπιστήμιο, MSc Εφαρμοσμένη Διαιτολογία και Διατροφή – Κλινική Διατροφή)."),
   ("h2","Τι περιλαμβάνει;"),
   ("ul",["**Αξιολόγηση αναγκών**: Ιατρικό και διατροφικό ιστορικό, προσωπικοί στόχοι.","**Εξατομικευμένο πλάνο** με βάση προτιμήσεις, αλλεργίες ή δυσανεξίες και το πρόγραμμα προπόνησής σου.","**Συνεχής υποστήριξη** με τακτικές αναθεωρήσεις.","**Διατροφική εκπαίδευση** ώστε να κάνεις σωστές επιλογές και εκτός προγράμματος."]),
   ("h2","Πώς μπορεί να σε βοηθήσει;"),
   ("ul",["**Απώλεια ή ρύθμιση βάρους** χωρίς στερήσεις.","**Περισσότερη ενέργεια** στην προπόνηση και την καθημερινότητα.","**Αύξηση μυϊκής μάζας**.","**Βελτίωση υγείας**: μείωση κινδύνων όπως καρδιαγγειακά ή διαταραχές σακχάρου.","**Ειδικές ανάγκες**: αθλητές, εγκυμοσύνη, συγκεκριμένες ιατρικές καταστάσεις."])],
  faq=[("Γίνεται η συνεδρία και online;","Ναι, μπορείς να κλείσεις online συνεδρία διατροφής από τη σελίδα κρατήσεων."),
       ("Ποιος είναι ο διαιτολόγος;","Η Μελίνα Τσαγκατάκη, πτυχιούχος Διαιτολόγος-Διατροφολόγος του Χαροκόπειου Πανεπιστημίου, με μεταπτυχιακό στην Εφαρμοσμένη Διαιτολογία και Διατροφή (Κλινική Διατροφή)."),
       ("Πρέπει να γυμνάζομαι στο Training Station για να πάρω διατροφή;","Όχι. Η υπηρεσία διατροφής είναι διαθέσιμη και αυτόνομα.")]),
]

# ---------------------------------------------------------------- πλαίσιο σελίδας
NAV = [("/", "Αρχική"), ("/services/", "Υπηρεσίες"), ("/pricing/", "Τιμές"), ("/about-us/", "Ποιοι είμαστε"),
       ("/faq/", "Συχνές ερωτήσεις"), ("/contact/", "Επικοινωνία")]

def gym_node():
    b = BUSINESS
    addr = {"@type": "PostalAddress", "streetAddress": b["street"], "addressLocality": b["city"],
            "addressRegion": b["region"], "addressCountry": "GR"}
    if b["postal"]: addr["postalCode"] = b["postal"]
    same = list(b["social"].values()) + ([b["google_business"]] if b["google_business"] else [])
    node = {"@type": ["ExerciseGym", "HealthClub"], "@id": SITE + "/#gym", "name": b["name"],
            "alternateName": "Training Station", "slogan": b["slogan"],
            "description": "Studio προσωπικής προπόνησης στο Περιστέρι (πλατεία Μπουρναζίου): personal training, small group training 2–3 ατόμων, Pilates Reformer, άσκηση για αποκατάσταση τραυματισμών, προετοιμασία για αθλήματα Αστυνομίας/Στρατού, online coaching και διατροφή.",
            "url": SITE + "/", "logo": SITE + "/assets/img/logo.png",
            "image": [SITE + "/assets/img/eleuthera-vari-bournazi.webp", SITE + "/assets/img/aerobia-mixanimata-bournazi.webp", SITE + "/assets/img/eisodos-training-station.webp"],
            "telephone": b["phone"], "email": b["email"], "address": addr,
            "geo": {"@type": "GeoCoordinates", "latitude": b["lat"], "longitude": b["lng"]},
            "hasMap": b["maps_url"], "priceRange": b["price_range"], "currenciesAccepted": "EUR",
            "areaServed": [{"@type": "City", "name": n} for n in ["Περιστέρι", "Αιγάλεω", "Πετρούπολη", "Αγίοι Ανάργυροι", "Ίλιον", "Χαϊδάρι"]],
            "founder": {"@id": SITE + "/#manos"}, "employee": [{"@id": SITE + "/#manos"}, {"@id": SITE + "/#melina"}],
            "contactPoint": [{"@type": "ContactPoint", "telephone": b["phone"], "contactType": "customer service", "availableLanguage": ["el", "en"]},
                             {"@type": "ContactPoint", "telephone": b["mobile"], "contactType": "reservations", "availableLanguage": ["el", "en"]}],
            "sameAs": same,
            "potentialAction": {"@type": "ReserveAction", "target": SITE + "/book-now/"},
            "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Υπηρεσίες", "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@id": f"{SITE}/{s['slug']}/#service"}} for s in SERVICES]}}
    if b["hours"]:
        node["openingHoursSpecification"] = [{"@type": "OpeningHoursSpecification", "dayOfWeek": d, "opens": o, "closes": c} for d, o, c in b["hours"]]
    return node

def people_nodes():
    return [
        {"@type": "Person", "@id": SITE + "/#manos", "name": "Μάνος Τσαγκατάκης", "alternateName": "Εμμανουήλ Τσαγκατάκης",
         "jobTitle": "Καθηγητής Φυσικής Αγωγής – Ιδρυτής Training Station Fitness",
         "image": SITE + "/assets/img/manos-tsagkatakis.webp", "url": SITE + "/about-us/",
         "worksFor": {"@id": SITE + "/#gym"},
         "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Δημοκρίτειο Πανεπιστήμιο Θράκης – ΤΕΦΑΑ"},
                      {"@type": "CollegeOrUniversity", "name": "Χαροκόπειο Πανεπιστήμιο"}],
         "knowsAbout": ["Personal training", "Άσκηση για αποκατάσταση τραυματισμών", "Διατροφή και άσκηση", "Προετοιμασία αθλημάτων Αστυνομίας", "Κολύμβηση"],
         "hasOccupation": {"@type": "Occupation", "name": "Καθηγητής Σωματικής Αγωγής στη Σχολή Αξιωματικών της Ελληνικής Αστυνομίας (ΣΑΕΑ)"}},
        {"@type": "Person", "@id": SITE + "/#melina", "name": "Μελίνα Τσαγκατάκη",
         "jobTitle": "Διαιτολόγος – Διατροφολόγος", "image": SITE + "/assets/img/melina-tsagkataki.webp", "url": SITE + "/about-us/",
         "worksFor": {"@id": SITE + "/#gym"},
         "alumniOf": {"@type": "CollegeOrUniversity", "name": "Χαροκόπειο Πανεπιστήμιο"},
         "knowsAbout": ["Κλινική διατροφή", "Αθλητική διατροφή", "Απώλεια βάρους"]},
    ]

def page(path, title, desc, h1_html, body, crumbs=None, extra_ld=None, og_image="eleuthera-vari-bournazi.webp", noindex=False):
    url = SITE + path
    graph = [
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": BUSINESS["name"], "inLanguage": "el",
         "publisher": {"@id": SITE + "/#gym"}},
        gym_node(),
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "el",
         "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#gym"}, "dateModified": TODAY},
    ]
    if crumbs:
        items = [("Αρχική", "/")] + crumbs
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)]})
        graph[2]["breadcrumb"] = {"@id": url + "#breadcrumb"}
    if extra_ld: graph += extra_ld
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1).replace("</", "<\\/")

    crumbs_html = ""
    if crumbs:
        lis = '<li><a href="/">Αρχική</a></li>' + "".join(
            (f'<li><a href="{p}">{esc(n)}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{esc(n)}</li>')
            for i, (n, p) in enumerate(crumbs))
        crumbs_html = f'<nav class="crumbs wrap" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'

    nav = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == path else ""}>{esc(t)}</a></li>' for h, t in NAV)
    svc_links = "".join(f'<li><a href="/{s["slug"]}/">{esc(s["name"])}</a></li>' for s in SERVICES)
    social = "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{esc(n)}</a></li>' for n, u in BUSINESS["social"].items())
    gb = BUSINESS["google_business"]
    reviews_link = f'<li><a href="{gb}" rel="noopener" target="_blank">Κριτικές Google</a></li>' if gb else (f'<li>{todo("Κριτικές Google (link)","Βάλε το link του Google Business Profile")}</li>')
    pixel = f'<script>window.TSF_FB_PIXEL_ID="{BUSINESS["fb_pixel_id"]}";</script>' if BUSINESS["fb_pixel_id"] else ""
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1"
    preview_bar = ('<div class="preview-bar">ΠΡΟΕΠΙΣΚΟΠΗΣΗ – τα <span class="todo">κίτρινα</span> σημεία θέλουν δικά σου στοιχεία (τιμές, ωράριο, ΤΚ κ.λπ.)</div>' if PREVIEW else "")

    doc = f"""<!doctype html>
<html lang="el">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="el" href="{url}">
<meta property="og:locale" content="el_GR">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Training Station Fitness">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="google-site-verification" content="q9PS32CcKog6PAXxr4ttqAQaPEJWBqULbN2rxX-uZc4">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/img/favicon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap">
<link rel="stylesheet" href="/assets/css/style.css">
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('consent','default',{{ad_storage:'denied',analytics_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',wait_for_update:500}});</script>
{pixel}
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<a class="skip" href="#main">Μετάβαση στο περιεχόμενο</a>
{preview_bar}
<div class="topbar"><div class="wrap">
 <a href="tel:{BUSINESS['phone']}">☎ {BUSINESS['phone_disp']}</a>
 <a href="tel:{BUSINESS['mobile']}">📱 {BUSINESS['mobile_disp']}</a>
 <a href="mailto:{BUSINESS['email']}">✉ {BUSINESS['email']}</a>
</div></div>
<header class="site"><div class="wrap">
 <a class="brand" href="/" aria-label="Training Station Fitness – Αρχική"><img src="/assets/img/logo.webp" width="190" height="88" alt="Training Station Fitness – γυμναστήριο στο Περιστέρι"></a>
 <button class="menu-btn" aria-expanded="false" aria-controls="menu">Μενού</button>
 <nav class="main" id="menu" aria-label="Κύριο μενού"><ul>{nav}<li class="cta"><a href="/book-now/">Κράτηση</a></li></ul></nav>
</div></header>
{crumbs_html}
<main id="main">
{h1_html}
{body}
</main>
<footer class="site"><div class="wrap">
 <div class="cols">
  <div>
   <img src="/assets/img/logo.webp" width="170" height="79" alt="Training Station Fitness" loading="lazy">
   <p style="margin-top:12px"><strong>Training Station Fitness</strong><br>{address_line()}<br>
   <a href="tel:{BUSINESS['phone']}">{BUSINESS['phone_disp']}</a> · <a href="tel:{BUSINESS['mobile']}">{BUSINESS['mobile_disp']}</a><br>
   <a href="mailto:{BUSINESS['email']}">{BUSINESS['email']}</a><br>{hours_html()}</p>
  </div>
  <div><h2>Υπηρεσίες</h2><ul>{svc_links}</ul></div>
  <div><h2>Πληροφορίες</h2><ul><li><a href="/pricing/">Τιμές</a></li><li><a href="/about-us/">Ποιοι είμαστε</a></li><li><a href="/faq/">Συχνές ερωτήσεις</a></li><li><a href="/gift-cards/">Gift cards</a></li><li><a href="/book-now/">Online κράτηση</a></li><li><a href="/contact/">Επικοινωνία</a></li></ul></div>
  <div><h2>Ακολούθησέ μας</h2><ul>{social}{reviews_link}<li><a href="https://www.instagram.com/onlinefitnessgr/" rel="noopener" target="_blank">Online Fitness GR</a></li></ul></div>
 </div>
 <div class="legal"><span>© {datetime.date.today().year} Training Station Fitness · {esc(BUSINESS['legal_name'])} · Αρ. Γ.Ε.ΜΗ {BUSINESS['gemi']}</span>
 <span><a href="/conditions/">Όροι χρήσης &amp; απόρρητο</a> · <a href="#" data-cookie-settings>Ρυθμίσεις cookies</a></span></div>
</div></footer>
<div class="consent" role="dialog" aria-live="polite" aria-label="Cookies">
 <p>Χρησιμοποιούμε απαραίτητα cookies για τη λειτουργία του site. Με τη συγκατάθεσή σου χρησιμοποιούμε και cookies μέτρησης και διαφήμισης (Google, Meta). <a href="/conditions/#cookies">Μάθε περισσότερα</a></p>
 <div class="btns"><button class="accept">Αποδοχή όλων</button><button class="reject">Μόνο απαραίτητα</button></div>
</div>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""
    if path.endswith(".html"):
        fn = os.path.join(OUT, path.strip("/"))
    else:
        d = os.path.join(OUT, path.strip("/"))
        os.makedirs(d, exist_ok=True)
        fn = os.path.join(d, "index.html")
    with open(fn, "w", encoding="utf-8") as f: f.write(doc)
    return path

def blocks(bl):
    out = []
    for t, x in bl:
        if t == "p": out.append(f"<p>{md(x)}</p>")
        elif t == "h2": out.append(f"<h2>{md(x)}</h2>")
        elif t == "h3": out.append(f"<h3>{md(x)}</h3>")
        elif t == "ul": out.append("<ul>" + "".join(f"<li>{md(i)}</li>" for i in x) + "</ul>")
    return "\n".join(out)

def faq_html(faqs, heading="Συχνές ερωτήσεις"):
    items = "".join(f"<details><summary>{esc(q)}</summary><p>{md(a)}</p></details>" for q, a in faqs)
    return f'<div class="faq"><h2>{esc(heading)}</h2>{items}</div>'

def faq_ld(faqs, url):
    return {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\*\*", "", a)}} for q, a in faqs]}

CTA = '''<section class="center"><div class="wrap">
<h2>Ξεκίνα με μια δωρεάν γνωριμία</h2>
<p>Κλείσε online ή πάρε μας τηλέφωνο. Συζητάμε τους στόχους σου και σου προτείνουμε το κατάλληλο πρόγραμμα.</p>
<div class="btns"><a class="btn" href="/book-now/">ΚΛΕΙΣΕ ΡΑΝΤΕΒΟΥ</a><a class="btn ghost" href="tel:+302105767892">210 576 7892</a></div>
</div></section>'''

def map_block(title_tag="h2"):
    b = BUSINESS
    return f'''<section><div class="wrap contact-grid">
<div><{title_tag}>Βρείτε μας στον χάρτη</{title_tag}>
<div class="map-facade"><button class="btn" data-src="{esc(b['maps_embed'])}">Εμφάνιση χάρτη</button></div>
<p style="margin-top:10px"><a href="{esc(b['maps_url'])}" target="_blank" rel="noopener">Οδηγίες στο Google Maps →</a></p></div>
<div class="nap"><{title_tag}>Επικοινωνία</{title_tag}>
<p><strong>Διεύθυνση</strong><br>{address_line()}</p>
<p><strong>Ωράριο</strong><br>{hours_html()}</p>
<p><strong>Τηλέφωνο</strong><br><a href="tel:{b['phone']}">{b['phone_disp']}</a> · <a href="tel:{b['mobile']}">{b['mobile_disp']}</a></p>
<p><strong>E-mail</strong><br><a href="mailto:{b['email']}">{b['email']}</a></p>
<p><strong>Πρόσβαση</strong><br>Στην πλατεία Μπουρναζίου, κοντά σε στάσεις λεωφορείων. {todo("Πλησιέστερος σταθμός μετρό / στάσεις / στάθμευση","Πρόσθεσε οδηγίες πρόσβασης – βοηθούν local SEO και AI")}</p>
</div></div></section>'''

TESTIMONIALS = [
    ("Καθαρός και ευχάριστος χώρος για προπόνηση! Ο Μάνος έμπειρος γνώστης και σε εμπνέει για προπόνηση, με ποικιλία προπονήσεων!", "Βασίλης"),
    ("Τα δυτικά απέκτησαν ένα ΣΩΣΤΟ personal studio. Ο Μάνος φανταστικός στη δουλειά του, πάντα εκεί να σε ενθαρρύνει σε κάθε σου στόχο.", "Ευαγγελία"),
    ("The ultimate place for training! Manos, the instructor, is amazing and really helped me to regain my confidence and shape in zero time!!!", "Panayiotis"),
    ("Ο Μάνος είναι καταπληκτικός! Κάνουμε μαζί προπόνηση εδώ και 2 χρόνια (με χρόνια προβλήματα στη μέση μου) είναι δάσκαλος στο πώς θα προσεγγίσει την κάθε άσκηση! Έχω δει φανταστική διαφορά. Σε ευχαριστώ!!", "Γιώργος"),
    ("Ο χώρος είναι πεντακάθαρος και με πολύ καλό εξοπλισμό. Κεντρικά και κοντά με ΜΜΜ. Όσο για την προπόνηση είναι τοπ. Αν και έχω θέμα με τη μέση μου λόγω μπάσκετ και φοβόμουν να ξεκινήσω, τελικά δικαιώθηκα. Επαγγελματίες, που είναι από πάνω σου και κάνουν φοβερή δουλειά όχι μόνο στο κομμάτι γυμναστικής αλλά και διατροφής.", "Τζαννής"),
    ("Επιτέλους βρήκα έναν γυμναστή καταρτισμένο, με επιστημονικές γνώσεις, που προσέχει τους ασκούμενούς του στο έπακρο! Μπράβο για όλα!!! Ο χώρος καταπληκτικός!!!", "Μαρία"),
]

def testimonials():
    q = "".join(f'<blockquote><div class="stars" aria-label="5 στα 5">★★★★★</div><p>{esc(t)}</p><cite>— {esc(n)}</cite></blockquote>' for t, n in TESTIMONIALS)
    gb = BUSINESS["google_business"]
    link = f'<a href="{gb}" target="_blank" rel="noopener">Δες όλες τις κριτικές στο Google →</a>' if gb else todo("Δες όλες τις κριτικές στο Google → (link)", "Link του Google Business Profile")
    return f'<section class="blue"><div class="wrap"><h2 class="center">Τι λένε οι ασκούμενοί μας</h2><div class="quotes">{q}</div><p class="center" style="margin-top:24px">{link}</p></div></section>'

# ---------------------------------------------------------------- σελίδες
pages = []

# Αρχική
home_faq = [
    ("Πού βρίσκεται το Training Station Fitness;", "Στην οδό Παρασκευοπούλου 47, στην πλατεία Μπουρναζίου στο Περιστέρι (Δυτική Αθήνα)."),
    ("Τι υπηρεσίες προσφέρετε;", "Ατομικό personal training, small group training για 2–3 άτομα, Pilates Reformer, άσκηση για αποκατάσταση τραυματισμών, προετοιμασία για τα αθλήματα Αστυνομίας και Στρατού, online coaching και διατροφή με Διαιτολόγο."),
    ("Χρειάζεται ραντεβού;", "Ναι, όλες οι συνεδρίες γίνονται κατόπιν ραντεβού. Κλείνεις online από τη σελίδα «Κράτηση» ή στο 210 576 7892."),
    ("Υπάρχει δωρεάν δοκιμαστική συνάντηση;", "Ναι, μπορείς να κλείσεις μια δωρεάν ενημερωτική συνάντηση γνωριμίας για να συζητήσουμε τους στόχους σου."),
]
svc_cards = "".join(f'''<article class="card"><img class="icon" src="/assets/img/{s["icon"]}" alt="" width="84" height="84" loading="lazy">
<h3><a href="/{s["slug"]}/" style="color:inherit;text-decoration:none">{esc(s["name"])}</a></h3><p>{esc(s["desc"].split(".")[0])}.</p><a class="more" href="/{s["slug"]}/">Μάθε περισσότερα →</a></article>''' for s in SERVICES)
home_body = f'''
<section style="padding-top:0"><div class="wrap grid-2">
<div><h2>Wellness place στην πλατεία Μπουρναζίου</h2>
<p>Στον πλήρως εξοπλισμένο μας χώρο στην πλατεία <strong>Μπουρναζίου στο Περιστέρι</strong>, μπορείτε να κάνετε <strong>ατομικές προπονήσεις</strong>, <strong>ομαδικές προπονήσεις έως 3 άτομα</strong>, <strong>Pilates Reformer</strong>, <strong>online προπονητική</strong>, καθώς και <strong>άσκηση για αποκατάσταση τραυματισμών</strong>. Σας προσφέρουμε προπονητική και διατροφική αξιολόγηση και μελετάμε με λεπτομέρεια την κάθε σας ανάγκη, δημιουργώντας το καταλληλότερο πρόγραμμα προπόνησης και διατροφής.</p>
<div class="btns"><a class="btn" href="/book-now/">BOOK NOW!</a><a class="btn ghost" href="/pricing/">Δες τιμές</a></div></div>
<img src="/assets/img/eisodos-training-station.webp" width="900" height="720" alt="Η είσοδος του Training Station Fitness στο Περιστέρι με το λογότυπο στον καθρέφτη" fetchpriority="high">
</div>
<div class="wrap facts">
<div><strong>Έως 3 άτομα</strong>ανά προπόνηση</div><div><strong>Καθηγητές Φ.Α.</strong>πτυχιούχοι ΤΕΦΑΑ</div><div><strong>Διαιτολόγος</strong>στην ομάδα</div><div><strong>Δωρεάν</strong>γνωριμία</div>
</div></section>
<section style="padding-top:0"><div class="wrap photos">
<img src="/assets/img/eleuthera-vari-bournazi.webp" width="900" height="720" alt="Rack, ιμάντες TRX και μπάρα Olympic στον χώρο ελεύθερων βαρών του Training Station Fitness" loading="lazy">
<img src="/assets/img/aerobia-mixanimata-bournazi.webp" width="900" height="720" alt="Διάδρομος, αλτήρες και πολυόργανο τροχαλίας στο γυμναστήριο στο Περιστέρι" loading="lazy">
<img src="/assets/img/gift-card.webp" width="900" height="638" alt="Δωροκάρτα (gift card) Training Station Fitness" loading="lazy">
</div></section>
<section><div class="wrap"><h2 class="center">Οι υπηρεσίες μας</h2><div class="grid-3">{svc_cards}</div></div></section>
<section><div class="wrap grid-2">
<div><h2>Ποιοι είμαστε</h2>
<p>Ονομάζομαι <strong>Μάνος Τσαγκατάκης</strong>. Είμαι απόφοιτος του <strong>ΤΕΦΑΑ του Δημοκρίτειου Πανεπιστημίου Θράκης</strong>, με ειδικότητα στην κολύμβηση, και μεταπτυχιακός φοιτητής του <strong>Χαροκόπειου Πανεπιστημίου</strong> στην Εφαρμοσμένη Διατροφή &amp; Διατροφολογία (κατεύθυνση Διατροφή &amp; Άσκηση). Από το 2020 διδάσκω <strong>Σωματική Αγωγή στη Σχολή Αξιωματικών της Ελληνικής Αστυνομίας (ΣΑΕΑ)</strong>.</p>
<p>Η πολυετής εμπειρία μου στις εξατομικευμένες προπονήσεις με ώθησε να δημιουργήσω έναν χώρο όπου ο κάθε ασκούμενος, με <strong>σωστή καθοδήγηση</strong>, <strong>επιστημονική γνώση</strong> και <strong>ασφάλεια</strong>, πετυχαίνει κάθε στόχο.</p>
<a class="btn ghost" href="/about-us/">Γνώρισε την ομάδα</a></div>
<img src="/assets/img/manos-tsagkatakis.webp" width="768" height="768" alt="Μάνος Τσαγκατάκης, Καθηγητής Φυσικής Αγωγής και ιδρυτής του Training Station Fitness" loading="lazy" style="border-radius:14px;max-width:420px;justify-self:center">
</div></section>
{testimonials()}
<section><div class="wrap content" style="margin:0 auto">{faq_html(home_faq)}<p><a href="/faq/">Όλες οι συχνές ερωτήσεις →</a></p></div></section>
{map_block()}
'''
pages.append(page("/", "Γυμναστήριο Περιστέρι – Personal Training & Pilates | Training Station",
    "Personal training, Pilates Reformer, group 2–3 ατόμων & αποκατάσταση τραυματισμών στην πλ. Μπουρναζίου, Περιστέρι. Καθηγητές Φ.Α. & Διαιτολόγος.",
    '<section class="hero"><div class="wrap"><p class="eyebrow">Personal training studio · Περιστέρι</p><h1>Training Station Fitness – Γυμναστήριο στο Περιστέρι</h1><p class="lead">Η γυμναστική σου μόλις απέκτησε ενδιαφέρον! Εξατομικευμένη προπόνηση, Pilates Reformer και διατροφή στην πλατεία Μπουρναζίου.</p><div class="btns" style="justify-content:center"><a class="btn" href="/book-now/">ΚΛΕΙΣΕ ΡΑΝΤΕΒΟΥ</a><a class="btn ghost" href="tel:+302105767892">210 576 7892</a></div></div></section>',
    home_body, extra_ld=[faq_ld(home_faq, SITE + "/")]))

# Σελίδες υπηρεσιών
for s in SERVICES:
    url = f"{SITE}/{s['slug']}/"
    svc_ld = {"@type": "Service", "@id": url + "#service", "name": s["name"], "serviceType": s["stype"], "url": url,
              "description": s["desc"], "provider": {"@id": SITE + "/#gym"},
              "areaServed": {"@type": "City", "name": "Περιστέρι"} if not s.get("online") else [{"@type": "City", "name": "Περιστέρι"}, {"@type": "Country", "name": "Ελλάδα"}]}
    head = f'''<section style="padding-bottom:20px"><div class="wrap service-head"><div><h1>{esc(s["h1"])}</h1></div>
<img src="/assets/img/{s["icon"]}" alt="" width="220" height="220"></div></section>'''
    body = f'''<section style="padding-top:0"><div class="wrap content">{blocks(s["body"])}
<p><a class="btn" href="/book-now/">BOOK NOW</a></p>
{faq_html(s["faq"])}
<p>Δες επίσης: {" · ".join(f'<a href="/{o["slug"]}/">{esc(o["name"])}</a>' for o in SERVICES if o is not s)} · <a href="/pricing/">Τιμές</a></p>
</div></section>{map_block()}'''
    pages.append(page(f"/{s['slug']}/", s["title"], s["desc"], head, body,
                      crumbs=[("Υπηρεσίες", "/services/"), (s["name"], f"/{s['slug']}/")],
                      extra_ld=[svc_ld, faq_ld(s["faq"], url)]))

# Υπηρεσίες
pages.append(page("/services/", "Υπηρεσίες Γυμναστηρίου στο Περιστέρι | Training Station Fitness",
    "Personal training, Pilates Reformer, group 2–3 ατόμων, online coaching, αποκατάσταση τραυματισμών, Forces training και διατροφή στο Περιστέρι.",
    '<section class="hero"><div class="wrap"><h1>Υπηρεσίες γυμναστηρίου στο Περιστέρι</h1><p class="lead">Κάθε πρόγραμμα ξεκινά με αξιολόγηση και σχεδιάζεται από Καθηγητές Φυσικής Αγωγής για τους δικούς σου στόχους.</p></div></section>',
    f'<section style="padding-top:0"><div class="wrap"><div class="grid-3">{svc_cards}</div></div></section>{CTA}',
    crumbs=[("Υπηρεσίες", "/services/")],
    extra_ld=[{"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/{s['slug']}/", "name": s["name"]} for i, s in enumerate(SERVICES)]}]))

# Τιμές
rows = "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td><td><strong>{esc(c) if c else todo('XX €','Βάλε την τιμή')}</strong></td><td>{esc(d)}</td></tr>" for a, b, c, d in PRICES)
offers = [{"@type": "Offer", "name": f"{a} – {b}", "price": "0" if c == "Δωρεάν" else re.sub(r"[^\d.,]", "", c).replace(",", "."), "priceCurrency": "EUR", "seller": {"@id": SITE + "/#gym"}} for a, b, c, d in PRICES if c]
price_faq = [("Υπάρχει δωρεάν δοκιμή;", "Ναι, η πρώτη ενημερωτική συνάντηση γνωριμίας είναι δωρεάν."),
             ("Πώς πληρώνω;", "Μπορείς να πληρώσεις online κατά την κράτηση ή στον χώρο μας."),
             ("Ισχύουν οι τιμές για gift cards;", "Ναι, μπορείς να αγοράσεις οποιοδήποτε πακέτο ως δωροκάρτα.")]
pages.append(page("/pricing/", "Τιμές Personal Training & Pilates Περιστέρι | Training Station",
    "Τιμές και πακέτα για personal training, Pilates Reformer, group 2–3 ατόμων, online coaching και διατροφή στο Training Station Fitness, Περιστέρι. Δωρεάν γνωριμία.",
    '<section class="hero"><div class="wrap"><h1>Τιμές &amp; πακέτα</h1><p class="lead">Ξεκάθαρες τιμές, χωρίς δεσμεύσεις. Η πρώτη συνάντηση γνωριμίας είναι δωρεάν.</p></div></section>',
    f'''<section style="padding-top:0"><div class="wrap"><div class="table-scroll"><table class="price-table"><thead><tr><th>Υπηρεσία</th><th>Πακέτο</th><th>Τιμή</th><th>Σημείωση</th></tr></thead><tbody>{rows}</tbody></table></div>
<p style="margin-top:14px;font-size:15px">Οι τιμές περιλαμβάνουν ΦΠΑ. Τελευταία ενημέρωση: {TODAY}.</p>
<div class="content">{faq_html(price_faq)}</div></div></section>{CTA}''',
    crumbs=[("Τιμές", "/pricing/")], extra_ld=([{"@type": "OfferCatalog", "name": "Τιμοκατάλογος", "itemListElement": offers}] + [faq_ld(price_faq, SITE + "/pricing/")])))

# FAQ
all_faq = home_faq + [q for s in SERVICES for q in s["faq"]] + price_faq
seen, uniq = set(), []
for q in all_faq:
    if q[0] not in seen: seen.add(q[0]); uniq.append(q)
faq_sections = faq_html(home_faq, "Γενικά") + "".join(faq_html(s["faq"], s["name"]) for s in SERVICES) + faq_html(price_faq, "Τιμές & πληρωμές")
pages.append(page("/faq/", "Συχνές Ερωτήσεις | Training Station Fitness Περιστέρι",
    "Απαντήσεις για personal training, Pilates Reformer, αποκατάσταση τραυματισμών, αθλήματα Αστυνομίας, διατροφή, τιμές και κρατήσεις στο Training Station.",
    '<section class="hero"><div class="wrap"><h1>Συχνές ερωτήσεις</h1></div></section>',
    f'<section style="padding-top:0"><div class="wrap content" style="margin:0 auto">{faq_sections}</div></section>{CTA}',
    crumbs=[("Συχνές ερωτήσεις", "/faq/")], extra_ld=[faq_ld(uniq, SITE + "/faq/")]))

# Ποιοι είμαστε
pages.append(page("/about-us/", "Ποιοι Είμαστε – Μάνος & Μελίνα Τσαγκατάκη | Training Station Fitness",
    "Γνώρισε την ομάδα του Training Station Fitness στο Περιστέρι: Μάνος Τσαγκατάκης, Καθηγητής Φυσικής Αγωγής (ΤΕΦΑΑ, ΣΑΕΑ) και Μελίνα Τσαγκατάκη, Διαιτολόγος-Διατροφολόγος.",
    '<section class="hero"><div class="wrap"><h1>Ποιοι είμαστε</h1><p class="lead">Επιστημονική γνώση, σωστή καθοδήγηση και ασφάλεια, σε έναν φιλικό χώρο στην πλατεία Μπουρναζίου.</p></div></section>',
    f'''<section style="padding-top:0"><div class="wrap people">
<article class="card"><img src="/assets/img/manos-tsagkatakis.webp" width="768" height="768" alt="Μάνος Τσαγκατάκης, Καθηγητής Φυσικής Αγωγής" loading="lazy">
<h2 style="margin-top:18px">Μάνος Τσαγκατάκης</h2><p><strong>Καθηγητής Φυσικής Αγωγής – Ιδρυτής</strong></p>
<ul><li>Πτυχίο ΤΕΦΑΑ, Δημοκρίτειο Πανεπιστήμιο Θράκης (ειδικότητα κολύμβηση)</li><li>Μεταπτυχιακός φοιτητής, Χαροκόπειο Πανεπιστήμιο – Εφαρμοσμένη Διατροφή &amp; Διατροφολογία (Διατροφή &amp; Άσκηση)</li><li>Από το 2020 διδάσκει Σωματική Αγωγή στη Σχολή Αξιωματικών της Ελληνικής Αστυνομίας (ΣΑΕΑ)</li></ul>
<p>Η πολυετής εμπειρία μου στον χώρο της άσκησης και των εξατομικευμένων προπονήσεων με ώθησε να δημιουργήσω έναν χώρο όπου ο κάθε ασκούμενος, με σωστή καθοδήγηση, επιστημονική γνώση και ασφάλεια, πετυχαίνει κάθε στόχο.</p></article>
<article class="card"><img src="/assets/img/melina-tsagkataki.webp" width="900" height="900" alt="Μελίνα Τσαγκατάκη, Διαιτολόγος-Διατροφολόγος" loading="lazy">
<h2 style="margin-top:18px">Μελίνα Τσαγκατάκη</h2><p><strong>Διαιτολόγος – Διατροφολόγος</strong></p>
<ul><li>Πτυχίο Διαιτολογίας-Διατροφολογίας, Χαροκόπειο Πανεπιστήμιο</li><li>Μεταπτυχιακό στην Εφαρμοσμένη Διαιτολογία και Διατροφή, κατεύθυνση Κλινική Διατροφή</li></ul>
<p>Υπεύθυνη για τις <a href="/dietetics-and-nutrition/">διατροφικές υπηρεσίες</a>, στον χώρο μας ή online.</p></article>
</div></section>
<section style="padding-top:0"><div class="wrap content"><h2>Ο χώρος μας</h2><p>Στον χώρο μας στην πλατεία <strong>Μπουρναζίου στο Περιστέρι</strong>, μπορείτε να κάνετε ατομικές προπονήσεις, ομαδικές προπονήσεις έως 3 άτομα, Pilates Reformer, online προπονητική, καθώς και άσκηση για αποκατάσταση τραυματισμών. Σας προσφέρουμε προπονητική και διατροφική αξιολόγηση και μελετάμε με λεπτομέρεια την κάθε σας ανάγκη.</p></div>
<div class="wrap photos"><img src="/assets/img/eisodos-training-station.webp" width="900" height="720" alt="Είσοδος του Training Station Fitness" loading="lazy"><img src="/assets/img/eleuthera-vari-bournazi.webp" width="900" height="720" alt="Χώρος ελεύθερων βαρών με rack και TRX" loading="lazy"><img src="/assets/img/aerobia-mixanimata-bournazi.webp" width="900" height="720" alt="Διάδρομος και αλτήρες στο γυμναστήριο" loading="lazy"></div></section>
{testimonials()}{CTA}''',
    crumbs=[("Ποιοι είμαστε", "/about-us/")], og_image="manos-tsagkatakis.webp",
    extra_ld=people_nodes() + [{"@type": "AboutPage", "@id": SITE + "/about-us/#about", "url": SITE + "/about-us/", "mainEntity": {"@id": SITE + "/#gym"}}]))

# Επικοινωνία
pages.append(page("/contact/", "Επικοινωνία – Παρασκευοπούλου 47, Περιστέρι | Training Station Fitness",
    "Επικοινώνησε με το Training Station Fitness: Παρασκευοπούλου 47, πλατεία Μπουρναζίου, Περιστέρι. Τηλ. 210 576 7892 · 694 619 4809 · info@trainingstationfitness.com.",
    '<section class="hero"><div class="wrap"><h1>Επικοινωνία</h1><p class="lead">Συνεδρίες και ενημέρωση πραγματοποιούνται κατόπιν ραντεβού.</p></div></section>',
    f'''{map_block("h2")}
<section style="padding-top:0"><div class="wrap content" style="margin:0 auto"><h2>Στείλε μας μήνυμα</h2>
<form class="contact" method="post" action="#" onsubmit="alert('Προεπισκόπηση: εδώ συνδέεται η φόρμα του WordPress (π.χ. Contact Form 7).');return false">
<label for="f-name">Ονοματεπώνυμο *</label><input id="f-name" name="name" required autocomplete="name">
<label for="f-mail">Email *</label><input id="f-mail" name="email" type="email" required autocomplete="email">
<label for="f-tel">Τηλέφωνο *</label><input id="f-tel" name="tel" type="tel" required autocomplete="tel">
<label for="f-msg">Μήνυμα *</label><textarea id="f-msg" name="msg" rows="5" required></textarea>
<label style="font-weight:400"><input type="checkbox" required style="width:auto"> Συμφωνώ με την <a href="/conditions/">πολιτική απορρήτου</a>.</label>
<button class="btn" type="submit">Αποστολή</button></form></div></section>''',
    crumbs=[("Επικοινωνία", "/contact/")],
    extra_ld=[{"@type": "ContactPage", "@id": SITE + "/contact/#contact", "url": SITE + "/contact/", "mainEntity": {"@id": SITE + "/#gym"}}]))

# Κράτηση
pages.append(page("/book-now/", "Online Κράτηση Ραντεβού | Training Station Fitness Περιστέρι",
    "Κλείσε online ραντεβού για personal training, group 2–3 ατόμων, digital coaching, διατροφή ή δωρεάν συνάντηση γνωριμίας στο Training Station Fitness, Περιστέρι.",
    '<section class="hero"><div class="wrap"><h1>Κλείσε online ραντεβού</h1><p class="lead">Διάλεξε υπηρεσία, ημέρα και ώρα. Αν δεν υπάρχει διαθεσιμότητα την ώρα που σε ενδιαφέρει, <a href="tel:+302105767892">κάλεσέ μας</a>!</p></div></section>',
    f'''<section style="padding-top:0"><div class="wrap">
<div class="card center" style="min-height:260px;display:flex;flex-direction:column;justify-content:center;border:2px dashed var(--line)">
<p><strong>Εδώ εμφανίζεται το σύστημα κρατήσεων (Booknetic)</strong></p><p style="font-size:15px">Στην προεπισκόπηση δεν φορτώνει. Στο WordPress μένει όπως είναι σήμερα.</p></div>
<div class="content" style="margin-top:32px">
<h2>Ποιες υπηρεσίες μπορείς να κλείσεις;</h2>
<ul><li><strong>Personal Training (ατομική προπόνηση)</strong> με Καθηγητή Φυσικής Αγωγής.</li><li><strong>Small Group Training (2–3 άτομα)</strong>.</li><li><strong>Digital Coaching</strong> εξ αποστάσεως.</li><li><strong>Διατροφή online</strong> με τη Διαιτολόγο μας.</li><li><strong>Δωρεάν ενημερωτική συνάντηση</strong> γνωριμίας.</li></ul>
<h2>Πώς κλείνεις ραντεβού;</h2>
<ol><li>Διάλεξε την υπηρεσία.</li><li>Επίλεξε ημερομηνία και ώρα.</li><li>Συμπλήρωσε τα στοιχεία σου.</li><li>Λαμβάνεις επιβεβαίωση με email ή SMS.</li></ol>
</div></div></section>''',
    crumbs=[("Κράτηση", "/book-now/")]))

# Gift cards
pages.append(page("/gift-cards/", "Δωροκάρτες Γυμναστικής (Gift Cards) Περιστέρι | Training Station",
    "Χάρισε προπόνηση! Δωροκάρτες για personal training, Pilates Reformer και διατροφή στο Training Station Fitness, Περιστέρι. Ιδανικό δώρο για γενέθλια και γιορτές.",
    '<section class="hero"><div class="wrap"><h1>Gift cards – Χάρισε προπόνηση</h1><p class="lead">Το δώρο που φροντίζει την υγεία: συνεδρίες personal training, Pilates Reformer ή διατροφής, σε δωροκάρτα.</p></div></section>',
    f'''<section style="padding-top:0"><div class="wrap grid-2">
<div class="content"><h2>Πώς λειτουργεί</h2><ol><li>Διάλεξε υπηρεσία ή πακέτο από τον <a href="/pricing/">τιμοκατάλογο</a> ή ποσό της επιλογής σου.</li><li>Επικοινώνησε μαζί μας στο <a href="tel:+302105767892">210 576 7892</a> ή στο <a href="mailto:info@trainingstationfitness.com">info@trainingstationfitness.com</a>.</li><li>Παραλαμβάνεις τη δωροκάρτα (έντυπη ή ψηφιακή) με το όνομα του δικού σου ανθρώπου.</li><li>Ο κάτοχος κλείνει ραντεβού όποτε τον βολεύει.</li></ol>
<p>Διάρκεια ισχύος: {todo("π.χ. 6 μήνες","Πόσο ισχύει η δωροκάρτα;")}</p>
<h2>Ιδανική για</h2><ul><li>Γενέθλια, γιορτές, Χριστούγεννα</li><li>Όποιον θέλει να ξεκινήσει γυμναστική με σωστή καθοδήγηση</li><li>Εταιρικά δώρα</li></ul>
<a class="btn" href="/contact/">Παράγγειλε gift card</a></div>
<img src="/assets/img/gift-card.webp" width="900" height="638" alt="Δωροκάρτα Training Station Fitness" loading="lazy" style="border-radius:14px">
</div></section>''',
    crumbs=[("Gift cards", "/gift-cards/")], og_image="gift-card.webp"))

# Όροι (σύνοψη – το πλήρες κείμενο μένει από το υπάρχον site)
pages.append(page("/conditions/", "Όροι Χρήσης & Πολιτική Απορρήτου | Training Station Fitness",
    "Όροι χρήσης, πολιτική απορρήτου και cookies του trainingstationfitness.com (ΕΜΜΑΝΟΥΗΛ ΤΣΑΓΚΑΤΑΚΗΣ – Training Station Fitness).",
    '<section class="hero"><div class="wrap"><h1>Όροι χρήσης &amp; πολιτική απορρήτου</h1></div></section>',
    f'''<section style="padding-top:0"><div class="wrap content" style="margin:0 auto">
<p>Η ιστοσελίδα trainingstationfitness.com ανήκει στην επιχείρηση «{esc(BUSINESS['legal_name'])}» με διακριτικό τίτλο «TRAINING STATION FITNESS» (Αρ. Γ.Ε.ΜΗ {BUSINESS['gemi']}), με έδρα την οδό Παρασκευοπούλου 47, Περιστέρι.</p>
<p class="todo">Προεπισκόπηση: εδώ μπαίνει αυτούσιο το πλήρες κείμενο όρων από το υπάρχον site.</p>
<h2 id="cookies">Cookies</h2>
<p>Τα απαραίτητα cookies χρειάζονται για τη λειτουργία του site. Cookies μέτρησης (Google Analytics) και διαφήμισης (Meta Pixel) ενεργοποιούνται <strong>μόνο</strong> αν δώσεις συγκατάθεση, και μπορείς να την ανακαλέσεις οποιαδήποτε στιγμή από τις <a href="#" data-cookie-settings>ρυθμίσεις cookies</a>.</p>
</div></section>''',
    crumbs=[("Όροι χρήσης", "/conditions/")]))

# 404
page("/404.html", "Η σελίδα δεν βρέθηκε | Training Station Fitness", "Η σελίδα που ζητήσατε δεν βρέθηκε. Δείτε τις υπηρεσίες του Training Station Fitness στο Περιστέρι.",
     '<section class="hero"><div class="wrap"><h1>Η σελίδα δεν βρέθηκε</h1><p class="lead">Ίσως σε ενδιαφέρουν:</p><div class="btns" style="justify-content:center"><a class="btn" href="/">Αρχική</a><a class="btn ghost" href="/services/">Υπηρεσίες</a></div></div></section>',
     "", noindex=True)

# ---------------------------------------------------------------- robots / sitemap / llms.txt
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"""User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php

# Μηχανές αναζήτησης AI: επιτρέπονται ρητά
User-agent: GPTBot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: ClaudeBot
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Google-Extended
User-agent: Applebot-Extended
Allow: /

Sitemap: {SITE}/sitemap.xml
""")

prio = {"/": "1.0"}
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for p in pages:
        f.write(f"  <url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod></url>\n")
    f.write("</urlset>\n")

svc_lines = "\n".join(f"- [{s['name']}]({SITE}/{s['slug']}/): {s['desc']}" for s in SERVICES)
hours_txt = "; ".join(f"{','.join(d)} {o}-{c}" for d, o, c in BUSINESS["hours"]) if BUSINESS["hours"] else "Κατόπιν ραντεβού"
with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8") as f:
    f.write(f"""# Training Station Fitness

> Studio προσωπικής προπόνησης (personal training studio) στο Περιστέρι Αττικής, στην πλατεία Μπουρναζίου. Personal training, small group training 2–3 ατόμων, Pilates Reformer, άσκηση για αποκατάσταση τραυματισμών, προετοιμασία για τις αθλητικές δοκιμασίες Αστυνομίας/Στρατού, online coaching και διατροφή με Διαιτολόγο. Όλες οι συνεδρίες γίνονται κατόπιν ραντεβού· η πρώτη συνάντηση γνωριμίας είναι δωρεάν.

- Διεύθυνση: {BUSINESS['street']}, {BUSINESS['postal'] + ' ' if BUSINESS['postal'] else ''}{BUSINESS['city']} ({BUSINESS['area']}), Ελλάδα
- Τηλέφωνο: {BUSINESS['phone_disp']} · Κινητό: {BUSINESS['mobile_disp']}
- Email: {BUSINESS['email']}
- Ωράριο: {hours_txt}
- Online κράτηση: {SITE}/book-now/
- Ιδρυτής: Μάνος Τσαγκατάκης, Καθηγητής Φυσικής Αγωγής (ΤΕΦΑΑ Δημοκρίτειου Πανεπιστημίου Θράκης), διδάσκει Σωματική Αγωγή στη Σχολή Αξιωματικών της Ελληνικής Αστυνομίας από το 2020.
- Διαιτολόγος: Μελίνα Τσαγκατάκη, Διαιτολόγος-Διατροφολόγος (Χαροκόπειο Πανεπιστήμιο, MSc Κλινική Διατροφή).

## Υπηρεσίες

{svc_lines}

## Πληροφορίες

- [Τιμές]({SITE}/pricing/): Τιμοκατάλογος και πακέτα
- [Συχνές ερωτήσεις]({SITE}/faq/): Απαντήσεις για υπηρεσίες, κρατήσεις και τιμές
- [Ποιοι είμαστε]({SITE}/about-us/): Η ομάδα και τα προσόντα της
- [Επικοινωνία]({SITE}/contact/): Διεύθυνση, χάρτης, τηλέφωνα
- [Gift cards]({SITE}/gift-cards/): Δωροκάρτες προπόνησης

## Optional

- [Instagram]({BUSINESS['social']['Instagram']})
- [Facebook]({BUSINESS['social']['Facebook']})
""")

print(f"OK – {len(pages)} σελίδες στο {OUT} ({'ΠΡΟΕΠΙΣΚΟΠΗΣΗ' if PREVIEW else 'τελικό'})")
