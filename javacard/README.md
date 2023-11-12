# Javacard

## Limitations

La carte ne peut signer que des messages de taille inférieure à 127 octets. Nous ne comprenons pas d'où vient exactement cette limitation puisqu'un APDU peut normalement transporter dans la partie `data` jusqu'à 255 octets.

Nous avons ensuite regardé comment modifier le code pour accepter des messages de tailles plus longs que 255 octets. Nous avons vu qu'il faillait mettre en place de l'APDU chaining. Le processus consiste à avoir une instruction spécifique sur la carte qui permet de récupérer des données et de les concaténer aux données déjà reçues via cette instruction.
Le terminal n'a qu'à couper la donnée qu'il veut signer en blocs de taille X (255) et envoyer séquentiellement chaque bloc. Une fois toutes les données transmises, le terminal appelle l'instruction de signature. La carte va signer l'ensemble des données reçues précédemment durant la phase de chaining. Finalement la carte vide son buffer de chaining après signature.

Cependant, nous n'avons pas réussi à mettre en place cette technique. Comme le but du projet ne portait pas vraiment sur cette partie, nous avons donc décidé de laisser la limitation de la taille des messages à 127 octets.

### Ressources

- [How to send and receive data more than 255 bytes? - Oracle Forums](https://forums.oracle.com/ords/apexds/post/how-to-send-and-receive-data-more-than-255-bytes-6131)

## Comment installer pour développer

Nous développons sous Windows, ainsi, ce tutoriel est pour Windows.

- Téléchargez [Java SE Development Kit 8u381](https://www.oracle.com/fr/java/technologies/javase/javase8u211-later-archive-downloads.html) (dans mon cas `Windows x64 Installer`).
  - Installez Java dans le dossier spécifié dans [`./Common.properties` #JAVA_BUILD_HOME](Common.properties) :

```path
C:\Program Files (x86)\Java\jdk-1.8\
```

- Téléchargez [GPShell](https://kaoh.github.io/globalplatform/) 
  - Dézippez le fichier dans un dossier temporaire
  - Copiez le contenu du dossier `bin` à la racine de ce projet (`bin` est situé dans le dossier `gpshell-binary-2.3.1\bin`)) 

Voici la structure que vous devriez avoir 

```txt
.
├── Common.properties
├── README.md
├── build.xml
├── globalplatform.dll
├── gppcscconnectionplugin.dll
├── gpshell.exe
├── javacard.iml
├── legacy.dll
├── lib
│   ├── Egate
│   │   └── ...
│   └── jc221
│       └── ...
├── libcrypto-1_1.dll
├── libcrypto-3.dll
├── libssl-1_1.dll
├── libssl-3.dll
├── list.gp
├── src
│   └── ...
├── upload.gp
├── vcruntime140.dll
└── zlibwapi.dll
```

- Ouvrez IntelliJ dans ce dossier (`javacard`)
  - File > Project Structure
    - Project Settings > Project
      - SDK : choisissez le dossier où vous avez installé Java 1.8 (dans mon cas `C:\Program Files (x86)\Java\jdk-1.8\`)
      - Language level : `SDK default`
      - Validez
  - Cliquez sur "Add Ant build file"
    - Dans le menu Ant cliquez sur `Binarize.all.standard` puis sur `Build` (bouton play vert)

> **Note**  
> Vous devriez avoir un fichier `out/savacard/savacard.cap` qui est le fichier compilé.

> **Note**  
> Si vous voulez tester le projet, vous pouvez utiliser la commande suivante : `gpshell.exe list.gp`

- Installation sur la carte
  - Ouvrez un terminal dans le dossier `javacard`
  - Tapez la commande suivante (depuis PowerShell)

```bash
.\gpshell.exe upload.gp
```

  - La dernière ligne de l'output devrait être : `release_contextcommand time: 0 ms`
