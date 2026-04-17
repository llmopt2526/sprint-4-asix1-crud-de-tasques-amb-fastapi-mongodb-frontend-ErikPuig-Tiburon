[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ULL36zWV)

### To guapo esto de arriba

## Ordre

El ordre es molt important al hora de fer projectes, en aquest cas aqui tindrem l'estructura del meu projecte:

```
├── 📁 .github
│   └── ⚙️ .keep
├── 📁 backend
│   ├── 🐍 app.py
│   └── 📄 requirements.txt
├── 📁 frontend
│   ├── 🌐 index.html
│   ├── 📄 javascript.js
│   └── 🎨 styles.css
├── 📁 img
│   ├── 🖼️ Delete.png
│   ├── 🖼️ Delteresposta.png
│   ├── 🖼️ GET.png
│   ├── 🖼️ GETTOTSresposta.png
│   ├── 🖼️ GetIDFrontend.png
│   ├── 🖼️ GetTOTS.png
│   ├── 🖼️ GetTOTSFrontend.png
│   ├── 🖼️ POST.png
│   ├── 🖼️ POSTresposta.png
│   ├── 🖼️ PUT.png
│   ├── 🖼️ PUTresposta.png
│   ├── 🖼️ PostFrontend.png
│   ├── 🖼️ frontend.png
│   └── 🎬 videoito.mp4
├── 📁 tests
│   └── ⚙️ Gestor_de_Tasques.postman_collection.json
└── 📝 README.md
```


## Tutorial

### Preparacio

Pases per a replicar el meu fet, primer tindrem que OBVIAMENT clona el meu repositori, per a fer aixo, haurem que utilitza la comanda seguent:

> [!TIP]
> Aixo ho tens que fer si o si tt

```
git clone https://github.com/llmopt2526/sprint-4-asix1-crud-de-tasques-amb-fastapi-mongodb-frontend-ErikPuig-Tiburon.git
```

Seguidament tindrem que veure que tenim python instalat al nostre sistema operatiu

> [!IMPORTANT]
> Honestament nomes vull probar aixo de important, warning i tip perque ho he vis al TikTok

> [!WARNING]
> Ara explicare com fer-ho des de un sistema linux

### Instalacio de python

Si tens un sistema operatiu basat en Debian, les commandes son el seguent:

```
sudo apt update && sudo apt upgrade
```

```
sudo apt install -y python3-pip
```

Si tens un sistema operatiu basat en Arch, les commandes son el seguent:

```
sudo pacman -Syu
```

```
sudo pacman -S python
```
### Creacio d'entorn

Ja amb aixo, entrarem a la carpeta de `backend` aqui dins, crearem un entorn de python per a instalar els requisits de `requirements.txt` que he creat amb la comanda

```
pip freeze > requirements.tx
```

Per crear l'entorn ho farem tranqulament amb la comanda

```
python -m venv "nom que tu vulgues"
```
### Activacio d'entorn

I ara tindrem que crear el entorn, haurem de entrar dins de la carpeta creada o activant l'arxiu amb la ruta complet, ho farem amb la comanda

```
source bin/activate
```

Fet aixo, podrem instalar els requisits dins de l'entorn de la seguent manera
```
pip install -r requirements.txt
```
Ara, el seguent sera crear una variable d’entorn de la URL necessaria per a el Cluster al que ens conectarem (no funcionara la meva URL ja que no tinc permeses les vostres IP, menys al insti claro)

```
export MONGODB_URL="mongodb+srv://erikpuig_db_user:CL0xkjQ5eJaIlAWN@ejemplocluster.aa9a78t.mongodb.net/?appName=EjemploCluster"
```

Ara si que si, ja dins de la carpeta de `backend` haurem de fer la comanda necessaria per a poder arrancar la aplicacio de API per a crear els endpoints necessaris, la comanda es la seguent:

```
uvicorn app:app --reload
```
Ja fet aixo, tindrem que obrir un altre terminal i entra a la carpeta de `frontend` i crearem un servidor web de python amb la comanda
```
python -m http.server 8080
```
### Comprovacio

Amb aixo fet, entrarem a el navegador i ficarem `localhost:8080`i vuerem el frontend

![Frontend](img/frontend.png)

Seguidament farem una porva de insercio de dades

![Frontend](img/PostFrontend.png)

![Frontend](img/GetTOTSFrontend.png)

![Frontend](img/GetIDFrontend.png)


## POSTMAN

### PUT

El endpoint seria aquest

![GetPostman](img/PUT.png)

La resposta es aquesta

![GetPostman](img/PUTresposta.png)

### GET a todos

El endpoint seria aquest

![GetPostman](img/GetTOTS.png)

La resposta es aquesta

![GetPostman](img/GETTOTSresposta.png)

### GET individual

El endpoint seria aquest

![GetPostman](img/GET.png)

### PUT

El endpoint seria aquest

![GetPostman](img/PUT.png)

La resposta es aquesta

![GetPostman](img/PUTresposta.png)

### Delete

El endpoint seria aquest

![GetPostman](img/Delete.png)

La resposta es aquesta

![GetPostman](img/Delteresposta.png)

## Video de la practica completa

Se que tenia que ser un video curtet, pero una cosa llevo a la otra

https://github.com/llmopt2526/sprint-4-asix1-crud-de-tasques-amb-fastapi-mongodb-frontend-ErikPuig-Tiburon/blob/main/img/videoito.mp4
