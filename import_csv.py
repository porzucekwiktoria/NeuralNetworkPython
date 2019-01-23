# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 13:32:25 2018

@author: Kusziaa
"""

import pandas as pd
import random
import numpy as np
import csv

data = pd.read_csv('data.csv')
random.seed( 10 )
data=data.sample(n=150)

with open('plik.csv', 'w') as csvfile:
    # definiujemy nagłówek (czyli nasze kolumny)
    fieldnames = ['kolumna_1', 'kolumna_2', 'kolumna_3', 'kolumna_4']
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # zapisujemy do pierwszej linii zdefiniowane wczesniej nazwy kolumn
    csvwriter.writeheader()

    # zapisujemy do pliku po kolei nasze struktury iterujac po ich liscie
    for n in data:
        csvwriter.writerow(n)
#M-0 zlosliwy B-1 niezlosliwy
y = data[['diagnosis']].replace(['M','B'],[0,1])
#dane po normalizacji 
X = data[['radius_mean','texture_mean','perimeter_mean','area_mean','smoothness_mean','compactness_mean','concavity_mean','concave points_mean','symmetry_mean','fractal_dimension_mean']].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
