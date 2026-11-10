# Prononciation — comment la voix off lit le cours

La voix de la série est **Kokoro v1.0 ONNX**, voix française `ff_siwis`, 24 kHz, vitesse 1.08 —
la même sur les 61 épisodes. Elle lit le **texte prononcé**, qui n'est pas le texte affiché :
`outils/lexique.py` transforme l'un en l'autre, puis `outils/voice.py` impose la transcription
phonétique (API) des termes que la phonémisation automatique lit mal.

Vérifier une phrase, le lexique complet ou un épisode entier :

```bash
python3 outils/verif_prononciation.py "L'ADN contient 10⁻⁷ mole de Na+/K+"
python3 outils/verif_prononciation.py --lexique
python3 outils/verif_prononciation.py --episode 42
```

## 1. Ordre des transformations

1. **Formules, ions et expressions spécifiques** (`REGLES`) : `Na+/K+` → « sodium potassium », `C₆H₁₂O₆` → « C six H douze O six », `ARNm` → « A R N messager ».
2. **Sigles épelés à la française** (`SIGLES_EPELES`) : `ADN` → « adéène ». Après une élision, l'épellation est soudée (`L'ADN` → « L'adéène ») pour éviter que la voix dise « L apostrophe A ».
3. **Unités** (`UNITES`) : `µm` → « micromètres », `kcal` → « kilocalories ».
4. **Symboles génériques** (`SYMBOLES`) : `→` → « donne », `%` → « pour cent », `±` → « environ ».
5. **Nombres** : convertis en toutes lettres (`num2words`), y compris les puissances : `10⁻⁷` → « dix puissance moins sept ».
6. **Transcription phonétique imposée** (`IPA`) : pour les termes restants mal lus, la chaîne de phonèmes est écrite à la main et passée directement au moteur.

Les astérisques du script (`*mot-clé*`) ne sont **pas** prononcées : elles servent à colorer le mot
dans les sous-titres et le texte incrusté.

## 2. Prononciations imposées (API)

40 entrées, chacune contrôlée en relisant la transcription produite.

| Terme | Phonèmes (API) |
|---|---|
| `Carnegie` | `kaʁnəɡˈi` |
| `Duve` | `dˈyv` |
| `Ehlers-Danlos` | `elˈɛʁs dɑ̃lˈɔs` |
| `Ensembl` | `ɑ̃sˈɑ̃bl` |
| `Floweri` | `flˈɔweʁi` |
| `Graaf` | `ɡʁˈaf` |
| `Heuser` | `øzˈɛʁ` |
| `Hooke` | `ˈuk` |
| `Janssens` | `ʒɑ̃sˈɛns` |
| `Kartagener` | `kaʁtaʒenˈɛʁ` |
| `Klinefelter` | `klinfɛltˈɛʁ` |
| `Krebs` | `kʁˈɛbs` |
| `Leydig` | `lɛjdˈiɡ` |
| `Mangold` | `manɡˈɔld` |
| `Mendel` | `mɛ̃dˈɛl` |
| `Moodle` | `mˈudœl` |
| `Naegleria` | `nɛɡlˈeʁja` |
| `Pfeiffer` | `pfajfˈɛʁ` |
| `Sertoli` | `sɛʁtolˈi` |
| `Spemann` | `ʃpˈeman` |
| `Stemagen` | `stɛmaʒˈɛn` |
| `Sucraid` | `sykʁˈɛd` |
| `Tay-Sachs` | `tˈɛ saks` |
| `Turner` | `tyʁnˈɛʁ` |
| `Victoria` | `viktɔʁjˈa` |
| `Viridiplantae` | `viʁidiplˈɑ̃te` |
| `Wood` | `wˈud` |
| `archée` | `aʁkˈe` |
| `archées` | `aʁkˈe` |
| `buttonhead` | `bœtœnˈɛd` |
| `case report` | `kˈɛjz ʁipˈɔʁt` |
| `case reports` | `kˈɛjz ʁipˈɔʁts` |
| `cellulae` | `selylˈe` |
| `choline` | `kɔlˈin` |
| `elegans` | `eleɡˈɑ̃s` |
| `glut` | `ɡlˈyt` |
| `izoumo` | `izumˈo` |
| `lefty` | `lɛftˈi` |
| `phosphatidylcholine` | `fɔsfatidilkɔlˈin` |
| `sonic hedgehog` | `sɔnˈik ɛdʒɔɡ` |

## 3. Sigles épelés

**ADN** → « adéène », **ARN** → « aèrène », **ATP** → « atépé », **ADP** → « adépé », **GTP** → « gétépé », **RER** → « èreuèr », **REL** → « èreuèl », **RE** → « èreu », **MEC** → « èmeucé », **SRP** → « èssèrpé », **SGLT** → « èssgéèlté », **LDL** → « èldéèl », **AQP** → « akupé », **CFTR** → « céèftéèr », **INS** → « ièneèss », **ADA** → « adéa », **SCID** → « èsscéidé », **HSPA** → « acheèsspéa », **NCBI** → « ènecébéi », **AP** → « apé », **ETS** → « eutéèss », **OCT** → « océté », **EGR** → « eugéèr », **HES** → « acheeuèss », **FSH** → « èfèssache », **LH** → « èlache », **GnRH** → « géèneèrache », **hCG** → « achecégé », **CGP** → « cégépé », **ZP** → « zèdepé », **SED** → « èsseudé », **CD** → « cédé », **TEM** → « tééuèm », **ES** → « euèss », **OPC** → « opécé », **iPS** → « ipéèss », **KLF** → « kaèlèf », **RA** → « èra », **Lrd** → « èlèrdé », **FGF** → « èfgéèf », **BMP** → « béèmpé », **CEA** → « cééua », **IgG** → « igégé », **DPI** → « dépéi », **ICM** → « icéèm », **EPI** → « eupéi », **TP** → « tépé », **CIB** → « céibé », **MEB** → « èmeubé », **UCL** → « ucéèl », **QCM** → « kucéèm », **SNC** → « èssènecé », **SNE** → « èssèneeu », **FIV** → « èfivé », **NADH** → « èneadéache », **NAD** → « èneadé », **FAD** → « èfadé », **FADH** → « èfadéache », **dGTP** → « dégétépé », **HCl** → « achecéèl », **NaOH** → « èneaoache », **NaCl** → « èneacéèl », **BA** → « béa », **Fgfr** → « èfgéèfèr », **MCI** → « èmcéi », **PMA** → « péèma », **IUPAC** → « iupéacé », **SHH** → « èssacheache »


## 4. Points d'attention vérifiés

- **Élisions** : « l'ADN », « l'ARN », « l'ATP » sont soudés à l'épellation, sinon la voix lit l'apostrophe.
- **Ions et pompes** : la barre de `Na+/K+` est traitée **avant** la règle générale de la barre oblique, sinon la voix dit « sur ».
- **Exposants** : les chiffres en exposant (⁻⁷, ²) ne sont pas des chiffres ordinaires ; ils ont leur propre table.
- **Mots lus en anglais** : « NADH », « Floweri », « elegans » basculaient en prononciation anglaise ; ils sont imposés en API.
- **Termes grecs ou latins** : archées, phosphatidylcholine, Naegleria, Sertoli, Leydig, Krebs, Graaf, cumulus oophorus.
- **Orthographe du cours conservée** : « Naegleria Floweri » est prononcé comme le cours l'écrit (la graphie correcte est signalée dans l'annexe confidentielle, pas dans la vidéo).

