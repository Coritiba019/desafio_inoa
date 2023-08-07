# B3Alerta - Guia de Instalação e Execução

## Este é um guia simples para clonar, configurar e executar o projeto Alura Space em seu ambiente local.

# 🚀 Pré-requisitos

Antes de começar, verifique se você possui os seguintes requisitos instalados em seu sistema:

1. Python (versão 3.6 ou superior)
2. Git
3. Redis server

# 📥 Instalação

## Clone o projeto
```
git clone git@github.com:Coritiba019/desafio_inoa.git
```

## Navegue até a pasta do projeto
```
cd desafio_inoa
```

# Configuração do Ambiente Virtual

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
```
python3 manage.py makemigrations
python3 manage.py migrate
```

## Gere a Secret Key
```
python3 secret_key_generator.py
```

Após a geração da key, copie o conteúdo do .env.example para um novo arquivo chamado .env.

## Instalação do Redis no Linux (Ubuntu)
```
sudo apt update
sudo apt install redis-server
```

# 🚀 Execução

# Abra três terminais distintos e execute os seguintes comandos em cada um deles:


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

## 🌐 Agora, você pode acessar o projeto pelo seu navegador no endereço http://localhost:8000/.

## 💡 Dica: Mantenha os terminais abertos enquanto estiver usando o projeto. Para encerrar, pressione Ctrl+C.
