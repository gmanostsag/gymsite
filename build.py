#!/usr/bin/env python3
"""Γεννήτρια του βελτιωμένου (SEO + AI-ready) site του Training Station Fitness.

Τρέξε:  python3 build.py            -> γράφει τα HTML στο site/
        python3 build.py --final    -> χωρίς κίτρινες σημάνσεις προεπισκόπησης

Όλα τα στοιχεία που πρέπει να συμπληρώσεις είναι στο BUSINESS παρακάτω
(ωράριο, ΤΚ, Facebook Pixel). Όσα έχουν None εμφανίζονται κίτρινα στην προεπισκόπηση.
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
  body=[("p","Το ατομικό **Personal Training** δεν είναι απλώς μια προπόνηση – είναι μια εξατομικευμένη εμπειρία που δημιουργείται αποκλειστικά για τις **ανάγκες**, τους **στόχους** και τις **δυνατότητές σου**."),
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
  body=[("p","Ανακάλυψε τη δύναμη και την ευλυγισία σου με τα μαθήματα **Pilates Reformer**, την απόλυτη μέθοδο εκγύμνασης που προσφέρει εντυπωσιακά αποτελέσματα. Το κρεβάτι Reformer είναι ειδικά σχεδιασμένο για να υποστηρίζει κάθε κίνηση, μειώνοντας την καταπόνηση και επιτρέποντας την ασφαλή και σωστή ευθυγράμμιση του σώματος."),
   ("h2","Γιατί το Reformer είναι μοναδικό;"),
   ("ul",["Προσαρμόζεται απόλυτα στο επίπεδό σου, είτε είσαι αρχάριος είτε προχωρημένος.",
          "Προσφέρει **ενδυνάμωση ολόκληρου του σώματος**, με ιδιαίτερη έμφαση στον κορμό.",
          "Βοηθά στη **βελτίωση της στάσης του σώματος** και στην **ανακούφιση** από **μυοσκελετικούς πόνους**.",
          "Συνδυάζει **αντίσταση** και **ευλυγισία** με τη χρήση ελατηρίων, κάνοντας κάθε άσκηση αποτελεσματική και ευχάριστη."]),
   ("h2","Για ποιον είναι κατάλληλο;"),
   ("p","Για όποιον θέλει δυνατό κορμό, καλύτερη στάση σώματος και ευλυγισία: από αρχάριους και άτομα που κάθονται πολλές ώρες, μέχρι αθλητές που θέλουν συμπληρωματική προπόνηση. Αν έχεις πόνους στη μέση ή παλιό τραυματισμό, ενημέρωσέ μας στην αρχική αξιολόγηση ώστε να προσαρμόσουμε τις ασκήσεις.")],
  faq=[("Χρειάζομαι προηγούμενη εμπειρία στο Pilates;","Όχι. Το Reformer προσαρμόζεται στο επίπεδό σου και ο εκπαιδευτής σε καθοδηγεί από την πρώτη κίνηση."),
       ("Βοηθά το Pilates Reformer στον πόνο στη μέση;","Η ενδυνάμωση του κορμού και η βελτίωση της στάσης σώματος βοηθούν πολλούς ανθρώπους με μυοσκελετικούς πόνους. Για σοβαρό ή πρόσφατο τραυματισμό, συμβουλεύσου πρώτα τον γιατρό σου και δες και την υπηρεσία Recovery Training."),
       ("Τι να φορέσω;","Άνετα, εφαρμοστά ρούχα γυμναστικής και αντιολισθητικές κάλτσες.")]),
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
NAV = [("/services/", "Υπηρεσίες"), ("/about-us/", "Η ομάδα"), ("/faq/", "Ερωτήσεις"), ("/contact/", "Επικοινωνία")]

# Σύντομη, ανθρώπινη περιγραφή κάθε υπηρεσίας (σειρά εμφάνισης, μορφή, μία φράση)
SHORT = {
    "personal-training": (1, "Ατομικά", "Ένας προπονητής, μόνο για σένα."),
    "pilates": (2, "Ατομικά ή σε μικρή ομάδα", "Δυνατός κορμός, καλύτερη στάση σώματος."),
    "group-training": (3, "2–3 άτομα", "Με φίλους, χωρίς να χάνεται η εξατομίκευση."),
    "recovery-injuries": (4, "Ατομικά", "Ασφαλής επιστροφή μετά από τραυματισμό."),
    "army-security-forces-training": (5, "Ατομικά ή σε μικρή ομάδα", "Προετοιμασία για τις αθλητικές δοκιμασίες σωμάτων ασφαλείας."),
    "digital-coaching": (6, "Online", "Πρόγραμμα, βίντεο και καθοδήγηση από απόσταση."),
    "dietetics-and-nutrition": (7, "Δια ζώσης ή online", "Διατροφικό πλάνο από Διαιτολόγο."),
}
SERVICES.sort(key=lambda s: SHORT[s["slug"]][0])

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
            "hasMap": b["maps_url"],
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
        crumbs_html = f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'
    h1_html = h1_html.replace("{CRUMBS}", crumbs_html)

    cur = lambda h: ' aria-current="page"' if path.startswith(h) else ""
    nav = "".join(f'<li><a href="{h}"{cur(h)}>{esc(t)}</a></li>' for h, t in NAV)
    svc_links = "".join(f'<li><a href="/{s["slug"]}/">{esc(s["name"])}</a></li>' for s in SERVICES)
    social = " · ".join(f'<a href="{u}" rel="noopener" target="_blank">{esc(n)}</a>' for n, u in BUSINESS["social"].items())
    gb = BUSINESS["google_business"]
    social += (f' · <a href="{gb}" rel="noopener" target="_blank">Google</a>' if gb else f' · {todo("Google", "Link του Google Business Profile")}')
    pixel = f'<script>window.TSF_FB_PIXEL_ID="{BUSINESS["fb_pixel_id"]}";</script>' if BUSINESS["fb_pixel_id"] else ""
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1"
    preview_bar = ('<div class="preview-bar">Προεπισκόπηση · τα <span class="todo">κίτρινα</span> σημεία περιμένουν δικά σου στοιχεία</div>' if PREVIEW else "")
    b = BUSINESS

    doc = f"""<!doctype html>
<html lang="el">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Commissioner:wght@300;400;500;600&display=swap">
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
<header class="site"><div class="wrap">
 <a class="brand" href="/" aria-label="Training Station Fitness – Αρχική"><img src="/assets/img/logo.webp" width="120" height="56" alt="Training Station Fitness"></a>
 <button class="menu-btn" aria-expanded="false" aria-controls="menu">Μενού</button>
 <nav class="main" id="menu" aria-label="Κύριο μενού"><ul>{nav}<li><a class="book" href="/book-now/">Κράτηση</a></li></ul></nav>
</div></header>
<main id="main">
{h1_html}
{body}
</main>
<footer class="site"><div class="wrap">
 <div class="cols">
  <div><p class="small">Training Station Fitness</p><p>{address_line()}</p><p><a href="tel:{b['phone']}">{b['phone_disp']}</a> · <a href="tel:{b['mobile']}">{b['mobile_disp']}</a><br><a href="mailto:{b['email']}">{b['email']}</a></p></div>
  <div><p class="small">Υπηρεσίες</p><ul>{svc_links}</ul></div>
  <div><p class="small">Περισσότερα</p><ul><li><a href="/about-us/">Η ομάδα</a></li><li><a href="/faq/">Ερωτήσεις</a></li><li><a href="/gift-cards/">Gift cards</a></li><li><a href="/book-now/">Κράτηση</a></li><li><a href="/contact/">Επικοινωνία</a></li></ul></div>
 </div>
 <div class="legal"><span>{social}</span><span>© {datetime.date.today().year} {esc(b['legal_name'])} · Γ.Ε.ΜΗ {b['gemi']} · <a href="/conditions/">Όροι &amp; απόρρητο</a> · <a href="#" data-cookie-settings>Cookies</a></span></div>
</div></footer>
<div class="consent" role="dialog" aria-live="polite" aria-label="Cookies">
 <p>Χρησιμοποιούμε απαραίτητα cookies για να λειτουργεί το site και, αν συμφωνείς, cookies μέτρησης και διαφήμισης. <a href="/conditions/#cookies">Περισσότερα</a></p>
 <div class="consent-actions"><button class="reject">Μόνο απαραίτητα</button><button class="accept">Αποδοχή</button></div>
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

def faq_items(faqs):
    return "".join(f"<details><summary>{esc(q)}</summary><p>{md(a)}</p></details>" for q, a in faqs)

def faq_ld(faqs, url):
    return {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\*\*", "", a)}} for q, a in faqs]}

def ph(h1, lead=""):
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<section class="ph"><div class="wrap">{{CRUMBS}}<h1>{h1}</h1>{lead_html}</div></section>'

def svc_list(exclude=None):
    rows = "".join(f'<li><a href="/{s["slug"]}/"><span class="n">{esc(s["name"])}</span><span class="d">{esc(SHORT[s["slug"]][2])}</span><span class="f">{esc(SHORT[s["slug"]][1])}</span></a></li>'
                   for s in SERVICES if s["slug"] != exclude)
    return f'<ul class="list">{rows}</ul>'

def contact_block(title="Θα μας βρεις"):
    b = BUSINESS
    return f'''<section class="rule"><div class="wrap">
<h2>{esc(title)}</h2>
<div class="cols3">
 <div><p class="small">Διεύθυνση</p><p>{address_line()}<br><a href="{esc(b['maps_url'])}" target="_blank" rel="noopener">Οδηγίες στο Google Maps</a></p></div>
 <div><p class="small">Τηλέφωνο &amp; e-mail</p><p><a href="tel:{b['phone']}">{b['phone_disp']}</a><br><a href="tel:{b['mobile']}">{b['mobile_disp']}</a><br><a href="mailto:{b['email']}">{b['email']}</a></p></div>
 <div><p class="small">Ώρες</p><p>{hours_html()}</p></div>
</div>
<p class="cta-line"><a class="button" href="/book-now/">Κλείσε ραντεβού</a></p>
</div></section>'''

TESTIMONIALS = [
    ("Ο Μάνος είναι καταπληκτικός! Κάνουμε μαζί προπόνηση εδώ και 2 χρόνια (με χρόνια προβλήματα στη μέση μου) είναι δάσκαλος στο πώς θα προσεγγίσει την κάθε άσκηση! Έχω δει φανταστική διαφορά.", "Γιώργος"),
    ("Τα δυτικά απέκτησαν ένα ΣΩΣΤΟ personal studio. Ο Μάνος φανταστικός στη δουλειά του, πάντα εκεί να σε ενθαρρύνει σε κάθε σου στόχο.", "Ευαγγελία"),
    ("Επιτέλους βρήκα έναν γυμναστή καταρτισμένο, με επιστημονικές γνώσεις, που προσέχει τους ασκούμενούς του στο έπακρο!", "Μαρία"),
    ("Ο χώρος είναι πεντακάθαρος και με πολύ καλό εξοπλισμό. Κεντρικά και κοντά με ΜΜΜ. Αν και έχω θέμα με τη μέση μου λόγω μπάσκετ και φοβόμουν να ξεκινήσω, τελικά δικαιώθηκα.", "Τζαννής"),
    ("Καθαρός και ευχάριστος χώρος για προπόνηση! Ο Μάνος έμπειρος γνώστης και σε εμπνέει για προπόνηση, με ποικιλία προπονήσεων!", "Βασίλης"),
    ("The ultimate place for training! Manos, the instructor, is amazing and really helped me to regain my confidence and shape in zero time!", "Panayiotis"),
]

def quotes(n=3):
    q = "".join(f'<figure><blockquote>{esc(t)}</blockquote><figcaption>{esc(a)}</figcaption></figure>' for t, a in TESTIMONIALS[:n])
    gb = BUSINESS["google_business"]
    link = f'<p class="more"><a href="{gb}" target="_blank" rel="noopener">Όλες οι κριτικές στο Google</a></p>' if gb else f'<p class="more">{todo("Όλες οι κριτικές στο Google (link)", "Link του Google Business Profile")}</p>'
    return f'<section class="rule"><div class="wrap"><h2>Τι λένε για εμάς</h2><div class="quotes">{q}</div>{link}</div></section>'

# ---------------------------------------------------------------- σελίδες
pages = []

home_faq = [
    ("Πού βρίσκεται το Training Station Fitness;", "Στην οδό Παρασκευοπούλου 47, στην πλατεία Μπουρναζίου στο Περιστέρι (Δυτική Αθήνα)."),
    ("Τι υπηρεσίες προσφέρετε;", "Ατομικό personal training, small group training για 2–3 άτομα, Pilates Reformer, άσκηση για αποκατάσταση τραυματισμών, προετοιμασία για τα αθλήματα Αστυνομίας και Στρατού, online coaching και διατροφή με Διαιτολόγο."),
    ("Χρειάζεται ραντεβού;", "Ναι, όλες οι συνεδρίες γίνονται κατόπιν ραντεβού. Κλείνεις online από τη σελίδα «Κράτηση» ή στο 210 576 7892."),
    ("Υπάρχει δωρεάν δοκιμαστική συνάντηση;", "Ναι, μπορείς να κλείσεις μια δωρεάν ενημερωτική συνάντηση γνωριμίας για να συζητήσουμε τους στόχους σου."),
]

home_hero = f'''<section class="hero"><div class="wrap">
<p class="small">Training Station Fitness · Πλατεία Μπουρναζίου</p>
<h1>Η γυμναστική σου μόλις απέκτησε ενδιαφέρον.</h1>
<p class="lead">Προσωπική προπόνηση, Pilates Reformer και διατροφή, με Καθηγητές Φυσικής Αγωγής και Διαιτολόγο.</p>
<p class="cta-line"><a class="button" href="/book-now/">Κλείσε μια δωρεάν γνωριμία</a><a class="arrow" href="/services/">Δες τις υπηρεσίες</a></p>
</div>
<div class="wrap"><img class="hero-img" src="/assets/img/eleuthera-vari-bournazi.webp" width="900" height="720" alt="Rack, ιμάντες TRX και μπάρα στον χώρο ελεύθερων βαρών του Training Station Fitness" fetchpriority="high"></div>
</section>'''

home_body = f'''
<section class="rule"><div class="wrap two">
<div><h2>Ο χώρος</h2></div>
<div class="text">
<p>Στον πλήρως εξοπλισμένο μας χώρο στην πλατεία Μπουρναζίου κάνεις ατομικές προπονήσεις, ομαδικές έως 3 άτομα, Pilates Reformer, online προπονητική και άσκηση για αποκατάσταση τραυματισμών.</p>
<p>Ξεκινάμε με προπονητική και διατροφική αξιολόγηση και μελετάμε με λεπτομέρεια κάθε σου ανάγκη, για να φτιάξουμε το καταλληλότερο πρόγραμμα προπόνησης και διατροφής.</p>
</div></div>
<div class="wrap pair"><img src="/assets/img/eisodos-training-station.webp" width="900" height="720" alt="Η είσοδος του Training Station Fitness με το λογότυπο στον καθρέφτη" loading="lazy"><img src="/assets/img/aerobia-mixanimata-bournazi.webp" width="900" height="720" alt="Διάδρομος, αλτήρες και πολυόργανο τροχαλίας" loading="lazy"></div>
</section>
<section class="rule"><div class="wrap two">
<div><h2>Υπηρεσίες</h2></div>
<div>{svc_list()}</div>
</div></section>
<section class="rule"><div class="wrap two">
<div><img class="portrait" src="/assets/img/manos-tsagkatakis.webp" width="768" height="768" alt="Μάνος Τσαγκατάκης, Καθηγητής Φυσικής Αγωγής" loading="lazy"></div>
<div class="text">
<h2>Μάνος Τσαγκατάκης</h2>
<p>Καθηγητής Φυσικής Αγωγής, απόφοιτος του ΤΕΦΑΑ του Δημοκρίτειου Πανεπιστημίου Θράκης και μεταπτυχιακός φοιτητής του Χαροκόπειου στη Διατροφή &amp; Άσκηση. Από το 2020 διδάσκει Σωματική Αγωγή στη Σχολή Αξιωματικών της Ελληνικής Αστυνομίας.</p>
<p>«Η εμπειρία μου στις εξατομικευμένες προπονήσεις με ώθησε να δημιουργήσω έναν χώρο όπου ο καθένας, με σωστή καθοδήγηση, επιστημονική γνώση και ασφάλεια, πετυχαίνει τον στόχο του.»</p>
<p><a class="arrow" href="/about-us/">Η ομάδα</a></p>
</div></div></section>
{quotes(3)}
{contact_block()}
'''
pages.append(page("/", "Training Station Fitness",
    "Personal training studio στην πλατεία Μπουρναζίου, στο Περιστέρι. Ατομική προπόνηση, ομάδες έως 3 ατόμων, Pilates Reformer και διατροφή, με Καθηγητές Φυσικής Αγωγής και Διαιτολόγο.",
    home_hero, home_body, extra_ld=[faq_ld(home_faq, SITE + "/")]))

# Σελίδες υπηρεσιών
for s in SERVICES:
    url = f"{SITE}/{s['slug']}/"
    order, fmt, tag = SHORT[s["slug"]]
    svc_ld = {"@type": "Service", "@id": url + "#service", "name": s["name"], "serviceType": s["stype"], "url": url,
              "description": s["desc"], "provider": {"@id": SITE + "/#gym"},
              "areaServed": {"@type": "City", "name": "Περιστέρι"} if not s.get("online") else [{"@type": "City", "name": "Περιστέρι"}, {"@type": "Country", "name": "Ελλάδα"}]}
    head = ph(esc(s["name"]), esc(tag))
    body = f'''<section><div class="wrap two">
<div><p class="small">{esc(fmt)}</p></div>
<div class="text prose">{blocks(s["body"])}
<p class="cta-line"><a class="button" href="/book-now/">Κλείσε ραντεβού</a><a class="arrow" href="tel:{BUSINESS['phone']}">{BUSINESS['phone_disp']}</a></p>
</div></div></section>
<section class="rule"><div class="wrap two"><div><h2>Ερωτήσεις</h2></div><div class="faq">{faq_items(s["faq"])}</div></div></section>
<section class="rule"><div class="wrap two"><div><h2>Άλλες υπηρεσίες</h2></div><div>{svc_list(exclude=s["slug"])}</div></div></section>
{contact_block()}'''
    pages.append(page(f"/{s['slug']}/", f"{s['name']} | Training Station Fitness", s["desc"], head, body,
                      crumbs=[("Υπηρεσίες", "/services/"), (s["name"], f"/{s['slug']}/")],
                      extra_ld=[svc_ld, faq_ld(s["faq"], url)]))

# Υπηρεσίες
pages.append(page("/services/", "Υπηρεσίες | Training Station Fitness",
    "Personal training, Pilates Reformer, group 2–3 ατόμων, online coaching, αποκατάσταση τραυματισμών, Forces training και διατροφή στο Training Station Fitness, Περιστέρι.",
    ph("Υπηρεσίες", "Κάθε πρόγραμμα ξεκινά με αξιολόγηση και σχεδιάζεται από Καθηγητές Φυσικής Αγωγής γύρω από τους δικούς σου στόχους."),
    f'''<section><div class="wrap">{svc_list()}</div></section>
<section class="rule"><div class="wrap two"><div><h2>Πώς ξεκινάς</h2></div><div class="text prose"><ol>
<li><strong>Δωρεάν γνωριμία.</strong> Μια σύντομη συνάντηση για να ακούσουμε τι θέλεις να πετύχεις.</li>
<li><strong>Αξιολόγηση.</strong> Προπονητική και διατροφική, με προσοχή σε τραυματισμούς και ιστορικό.</li>
<li><strong>Το πρόγραμμά σου.</strong> Ατομικά ή σε ομάδα έως 3 ατόμων.</li>
<li><strong>Πρόοδος.</strong> Παρακολουθούμε κάθε βήμα και προσαρμόζουμε το πρόγραμμα.</li></ol>
<p class="cta-line"><a class="button" href="/book-now/">Κλείσε μια δωρεάν γνωριμία</a></p></div></div></section>''',
    crumbs=[("Υπηρεσίες", "/services/")],
    extra_ld=[{"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/{s['slug']}/", "name": s["name"]} for i, s in enumerate(SERVICES)]}]))

# FAQ
all_faq = home_faq + [q for s in SERVICES for q in s["faq"]]
seen, uniq = set(), []
for q in all_faq:
    if q[0] not in seen: seen.add(q[0]); uniq.append(q)
faq_sections = f'<section><div class="wrap two"><div><h2>Γενικά</h2></div><div class="faq">{faq_items(home_faq)}</div></div></section>' + "".join(
    f'<section class="rule"><div class="wrap two"><div><h2>{esc(s["name"])}</h2></div><div class="faq">{faq_items(s["faq"])}</div></div></section>' for s in SERVICES)
pages.append(page("/faq/", "Ερωτήσεις | Training Station Fitness",
    "Απαντήσεις για personal training, Pilates Reformer, αποκατάσταση τραυματισμών, αθλήματα Αστυνομίας, διατροφή και κρατήσεις στο Training Station Fitness.",
    ph("Ερωτήσεις", f'Δεν βρίσκεις αυτό που ψάχνεις; Πάρε μας στο <a href="tel:{BUSINESS["phone"]}">{BUSINESS["phone_disp"]}</a>.'),
    faq_sections, crumbs=[("Ερωτήσεις", "/faq/")], extra_ld=[faq_ld(uniq, SITE + "/faq/")]))

# Η ομάδα
pages.append(page("/about-us/", "Η ομάδα | Training Station Fitness",
    "Η ομάδα του Training Station Fitness στο Περιστέρι: Μάνος Τσαγκατάκης, Καθηγητής Φυσικής Αγωγής (ΤΕΦΑΑ, ΣΑΕΑ) και Μελίνα Τσαγκατάκη, Διαιτολόγος-Διατροφολόγος.",
    ph("Η ομάδα", "Επιστημονική γνώση, σωστή καθοδήγηση και ασφάλεια."),
    f'''<section><div class="wrap people">
<article><img src="/assets/img/manos-tsagkatakis.webp" width="768" height="768" alt="Μάνος Τσαγκατάκης, Καθηγητής Φυσικής Αγωγής" loading="lazy">
<h2>Μάνος Τσαγκατάκης</h2><p class="small">Καθηγητής Φυσικής Αγωγής · Ιδρυτής</p>
<div class="prose"><p>Απόφοιτος του Τμήματος Φυσικής Αγωγής &amp; Αθλητισμού (ΤΕΦΑΑ) του Δημοκρίτειου Πανεπιστημίου Θράκης, με ειδικότητα στην κολύμβηση, και μεταπτυχιακός φοιτητής του Χαροκόπειου Πανεπιστημίου στην Εφαρμοσμένη Διατροφή &amp; Διατροφολογία, με κατεύθυνση Διατροφή &amp; Άσκηση. Από το 2020 διδάσκει Σωματική Αγωγή στη Σχολή Αξιωματικών της Ελληνικής Αστυνομίας (ΣΑΕΑ).</p>
<p>«Η πολυετής εμπειρία μου στον χώρο της άσκησης και των εξατομικευμένων προπονήσεων με ώθησε να δημιουργήσω έναν χώρο όπου ο κάθε ασκούμενος, με σωστή καθοδήγηση, επιστημονική γνώση και ασφάλεια, πετυχαίνει κάθε στόχο.»</p></div></article>
<article><img src="/assets/img/melina-tsagkataki.webp" width="900" height="900" alt="Μελίνα Τσαγκατάκη, Διαιτολόγος-Διατροφολόγος" loading="lazy">
<h2>Μελίνα Τσαγκατάκη</h2><p class="small">Διαιτολόγος · Διατροφολόγος</p>
<div class="prose"><p>Πτυχιούχος Διαιτολόγος-Διατροφολόγος του Χαροκόπειου Πανεπιστημίου, με μεταπτυχιακή εξειδίκευση στην Εφαρμοσμένη Διαιτολογία και Διατροφή, κατεύθυνση Κλινική Διατροφή. Υπεύθυνη για τις <a href="/dietetics-and-nutrition/">διατροφικές υπηρεσίες</a>, στον χώρο μας ή online.</p></div></article>
</div></section>
<section class="rule"><div class="wrap two"><div><h2>Ο χώρος</h2></div><div class="text"><p>Ατομικές προπονήσεις, ομάδες έως 3 ατόμων, Pilates Reformer, online προπονητική και άσκηση για αποκατάσταση τραυματισμών, στην πλατεία Μπουρναζίου.</p></div></div>
<div class="wrap trio"><img src="/assets/img/eisodos-training-station.webp" width="900" height="720" alt="Είσοδος του Training Station Fitness" loading="lazy"><img src="/assets/img/eleuthera-vari-bournazi.webp" width="900" height="720" alt="Χώρος ελεύθερων βαρών με rack και TRX" loading="lazy"><img src="/assets/img/aerobia-mixanimata-bournazi.webp" width="900" height="720" alt="Διάδρομος και αλτήρες" loading="lazy"></div></section>
{quotes(6)}{contact_block()}''',
    crumbs=[("Η ομάδα", "/about-us/")], og_image="manos-tsagkatakis.webp",
    extra_ld=people_nodes() + [{"@type": "AboutPage", "@id": SITE + "/about-us/#about", "url": SITE + "/about-us/", "mainEntity": {"@id": SITE + "/#gym"}}]))

# Επικοινωνία
pages.append(page("/contact/", "Επικοινωνία | Training Station Fitness",
    "Επικοινώνησε με το Training Station Fitness: Παρασκευοπούλου 47, πλατεία Μπουρναζίου, Περιστέρι. Τηλ. 210 576 7892 · 694 619 4809 · info@trainingstationfitness.com.",
    ph("Επικοινωνία", "Συνεδρίες και ενημέρωση γίνονται κατόπιν ραντεβού."),
    f'''<section><div class="wrap cols3">
 <div><p class="small">Διεύθυνση</p><p>{address_line()}<br><a href="{esc(BUSINESS['maps_url'])}" target="_blank" rel="noopener">Οδηγίες στο Google Maps</a></p><p>Κοντά σε στάσεις λεωφορείων. {todo("Μετρό, στάσεις, στάθμευση","Οδηγίες πρόσβασης")}</p></div>
 <div><p class="small">Τηλέφωνο &amp; e-mail</p><p><a href="tel:{BUSINESS['phone']}">{BUSINESS['phone_disp']}</a><br><a href="tel:{BUSINESS['mobile']}">{BUSINESS['mobile_disp']}</a><br><a href="mailto:{BUSINESS['email']}">{BUSINESS['email']}</a></p></div>
 <div><p class="small">Ώρες</p><p>{hours_html()}</p></div>
</div></section>
<section class="rule"><div class="wrap two"><div><h2>Στείλε μήνυμα</h2></div>
<form class="form" method="post" action="#" onsubmit="alert('Προεπισκόπηση: εδώ συνδέεται η φόρμα του WordPress (π.χ. Contact Form 7).');return false">
<label for="f-name">Ονοματεπώνυμο</label><input id="f-name" name="name" required autocomplete="name">
<label for="f-tel">Τηλέφωνο</label><input id="f-tel" name="tel" type="tel" required autocomplete="tel">
<label for="f-mail">E-mail</label><input id="f-mail" name="email" type="email" required autocomplete="email">
<label for="f-msg">Μήνυμα</label><textarea id="f-msg" name="msg" rows="5" required></textarea>
<label class="check"><input id="f-ok" type="checkbox" required> Συμφωνώ με την <a href="/conditions/">πολιτική απορρήτου</a>.</label>
<p><button class="button" type="submit">Αποστολή</button></p></form></div></section>''',
    crumbs=[("Επικοινωνία", "/contact/")],
    extra_ld=[{"@type": "ContactPage", "@id": SITE + "/contact/#contact", "url": SITE + "/contact/", "mainEntity": {"@id": SITE + "/#gym"}}]))

# Κράτηση
pages.append(page("/book-now/", "Κράτηση | Training Station Fitness",
    "Κλείσε online ραντεβού για personal training, group 2–3 ατόμων, digital coaching, διατροφή ή δωρεάν συνάντηση γνωριμίας στο Training Station Fitness, Περιστέρι.",
    ph("Κράτηση", f'Διάλεξε υπηρεσία, ημέρα και ώρα. Αν δεν βρίσκεις διαθεσιμότητα, κάλεσε στο <a href="tel:{BUSINESS["phone"]}">{BUSINESS["phone_disp"]}</a>.'),
    f'''<section><div class="wrap"><div class="placeholder"><p>Εδώ εμφανίζεται το σύστημα κρατήσεων (Booknetic).</p><p class="small">Στην προεπισκόπηση δεν φορτώνει· στο WordPress μένει όπως είναι.</p></div></div></section>
<section class="rule"><div class="wrap two"><div><h2>Τι μπορείς να κλείσεις</h2></div><div class="text prose"><ul>
<li>Personal Training, ατομικά</li><li>Small Group Training, 2–3 άτομα</li><li>Digital Coaching</li><li>Διατροφή με τη Διαιτολόγο μας, και online</li><li>Δωρεάν συνάντηση γνωριμίας</li></ul>
<p>Μετά την κράτηση παίρνεις επιβεβαίωση με e-mail ή SMS.</p></div></div></section>''',
    crumbs=[("Κράτηση", "/book-now/")]))

# Gift cards
pages.append(page("/gift-cards/", "Gift cards | Training Station Fitness",
    "Χάρισε προπόνηση: δωροκάρτες για personal training, Pilates Reformer και διατροφή στο Training Station Fitness, Περιστέρι.",
    ph("Gift cards", "Χάρισε προπόνηση σε κάποιον που αγαπάς."),
    f'''<section><div class="wrap two">
<div><img src="/assets/img/gift-card.webp" width="900" height="638" alt="Δωροκάρτα Training Station Fitness" loading="lazy"></div>
<div class="text prose"><p>Μια δωροκάρτα για συνεδρίες personal training, Pilates Reformer ή διατροφής. Ιδανική για γενέθλια, γιορτές ή για κάποιον που θέλει να ξεκινήσει με σωστή καθοδήγηση.</p>
<ol><li>Επικοινώνησε μαζί μας στο <a href="tel:+302105767892">210 576 7892</a> ή στο <a href="mailto:info@trainingstationfitness.com">info@trainingstationfitness.com</a>.</li><li>Διαλέγουμε μαζί την υπηρεσία.</li><li>Παραλαμβάνεις τη δωροκάρτα, έντυπη ή ψηφιακή, με το όνομα του δικού σου ανθρώπου.</li><li>Ο κάτοχος κλείνει ραντεβού όποτε τον βολεύει.</li></ol>
<p>Ισχύς: {todo("π.χ. 6 μήνες", "Πόσο ισχύει η δωροκάρτα;")}</p>
<p class="cta-line"><a class="button" href="/contact/">Επικοινωνία</a></p></div>
</div></section>''',
    crumbs=[("Gift cards", "/gift-cards/")], og_image="gift-card.webp"))

# Όροι
pages.append(page("/conditions/", "Όροι χρήσης | Training Station Fitness",
    "Όροι χρήσης, πολιτική απορρήτου και cookies του trainingstationfitness.com (ΕΜΜΑΝΟΥΗΛ ΤΣΑΓΚΑΤΑΚΗΣ – Training Station Fitness).",
    ph("Όροι χρήσης &amp; απόρρητο"),
    f'''<section><div class="wrap"><div class="prose">
<p>Η ιστοσελίδα trainingstationfitness.com ανήκει στην επιχείρηση «{esc(BUSINESS['legal_name'])}» με διακριτικό τίτλο «TRAINING STATION FITNESS» (Αρ. Γ.Ε.ΜΗ {BUSINESS['gemi']}), με έδρα την οδό Παρασκευοπούλου 47, Περιστέρι.</p>
<p>{todo("Εδώ μπαίνει αυτούσιο το πλήρες κείμενο όρων από το υπάρχον site.", "Κείμενο όρων")}</p>
<h2 id="cookies">Cookies</h2>
<p>Τα απαραίτητα cookies χρειάζονται για τη λειτουργία του site. Cookies μέτρησης (Google Analytics) και διαφήμισης (Meta Pixel) ενεργοποιούνται μόνο αν δώσεις συγκατάθεση, και μπορείς να την ανακαλέσεις οποιαδήποτε στιγμή από τις <a href="#" data-cookie-settings>ρυθμίσεις cookies</a>.</p>
</div></div></section>''',
    crumbs=[("Όροι χρήσης", "/conditions/")]))

# 404
page("/404.html", "Η σελίδα δεν βρέθηκε | Training Station Fitness", "Η σελίδα που ζητήσατε δεν βρέθηκε.",
     ph("Η σελίδα δεν βρέθηκε", 'Γύρνα στην <a href="/">αρχική</a> ή διάλεξε μια υπηρεσία.'),
     f'<section><div class="wrap">{svc_list()}</div></section>', noindex=True)

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

- [Συχνές ερωτήσεις]({SITE}/faq/): Απαντήσεις για υπηρεσίες και κρατήσεις
- [Ποιοι είμαστε]({SITE}/about-us/): Η ομάδα και τα προσόντα της
- [Επικοινωνία]({SITE}/contact/): Διεύθυνση, χάρτης, τηλέφωνα
- [Gift cards]({SITE}/gift-cards/): Δωροκάρτες προπόνησης

## Optional

- [Instagram]({BUSINESS['social']['Instagram']})
- [Facebook]({BUSINESS['social']['Facebook']})
""")

print(f"OK – {len(pages)} σελίδες στο {OUT} ({'ΠΡΟΕΠΙΣΚΟΠΗΣΗ' if PREVIEW else 'τελικό'})")
