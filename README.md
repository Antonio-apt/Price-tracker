## Tracker de preços :star:

Tracker para saber se o preço de algum produto de seu interesse diminuiu. A pesquisa dos produtos é feita por um spider que busca no site americanas.com

---
### Funcionalidades

- Procurar produtos
- Salvar produto para acompanhar o preço
- Listar produtos salvos
- Limpar todos os produtos
- Gerar dados estatísticos basicos sobre os preços salvos
- Envia emails caso o preço do produto salvo diminua

### Como executar

Você precisa ter o Python na versão 3 e o PIP

    $ pip install -r requirement.txt

Ou executar 'pip intall' em cada em cada dependência

    $ py create_database.py

Crie um .env com as variaveis EMAIL e EMAIL_PASSWORD

Va até [a configuração de segurança do Google](https://myaccount.google.com/u/2/lesssecureapps?pageId=none)
e ative a opção para conseguir enviar emails

A aplicação é dividida em duas partes:
 - A primeira parte é o checker price que é o script responsavel por verificar a cada uma hora os valores salvos no banco e enviar os emails:
    
    $ py checker_price.py

 - A segunda parte é o menu para gerenciar as ações:
 Em outra instância execute:
    
    $ py find_price.py

---
_Feito apenas para estudar conceitos do Python_


