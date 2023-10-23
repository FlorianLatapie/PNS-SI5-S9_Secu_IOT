# javacard

## Comment installer pour développer

Nous développons sous Windows, ainsi, ce tutoriel est pour Windows.

- [Java SE Development Kit 8u381](https://www.oracle.com/fr/java/technologies/javase/javase8u211-later-archive-downloads.html) (dans mon cas `Windows x64 Installer`).
  - Installez Java dans le dossier spécifié dans [`./Common.properties` #JAVA_BUILD_HOME](Common.properties) :

```path
C:\Program Files (x86)\Java\jdk-1.8\
```

- Ouvrez IntelliJ dans ce dossier (javacard)
  - File > Project Structure
    - Project Settings > Project
      - SDK : choisissez le dossier où vous avez installé Java 1.8 (dans mon cas `C:\Program Files (x86)\Java\jdk-1.8\`)
      - Language level : `SDK default`
      - Validez
  - Cliquez sur "Add ant file"
    - Dans le menu Ant cliquez sur `Binarize.all.standard` puis sur `Build` (bouton play vert)

Vous devirez avoir un fichier `out/notreprojet/notreprojet.cap` qui est le fichier compilé.
