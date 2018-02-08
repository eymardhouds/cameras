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

Pour les deux solutions nous avons discrétisé le problème en créent un grille de caméra potentielle, paramétrés par une taille de carreau epsilon
Nous avons ensuite testé notre solution avec différentes valeurs de epsilon, jusqu'a dépasser un temps de calcul acceptable.
Pour la première solution nous obtenons ainsi un cout de 2607 en un temps de 426 secondes avec epsilon = 0.5 (fichier result1.txt)
Nos résultats pour la deuxième solution sont moins performant: un cout de 2990 en un temps de 370 secondes (initialisation = 137, résolution = 233) avec epsilon = 2.
Cela est en partie due au manque de temps pour implémenter toutes nos idées.
Nous expliquerons dans la partie les amméliorations envisageable

## <a name="description"></a>1. Programmation linéaire à variables entières

Cette solution utilise le solveur SCIP avec son interface python.

Nous créons deux grilles, de taille de carreau epislon, une pour les petites caméras et une pour les grandes. P
Pour chacune de ces grilles nous créeons une variable booleene (presence ou non de caméra) pour chaque intersection de la grille.
Ensuite pour chaque oeuvre nous ajoutons la contrainte que chaque oeuvre, au moins une des variables caméra situé à porté est vrai.
Dans cette phase, l'initialisation peux être trés longue si le code n'est pas optimisé et calcule la distance entre chaque caméra est chaque oeuvre.
Nous l'avons optimisé en ne prenant pour chaque oevre que les caméras situé dans le carré de coté porté*2  centré auteur de l', ce qui évitait d'avoir à parcourir tout le dictionnaire.



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


Resultat 2 partie 2 = un cout de 3146 en un temps de 177 secondes (initialisation = 60, résolution = 117) avec epsilon = 3.
