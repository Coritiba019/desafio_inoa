# B3Alerta - Guia de Instalação e Execução

Este é um guia simples para clonar, configurar e executar o projeto Alura Space em seu ambiente local.

## Pré-requisitos

Antes de começar, verifique se você possui os seguintes requisitos instalados em seu sistema:

1. Python (versão 3.6 ou superior)
2. Git
3. Redis server

## Clone o projeto
```
git clone https://github.com/Coritiba019/alura-space.git
```

## Entre na pasta do projeto
```
cd alura_space
```

## Crie o ambiente virtual

### No Windows
```
pip install virtualenv
python -m virtualenv .venv
```

### No Linux
```
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

## Inicie o projeto
### Abra três terminais e execute os seguintes comandos
```
python manage.py runserver
```

```
celery -A setup beat -l INFO
```

```
celery -A setup worker -l INFO --pool=solo
```

Agora você pode acessar o projeto em `http://localhost:8000/` no seu navegador.

Lembre-se de manter o terminal aberto enquanto o projeto estiver em execução. Você pode parar o servidor pressionando `Ctrl+C` no terminal.

Espero que essas instruções tenham sido úteis! Se você seguiu os passos corretamente, o projeto Alura Space deve estar rodando em seu ambiente local. Se tiver alguma dúvida, sinta-se à vontade para perguntar!
