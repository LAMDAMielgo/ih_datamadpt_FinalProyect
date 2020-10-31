## URBAN LANDSCAPE QUALITY INDEX
![](https://res.cloudinary.com/dute7e5ne/image/upload/v1604109631/WhatsApp_Image_2020-10-31_at_01.43.00_zrqa3c.jpg)

---------------------------------------------------------------------------
---------------------------------------------------------------------------
####ABOUT

El objetivo de este proyecto es ver la capidad que tienen el aprendizaje automático para 
realizar un Plano de Calidad del Paisaje Urbano de forma análoga al existente para la
ciudad de Madrid, realizado por Prointec dentro del marco de la revisión del PGOUM de 2009.


---------------------------------------------------------------------------
### Project Result
![](https://res.cloudinary.com/dute7e5ne/image/upload/v1604109643/HowToGif_zrjbhv.gif)

--------------------------------------------------------------------------------------
**¿Por qué medir la calidad del paisaje urbano?**

La ciudad que habitamos se puede entender, entre otras cosas, como una experiencia estética y
una construcción cultural portadora de significados. El análisis de su morfología, por un lado,
nos permite entender y asumir el relato paisajísticos de ésta, siendo el Plan una herramienta
de gestión más dentro de toda la documentación que integra un Plan General Urbanístico.

Conectar morfología urbana y calidad del espacio público, nor permite

La calidad del paisaje urbano permite contectar **morfología urbana con espacio público**,
permitiendo añadir recomendaciones y directrices que permitan a construir una cuidad 
mejor a partir de las herramientas urbanísticas pertenecientes a la gestión del patrimonio
edificado: las ordenanzas urbanísticas, modificando aquéllos parámetros que sean relevante:

* Mobiliario Urbano y Jardinería
* Accesibilidad y eliminación de barreras arquitectónicas
* Licencias
* Rehabilitación
* Integración de instalaciones (teleco, alumbraod, señaléctica)


La unificación de datos obtenidos mediante participación ciudadana y datos catastrales,
permite incorporar la opinión pública en el diagnóstico de su ciudad, fomentando el diágolo
y las políticas públicas abiertas. Así mismo, la elaboración de este tipo de planes, 
constituyen un compromiso colectivo para proyecta la imagen de la ciudad.

### :star: Project Pipeline
![](https://res.cloudinary.com/dute7e5ne/image/upload/v1604109612/WhatsApp_Image_2020-10-31_at_02.03.23_rwukmf.jpg)

--------------------------------------------------------------------------------------
### DOCUMENTATION SOURCES
* [Encuesta Abierta sobre Calidad del Espacio Público](http://arturo.300000kms.net/#1)

Realizado por el [estudio 300.000km/s](), Arturo es un algoritmo entrenado entrenado a 
partir de una encuesta ciudadana sobre evaluación comparativa de calles de Madrid, que
han sido previamente labelizadas con diferentes parámetros urbanísticos.

La encuesta recoge el 10% de las calles de Madrid, y mediante el uso de Gradient 
Boost se buscan los patrones comunes en el resto de calles de la ciudad; de esta manera
se obtiene un plano interactivo de la calidad del espacio público así como se determina
qué índices son más importantes para determinar dicha calidad.

* [Datos Abiertos del Castastro](http://www.catastro.minhap.es/webinspire/index.html)

La Dirección General del Catastro ofrece diferentes conjuntos de datos respecto a los datos
que gestiona sobre el patrimonio edificado dentro del marco europeo Inspire.
En el enlace se especifica qué recursos ofrece; para este proyecto, se trabajan con las 6 capas 
disponibles, obtenidas a partir de qGIS:
* Buildings
* Building Parts
* Cadastral Zoning
* Cadastral Parcels
* 28900 

----
### Links de interés
Experiencias anteriores basadas en NYC:

* [Street Score](http://streetscore.media.mit.edu/): Realizado en 
* [Urbanopticon](https://goodcitylife.org/)

Estudio sobre Calidad del Paisaje urbano realizado dentro del marco de la revisión del
PGOUM de 2009:
* [Plan Director](http://www.urbanalibi.es/plan-director-para-la-calidad-del-paisaje-urbano-de-madrid/)
* [Ficha del Proyecto en Prointec](https://www.prointec.es/es/project/calidad-paisaje-urbano-madrid-espana)

----
### :computer: **Technology stack**
As a prerequisite, the programming lenguage of this repository is Python 3.7.3, therefore must have Python 3 installed. The native packages in use are:
- [Os](https://docs.python.org/3/library/os.html)
- [Functools](https://docs.python.org/3/library/functools.html)
- [Re](https://docs.python.org/3/library/re.html)

Furthermore, it is need to be installed in the proper environment the following libraries:

- [Pandas (v.0.24.2)](https://pandas.pydata.org/pandas-docs/stable/reference/index.html)
- [Numpy (v.1.18.1)](https://numpy.org/doc/stable/)
- [Scikit-learn (v.0.23.1)](https://towardsdatascience.com/preprocessing-with-sklearn-a-complete-and-comprehensive-guide-670cb98fcfb9)
- [Matplotlib (v.3.1.2)](https://matplotlib.org/contents.html)
- [Plotly (v.3.1.2)](https://matplotlib.org/contents.html)
- [Streamlit (v.3.1.2)](https://matplotlib.org/contents.html)

-----
#### :construction: Status
Version 1.0 [04.07.2020] > First version done for class presentation
```
ISSUES
----------------
+ Spider Plot finally dropped of Web
+ To do: Deploy with Hedoku
+ To do: Map has performance issues regarding making filtering better
+ Data: raw/ clean data to large for repo
+ Streamlit front need of review
+ Tranlate: - Links 
            - Data Sources
+ At least, upload final GDF
```

---
### :love_letter: **Contact info**
linkedin.com/in/lauramielgo for inqueries.

### :hearts: **Thanks**
Big thanks to TAs and teachers for the help and support in the development of this project:

@github/potacho

@github/TheGurus

---
#### :file_folder: **Folder structure**
The project's structure is as follows:
```
└── project
    ├── __trash__
    ├── .gitignore
    ├── .env
    ├── requeriments.txt
    ├── README.md
    ├── str_app.py
    ├── notebooks
    │   ├── 01_Catastro pt1.ipynb
    │   ├── 02_Catastro pt2.ipynb
    │   ├── 03_Arturo Model - Gradient Boosting.ipynb
    │   ├── 04_Merging DataSets.ipynb 
    │   ├── 05_Clustering Results - Viz.ipynb    
    │   └── 06_Final Map.ipynb
    ├── models
    │   ├── 011_Partitioning Algos.ipynb
    │   ├── 012_Density Algos - UMAP 10.py
    │   ├── 022_Density Algos - UMAP 25.py
    │   ├── 122_Density Algos - Catastro.py
    │   ├── model_dbscan_silh167.sav
    │   ├── model_dbscan_silh193.sav
    │   └── mmdel_dbscan_silh261.sav
    ├── catastro_inspire_etl
    │   ├── m_acquisition.py
    │   ├── m_cleaning.py
    │   └── __init__.py
    ├── streamlit_back
    │   ├── m_opening_final.py
    │   └── __init__.py
    ├── streamlit_front
    │   ├── load_css.py
    │   ├── style.css.py
    │   └── __init__.py
    ├── streamlit_graphics
    │   ├── main_map.py
    │   ├── ranking_fig.py
    │   ├── spider_plot.py
    │   ├── map_to_render.html
    │   ├── ranking_fig.html
    │   └── __init__.py
    └── data
        ├── raw
        ├── labelled
        ├── final_streamlit
        └── clean


```

