# Manuel d’utilisation du système de notation SF26 :

 ## Accéder aux ressources 

La **grille de critère** doit être accessible depuis les archives gérées par Mme Vitry-Roche. 

**L’application**, quand à elle se trouve sur [**glide**](https://go.glideapps.com) où l’adresse de la science-fair [**sciencefair.gmonge73@gmail.com**](sciencefair.gmonge73@gmail.com) devrait avoir accès au modèle (Template) ou à l’application déjà créée. 

**L’algorithme** qui sert à calculer les scores devrait se trouver sous la forme d’un code python dans ce dépôt github, ou plus exactement sous la forme de plusieurs codes différents en fonction des variantes et améliorations que je détaillerai ci-après. Il suffit de l’ouvrir à l’aide d’un éditeur de code (python, Visual Studio Code…) en prenant soin d’installer les bibliothèques nécessaires pour faire tourner le code (*numpy* et *panda*) ou de le faire tourner sur **capytale** qui est un éditeur de code en ligne inclut avec l’ENT. Je déposerai aussi le diaporama que j’ai utilisé pour présenter tous les outils originaux pour donner des éléments de visualisation.

## Utiliser les ressources 

Pour utiliser l’application lors des notations, il suffit d’ouvrir le lien de partage de l’application web (site internet qui offre des capacités semblables à une application) ou le QR code qui y renvoi. Il faut donc nécessairement une connexion internet car il faut que les scores soient centralisé vers un serveur pour pouvoir faire tourner l’algorithme par-dessus. L’application est composé d’un volet où l’utilisateur peut choisir le candidat qu’il évalue (par nom d’équipe ou d’identifiant), ce qui l’envoi vers un formulaire où il peut rentrer les scores dans chaque catégorie puis soumettre le résultat. Attention !!! Le score d’un candidat n’est pas modifiable depuis le côté client après qu’il est été soumis car chaque entrée crée une nouvelle ligne dans la table des scores, et il faut donc demander à un administrateur de l’application (vous) pour supprimer ou corriger la ligne erronée. Ce qui implique aussi qu’un seul des membres du jury ne doit remplir le formulaire d’entrée des scores par groupe participant car sinon les lignes feraient doublon. Le 2<sup>ème</sup> volet est un simple récapitulatif des conditions nécessaires pour l’acquisition de chaque niveau pour chaque critère. C’est à mon avis nécessaire pour rendre le plus objectif possible la notation en supprimant les ambiguïtés, mais je comprendrai si vous ne vouliez pas modifier cette page car il faut changer et copier manuellement tous les critères et les conditions.

L’algorithme, lui s’utilise facilement car pour le faire fonctionner, il suffit de rentrer le chemin d’accès (l.8) du fichier CSV qui contient les scores finaux et que vous pouvez exportez en allant sur l’application en mode édition, puis « Data » et clic-droit sur la feuille « ScoreEntry » puis « export… ». Il suffit maintenant de faire tourner le programme et il devrait apparaitre la liste des meilleurs de chaque catégorie dans la console. (Il devrait s’afficher une erreur concernant « NAME\_COLUMN », mais le code devrait fonctionner après quelques secondes le temps qu’il initialise une 1<sup>re</sup> fois le nom) 

N.B : Il y aura surement plusieurs fichiers python qui représentent des variantes. Comme :

\- le type d’algorithme : un score pondéré pour l’algorithme original ou un algo [PROMETHEE](https://fr.wikipedia.org/wiki/Preference_ranking_organization_method_for_enrichment_evaluation) qui se veut plus objectif 

\- la gestion des égalités : Soit les égalités sont indiquées pour la 1<sup>re</sup> place, (soit pour toutes les places), soit l’algorithme gère automatiquement les égalités.

\- gestion des doublons : Soit l’algorithme liste simplement les meilleurs dans chaque catégorie, soit il va automatiquement éliminer les vainqueurs des meilleurs prix dans la compétition des prix moins important.

J'ajouterais aussi le jeu de donnée de l'année précedente avec les gagnants de chaque catégorie afin que vous puissiez vérifier que tout fonctionne correctement.

## Adapter les ressources 

Pour adapter l’application, il faudra changer : 

1. Les critères d’évaluation

Si vous voulez apposer des changements aux critères d’évaluation, il faudra simplement modifier, ajouter ou supprimer des colonnes dans la feuille « ScoreEntry » et les informations associés dans le formulaire d’entrée des scores et la page avec le résumé de chaque attendu par critère et par niveau (ce qui peut prendre un certain temps).  

1. Le type de notation

Pour changer le type de notation, par exemple passer d’un score numérique à analogique pour certains critères, inversement ou autre, il faudra aller sur la page d’édition du formulaire d’entrée des scores et changer le type d’entrée ( « switch » pour numérique, « Number entry » pour analogique, mais ça peut-être un choix multiple, un commentaire, une checkbox ou autre. Il suffit d’ajouter le composant et de le paramétrer. N.B : si vous changez les critères, il faudra sûrement changer les paramètres des notations associés, car j’ai paramétré chaque entré pour qu’elle n’accepte que les chiffres prévus par la grille de critère (de 0 à 2 par exemple). Enfin, si vous utilisez des scores numériques, le fichier CSV en ressorti une valeur booléenne, c’est-à-dire « true » or « false » où false est symbolisé par l’absence de caractère, et il faudra s’assurer que le code contient bien un moyen de numériser ces réponses (l.67 à 70 du code originel).

1. La liste des participants 

Pour changer la liste des participants, il faudra aller sur l’éditeur de l’application, puis « Data » et sur la feuille « équipe » renseigner les noms, coordonnées et participants pour chaque équipe, ce qui devrait se faire facilement avec un copier-coller depuis un autre tableur. La méthode la plus simple reviendrai quand même à une des améliorations possibles listés ci-dessous, c’est-à-dire à automatiser l’envoi des données sur l’application directement depuis le formulaire d’inscription. Vous pouvez aussi importer directement une feuille de calcul, mais il faudra vérifier que les noms des colonnes correspondent à celle de « ScoreEntry ».

Pour l’algorithme, il faudra changer : 

1. Les critères d’évaluation

J’ai espacé et commenté tous les fichiers python, donc vous ne devriez pas avoir trop de mal à trouver quoi que ce soit, mais au cas où : les différents critères d’évaluations sont listés à partir de la ligne 10, et il faut bien faire attention à 2 choses : que les noms soient écrits à l’identique (à l’espace ou la majuscule près) que les colonnes du tableau de notation de l’application. Et qu’ils soient dans le même ordre que le tableau. Pour retrouver le nom des colonnes du tableau, vous pouvez exécuter simplement la ligne « print(df.columns) ».

1. Les catégories ou prix et les poids

Il faudra changer le nom des catégories 2 fois, une première fois dans la liste « weights » pour attribuer les poids de chaque critère à chaque catégorie/prix, à noter que [1]\*14 indique que c’est une liste de 14 éléments où tous les éléments valent 1. L’ordre ne devrait pas être important dans cette liste, mais vous devriez garder le même avec la liste « CATEGORY\_ORDER » ligne 45 où vous devez lister dans l’ordre décroissant l’importance des prix pour que ceux qui gagne un prix important soient éliminés des catégories moins séléctives.

Potentielles améliorations

Les améliorations les plus faciles à implémenter seraient probablement : 

- L’automatisation des inscriptions directement vers la base de donnée gérant les groupes sur l’app (par une automatisation Zappier j’imagine) 
- Vous pouvez opter pour une fonction de préférence (pour PROMETHEE) plus complexe (ligne 69) afin d’avoir un résultat plus précis ou pour faire un classement général.
- Pour l’algorithme PROMETHEE, une version vectorisée (c.f wikipédia) pourrait être intéressant s’il y a beaucoup d’équipes, même si pour jusqu’à une centaine d’équipes, il devrait prendre moins d’une seconde.
- Un moyen de rendre les résultats sous forme d’un fichier pdf ou d’une image ( à l’aide de la bibliothèque *reportlab* ou autre)
- Des critères et des poids encore moins ambigües et permettant un jugement objectif

Ajouts Post Science Fair:
- Des problèmes sont survenus quant au rendu de l'algorithme, qui semblerait provenir de la mise en page des résultats qui ne sont pas adaptés au identifiants contenant les noms complets des membres du groupe, je proposerai donc de changer le code pour attribuer un identifiant plus court à chaque équipe pour ensuite s'y réferrer dans la base de donnée et éviter de bouleverser la mise en page.
- Dans l'application, il y a eu certains problèmes mineurs (fonctionnait bien dans l'ensemble), il faudrait simplement corriger les valeurs min et max du critère "impressiveness" qui était minoré par 2 au lieu de majoré, et à penser aussi de changer les valeurs possibles de chaque critère si vous changez de critères.
- enlever les critères ambigus comme 'Off-Topic' et 'English' qui ne servent qu' à créer de la confusion inutile
- être plus clair sur la répartition des points, exemple: 'French usage' = 2 implique qu'il n'y a pas eu d'utilisation du français
- s'assurer avant le jour J que tout le monde a bien un accès à l'pplication fonctionelle
- enlever ou mieux incorporer les bonus de chaque catégorie
- rajouter un critère de respect des règles de sécurité et de propreté pour éviter des comportements dangereux ou plus régulièrements irrespectueux du personnel d'entretien

Il doit y avoir d’autres améliorations auxquelles je n’aurai pas pensé. 

Si vous avez des questions (importantes) vous pouvez me contacter via <brucher.nans@gmail.com>. Bon courage !!! 

