<h1 align='center'> Optimisation TD2 </h1>
<p align='center'>
<i>Option ISIA - Centrale Paris <br>
Février 2017 <hr></i></p>

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
- Une solution utilisant un algorithme de recherche locale

On peut formaliser notre problème : Etant donné une famille de points T (les tableaux), on veut savoir quel est le k minimal, tel que k=(n1,n2) couvrant entièrement les points T.

Il nous faut minimiser la norme du duplet (n1,n2) (la norme étant le prix total et n1, n2 le nombre de cameras) pour avoir k le plus petit possible (en prix).

## <a name="res"></a>1. Résultats & Observations

Nous livrons deux codes qui fonctionnent pour résoudre le problème proposé. Ils ont néanmoins des efficacités différentes.

Pour les deux solutions nous avons discrétisé le problème en créent un grille de caméra potentielle, paramétrés par une taille de carreau epsilon.

Nous avons ensuite testé notre solution avec différentes valeurs de epsilon, jusqu'a dépasser un temps de calcul acceptable.

**Premier résultat**

Pour la première solution nous obtenons ainsi un cout de 2607 en un temps de 426 secondes avec epsilon = 0.5 (fichier result1.txt)

**Second résultat**

- Première expérience

>Avec epsilon = 2

>Coût: 2990

>Temps: 370 secondes (initialisation: 137s, résolution: 233s)

- Seconde expérience

>Avec epsilon = 3

>Coût: 3146

>Temps de 177 secondes (initialisation: 60s, résolution: 117s)

- Troisième expérience


>Avec epsilon = 5

>Coût: 3324

>Temps: 69s secondes (initialisation: 21s, résolution: 69s)



**Approfondissement**

Nous avons plusieurs idées pour améliorer significativement nos résultats du second algorithme que nous expliquerons en conclusion.

## <a name="description"></a>1. Programmation linéaire à variables entières

Cette solution utilise le solveur SCIP avec son interface python.

Nous créons deux grilles, de taille de carreau epsilon, une pour les petites caméras et une pour les grandes.

Pour chacune de ces grilles nous crééons une variable booléene (présence ou non de caméra) pour chaque intersection de la grille.

Ensuite pour chaque oeuvre nous ajoutons la contrainte que chaque oeuvre, au moins une des variables caméra situé à porté est vrai.

Dans cette phase, l'initialisation peux être trés longue si le code n'est pas optimisé et calcule la distance entre chaque caméra est chaque oeuvre.

Nous l'avons optimisé en ne prenant pour chaque oevre que les caméras situé dans le carré de coté portée*2 centré auteur de l'oeuvre, ce qui évitait d'avoir à parcourir tout le dictionnaire.


## <a name="A"></a>2. Recherche locale

### A) Discrétisation

On commence par définir un quadrillage du musée à surveiller et on définit epsilon la largeur et la hauteur des cases (on pourra jouer sur cet epsilon)

### B) Création d'une matrice de densité

On imagine que l'on peut poser une camera à chacune des intersection du quadrillage.
On stocke ces cameras (et les tableaux qu'elles surveillent) dans un tableau "cameras"

On continue ensuite en créant une matrice de la densité de tableaux surveillés par chacune des cameras divisé par le prix d'une camera (on dispose en effet de deux sortes de cameras)

### C) Itérations & updates de la matrice de densité

On sélectionne la camera avec la plus haute densité de tableaux et on l'ajoute à notre solution.

Lorsque l'on ajoute une camera ainsi, on update les poids de la matrice de densité : les tableaux déjà surveillés sont supprimés et les cameras environnantes n'ont plus à les surveiller.

On continue ainsi jusqu'à épuiser complètement l'espace des tableaux à surveiller.

On améliore ainsi cette solution en prenant des solutions dans le voisinage de cette dernière. Autrement dit, on améliore localement notre solution.


### Améliorations possibles

Notons deux améliorations qui rendraient notre solution B encore meilleure:

1. Il faudrait que nous rajoutions une étape à la fin qui nous permette de nous concentrer sur les caméras peu efficaces: il devrait être possible de les remplacer dans certaines cas par des caméras plus efficaces aux alentours

On propose pour éviter d'être pris dans un minimum local d'introduire une idée de température dans notre algorithme: il s'agit de définir une fonction strictement décroissante qui représente la dose de hasard avec laquelle on sélectionne une camera à chaque itération (vs le schéma rationnel = "choisir la camera avec la plus grande densité de tableaux surveillés")



2. Pour améliorer l'initialisation de notre systèmes on devrait probablement changer notre structure de données et créer une structure de graph ou les tableaux dans le voisinage d'une caméras sont connectés entre eux: cela faciliterait beaucoup l'exploration du problème et l'ajout des caméras.

Resultat 2 partie 2 = un cout de 3146 en un temps de 177 secondes (initialisation = 60, résolution = 117) avec epsilon = 3.
