# Outil de debug visuel de la recherche

Un plateau d'analyse en pygame pour **voir ce que fait le Minimax** : quels coups
sont envoyés à l'évaluation, quelle note chacun reçoit, lesquels l'alpha-bêta a
coupés, et quelle suite de coups l'IA imagine après chacun.

On peut charger une partie enregistrée (`logs/game_*.log`), revenir à n'importe
quel coup, lancer l'analyse de la position affichée, puis descendre dans l'arbre
de recherche avec la souris. Rien n'est modifié dans la recherche : l'outil
exécute le vrai `best_move` et enregistre ce qu'il fait.

## Lancer

Depuis le dossier du dépôt (celui qui contient `src/`), avec l'environnement
virtuel activé :

```bash
python3 -m src.debug.gomoku_debug logs/game_2026-11-26_17-41-08.log
```

Sans argument, l'outil démarre sur un plateau vide :

```bash
python3 -m src.debug.gomoku_debug
```

Les journaux sont écrits par le jeu dans `logs/` (une partie par fichier, avec la
profondeur utilisée dans la première ligne).

## Prise en main en une minute

1. Ouvre un journal. Le plateau affiche la fin de la partie.
2. Avec **←**, recule jusqu'à la position qui t'intéresse (par exemple juste avant
   un coup de l'IA qui te semble mauvais).
3. Règle la profondeur avec **+** / **-** (2 au départ) et appuie sur **A**. La
   fenêtre se fige pendant le calcul : « Analysing... » s'affiche juste avant.
4. Le plateau se couvre de notes. **Survole** une case notée pour voir la suite
   de coups prévue, **clique** dessus pour descendre d'un niveau.

## La fenêtre

```
┌────────────────────────────────┬──────────────────────────────────────┐
│ plateau                        │ Move 27 / 38     To play: White      │
│  bordure verte = candidat      │ Depth 4  Radius 1  (real search)     │
│  disque coloré = coup essayé   │                                      │
│    avec sa note                │ Time 9.39 s   Leaves 7196            │
│  anneau doré   = meilleur coup │ Nodes per level: L0: 1  L1: 45 ...   │
│  point gris    = coup coupé    │                                      │
│  croix rouge   = coup illégal  │ Path: root > (11,14)                 │
│  point rouge   = dernier coup  │ White to play (AI maximizes)         │
│                                │ Moves, best first                    │
│                                │ * 1. (11,14)  -503   ████████  2502  │
│                                │   2. (11,11)  -511   ███████   2419  │
│                                │   3. (11, 9) <-521   ██         629  │
│                                │ ...                                  │
└────────────────────────────────┴──────────────────────────────────────┘
```

## Commandes

| Action | Effet |
|---|---|
| **←** / **→** | coup précédent / suivant de la partie chargée |
| **Maj + ←** / **Maj + →** | recule / avance de **deux coups** (un tour complet : un coup de chaque joueur) |
| **Début** / **Fin** | premier coup / dernier coup |
| **A** | analyser la position affichée |
| **+** / **-** | profondeur de recherche (1 à 8) |
| **R** | rayon des candidats (1, 2 ou 3) |
| **E** | notes exactes à la racine (voir plus bas) |
| **clic sur une case notée** | descendre d'un niveau dans l'arbre |
| **Retour arrière** | remonter d'un niveau ; à la racine, revenir au coup précédent |
| **clic droit** | remonter d'un niveau (sans effet à la racine) |
| **Entrée** | jouer pour de bon la ligne affichée (les coups suivants de la partie chargée sont abandonnés) |
| **clic sur une autre case** (à la racine) | jouer un coup sur la position affichée |
| **survol d'une case notée** | affiche la suite de coups prévue, numérotée |
| **Q** ou **Échap** | quitter |

Les analyses sont gardées en mémoire : revenir sur une position déjà analysée (avec
les mêmes réglages) l'affiche tout de suite, sans recalcul.

## Lire le plateau

- **Bordure verte** : toutes les cases *candidates* du nœud affiché, c'est-à-dire
  les cases vides à moins de `Radius` cases d'une pierre (distance « en carré »,
  diagonales comprises). Ce sont les seules que la recherche envisage. La bordure
  est recalculée à chaque nœud, donc elle suit les pierres du chemin parcouru.
- **Disque coloré avec un nombre** : un coup que la recherche a essayé, avec la
  note qu'elle lui donne. La note est toujours du point de vue de **l'IA** (le
  joueur qui jouait à la racine) : plus elle est haute, mieux c'est pour elle.
  - La **couleur** dépend de l'écart au meilleur coup *du joueur qui doit jouer*
    à ce nœud (échelle logarithmique) : deux notes presque égales ont la même
    couleur, un écart de quelques dizaines de points se voit, un écart de plusieurs
    milliers est rouge foncé.
  - Une couleur **plus pâle** veut dire que la note n'est qu'une **borne** (voir
    « Notes exactes et bornes »).
  - Les grands nombres s'écrivent en milliers (`-1.6k`) ; `WIN` / `LOSS` signalent
    une victoire ou une défaite certaine.
- **Anneau doré** : le meilleur coup du joueur qui doit jouer à ce nœud (à la
  racine, c'est le coup que choisit l'IA).
- **Point gris** : une case candidate que l'alpha-bêta n'a **pas** essayée parce
  qu'il avait déjà prouvé que la branche était inutile (coupure).
- **Croix rouge** : une case candidate **illégale** (double-three interdit).
- **Point rouge** : le dernier coup joué sur la position affichée.
- **Pierres numérotées** : la ligne de coups du curseur (quand tu es descendu dans
  l'arbre) et, au survol, la suite de coups prévue. Les numéros sont ceux des coups
  de la partie.
- **Points rouges de la grille** : les cases interdites au joueur qui doit jouer,
  comme dans le jeu.

## Lire le panneau

- **Move 27 / 38** : on regarde la position après 27 coups, la partie chargée en
  compte 38.
- **Depth, Radius, mode** : les réglages de l'analyse affichée.
- **Time, Leaves** : durée de l'analyse (avec l'enregistrement, légèrement plus
  longue qu'en jeu), nombre d'évaluations (les feuilles) et cadence.
- **Root candidates / legal moves tried** : cases candidates à la racine, et coups
  légaux effectivement essayés.
- **Nodes per level** : nombre de nœuds par niveau de l'arbre (L0 = la position, L1
  = ses coups, L2 = leurs réponses, etc.).
- **Path** : le chemin parcouru depuis la racine.
- **Node score, window** (quand tu es descendu) : la note renvoyée par le nœud et la
  fenêtre alpha-bêta avec laquelle il a été appelé.
- **Subtree** : taille du sous-arbre du nœud (nœuds, feuilles, temps).
- **Moves explored X of Y legal candidates (Z cut)** : combien de coups légaux la
  recherche a essayés, et combien elle a coupés.
- **Liste « Moves, best first »** : les coups du nœud classés du meilleur au moins bon
  pour le joueur qui doit jouer. La barre est proportionnelle au nombre de nœuds du
  sous-arbre : elle montre **où la recherche a dépensé son temps**.

## Vocabulaire

- **Nœud** : une position de l'arbre, atteinte par une suite de coups.
- **Niveau** : le nombre de coups joués depuis la racine. Aux niveaux pairs (0, 2,
  4...) c'est l'IA qui joue et elle **maximise** la note ; aux niveaux impairs c'est
  l'adversaire, qui la **minimise**. Pour le joueur adverse, le « meilleur » coup est
  donc celui de plus **basse** note.
- **Feuille** : un nœud où la recherche s'arrête et appelle l'évaluation (profondeur
  atteinte).
- **Fenêtre alpha-bêta** `[alpha, bêta]` : les notes qui peuvent encore changer la
  décision à ce nœud. Hors de la fenêtre, on peut couper.
- **Coupure** : l'alpha-bêta abandonne les coups restants d'un nœud parce que la
  fenêtre prouve qu'ils ne changeront rien.

## Notes exactes et bornes

Quand une branche est coupée, la note renvoyée n'est plus la vraie valeur : c'est
seulement un **encadrement**. L'outil l'indique dans le panneau :

- sans préfixe : note **exacte** ;
- `<` : la vraie valeur est **inférieure ou égale** à la note affichée ;
- `>` : la vraie valeur est **supérieure ou égale** à la note affichée.

À la racine, seul le meilleur coup (et ceux qui ont amélioré `alpha` au moment où ils
ont été essayés) ont une note exacte : les autres sont des `<`. C'est normal, et c'est
justement ce qui rend la recherche rapide.

La touche **E** relance la racine sans cette coupure : chaque coup est cherché avec la
fenêtre complète, donc **toutes** les notes de la racine sont exactes. C'est plus long,
mais c'est le vrai classement des coups.

## Utilisations typiques

- **Pourquoi l'IA a-t-elle joué ce coup ?** Recule jusqu'à la position, analyse, regarde
  l'anneau doré, survole-le pour voir la suite prévue, puis survole les autres coups
  bien notés pour comparer.
- **L'IA a raté une défense** : regarde la note des coups qui bloquent. Est-ce qu'ils
  sont dans la bordure verte ? Sont-ils notés plus bas que le coup choisi ? Descends
  dans l'arbre pour voir ce que l'IA croit que l'adversaire répond.
- **Vérifier la zone des candidats** : change le rayon avec **R** et observe la bordure
  verte. Après un clic sur un coup, la bordure est celle du nœud suivant (la zone suit
  les pierres simulées).
- **Voir la qualité du tri des coups** : regarde les barres. Si le premier coup essayé
  concentre presque tous les nœuds, le tri a bien placé le bon coup en premier ; si
  plusieurs coups ont de longues barres, la recherche a perdu du temps à les prouver.
- **Comparer deux réglages** : analyse la même position avec deux profondeurs ou deux
  rayons, et compare les compteurs et les temps (chaque analyse est mémorisée).
- **Tester un coup alternatif** : descends jusqu'à une ligne, appuie sur **Entrée**
  pour la jouer, puis analyse la position qui en résulte.

## Limites à connaître

- **La fenêtre se fige** pendant une analyse. Les profondeurs élevées en milieu de
  partie peuvent durer longtemps ; commence par une petite profondeur.
- **L'arbre enregistré est plafonné** (300 000 nœuds). Au-delà, le panneau le signale
  (« Tree truncated ») : les compteurs restent exacts, mais les nœuds profonds ne sont
  plus consultables.
- **Un léger hasard** (moins de 0,01) est ajouté à chaque évaluation pour départager
  les égalités : deux analyses de la même position peuvent différer de cette valeur et
  choisir deux coups équivalents différents.
- Une ligne que la recherche n'a jamais jouée (coupée) n'a pas de note : l'outil
  l'indique (« This line was never searched. »).
- La suite prévue au survol est celle que **l'arbre enregistré** contient : sur une
  branche coupée, c'est la ligne qui a servi à la réfuter, pas forcément la meilleure
  pour le joueur.

## Organisation du code

| Fichier | Rôle |
|---|---|
| `recorder.py` | `analyse(...)` : enrobe temporairement `minimax`, `evaluate` et `candidate_cells` du module de recherche, enregistre l'arbre (nœuds, notes, fenêtre alpha-bêta, enfants, tailles des sous-arbres) et restitue tout à la fin. Fonctions de lecture : `find_node`, `best_child`, `principal_line`, `bound_kind`. |
| `gomoku_debug.py` | la fenêtre pygame : lecture d'un journal, navigation, curseur dans l'arbre, dessin du plateau et du panneau. |

Le code de la recherche (`src/ai/`) n'est jamais modifié par l'outil.
