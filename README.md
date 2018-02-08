<h1 align='center'> Optimisation TD1 </h1>
<p align='center'>
<i>Option ISIA - Centrale Paris <br>
Janvier 2017 <hr></i></p>

__Auteur__ : Eymard Houdeville, Antoine Aubay<br>

## Index
1. [Programmation linéaire à variables entières](#description)
2. [Recherche locale](#init)

L'objectif de ce TP est de trouver une solution au problème des cameras du musée: http://primers.xyz/9
Ce problème est un problème de couverture minimale d'un ensemble de points qui est NP Complet.
Nous proposons néanmoins deux solutions:
- Une solution avec le solveur SCIP
- Une solution utilisant un algorithme greedy

On peut formaliser notre problème : Etant donné une famille de points T (les tableaux), on veut savoir s'il existe un duplet k=(n1,n2) couvrant entièrement les points T.

Il nous faut minimiser la norme du duplet (n1,n2) (la norme étant le prix total et n1, n2 le nombre de cameras) pour avoir k le plus petit possible (en prix).

## <a name="description"></a>1. Programmation linéaire à variables entières
Cette solution utilise le solveur SCIP.



(DESCRIPTION SOLUTION SCIP)

## <a name="init"></a>2. Recherche locale

Nous proposons les étapes suivantes pour résoudre ce problème:

# A) Discrétisation

On commence par définir un quadrillage du musée à surveiller et on définit epsilon la largeur et la hauteur des cases (on pourra jouer sur cet epsilon)

# B) Création d'une matrice de densité

On imagine que l'on peut poser une camera à chacune des intersection du quadrillage.
On continue ensuite en créant une matrice de la densité de tableaux surveillés par chacune des cameras divisé par le prix d'une camera (on dispose en effet de deux sortes de cameras)

On sélectionne la camera avec la plus haute densité de tableaux et on l'ajoute à notre solution.

On update les poids de la matrice de densité : les tableaux déjà surveillés sont supprimés et les cameras environnantes n'ont plus à les surveiller.

On continue ainsi jusqu'à épuiser complètement l'espace des tableaux à surveiller.

# C) Température

On propose pour éviter d'être pris dans un minimum local d'introduire une idée de température dans notre algorithme: il s'agit de définir une fonction strictement décroissante qui représente la dose de hasard avec laquelle on sélectionne une camera à chaque itération (vs le schéma rationnel = "choisir la camera avec la plus grande densité de tableaux surveillés")
