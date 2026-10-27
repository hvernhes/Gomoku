# regles.md — Les règles du Gomoku (version de notre sujet)

Référence pour écrire le plateau et les règles. Source : le sujet du
projet (version 3.3, texte et schémas de l'appendice). En cas de doute, le
sujet fait foi.

Légende : ✅ compris et validé · ⏳ en cours · ⬜ à faire

## 1. Le Gomoku de base

* Deux joueurs, noir et blanc. Noir commence.
* À tour de rôle, chacun pose une pierre sur une intersection libre.
* Une pierre posée ne bouge jamais et n'est jamais retirée.
* Le premier à aligner 5 pierres (horizontal, vertical ou diagonal) gagne.
* Plateau plein sans alignement : match nul.

Le Gomoku se joue sur un plateau de Go avec des pierres de Go, mais ce
n'est pas le jeu de Go (pas de territoires, pas d'encerclement de groupes).

## 2. Ce que notre sujet change ou ajoute

| | Gomoku de base | Notre sujet |
|---|---|---|
| Plateau | Souvent 15×15 | 19×19, sans limite de pierres |
| Alignement gagnant | 5 (parfois exactement 5) | 5 ou plus |
| Captures | Aucune | On retire une paire adverse encadrée ; la case redevient jouable |
| Autre victoire | Aucune | 10 pierres capturées |
| Endgame capture | N'existe pas | Un 5 ne gagne que s'il n'est pas cassable par une capture ; avec 4 paires déjà perdues, une capture de plus donne la victoire |
| Double-three | Autorisé (interdit pour Noir seulement au Renju) | Interdit, sauf s'il est introduit par une capture (le sujet ne distingue pas les joueurs) |
| Ouverture | Noir joue où il veut | Non précisé (Standard, Pro, Swap… = bonus) |

Les captures et le double-three viennent de variantes du Gomoku (Pente,
Ninuki-renju, Renju). Ce rattachement est de mémoire, non vérifié ; il ne
change rien : seul le sujet fait foi.

## 3. Les trois règles spécifiques, à approfondir

### 3.1 Capture ✅ (sauf le point ouvert en bas de la section)

Établi (sujet + schémas) :
* On capture en **encadrant une paire** de pierres adverses : posée en
  bout de paire, ma pierre doit avoir, de l'autre côté de la paire, une
  autre pierre à moi.
* Cela marche dans toutes les directions : horizontale, verticale,
  diagonales (le schéma du sujet est en diagonale).
* On ne capture que des **paires** : pas une pierre seule, pas trois
  pierres ou plus alignées.
* Les deux pierres sont retirées, les cases redevenues libres se rejouent
  « comme si elles n'avaient jamais été occupées ».
* **Jouer dans une capture est légal et sans danger** : si je pose ma
  pierre de façon à former une paire déjà encadrée par deux pierres
  adverses, elle n'est pas capturée. Mais si ensuite je capture l'une des
  deux pierres adverses qui l'encadrent, ma paire redevient vulnérable.
* 10 pierres capturées (5 paires) = victoire.

Mécanisme : à la pose d'une pierre, dans chacune des 8 directions, on
regarde les 3 cases suivantes : adversaire, adversaire, moi → capture.

Scénarios validés (X joue, O est l'adversaire, `.` est une case vide) :
```
 Capture simple :        X O O .     X joue en .  ->  X . . X
 Trois pierres :         X O O O .   X joue en .  ->  X O O O X (rien)
 Une seule pierre :      X O .       X joue en .  ->  X O X     (rien)
 Quatre pierres :        X O O O O X                  (rien : seulement des paires,
                                                       même avec X aux deux bouts)
 Jouer dans une capture: X . O X     O joue en .  ->  X O O X   (légal, O n'est
                                                       pas capturé)
```
Lecture validée le 2026-10-26 : « Red can play in a without losing the
pair » (sujet, VI.1) tranche le sens de « one can not move into a
capture » : le coup est légal et sans danger sur le moment. Chaque
direction se vérifie séparément (une pierre d'une ligne de quatre peut
former une autre paire dans une autre direction).

À préciser (à valider ensemble, pas dans le sujet) :
* Une seule pose peut-elle capturer dans plusieurs directions ? Rien ne
  l'interdit dans le texte ; lecture naturelle : oui.

### 3.2 Endgame capture ✅ (sauf les points ouverts en bas de la section)

Texte du sujet :
* Un joueur qui aligne 5 pierres ne gagne que si l'adversaire ne peut pas
  casser cet alignement en capturant une paire.
* Si un joueur a déjà perdu 4 paires et que l'adversaire peut en capturer
  une de plus, l'adversaire gagne par capture.
* S'il n'y a aucune possibilité que cela arrive, inutile de continuer la
  partie.

Lecture (2026-10-26, à valider) :
* **Casser un 5** = en retirer au moins une pierre par la capture d'une
  paire dont l'une des pierres est dans la ligne.
* Si aucune capture de ce genre n'est possible pour l'adversaire, le 5
  gagne tout de suite.
* **Briser un 5 ne fait en général que gagner du temps** : la case libérée
  se rejoue. Exemple (X vient d'aligner 5 ; O capture la paire verticale
  en jouant en a, puis X rejoue en (2,3) et retrouve son 5) :
```
      0 1 2 3 4 5 6            0 1 2 3 4 5 6
  1   . . . O . . .        1   . . . O . . .
  2   . X X X X X .        2   . X X . X X .   <- après la capture
  3   . . . X . . .        3   . . . . . . .
  4   . . . a . . .        4   . . . O . . .
```
* La capture de O change vraiment l'issue dans trois cas :
  1. le 5 est de nouveau cassable après que X a rejoué ;
  2. X ne peut pas rejouer la case (par exemple double-three interdit) ;
  3. la capture donne 10 pierres à O : O gagne tout de suite (deuxième
     phrase du sujet : si le joueur au 5 avait déjà perdu 4 paires et
     que l'adversaire en capture une de plus, l'adversaire gagne par
     capture ; la victoire par 10 captures prime sur le 5).

Décisions prises le 2026-10-26 (lectures validées, le sujet est bref) :
* **Qui doit casser le 5, et quand ?** L'adversaire n'a que son prochain
  coup ; s'il ne casse pas le 5, le 5 gagne.
* **Ligne de 6 ou plus** : le 5 est cassé si, après la capture, la pierre
  qui avait fait l'alignement ne fait plus partie d'un alignement de 5 ou
  plus. Une ligne de 6 qui garde 5 pierres consécutives n'est pas cassée.
* **Ordre dans un même coup** : poser la pierre, puis les captures, puis
  la fin de partie.

Implémentation (`winner()` dans `Game/board.py`, calculée à la demande à
partir du dernier coup) :
1. 10 pierres capturées par celui qui vient de jouer : il gagne.
2. Le 5 formé par l'adversaire au coup précédent est toujours intact :
   l'adversaire gagne.
3. Le dernier coup forme un 5 que l'adversaire ne peut ni casser ni
   transformer en 10 captures (simulation de chaque case libre) : le
   joueur gagne.
4. Sinon, personne.

Non traité : match nul (plateau plein), le sujet n'en parle pas.

### 3.3 Double-three ✅ (sauf les points ouverts en bas de la section)

Texte et schémas du sujet :
* **Free-three** : alignement de trois pierres qui, s'il n'est pas
  immédiatement bloqué, permet un alignement de quatre **indéfendable**
  (quatre pierres avec deux extrémités libres).
* Les exemples du sujet : trois pierres en diagonale, bouts libres ; et
  trois pierres **avec un trou** (`. R . R R .`). Un free-three n'est donc
  pas forcément fait de pierres collées.
* **Double-three** : un coup qui introduit deux free-threes en même temps.
  Il est **interdit**.
* **Exception** : ce n'est pas interdit si le double-three est introduit
  par une capture.
* Exemple du sujet : le coup `a` crée un free-three en ligne et un
  free-three en diagonale (avec un trou). Avec une pierre bleue en `b`,
  l'une des deux extrémités du free-three en ligne est bouchée : le coup
  devient légal.

Pourquoi un free-three est une menace : un **quatre ouvert** (4 pierres,
les deux bouts libres) est indéfendable, l'adversaire ne bloquant qu'un
seul bout par coup. Un free-three est un trois qui peut devenir un quatre
ouvert au prochain coup.
```
 Free-three :        . . X X X . .   ->  . . X X X X .   (quatre ouvert)
 Pas un free-three : O X X X . .     ->  O X X X X .     (un seul bout libre)
 Avec un trou :      . X . X X .     ->  . X X X X .     (quatre ouvert)
```

Pourquoi le double-three est interdit : l'adversaire ne peut bloquer qu'un
des deux free-threes, l'autre devient un quatre ouvert.

Effet sur la question « coups légaux » : pour chaque coup candidat, on
pose la pierre, on compte les free-threes qu'elle crée dans ses 4
directions ; si ce nombre est 2 ou plus **et** que le coup ne capture
rien, il est illégal. Seuls comptent les free-threes que ce coup introduit.

Exemple de l'exception (X joue en c : deux free-threes, plus une capture
en diagonale ; coup légal) :
```
      0 1 2 3 4 5 6 7 8
  0   . . . . . . . . .
  1   . . . . . . . . .
  2   . . . . X . . . .
  3   . . . . X . . . .
  4   . . X X c . . . .
  5   . . . . . O . . .
  6   . . . . . . O . .
  7   . . . . . . . X .
  8   . . . . . . . . .
```
Sans le X en (7,7), il n'y aurait pas de capture et le coup en c serait
interdit.

Implémentation (2026-10-26, `is_legal` dans `Game/board.py`) :
* Free-three, formalisation retenue : sur un axe, la pierre posée crée un
  free-three s'il existe une case vide e qui, remplie par le même joueur,
  donne un **quatre ouvert** (exactement 4 pierres de suite, les deux bouts
  libres) contenant la pierre posée et e. Un bout est libre s'il est dans
  le plateau et vide : **le bord du plateau ou une pierre adverse le
  ferme** (réponse à la question sur les bords).
* Un seul free-three comptabilisé par axe ; coup interdit à partir de deux
  axes, sauf si le coup capture une paire.
* Une pierre qui fait déjà un quatre ouvert (pas un trois) n'ajoute pas de
  free-three.

Points ouverts :
* Les trous multiples et les cas limites non testés.
* Une capture qui retire une pierre adverse bouchant une extrémité
  « introduit »-elle un free-three ? Le sujet dit seulement « introduce a
  double-three by capturing a pair ».

## 4. Points à vérifier avec le sujet

* Capture dans plusieurs directions en un seul coup (voir 3.1).
* Ordre des vérifications quand un coup capture ET aligne 5 (capture
  d'abord, puis fin de partie ?).
* Les bords du plateau comptent-ils comme extrémité bouchée pour un
  free-three ? (probablement oui, à confirmer.)
* Endgame capture : lectures décidées le 2026-10-26 (voir 3.2).
* Double-three et capture : le cas où la capture débouche une extrémité
  (voir 3.3).
* Un free-three peut-il être « défendu » par une capture d'une paire de
  ses pierres, et pas seulement en le bloquant ? La définition du sujet ne
  parle que de blocage.
