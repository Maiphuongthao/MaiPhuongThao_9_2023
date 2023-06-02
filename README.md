# Projet 9 DA-Python
***Développer une nouvelle application web avec avec Django;***

**L'applocation présente deux cas d'utilisation principaux:**


1. Les personnes qui demandent des critiques sur un livre ou sur un article particulier ;
2. Les personnes qui recherchent des articles et des livres intéressants à lire, en se basant sur les critiques des autres.



**Le site doit respecter les directives suivantes:**


- Se connecter et s'incrire, le site n'est pas accessible sans l'uthentification
- User peut voir les tickets et critiques qui sont crées par lui même ou par ses abonnements en ordre le plus récents
- Créer unt ticket avec la demande d'une crique
- Créer une critique ou critiquer les autres tickets
- Voir leur propres tickets ou critiques sur la page posts
- Suivre les autres utilisateurs en mettant leur username
- Voir les abonnements et abonés


## Initialisation du projet

### Windows :
    git clone https://github.com/Maiphuongthao/MaiPhuongThao_9_2023.git

    cd MaiPhuongThao_9_2023
    python -m venv env 
    env\scripts\activate

    pip install -r requirements.txt


### MacOS et Linux :
    git clone https://github.com/Maiphuongthao/MaiPhuongThao_9_2023.git

    cd MaiPhuongThao_9_2023
    python3 -m venv env 
    source env/bin/activate

    pip install -r requirements.txt



## Exécution du programme

Pour lancer le serveur:

    cd LITREVIEW
    python3 manage.py runserver
    
   
Entrez l'adresse suivante dans le navigateur:

    http:/127.0.0.1:8000/

Afin de tester les différentes donctionalités su site: il y a 3 utilisateurs qui sont crées:

| *Identifiant* | *Mot de passe* |
|---------------|----------------|
| admin         | litreview      |
| Ben           | password456    |
| Thomas        | password456    |


