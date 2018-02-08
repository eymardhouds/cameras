<h1 align='center'> Optimisation TD1 </h1>
<p align='center'>
<i>Option ISIA - Centrale Paris <br>
Janvier 2017 <hr></i></p>

__Auteur__ : Eymard Houdeville, Antoine Aubay<br>

## Index
1. [Programmation linéaire à variables entières](#description)
2. [Recherche locale](#init)

L'objectif de ce TP est de trouver une solution au problème des cameras du musée: http://primers.xyz/9

## <a name="description"></a>1. Programmation linéaire à variables entières
Cette solution utilise le solveur SCIP.


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
