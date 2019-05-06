# Bakalauras

## Turinys:

 * Darbo planas (iki Kovo 10 d.)
 * Darbas (iki Gegužės vidurio)
     * [Bakalauro darbas](https://docs.google.com/viewer?url=https://raw.githubusercontent.com/vzilinas/bakalauras/master/Bakalauras/bakalaurinis.pdf)
 * Praktinė dalis (iki Gegužės vidurio) 



## Paleidimas:

### Darbo plano ir Darbo aprašo kompiliavimas:
 1. Įsirašyti ```xelatex``` ir ```biber``` ([Šito](http://stefanocoretta.altervista.org/xelatex-linguistics/installation/) užteko)
 2. Sukompiliuoti naudojant: 
    - [Visual Studio Code](https://code.visualstudio.com/) ir [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop) (Nustatymai - .vscode/setting.json)
    - Komandas:
        ```	
        xelatex bakalaurinis.tex
        biber bakalaurinis
        xelatex bakalaurinis.tex
        ```