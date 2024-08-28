
# Descrição

Este projeto é uma aplicação Django que gera páginas HTML completas com base em descrições fornecidas pelo usuário. Utiliza a API do Google para geração de conteúdo e permite visualizar e baixar as páginas geradas.

# Utilidade

A aplicação é útil para criar rapidamente protótipos de páginas web baseadas em descrições textuais. Pode ser usada para brainstorming de design, criação de conteúdo dinâmico e exploração de conceitos de design web.

## Instalação

1. Clone o projeto

```bash
  git clone https://github.com/AndreBorgesXS/pagebuild.git
```

2. Entre no diretório do projeto

```bash
  cd pagebuild
```
3. Crie e ative um ambiente virtual

```bash
  python -m venv .venv
  # Ativar no Windows
  .venv\Scripts\activate
  # No linux use: 
  source venv/bin/activate
```

4. Instale as dependências

```bash
  pip install -r requirements.txt
```

5. Configure as variáveis de ambiente: Crie um arquivo .env na raiz do projeto e adicione sua chave de API do Google:

```bash
GOOGLE_API_KEY=your_google_api_key_here
```

6. Execute as migrações do banco de dados:

```bash
python manage.py migrate
```

## Execução

1. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

2. Acesse a aplicação no navegador em `http://127.0.0.1:8000/`.

3. Para gerar uma página HTML, vá para a rota /browse e forneça uma descrição.

4. Para baixar uma página HTML gerada, vá para a rota /download e forneça a descrição correspondente.

