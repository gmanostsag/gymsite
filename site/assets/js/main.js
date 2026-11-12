// Ελληνικά κεφαλαία χωρίς τόνους: όπου η μορφοποίηση κάνει το κείμενο κεφαλαίο,
// αφαιρούμε τους τόνους (και βάζουμε διαλυτικά όπου χρειάζεται: ρολόι -> ΡΟΛΟΪ).
// Στον κώδικα HTML το κείμενο μένει σωστά τονισμένο για τις μηχανές αναζήτησης.
(function(){
  document.documentElement.lang='el';
  function strip(t){
    return t.normalize('NFD')
      .replace(/([αεοΑΕΟ])\u0301([ιυ])(?!\u0308)/g,function(m,a,b){return a+b+'\u0308'})
      .replace(/\u0301/g,'').normalize('NFC');
  }
  function run(root){
    var w=document.createTreeWalker(root||document.body,NodeFilter.SHOW_TEXT,null),n,cache=new Map();
    while((n=w.nextNode())){
      var el=n.parentElement; if(!el||!/[\u0300-\u036f\u0386-\u03ce\u1f00-\u1fff]/.test(n.nodeValue.normalize('NFD'))) continue;
      var up=cache.get(el); if(up===undefined){up=getComputedStyle(el).textTransform==='uppercase';cache.set(el,up)}
      if(up){var v=strip(n.nodeValue); if(v!==n.nodeValue) n.nodeValue=v}
    }
  }
  run(); window.tsfCaps=run;
})();

// Μενού κινητού
(function(){
  var b=document.querySelector('.menu-btn'), n=document.querySelector('nav.main');
  if(b&&n){b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)})}
})();

// Χάρτης: φορτώνει μόνο όταν το ζητήσει ο επισκέπτης (ταχύτητα + GDPR)
document.querySelectorAll('.map-facade button').forEach(function(btn){
  btn.addEventListener('click',function(){
    var f=document.createElement('iframe');
    f.src=btn.dataset.src; f.title='Χάρτης: Training Station Fitness, Παρασκευοπούλου 47, Περιστέρι';
    f.loading='lazy'; f.referrerPolicy='no-referrer-when-downgrade';
    var box=btn.parentNode; box.innerHTML=''; box.style.background='none'; box.appendChild(f);
  });
});

// Cookies: Google Consent Mode v2. Τίποτα δεν φορτώνεται πριν τη συγκατάθεση.
(function(){
  var KEY='tsf-consent', box=document.querySelector('.consent');
  function get(){try{return localStorage.getItem(KEY)}catch(e){return null}}
  function set(v){try{localStorage.setItem(KEY,v)}catch(e){}}
  function grant(){
    if(window.gtag){gtag('consent','update',{ad_storage:'granted',analytics_storage:'granted',ad_user_data:'granted',ad_personalization:'granted'})}
    var id=window.TSF_FB_PIXEL_ID; // ορίζεται στο <head> μόνο όταν υπάρχει Pixel
    if(id&&!window.fbq){
      !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
      fbq('init',id); fbq('track','PageView');
    }
  }
  var c=get();
  if(c==='all'){grant()} else if(!c&&box){box.classList.add('show')}
  if(box){
    box.querySelector('.accept').addEventListener('click',function(){set('all');box.classList.remove('show');grant()});
    box.querySelector('.reject').addEventListener('click',function(){set('necessary');box.classList.remove('show')});
  }
  document.querySelectorAll('[data-cookie-settings]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();box&&box.classList.add('show')})});
})();

// Ρολόι του πίνακα αναχωρήσεων (ώρα Αθήνας)
(function(){
  var els=document.querySelectorAll('[data-clock]'); if(!els.length) return;
  function tick(){
    var t; try{t=new Intl.DateTimeFormat('el-GR',{hour:'2-digit',minute:'2-digit',hour12:false,timeZone:'Europe/Athens'}).format(new Date())}catch(e){var d=new Date();t=('0'+d.getHours()).slice(-2)+':'+('0'+d.getMinutes()).slice(-2)}
    els.forEach(function(el){el.textContent=t});
  }
  tick(); setInterval(tick,15000);
})();
