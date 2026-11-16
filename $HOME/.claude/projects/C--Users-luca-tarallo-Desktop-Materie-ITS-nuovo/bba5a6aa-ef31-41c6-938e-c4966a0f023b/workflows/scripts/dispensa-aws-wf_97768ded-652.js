export const meta = {
  name: 'dispensa-aws',
  description: 'Dispensa Obsidian di AWS: moduli 01-07 scritti da tre autori e revisione di completezza sulle fonti',
  phases: [
    { title: 'Stesura', detail: 'tre autori in parallelo sui moduli 01-07' },
    { title: 'Revisione', detail: 'confronto con le fonti: zero omissioni e formato' },
  ],
}

const REPO = 'C:\\Users\\luca.tarallo\\Desktop\\Materie_ITS_nuovo'
const SRC = REPO + '\\Amazon Web Services (AWS)'
const TXT = 'C:\\Users\\LUCA~1.TAR\\AppData\\Local\\Temp\\7\\claude\\c13e0dd8725d7e31\\bba5a6aa-ef31-41c6-938e-c4966a0f023b\\scratchpad\\aws'
const OUT = REPO + '\\_Dispensa_Completa\\AWS'

const NOMI = {
  '00': '00 - Indice AWS (MOC)',
  '01': '01 - Fondamenti di networking',
  '02': '02 - Reti Wi-Fi e VPN',
  '03': '03 - Simulazione dei protocolli di rete',
  '04': '04 - Fondamenti di cloud computing',
  '05': '05 - Classificazione dei servizi cloud',
  '06': '06 - Immagini, container e registri',
  '07': '07 - Dockerfile, networking e Kubernetes',
  '99': '99 - Glossario, Comandi e Cheat Sheet AWS',
}
const ROOT_MOC = '00 - Indice Generale ITS (MOC)'
const ORDINE = ['00', '01', '02', '03', '04', '05', '06', '07', '99']
const MODULI_NUM = ['01', '02', '03', '04', '05', '06', '07']

function nav(n) {
  const i = ORDINE.indexOf(n)
  if (n === '01') return '← [[' + NOMI['00'] + '|Indice AWS]] | [[' + NOMI['02'] + ']] →'
  return '← [[' + NOMI[ORDINE[i - 1]] + ']] | [[' + NOMI['00'] + '|Indice AWS]] | [[' + NOMI[ORDINE[i + 1]] + ']] →'
}

const MODULI = {
  '01': {
    titolo: 'Fondamenti di networking',
    lezione: 'lecture_01_fondamenti_networking_it',
    lab: '06-10-2026\\lab01-networking',
    labNote: 'consegna01.md, configurazione.txt, dns.txt, percorso.txt, ping-gateway.txt, ping-internet.txt',
    docs: 'docs\\aws\\2026-10-06-lab01-networking.md',
    extra: 'Per il contesto puoi leggere la lezione 00 (struttura del corso), testo in ' + TXT + '\\lecture_00_struttura_corso.txt, ma non riportarla: la tratta l\'indice della materia.',
  },
  '02': {
    titolo: 'Reti Wi-Fi e VPN',
    lezione: 'lecture_02_reti_wifi_vpn_it',
    lab: '09-10-2026\\lab02-wifi-vpn',
    labNote: 'caso-vpn-sintetico.md, configurazione-attuale.txt, configurazione-senza-vpn.txt, consegna02.md, percorso-senza-vpn.txt, schema-wifi.md, wifi.txt',
    docs: 'docs\\aws\\2026-10-09-lab02-wifi-vpn.md',
  },
  '03': {
    titolo: 'Simulazione dei protocolli di rete',
    lezione: 'lecture_03_simulazione_protocolli_rete_it',
    lab: '14-10-2026\\lab03-protocolli',
    labNote: 'consegna03.md, la sottocartella evidenze con 13 file .txt, sito\\messaggio.txt; la sottocartella sito-vuoto è vuota',
    docs: 'docs\\aws\\2026-10-14-lab03-protocolli-http-tcp.md',
  },
  '04': {
    titolo: 'Fondamenti di cloud computing',
    lezione: 'lecture_04_fondamenti_cloud_computing_it',
    lab: '15-10-2026\\lab04-cloud',
    labNote: 'consegna04.md e i file rapporto04.txt nelle sottocartelle originale-v1, originale-v2, scaricato-v1, scaricato-v2, ripristinato; la sottocartella evidenze è vuota',
    docs: 'docs\\aws\\2026-10-15-lab04-s3-storage.md',
    extra: 'Il PDF ' + SRC + '\\doc\\AWS - Introduzione e utilizzo.pdf non ha testo estraibile (contiene solo immagini): aprilo con il tool Read usando il parametro pages (al massimo 20 pagine per chiamata: prova "1-20", poi "21-40" e così via finché ci sono pagine) e leggilo come immagini. Integra i suoi contenuti nel modulo 04 o 05 dove sono pertinenti e, nel report, riassumi cosa contiene e dove lo hai usato.',
  },
  '05': {
    titolo: 'Classificazione dei servizi cloud',
    lezione: 'lecture_05_classificazione_servizi_cloud_it',
    lab: '22-10-2026\\lab05-servizi',
    labNote: 'architettura05.md, consegna05.md; la sottocartella evidenze è vuota',
    docs: 'docs\\aws\\2026-10-22-lab05-servizi-cloud.md',
  },
  '06': {
    titolo: 'Immagini, container e registri',
    lezione: 'lecture_06_immagini_container_registri_it',
    lab: '29-10-2026\\lab06-consegna',
    labNote: 'cosegna06.md (il nome del file ha un refuso; contiene l\'ID dell\'account AWS nell\'URI di ECR: mascheralo con <ACCOUNT_ID>)',
    docs: 'docs\\aws\\2026-10-29-lab06-container-to-aws.md',
  },
  '07': {
    titolo: 'Dockerfile, networking e Kubernetes',
    lezione: 'lecture_07_dockerfile_networking_kubernetes_it',
    lab: '02-11-2026\\lab07-windows',
    labNote: 'Dockerfile, .dockerignore, app.py, relazione_finale_lab_07.md; consegna07.md è vuoto (0 byte)',
    docs: 'docs\\aws\\2026-11-02-lab07-docker-k3s-officina-ticket.md',
  },
}

function fonti(n) {
  const m = MODULI[n]
  const righe = [
    '### ' + NOMI[n],
    '- File da creare: ' + OUT + '\\' + NOMI[n] + '.md',
    '- Titolo H1: # ' + m.titolo,
    '- Frontmatter: modulo: "' + n + '"',
    '- Barra di navigazione (in alto e, identica, in fondo): ' + nav(n),
    '- Lezione: ' + SRC + '\\doc\\' + m.lezione + '.pdf; testo già estratto in UTF-8 (slide numerate "N / totale") in ' + TXT + '\\' + m.lezione + '.txt',
    '- Laboratorio: cartella ' + SRC + '\\' + m.lab + ' (' + m.labNote + '). Leggi tutti i file.',
    '- Documentazione secondaria, scritta in precedenza: ' + REPO + '\\' + m.docs + ' (usala come aiuto, verificando ogni affermazione sugli originali)',
  ]
  if (m.extra) righe.push('- ' + m.extra)
  return righe.join('\n')
}

const ELENCO = [ROOT_MOC].concat(ORDINE.map(n => NOMI[n])).join(' · ')

const STYLE_COMUNE = `REGOLE DELLA DISPENSA (valgono per ogni file: seguile alla lettera)

Contenuto
- Lingua: italiano, tono discorsivo e tecnico. Spiega ogni acronimo alla prima occorrenza nel file.
- Fedeltà: basati solo sul materiale indicato. Non introdurre argomenti che le fonti non trattano; puoi aggiungere il minimo di contesto necessario a capire un passaggio dato per scontato, mai argomenti nuovi. Se un dettaglio non si ricava dalle fonti, scrivi *da verificare*.
- Espansione: trasforma appunti telegrafici, tabelle delle slide e schemi in spiegazioni complete, comprensibili a distanza di mesi senza le slide. Dove serve segui la progressione Intuizione → Definizione → Come funziona → Esempio.
- Zero omissioni: conserva tutte le definizioni, tabelle, comandi, parametri, protocolli, porte, output, errori comuni, best practice, mini-exercises e link suggeriti presenti nelle fonti.
- Laboratori: per ogni comando o blocco di configurazione indica i prerequisiti, cosa fa (opzione per opzione), il risultato atteso e come leggere l'output reale preso dai file di evidenza; spiega perché il passo serve all'obiettivo del lab. Se nella consegna dello studente trovi un'affermazione errata o imprecisa, riportala e correggila in un callout warning.
- Dati sensibili: maschera l'ID dell'account AWS (<ACCOUNT_ID>), gli indirizzi MAC (XX-XX-XX-XX-XX-XX), gli IP pubblici assegnati alla connessione dello studente, i nomi host e i nomi utente locali, chiavi, token e password. Lascia invariati gli IP privati (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16), gli indirizzi di servizi pubblici noti (es. 8.8.8.8, 1.1.1.1) e i domini pubblici.

Formato Obsidian
- Salva solo nella cartella ${OUT}, con i nomi esatti indicati ed estensione .md. Non modificare nient'altro e non usare git.
- Frontmatter YAML in testa al file, esattamente così (cambia solo il numero del modulo):
---
tags: [dispensa, its, aws]
modulo: "01"
stato: da-ripassare
---
- Subito dopo il frontmatter va la barra di navigazione indicata per il file; la stessa riga, identica, chiude il file.
- Callout ammessi, sempre con un titolo esplicito dopo il tipo:
  > [!abstract] Obiettivi e sintesi  (in apertura di ogni file)
  > [!important] Concetto chiave — <nome>  (definizioni, regole, teoria fondamentale)
  > [!example] Laboratorio — <titolo>  oppure  > [!example] Caso pratico — <titolo>  (esercizi svolti, comandi, configurazioni commentate)
  > [!warning] Attenzione — <tema>  (errori frequenti, troubleshooting, insidie d'esame, caveat tecnici)
  > [!success]- Risposte  (solo per le risposte alle domande di richiamo, pieghevole)
  Il callout [!question] è riservato all'indice della materia: non usarlo nei moduli.
  Un blocco di codice dentro un callout va prefissato con "> " su ogni riga.
- Blocchi di codice sempre con il linguaggio: powershell (comandi Windows), bash (Linux, EC2, shell), dockerfile, yaml, python, json, http (richieste e risposte HTTP), text (output e file di testo), mermaid (diagrammi).
- Tabelle Markdown per confrontare tecnologie, protocolli, opzioni e comandi. Dentro una tabella l'alias di un wikilink si scrive con la barra protetta: [[file#sezione\\|testo]].
- Diagrammi mermaid (flowchart LR o TD, sequenceDiagram) per topologie, percorsi e flussi presenti nelle fonti. Sintassi semplice: identificatori senza spazi, etichette tra virgolette doppie, nessun carattere speciale fuori dalle virgolette.
- Wikilink: collega i concetti tra i file con [[nome file]] o [[nome file#Titolo esatto della sezione|testo]]. Puoi linkare SOLO questi file (nomi esatti, senza .md): ${ELENCO}. Verso un modulo scritto da un altro autore linka il file intero, senza ancora #sezione; le ancore #sezione usale solo verso sezioni che esistono davvero.
- Titoli di sezione (H2, H3) senza i caratteri # ^ [ ] | : così le ancore dei wikilink funzionano.
- Fonti: alla fine di ogni sezione H2 principale e in fondo al file, una riga discreta in corsivo con i percorsi relativi alla radice della repo tra backtick (non wikilink: gli originali non sono nel vault), con le slide quando utile. Esempio:
*Fonti originali: \`Amazon Web Services (AWS)/doc/lecture_01_fondamenti_networking_it.pdf\` (slide 4–9), \`Amazon Web Services (AWS)/06-10-2026/lab01-networking/consegna01.md\`*`

const STRUTTURA_MODULO = `Struttura di ogni modulo, in quest'ordine
1. Frontmatter, barra di navigazione, titolo H1 indicato.
2. > [!abstract] Obiettivi e sintesi: obiettivi della lezione (dalla slide "Obiettivi"), data del laboratorio (dal nome della cartella), prerequisiti e sintesi del modulo in 5–8 righe.
3. Sezioni H2 di teoria nell'ordine dell'agenda della lezione, con sottosezioni H3 dove serve.
4. ## Mini-exercises: gli esercizi della lezione con soluzione ragionata (se presenti).
5. ## Laboratorio NN — <titolo> (NN = numero del modulo): il lab passo-passo, unendo le istruzioni delle slide ("Lab + cleanup") e ciò che lo studente ha fatto davvero (consegna ed evidenze). Sottosezioni H3: Obiettivo e prerequisiti, i passi numerati, Evidenze e come leggerle, Cleanup, Consegna (le risposte date, spiegate).
6. ## Errori comuni e troubleshooting.
7. ## Wrap-up e link suggeriti: la sintesi finale della lezione e i link indicati nelle slide.
8. ## Domande di richiamo: 6–10 domande numerate, seguite da un solo callout pieghevole "> [!success]- Risposte" con le risposte numerate.
9. Riga delle fonti dell'intero file e barra di navigazione.
Nessun limite di lunghezza: la profondità deve coprire ogni slide e ogni passaggio del lab, senza riempitivi.`

const REPORT_SCHEMA = {
  type: 'object',
  properties: {
    files: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          file: { type: 'string' },
          titolo: { type: 'string' },
          sezioni_h2: { type: 'array', items: { type: 'string' } },
          parole_stimate: { type: 'number' },
        },
        required: ['file', 'titolo', 'sezioni_h2'],
      },
    },
    lacune: { type: 'array', items: { type: 'string' } },
    dati_mascherati: { type: 'array', items: { type: 'string' } },
    note: { type: 'string' },
  },
  required: ['files', 'lacune', 'dati_mascherati', 'note'],
}

const REVIEW_SCHEMA = {
  type: 'object',
  properties: {
    moduli: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          file: { type: 'string' },
          aggiunte: { type: 'array', items: { type: 'string' } },
          correzioni: { type: 'array', items: { type: 'string' } },
          da_verificare: { type: 'array', items: { type: 'string' } },
        },
        required: ['file', 'aggiunte', 'correzioni', 'da_verificare'],
      },
    },
    lacune_materiale: { type: 'array', items: { type: 'string' } },
    note_per_indice: { type: 'string' },
  },
  required: ['moduli', 'lacune_materiale', 'note_per_indice'],
}

function promptAutore(gruppo) {
  return `Sei uno degli autori della dispensa di studio in formato Obsidian per la materia "Amazon Web Services - Introduzione e utilizzo" (ITS ICT Piemonte, corso Cloud Specialist, autunno 2026, docente Seyedhossein Javadizavieh). Lo studente la userà per ripassare anche dal telefono, a distanza di mesi: deve essere completa, dettagliata e comprensibile senza le slide.

Il tuo compito: scrivere questi moduli, uno alla volta, con la massima profondità. Gli altri moduli li scrivono altri autori in parallelo: non toccarli.

${gruppo.map(fonti).join('\n\n')}

Procedura per ogni modulo
1. Leggi per intero tutte le fonti: il testo della lezione, ogni file del laboratorio (comprese le evidenze .txt) e la documentazione secondaria. Se una slide contiene una tabella o uno schema poco leggibile nel testo estratto, apri il PDF con il tool Read usando il parametro pages (la pagina N del PDF è la slide N) e guardala.
2. Fai l'inventario di tutto ciò che le fonti contengono: ogni slide, definizione, tabella, comando con le sue opzioni, output, errore, best practice, mini-exercise, passo di laboratorio e di cleanup, link suggerito, risposta data nella consegna. Ogni voce deve comparire nella dispensa.
3. Scrivi il file con il tool Write.
4. Rileggi il file confrontandolo con l'inventario e integra con Edit ciò che manca o è troppo sbrigativo.

${STYLE_COMUNE}

${STRUTTURA_MODULO}

Alla fine restituisci il report richiesto: per ogni file scritto il percorso, il titolo, le sezioni H2 e le parole stimate; le lacune del materiale (file vuoti, mancanti, illeggibili, slide poco chiare, dettagli segnati da verificare); i dati sensibili che hai mascherato; note utili per chi scriverà l'indice e il glossario (date, argomenti chiave, contenuti dei file letti come immagini).`
}

function promptRevisore(sintesiAutori) {
  return `Sei il revisore di completezza della dispensa di studio in formato Obsidian per la materia "Amazon Web Services - Introduzione e utilizzo" (ITS ICT Piemonte, corso Cloud Specialist). Tre autori hanno appena scritto i moduli 01–07 nella cartella ${OUT}. Il requisito dello studente è "zero omissioni": tutto ciò che è nelle fonti deve essere nella dispensa, spiegato bene e senza errori.

Moduli e relative fonti:
${MODULI_NUM.map(fonti).join('\n\n')}

Sintesi dei report degli autori:
${JSON.stringify(sintesiAutori, null, 1)}

Procedura, un modulo alla volta (dal 01 al 07):
1. Rileggi per intero le fonti originali del modulo.
2. Leggi il modulo e confrontalo voce per voce con le fonti: ogni slide (titolo e contenuto), ogni tabella, ogni comando con le sue opzioni, ogni output di evidenza rilevante, ogni errore e troubleshooting, ogni mini-exercise, ogni passo di laboratorio e di cleanup, ogni link suggerito, le risposte della consegna. Cerca anche errori tecnici e spiegazioni troppo sbrigative.
3. Correggi direttamente il file con Edit: aggiungi ciò che manca nella sezione giusta e nello stesso stile, correggi gli errori. Non riscrivere le parti già corrette. Se un modulo manca del tutto, scrivilo tu seguendo le stesse regole.
4. Controlla il formato con le regole qui sotto: frontmatter esatto, barra di navigazione in alto e in fondo identica a quella indicata, solo i callout ammessi, linguaggio su ogni blocco di codice, righe delle fonti come percorsi tra backtick, domande di richiamo con risposte nel callout pieghevole, wikilink solo verso i file in elenco, ancore #sezione esistenti nel file di destinazione (ora che tutti i moduli esistono puoi aggiungere ancore verso sezioni di altri moduli, verificandone il titolo esatto), alias nelle tabelle con la barra protetta, mermaid con sintassi semplice, dati sensibili mascherati.
5. Alla fine uniforma terminologia e forma dei titoli dei callout tra i moduli.

${STYLE_COMUNE}

${STRUTTURA_MODULO}

Restituisci il report richiesto: per ogni modulo cosa hai aggiunto, cosa hai corretto e cosa resta da verificare; le lacune del materiale da segnalare nell'indice della materia; note utili per scrivere l'indice e il glossario (date, argomenti chiave per modulo, collegamenti tra moduli).`
}

phase('Stesura')
const GRUPPI = [['01', '02', '03'], ['04', '05'], ['06', '07']]
const reports = await parallel(GRUPPI.map(g => () =>
  agent(promptAutore(g), { label: 'autore moduli ' + g.join('-'), phase: 'Stesura', schema: REPORT_SCHEMA })))
GRUPPI.forEach((g, i) => {
  if (!reports[i]) log('Attenzione: l\'autore dei moduli ' + g.join(', ') + ' non ha completato: il revisore scriverà i moduli mancanti.')
})
const okReports = reports.filter(Boolean)
const sintesi = okReports.map(r => ({ files: (r.files || []).map(f => f.file), lacune: r.lacune, note: r.note }))

phase('Revisione')
const revisione = await agent(promptRevisore(sintesi), { label: 'revisore completezza 01-07', phase: 'Revisione', schema: REVIEW_SCHEMA })
if (!revisione) log('Attenzione: il revisore non ha completato.')

return { reports, revisione }
