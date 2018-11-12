#!/bin/bash
for i in {0..0}
do
    python SPRParser.py -d `sed "$(expr 1 + "$i" '*' 7)q;d" AllExperiments.txt` -f `sed "$(expr 2 + "$i" '*' 7)q;d" AllExperiments.txt` -cname `sed "$(expr 3 + "$i" '*' 7)q;d" AllExperiments.txt` -rname `sed "$(expr 4 + "$i" '*' 7)q;d" AllExperiments.txt` -title `sed "$(expr 5 + "$i" '*' 7)q;d" AllExperiments.txt` --concs `sed "$(expr 6 + "$i" '*' 7)q;d" AllExperiments.txt`
done
