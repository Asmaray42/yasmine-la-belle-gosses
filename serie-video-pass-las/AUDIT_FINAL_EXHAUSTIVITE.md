# AUDIT FINAL D'EXHAUSTIVITÉ

Contrôle automatique (`outils/audit.py`) : pour chaque page des 7 PDF, on extrait les chiffres et les termes significatifs (6 lettres ou plus, hors mots vides) puis on vérifie qu'ils apparaissent dans la voix off, les textes incrustés, le récapitulatif, les pièges, les mnémos ou le QCM de l'épisode qui couvre la page.

- Pages couvertes : **274 / 274**
- Épisodes écrits : **61 / 61** · vidéos rendues : **61 / 61**
- Termes et chiffres du PDF retrouvés dans les épisodes : **8677 / 9873 (87.9%)**

Les termes « absents » restants sont, sauf exception, des mots de mise en page (titres répétés, légendes anglaises d'images, mots d'en-tête), des formes conjuguées ou des synonymes : la notion est couverte, mais pas avec ce mot exact. Les pages sous 70 % ont été relues une à une.

## Pages avec des termes non repris mot pour mot

| Fichier | Page | Épisode(s) | Couverture des termes | Termes du PDF absents des épisodes |
|---|---|---|---|---|
| S1-3 | 16 | 31 | 14% | 31, cctgcaccgagagagatggaataaagcccttgaacc, cgccgggaggcagaggacctgcagg, gaggggtccctgcagaagcgtggcattgtggaacaatgctgtaccagcatctgctccctc, taccagctggagaactactgcaactagacgcagcccgcaggcagccccacacccgccgcct, tggggcaggtggagctgggcgggggccctggtgcaggcagcctgcagcccttggccctg |
| S1-3 | 15 | 31 | 57% | 29, agccctccaggacaggctgcatcagaagaggccatcaagcag, atcactgtccttctgccatggccctgtggatgcgcctcctgcccctgctggcgctgctg, correspondant, ctggtggaagctctctacctagtgtgcggggaacgaggcttcttctacacacccaagacc, gccctctggggacctgacccagccgcagcctttgtgaaccaacacctgtgcggctcacac |
| S1-3 | 14 | 31 | 62% | 27, accagctggagaactactgcaactagacgcagcccgcaggcagccccacacccgccgcct, agccctccaggacaggctgcatcagaagaggccatcaagcag, aggggtccctgcagaagcgtggcattgtggaacaatgctgtaccagcatctgctccctct, atcactgtccttctgccatggccctgtggatgcgcctcctgcccctgctggcgctgctgg, ccctctggggacctgacccagccgcagcctttgtgaaccaacacctgtgcggctcacacc, cctgcaccgagagagatggaataaagcccttgaacc, gccgggaggcagaggacctgcagg, tggggcaggtggagctgggcgggggccctggtgcaggcagcctgcagcccttggccctgg, tggtggaagctctctacctagtgtgcggggaacgaggcttcttctacacacccaagaccc |
| S1-2 | 3 | 15 | 62% | appelees, chloroplastes, eucaryote, eucaryotes, extra-cellulaires, generale, interne, introduction, mitochondries, procaryotes, structures, systeme |
| S1-3 | 5 | 28, 29 | 62% | asparagine, aspartique, cysteine, designe, excepte, glutamine, glutamique, histidine, isoleucine, l'assemblage, lysine, phenylalanine, poursuit, s'ensuit, tyrosine |
| S1-3 | 19 | 33 | 64% | 37, 38, actives, d'etre, definition, existe, generale, genetique, inactives, messagers, mutations, polymorphisme, trafic |
| S1-3 | 17 | 32 | 65% | 34, appele, comportent, controle, definition, engage, generale, genetique, genome, l'expression, messagers, mutations, polymorphisme, poursuivra, procaryotes, proteique, provenance |
| S1-2 | 35 | 23 | 66% | commencent, complexe, cytoplasme, distinctes, donnant, elle-meme, formant, naissance, presente, s'allonger |
| S1-4 | 9 | 38 | 66% | antecedants, c'est-a-dire, caracterisee, chacun, congenitale, desirent, dnormal, famille, hereditaire, hnormal, l'enfant, malformation, necessaires, possedait, receveur-donneur, reconnu, reponse, s'attaquer, sanguines, savent, serait, seront, soufre, viennent |
| S1-2 | 36 | 23 | 68% | continuent, contribuent, devient, endoplasmique, extremites, identifies, initiant, l'autre, maintenir, maniere, micotubules, mouvement, opposees, position, reseau, reticulum, s'allonger, servira |
| S1-1 | 34 | 7 | 68% | arginine, asparagine, aspartique, cysteine, glutamine, glutamique, glycine, nourisson, proline, quelques, serine, tyrosine |
| S2-3 | 19 | 60 | 69% | acides, amines, excretion, glucides, hydratation, immunite, immunoglobulines, nutrition, proteines, qu'elles, respiration, transports, travers, urique, vitamines |
| S2-3 | 6 | 58 | 70% | agenesis, defaut, deformities, dysplasia, extremity, pulmonary, twisted |
| S1-2 | 38 | 23 | 70% | autour, commencent, complexes, decondenser, endoplasmiques, finalement, former, rassembles, reticulum, s'approfondit |
| S1-1 | 9 | 2 | 70% | carbones, composition, generale |
| S2-2 | 36 | 57 | 70% | 71, 72, appelee, balayage, celles, differenciation, durant, electronique, en-dessous, entamant, evolution, expliquer, externe, fonction, microscopie, processus, structure, trouve |
| S1-3 | 10 | 30 | 71% | 19, direction, l'elongation, maniere, poursuit |
| S1-3 | 12 | 30 | 71% | 23, 24, achevee, appelee, observe, permettant |
| S1-2 | 24 | 20 | 73% | capables, celles-ci, concerne, dependant, implique, jusqu'a, l'addition, nature, presents, rassembles, regulee, reparties, resulte, retirer |
| S2-2 | 33 | 56 | 73% | 30, 65, 66, allantoide, anterieur, cellulaires, celui-ci, conduit, durant, ebauche, estromac, generant, hepatique, pharynx, posterieur, septum, trachees, transversum, vesicule, vitellin, vitelline |
| S1-4 | 7 | 37, 38 | 74% | blanches, completement, derive, descendance, descendants, determine, determines, genere, influencer, l'effet, masque, nombreux, parfois, phenotypiques, presente, rapport, rouges, toujours |
| S2-3 | 14 | 59 | 74% | associe, augmente, considerablement, decenies, durant, mettant, normal, planification, presence, risques, sereuse |
| S1-2 | 37 | 23 | 75% | allongement, appelle, continuent, denomme, imaginaire, pression, provoquant, reliant, s'allonger |
| S2-2 | 2 | 49 | 75% | definition, l'epibaste |
| S1-2 | 22 | 20 | 76% | absorption, appelees, atteindre, destruction, differents, entrainees, extracellulaire, l'ensemble, l'organisme, milieux |
| S2-2 | 37 | 57 | 76% | 73, 74, cellulaires, chacun, colonises, definitifs, differents, formeront, generent, initial, l'activation, l'origine, processus, rapport, structures |
| S1-1 | 56 | 12 | 76% | baignant, durant, eucaryotes, execution, independants, internes, intracellulaires, maladies, membranes, processus, progessive, simultanee, varies |
| S2-3 | 11 | 59 | 76% | appelee, constitue, evolution, fusionnera |
| S2-2 | 31 | 55 | 77% | 62, cranio-caudal, formant, formeront, s'allonger, seront, soulevement |
| S2-3 | 24 | 60 | 77% | cellules, dependante, immunitaire, neo-synthese, prescrits, teratogeniques |
| S1-1 | 30 | 6 | 77% | lui-meme, macromolecules, possede, representation, symbolique |
| S1-3 | 9 | 30 | 77% | 17, 18, creant, integre, present |
| S1-2 | 18 | 19 | 77% | assise, distingue, egalement, formee, generalement, intracellulaires, lipoproteines, membranaires, microoganismes, microorganismes, particuliere, proteique, proteiques, specialisees, structures, systeme, trans- |
| S1-2 | 6 | 15 | 78% | 13, 31, 311, 33, 531, assurent, connectees, constituees, preparation |
| S1-4 | 16 | 40 | 78% | assure, augmentee, correspond, donneuse, importante, l'apport, maintenant, qualifiee, quantite |
| S1-3 | 28 | 35 | 78% | 106, chacune, considere, contenant, d'avoir, estime, observes, portent, possedent, presenter, proviennent, resultat, tandis |
| S1-3 | 22 | 33 | 78% | 43, abimees, correspondante, d'erreurs, d'ubiquitine, degrades, fixation, generees, intracellulaire, l'environnement, non-fonctionnelles, phases, possedant, pourront, presents |
| S1-3 | 20 | 33 | 78% | 39, 40, appelees, caracterises, denombre, positionner, presence, quelques, stimuler |
| S2-3 | 18 | 59 | 78% | cependant, developpe, infiltre, libere, lorsqu'une, presents, puisqu'ils, s'attaqueront, seront |
| S1-1 | 44 | 9 | 78% | adn-arn, anti-paralleles, colles, egalement, re-transcription, represente, s'associe, simple-brin |
| S1-2 | 32 | 22 | 79% | 13, 14, 15, 16, 17, 18, 19, 21, 22, apercevoir, appeles, correspondent, parents |
| S1-3 | 6 | 29 | 79% | ajoutes, c'est-a-dire, d'aboutir, encodent, molecule, necessite, non-traduites, pre-arnm, realisent, residus, resultat, reunir, s'agit |
| S1-2 | 1 | 14 | 79% | eucaryote, eucaryotes, generale, interactions, introduction, membranaire, mitochondries, procaryotes, systeme |
| S1-3 | 23 | 34 | 79% | 45, controle, d'arnm, definition, l'expression, molecule, polymerases, simultanement, succedent, trafic |
| S2-3 | 17 | 59 | 79% | durant, excretion, fournis, glucides, hydratation, liaison, membranaires, nutrition, reposent, respiration, vitamines |
| S2-3 | 21 | 60 | 79% | 100, 40, 60, 80, grands, induit, lievre, normal |
| S2-2 | 12 | 51 | 80% | 2017, 23, 24, composition, entoure, essais, formant, protocoles, restauration |
| S1-3 | 11 | 30 | 80% | 21, 22, poursuit, precedant |
| S2-3 | 30 | 60 | 80% | 30, teratogeniques |
| S2-2 | 35 | 57 | 80% | 69, 70, apparaissant, d'oiseau, demontre, deviendront, differents, durant, l'apparition, l'application, l'experimentation, marquage, presence, revelant, stades |
| S1-2 | 33 | 22 | 81% | 13, 14, 15, 16, 17, 18, 19, 21, 22, appeles, cellule-mere, parents, recoivent |
| S1-2 | 44 | 25 | 81% | chacune, observe, s'attacher, separes, viennent |
| S1-1 | 29 | 6 | 81% | biologiques, lui-meme, macromolecules, possede, representation, symbolique, ulterieure, utilisation |
| S1-3 | 29 | 35 | 81% | affecte, cellulaire, considerablement, correspondent, dependra, induire, liaison, modifiant, non-codante, proteique, triplets |
| S1-4 | 14 | 40 | 81% | assurer, constituants, d'exemple, definitions, differentes, l'obtention, polymerization |
| S1-3 | 18 | 32 | 81% | 35, 36, cellule, cependant, intracellulaire, l'interieur, necessite, presence, presentes, tertiare |
| S1-2 | 9 | 16 | 81% | d'adherer, donner, l'intermediaire, marquent, permantes, permettent |
| S1-2 | 17 | 18 | 82% | change-, contole, egalement, interne, l'interieur, membranaire, reseau, s'ensuit, travers |
| S1-4 | 2 | 36 | 82% | analyse, facilement, genere, genitaux, l'autre, laquelle, modele, observables, portent, transfert |
| S1-4 | 12 | 39 | 82% | causee, ci-dessous, deficient, encode, impliquant, l'allele, l'exemple |
| S2-1 | 23 | 48 | 82% | accumulation, blastocyste, cellulaire, developpement, ebauche, extrembryonnaire, formation, tapissent |
| S1-3 | 7 | 30 | 82% | 13, 14, d'arnt, l'ensemble, permet, specifiques |
| S1-4 | 8 | 38 | 83% | co-dominants, determine, peut-on, phenotypique, reponse |
| S2-2 | 13 | 51 | 83% | 20,000, 25, 26, indifferenciee, induisent, l'activation, mecanismes, musculaires |
| S2-1 | 25 | 48 | 84% | circulatoire, entourant, evolution, intrusion, systeme |
| S1-1 | 41 | 8 | 84% | amener, d'aliments, denaturee, macromolecules |
| S1-2 | 31 | 22 | 84% | formant, former, interagir, permet, possedent, produites, rapprochement, subissent |
| S1-3 | 4 | 28 | 84% | contre, demarrage, egalement |
| S1-4 | 11 | 39 | 84% | mesure, non-lies, utilisee |
| S2-1 | 1 | 43 | 84% | 1152, charles, generale |
| S1-3 | 25 | 34 | 84% | controle, definition, l'expression, produites, trafic |
| S1-3 | 1 | 28 | 85% | cellule, est-elle, exploitee, generale |
| S1-4 | 3 | 36 | 85% | comprendre, existe, l'observation, presence, repartition, retrouve |
| S2-3 | 10 | 59 | 85% | evolution, formees, modification, provoque |
| S1-2 | 29 | 21 | 85% | celle-ci, conservent, d'allongement, finalement, presente |
| S1-4 | 19 | 40 | 85% | associees, correspondent, d'inhibiteur, fixation, l'estromac, mecanisme, neutre, quelques, responsables, servent |
| S1-1 | 40 | 8 | 85% | chaperone, fournie, l'action, macromolecules, necessiter, processus |
| S1-3 | 21 | 33 | 85% | 41, 42, l'association, phases, seront, travers |
| S1-3 | 30 | 35 | 85% | apparaissent, dommages, provoquer |
| S2-2 | 23 | 54 | 85% | differentes, direction, generale, longitudalement, s'accroitre |
| S2-2 | 25 | 54 | 85% | 50, anterieur, celle-ci, creent, donnant, egalement, mouvement, posterieur, repoussant |
| S1-1 | 15 | 3 | 86% | proprietes |
| S1-1 | 54 | 12 | 86% | abondante, addition, detinees, important, l'expedition, provenance, quantite, synthetisent, variable |
| S1-2 | 23 | 20 | 86% | constitue, plasmique, reagissent, traverser |
| S1-3 | 31 | 35 | 86% | affecte, cependant, conduire, impliquee, l'espece, maintenu, mortelle, precurseurs, systeme, transplantation |
| S1-4 | 20 | 41 | 86% | atomes, couplage, d'etapes, d'oxygene, exergonique, general, lui-meme, moleculaire, series |
| S2-1 | 2 | 43 | 86% | generale |
| S2-1 | 13 | 45 | 86% | 25, 26, cerveau, d'hormones, gonadoliberine, production, produits |
| S2-3 | 8 | 58 | 86% | gemmelite |
| S1-4 | 13 | 39, 40 | 86% | contenant, generale, herite, parents, parternel, qu'elle |
| S2-2 | 29 | 55 | 86% | affectee, mecanisme, mecanismes, normal, repartition |
| S2-2 | 17 | 52 | 86% | 33, 34, appelees, culture, impliques, micro-injection, morula, somatique, succes |
| S2-2 | 7 | 50 | 86% | 13, 14, craniorachischistosis, l'origine, naissances, neuro-, neuro-ectoderme, somite |
| S1-2 | 13 | 17 | 86% | donnee, formes, incapables, lipidique, structures |
| S1-1 | 37 | 8 | 87% | feuillets, formee, macromolecules, plisses |
| S1-2 | 25 | 20, 21 | 87% | celui-, concentration, generale, impliquant, induit, lorsque |
| S1-4 | 15 | 40 | 87% | depart, n'aura, possede, pourra, produite, realiser |
| S2-2 | 16 | 52 | 87% | 31, 32, culture, d'atteindre, descendant, enucleation, perspective, somatique, utiliser |
| S1-4 | 22 | 41 | 87% | d'oxydation, depart, enzymes, necessaires, reactions |
| S1-2 | 7 | 16 | 87% | assurant, exercant, formant, glyco-, imperme-, intra- |
| S1-2 | 19 | 19 | 87% | cardio-, composes, dirigees, duquel, intra-cellulaires, resultent, s'associer, seront, signalisation |
| S1-4 | 5 | 37 | 87% | deduire, egalement, encode, existe, l'allele, possede |
| S2-3 | 23 | 60 | 87% | grands, s'expliquer, specifique |
| S1-1 | 42 | 9 | 87% | generale, reproduction, segment, transmissions |
| S2-2 | 18 | 52, 53 | 87% | 35, capacite, divisions, non-differenciees |
| S1-2 | 46 | 26 | 87% | compose, existe, nucleotidique, probalement, repliquee |
| S2-2 | 11 | 51 | 87% | 21, 22, demonstration, l'origine, puisqu'ils, resultent |
| S2-3 | 15 | 59 | 87% | afflue, arteriole, atteint, presents, recueilli, veinule |
| S1-4 | 1 | 36 | 88% | constitue, generale, possedent, resultent |
| S1-2 | 21 | 20 | 88% | differents, divers, implique, membrannaires, transfomation |
| S1-2 | 34 | 23 | 88% | celluaire, cellulaires, differentes, productions |
| S1-1 | 27 | 6 | 88% | goutelettes, l'aggregation, macromolecules |
| S1-4 | 23 | 41, 42 | 88% | actionner, assurent, d'accepteur, d'oxydation, nouvelle, perdant |
| S2-2 | 24 | 54 | 88% | 47, 48, intraembryonnaire, prefigurant, provoque, transversales |
| S1-2 | 5 | 15 | 89% | assurant, composee, differentes, entre-elles, intracytoplasmique, niveau, presente |
| S1-2 | 20 | 19, 20 | 89% | actifs, depuis, generale, passifs |
| S2-2 | 10 | 51 | 89% | 19, durant, production, puisqu'elles |
| S1-1 | 60 | 14 | 89% | courtes, formee, frontale, longues, molecules, myosine-, opposee, region |
| S1-1 | 39 | 8 | 89% | compatibles, comporte, macromolecules |
| S2-2 | 14 | 52 | 89% | 28, centre, formation, maniere |
| S2-2 | 32 | 55, 56 | 89% | 63, generale, soulevement |
| S2-3 | 13 | 59 | 89% | associe, normal, oblige |
| S2-3 | 36 | 61 | 89% | echantillon, initial, ovocytaire |
| S1-1 | 28 | 6 | 89% | alignes, macromolecules, monoinsature, tempe- |
| S1-4 | 18 | 40 | 89% | appele, diminuer, l'intervention, particulieres |
| S1-1 | 51 | 11 | 89% | animales, bi-couches, cellules |
| S1-2 | 12 | 17 | 89% | depuis, lipidique, petites |
| S1-2 | 14 | 17 | 89% | aqueuse, dissoutes, formes, implique, migrer, transporter |
| S1-3 | 3 | 28 | 89% | implique, l'elimination, processus, utilisee |
| S1-1 | 59 | 13 | 90% | apposes, composes, elements, intermediares, intra-cellulaires, l'unite, tubulines |
| S2-1 | 14 | 45, 46 | 90% | 27, generale, inhiber |
| S1-2 | 39 | 24 | 90% | cellulaires, chromo-, differentes, eventuelles, observe, somiques |
| S1-1 | 26 | 5 | 90% | b-glucose, macromolecules |
| S1-1 | 38 | 8 | 90% | constituent, contribuent, macromolecules |
| S1-1 | 45 | 9 | 90% | 90, divisons, taille, transmissions |
| S2-3 | 31 | 61 | 90% | generale |
| S1-2 | 42 | 25 | 90% | former, naissance, phases, s'effectue |
| S1-2 | 49 | 26, 27 | 90% | cellulaire, chacun, depart, differente, modification |
| S1-3 | 26 | 34 | 91% | 51, l'espece, non-codant, non-transcrit, renferment |
| S1-4 | 4 | 36 | 91% | affectees, humaines, realise |
| S1-2 | 43 | 25 | 91% | l'homme, s'assurer |
| S1-2 | 47 | 26 | 91% | formant, microscopie, permettent, phenomenes |
| S2-2 | 4 | 49 | 91% | differents, migration |
| S2-3 | 1 | 58 | 91% | generale |
| S2-3 | 2 | 58 | 91% | subdvision |
| S2-3 | 7 | 58 | 91% | grosesse |
| S2-3 | 16 | 59 | 91% | cellulaires, initialement, presentes |
| S2-3 | 22 | 60 | 91% | concentration, grands |
| S1-2 | 16 | 18 | 91% | antiports, estime, fonctionnement, requerant, simultanement, travers |
| S1-2 | 8 | 16 | 91% | enzymatiques, extra-cellulaire, hydrophyle, hydrophyles |
| S1-4 | 6 | 37 | 91% | croisements, existe, polyhybrides, presentant |
| S2-1 | 12 | 45 | 91% | apposition, d'enzymes, production, tubulaires |
| S2-2 | 26 | 54 | 91% | 51, 52, anterieur, posterieur |
| S2-2 | 30 | 55 | 91% | mecanisme, presence, repartition |
| S2-2 | 15 | 52 | 91% | 29, 30 |
| S1-2 | 10 | 16, 17 | 91% | constitue, l'aide, milieu, nature, raison, repliements |
| S2-2 | 34 | 56 | 92% | 67, 68, celui-ci, lorsqu'il, sanguins, splanchnopleural |
| S2-1 | 15 | 46 | 92% | 100, accrue, deversement, flagelle, fusions, intermediaire |
| S2-2 | 6 | 50 | 92% | 21, 23, ceux-ci, dissequee, vitelline |
| S2-3 | 26 | 60 | 92% | teratogeniques |
| S2-3 | 29 | 60 | 92% | teratogeniques, variables |
| S2-3 | 27 | 60 | 92% | prescrits, teratogeniques |
| S1-2 | 30 | 22 | 92% | formant, repartir, subissent |
| S1-2 | 50 | 27 | 93% | chromoso-, durant, generant, produisant |
| S1-4 | 26 | 42 | 93% | fabriquent, nourrit, processus, propres |
| S1-1 | 2 | 1 | 93% | pendant, prises, s'inscrire |
| S1-1 | 25 | 5 | 93% | apparaissant, intolerence, macromolecules, ramifiees, tolerente |
| S1-2 | 2 | 14 | 93% | maladies, severites, tissus, variables |
| S2-2 | 9 | 50, 51 | 93% | apparition, generale |
| S1-1 | 33 | 7 | 93% | 30,000, facilitent, mouvements, transportent |
| S1-1 | 53 | 12 | 93% | bicouche, lipidique, presence |
| S2-2 | 1 | 49 | 94% | definition, generale |
| S1-1 | 14 | 3 | 94% | creation, proprietes |
| S1-2 | 51 | 27 | 94% | cependant, ci-contre, developpees |
| S2-1 | 16 | 46 | 94% | liberation, penetration |
| S2-3 | 28 | 60 | 94% | teratogeniques, variables |
| S1-1 | 23 | 5 | 94% | macromolecules |
| S1-1 | 24 | 5 | 94% | macromolecules |
| S2-3 | 34 | 61 | 94% | objectifs |
| S1-3 | 8 | 30 | 94% | 15, 16 |
| S1-2 | 27 | 21 | 94% | humain, nombre |
| S2-1 | 20 | 47 | 94% | differenciation |
| S2-2 | 3 | 49 | 94% | l'epibaste |
| S2-1 | 18 | 46 | 95% | decondensation, depuis, rapidements |
| S2-1 | 19 | 47 | 95% | 37, applatissement |
| S1-1 | 46 | 9, 10 | 95% | alimenter, generale |
| S1-1 | 12 | 2, 3 | 95% | generale |
| S2-3 | 25 | 60 | 95% | teratogeniques |
| S2-2 | 28 | 54, 55 | 95% | estromac, mecanismes |
| S1-1 | 13 | 3 | 95% | constitute |
| S2-3 | 20 | 60 | 95% | grands |
| S1-1 | 31 | 6 | 95% | ingeres, macromolecules, particuliere |
| S2-1 | 22 | 47, 48 | 95% | ecoulement, formation, secretent |
| S2-3 | 40 | 61 | 95% | optimal |
| S1-1 | 20 | 4 | 96% | generale |
| S1-1 | 47 | 10 | 96% | cellulae' |
| S2-1 | 11 | 45 | 96% | formation, l'espace |
| S2-1 | 21 | 47 | 96% | depuis |
| S1-1 | 48 | 10 | 96% | diffusions |
| S1-3 | 2 | 28 | 96% | chromosomes |
| S2-1 | 24 | 48 | 96% | formation |
| S2-2 | 27 | 54 | 96% | evolution |
| S1-4 | 21 | 41 | 96% | interme- |
| S1-1 | 16 | 3 | 96% | proprietes |
| S1-1 | 32 | 6 | 96% | ingeres, macromolecules |
| S2-3 | 37 | 61 | 96% | l'ovocyte |
| S1-1 | 17 | 3, 4 | 97% | generale |
| S1-2 | 41 | 25 | 97% | rapport |
| S1-1 | 50 | 10 | 97% | comprend |
| S1-2 | 40 | 24, 25 | 97% | generale |
| S1-1 | 55 | 12 | 97% | cellulaires, dirigent |
| S2-3 | 4 | 58 | 97% | sanguins |
| S1-1 | 19 | 4 | 97% | lequel |
| S2-1 | 8 | 44 | 97% | extra-cellulaire |
| S1-1 | 36 | 7, 8 | 97% | 30,000 |
| S1-1 | 52 | 11 | 97% | 103 |
| S2-3 | 41 | 61 | 97% | nombre |
| S1-3 | 24 | 34 | 97% | protegeant |
| S2-1 | 5 | 43 | 98% | formation |
| S2-2 | 8 | 50 | 98% | mobilisation |
| S1-2 | 15 | 17 | 98% | lipidique |
| S1-1 | 57 | 13 | 98% | l'intervention |
| S1-1 | 58 | 13 | 98% | implique |
| S2-1 | 7 | 44 | 98% | 36 |
