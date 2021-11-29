<div align='center'>
  
  <img width="280" src="https://user-images.githubusercontent.com/60857927/143723173-6831fb5d-b8b3-4aaf-ad73-791eb4a8a911.png" />
  
</div>

<div align = "center">

<p>

  <a href="#descricao">Descrição</a> &#xa0; | &#xa0;
  <a href="#tecnologias">Tecnologias</a> &#xa0; | &#xa0;
  <a href="#requisitos">Requisitos</a> &#xa0; | &#xa0;
  <a href="#executando">Executando</a> &#xa0; | &#xa0;
  <a href="#como_funciona">Como funciona?</a> &#xa0; | &#xa0;
  <a href="#referencias">Referências</a>

</p>

</div>

<div id = "descricao">

## :pushpin: Descrição ##

<p>

  Esse é o repositório da minha versão de uma **API REST**, uma ferramenta bastante utilizada em diversos projetos em múltiplas áreas. A idea inicial desse projeto foi desenvolver uma API REST do zero, bem como seus métodos de `GET`, `POST`, `PUT` e `DELETE`, para poder entender melhor como ela funciona.

</p>

</div>

<div id = "tecnologias">

## :rocket: Tecnologias ##

Todas as tecnologias usadas na realização do projeto:

* [Python][python] [Versão 3.8]
* [Gunicord][gunicorn]
* [PyCharm][pycharm]

</div>

<div id = "requisitos">

## :warning: Requisitos ##

<p>

  Antes de executar, você precisar ter o [Git][git] e o [Python][python] (Versão 3.8) instalados na sua máquina.

</p>

</div>

<div id = "executando">

## :computer: Executando ##

<p>

  Depois de correr tudo certo na instalação, está na hora de clonar o repositório.

</p>

```bash
# Clone este projeto
$ git clone https://github.com/Iuri-Almeida/small-rest-api.git
# Acesse a pasta do projeto
$ cd small-rest-api
# Instalar dependência
$ pip install -r requirements.txt
# Iniciar o programa
$ python rest_api/main.py
```

</div>

<div id = "como_funciona">

## :eyes: Como funciona? ##

<p>

  Como essa é uma **API REST** bem simples, temos apenas as funcionalidades de `GET`, `POST`, `PUT` e `DELETE`, com suas devidas **limitações**. Segue alguns exemplos da utilização:

</p>

* `GET` <br />

  ```python
  from requests import get
  from json import loads
  
  users = loads(get('http://127.0.0.1:8000/users').text)
  user = loads(get('http://127.0.0.1:8000/users/4601760041515573618').text)
  ```

* `POST` <br />

  ```python
  from requests import post
  
  res = post('http://127.0.0.1:8000/users', data={'name': 'Iuri', 'age': 22, 'city': 'Niterói'})
  ```

* `PUT` <br />

  ```python
  from requests import put
  
  res = put('http://127.0.0.1:8000/users', data={'id': '4601760041515573618', 'name': 'José'})
  ```

* `DELETE` <br />

  ```python
  from requests import delete
  
  res = delete('http://127.0.0.1:8000/users', data={'id': '4601760041515573618'})
  ```

</div>

<div id = "referencias">

## :key: Referências ##

Alguns locais de onde me baseei para realizar o projeto:

* [Small Web App - Iuri Almeida][small_web_app]

:mag: &#xa0; Os ícones usados nesse README foram tirados desse [repositório][icones].

</div>

<!-- Links -->
[gunicorn]: https://gunicorn.org/
[small_web_app]: https://github.com/Iuri-Almeida/small-web-app
[python]: https://www.python.org/
[pycharm]: https://www.jetbrains.com/pycharm/
[git]: https://git-scm.com
[icones]: https://gist.github.com/rxaviers/7360908