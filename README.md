# disney-plus-database

# Sumário

Aplicação Python demonstrando o acesso à BD Disney Plus

#  Referência

- [sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Jinja templates](https://jinja.palletsprojects.com/en/3.0.x/)


# Instalação de dependências

## Python 3 e pip 

Deve ter o Python 3 e o gestor de pacotes pip instalado. Pode
instalar os mesmos em Ubuntu por exemplo usando:

```
sudo apt-get install python3 python3-pip
```

## Bibliotecas Python

```
pip3 install --user Flask 
```

or

```
sudo apt install python3-flask
```

# Execução

Inicie a aplicação executando `python3 server.py` e interaja com a mesma
abrindo uma janela no seu browser  com o endereço [__http://localhost:9001/__](http://localhost:9001/) 

```
$ python3 server.py
2024-12-09 05:55:51 - INFO - Connected to database
 * Serving Flask app 'app'
 * Debug mode: off
2024-12-09 05:55:51 - INFO - WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:9001
 * Running on http://172.26.28.115:9001
2024-12-09 05:55:51 - INFO - Press CTRL+C to quit
...
```


