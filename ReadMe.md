# Mandy - Manufacturing AI Agent

-   AI agent that can store, recall, and answer queries about manufacturing company’s operations

## Perquisites

-   Ollama + llama3.2 [click here to download](https://ollama.com/download)
-   Python3.13 [click here to download](https://www.python.org/downloads/)

## Pre Install

-   OPull the base llm model

    ```
    ollama pull llama3.2
    ```

## Installation

-   Create virtual python Environment and activate it

    -   ### **Linux or Mac**

    ```
    python3 -m venv env
    source env/bin/activate
    ```

    -   ### **Windows**

    ```
    python3 -m venv env
    cd env/Scripts && activate && cd ../../
    ```

-   Install requirements

    ```
    python3 -m pip install -r requirements.txt
    ```

-   Start StreamLit
    ```
    streamlit run main.py
    ```

## Usage

-   Go to [here](https://127.0.0.1:8501) to start conversation with mandy
