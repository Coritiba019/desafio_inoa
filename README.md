# B3Alerta - Guia de Instalação e Execução

### Este é um guia simples para clonar, configurar e executar o projeto B3Alerta em seu ambiente local.

# 🚀 Pré-requisitos

Antes de começar, verifique se você possui os seguintes requisitos instalados em seu sistema:

1. [Python](https://www.python.org/downloads/)
2. [Git](https://git-scm.com/downloads)
3. [Redis server - Windows](https://github.com/tporadowski/redis/releases)

# 📥 Instalação

## Instalação do Redis no Linux (Ubuntu)
```
sudo apt update
sudo apt install redis-server
```

## Instalação do Redis no Windows
```
https://github.com/tporadowski/redis/releases
```

Para verificar se o Redis foi instalado corretamente, execute:
```
$ redis-cli ping
PONG
```

## Clone o projeto
```
git clone git@github.com:Coritiba019/desafio_inoa.git
```

## Navegue até a pasta do projeto
```
cd desafio_inoa
```

## Configuração do Ambiente Virtual

### No Windows
```
pip install virtualenv
python -m virtualenv .venv
```

### No Linux
```
pip install virtualenv
python3 -m virtualenv .venv
```

## Ative o ambiente virtual

### No Windows
```
.venv\Scripts\activate
```

### No Linux
```
source .venv/bin/activate
```

## Instale as dependências
```
pip install -r requirements.txt
```

## Configuração do Banco de Dados

### No Windows
```
python manage.py makemigrations
python manage.py migrate
```

### No Linux
```
python3 manage.py makemigrations
python3 manage.py migrate
```


## Gere a Secret Key

### No Windows
```
python secret_key_generator.py
```

### No Linux
```
python3 secret_key_generator.py
```

Após a geração da key, copie o conteúdo do .env.example para um novo arquivo chamado .env.

# 🚀 Execução

## Abra três terminais distintos e execute os seguintes comandos em cada um deles:


## Iniciar o servidor Django:
```
python manage.py runserver
```

## Iniciar o Celery Beat:
```
celery -A setup beat -l INFO
```

## Iniciar o Celery Worker:
```
celery -A setup worker -l INFO --pool=solo
```

### 🌐 Agora, você pode acessar o projeto pelo seu navegador no endereço http://localhost:8000/.

### 💡 Dica: Mantenha os terminais abertos enquanto estiver usando o projeto. Para encerrar, pressione Ctrl+C.
