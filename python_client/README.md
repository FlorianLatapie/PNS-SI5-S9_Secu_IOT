# python_client

## Prérequis

- Python 3.10
- Installer les dépendances avec la commande suivante :

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python main.py # ou python3 main.py
```

## Utilisation

Une fonction `main` est disponible dans le fichier `main.py`. Elle permet de tester les différentes fonctionnalités de la carte.

- En décommentant `test_everything()` dans le fichier `main.py`, on peut tester toutes les fonctionnalités de la carte d'un coup.
- Sinon vous pouvez utiliser le terminal interactif pour tester les fonctionnalités une par une. (fonction `repl()`)

### Exemple d'utilisation

![Alt text](image.png)

Les commandes utilisant l'ordinateur font appel à la carte pour faire les opérations.

#### Login

![Alt text](image-5.png)

#### Change PIN

![Alt text](image-1.png)

#### Debug

![Alt text](image-2.png)

#### Factory reset

![Alt text](image-3.png)

#### Get public key

![Alt text](image-4.png)

La méthode renvoie $e$ et $n$ permettant de reconstruire la clé publique.

#### Sign message

![Alt text](image-6.png)

#### Save public key

![Alt text](image-7.png)
![Alt text](image-8.png)

#### Store signature

![Alt text](image-9.png)
![Alt text](image-10.png)

#### Verify signature

En utilisant les données précédemment sauvegardées, on peut vérifier la signature :

![Alt text](image-11.png)

#### Sign file

![Alt text](image-12.png)
