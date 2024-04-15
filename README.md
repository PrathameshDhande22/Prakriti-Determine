# Prakriti Determine

![windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![NodeJS](https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white)
![Javascript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![css](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Tensorflow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009485?style=for-the-badge&logo=fastapi&logoColor=white)
![VSCode](https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)

![Built by](http://ForTheBadge.com/images/badges/built-by-developers.svg)

Determining an individual's Prakriti, a fundamental concept in Ayurveda has long been a challenging and intricate process. Traditional Prakriti assessment methods required extensive consultations with Ayurvedic practitioners, making it arduous and time-consuming. **Prikriti Determine** features a Machine learning-based chatbot capable of efficiently determining a user's Prakriti type. The chatbot assesses various facets of their body and mind by engaging users in a friendly conversation and asking a series of well-crafted questions. This approach allows for a more consistent and objective Prakriti analysis. Based on the Prakriti, the chatbot gives diet recommendations.

## Architecture of the Used Model FNN

![FNN Architecture](./Assets/Fnn%20architecture.png)

## Watch the Output video 👉 [Video](https://youtu.be/sECt1T-hV10)

## Installation Guide

### ChatBot 💻 Installation & Training Guide

1. Make Sure you have installed the **Python** and version should be **>=3.10**.

2. Navigate to the bot Folder using command

```
cd bot
```

then create the `Models` Folder inside it

```
mkdir Models
```

3. Create Virtual Environment using virtualenv or any package you need here I'm preferring `virtualenv`

   1. Install the `virtualenv` package using pip

   ```
   pip install virtualenv
   ```

   2. Create the Virtual Environment

   ```
   virtualenv project
   ```

   3. Activate the Virtual Environment.

      For windows :

      ```
      project/Scripts/activate
      ```

      For Ubuntu :

      ```
      source project/bin/activate
      ```

4. Install the packages required to run the project.

```
pip install tensorflow pandas nltk scikit-learn sqlalchemy fastapi uvicorn websockets
```

**Note :** Wait for the packages to be installed if you encountered any error or problems try to install the packages one by one.

5. Train the Chatbot Model on the same terminal. Make sure you are in the bot folder in terminal.

   For Windows:

   ```
   python Training/botmodel.py
   ```

   For Ubuntu:

   ```
   python3 Training/botmodel.py
   ```

6. Train the Prakriti Model on the same Terminal.

   For Windows:

   ```
   python Training/prakritimodel.py
   ```

   For Ubuntu:

   ```
   python3 Training/prakritimodel.py
   ```

7. Run the API to serve both trained Model to connect with the Frontend.

   For Windows:

   ```
   python app.py
   ```

   For Ubuntu:

   ```
   python3 app.py
   ```

8. Wait for the API to startup then copy the url in which the api is running.

   e.g: `https://127.0.0.1:8000` only copy part from `127.0.0.1:8000`

   The URL may be different for different OS make a note of it.

**The API is Running Successfully 😃😃😃😃.**

### Frontend Installation 🖼️

1. Make sure you have installed **Nodejs** in your system.

2. Navigate to `frontend` folder.

```
cd frontend
```

3. Install the packages.

```
npm i
```

4. After Installing all the packages make some changes in `.env` file which is located in `frontend` folder.

```
VITE_API=ws://127.0.0.1:8000
```

Paste your copied url or server url in place of `127.0.0.1:8000`

5. Run the Frontend.

```
npm run dev
```

**The frontend is Running Successfully 😃😃😃.**

You have successfully setup your project.

## Author: Prathamesh Dhande
