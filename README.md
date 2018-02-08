<h1 align='center'> Optimisation TD2 </h1>
<p align='center'>
<i>Option ISIA - Centrale Paris <br>
Janvier 2017 <hr></i></p>

__Auteur__ : Eymard Houdeville, Antoine Aubay<br>

## Index
1. [Introduction](#intro)
2. [Programmation linéaire à variables entières](#description)
3. [Recherche locale](#A)


## <a name="intro"></a>1. Introduction

L'objectif de ce TP est de trouver une solution au problème des cameras du musée: http://primers.xyz/9

Ce problème est un problème de couverture minimale d'un ensemble de points qui est NP hard.

Nous proposons deux solutions:
- Une solution avec le solveur SCIP
- Une solution utilisant un algorithme greedy

On peut formaliser notre problème : Etant donné une famille de points T (les tableaux), on veut savoir quel est le k minimal, tel que k=(n1,n2) couvrant entièrement les points T.

Il nous faut minimiser la norme du duplet (n1,n2) (la norme étant le prix total et n1, n2 le nombre de cameras) pour avoir k le plus petit possible (en prix).

## <a name="res"></a>1. Résultats & Observations



## <a name="description"></a>1. Programmation linéaire à variables entières
Cette solution utilise le solveur SCIP.

(DESCRIPTION SOLUTION SCIP)

## <a name="A"></a>2. Recherche locale

# A) Discrétisation

On commence par définir un quadrillage du musée à surveiller et on définit epsilon la largeur et la hauteur des cases (on pourra jouer sur cet epsilon)

# B) Création d'une matrice de densité

On imagine que l'on peut poser une camera à chacune des intersection du quadrillage.
On stocke ces cameras (et les tableaux qu'elles surveillent) dans un tableau "cameras"

On continue ensuite en créant une matrice de la densité de tableaux surveillés par chacune des cameras divisé par le prix d'une camera (on dispose en effet de deux sortes de cameras)

# C) Itérations

On sélectionne la camera avec la plus haute densité de tableaux et on l'ajoute à notre solution.

Lorsque l'on ajoute une camera ainsi, on update les poids de la matrice de densité : les tableaux déjà surveillés sont supprimés et les cameras environnantes n'ont plus à les surveiller.

On continue ainsi jusqu'à épuiser complètement l'espace des tableaux à surveiller.

On améliore ainsi cette solution en prenant des solutions dans le voisinage de cette dernière. Autrement dit, on améliore localement notre solution.


# Améliorations possibles

Notons deux améliorations qui rendraient notre solution B encore meilleure:

1. Il faudrait que nous rajoutions une étape à la fin qui nous permette de nous concentrer sur les caméras peu efficaces: il devrait être possible de les remplacer dans certaines cas par des caméras plus efficaces aux alentours

2. Pour améliorer l'initialisation de notre systèmes on devrait probablement changer notre structure de données et créer une structure de graph ou les tableaux dans le voisinage d'une caméras sont connectés entre eux: cela faciliterait beaucoup l'exploration du problème et l'ajout des caméras.
