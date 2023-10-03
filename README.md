# Produto-Analise-APP
Repositório que contém um protótipo de produto voltado para análise de empresas com aplicativos publicados na Google Play e App Store

## Contexto
Este projeto apresenta um conjunto de scripts que compõe um protótipo de solução inteligente e aplicável em cenários que envolvem inteligência de mercado, avaliação de marca, comparação com concorrentes e mensuração de impacto de modificações em produtos (aplicativos).

## Tutorial de Uso
Para rodar o processo e gerar a interface ao usuário, basta executar o comando _streamlit run web_scraping_app_id.py_. Com isto, uma janela abrirá em seu navegador com a interface construída, tornando possível a interação com o usuário. Assim, pode-se controlar na interface a apresentação de alguns elementos na tela e definir alguns parâmetros da requisição. São eles:

* Fonte da informação: Google, Apple ou Ambos. Esta opção define da onde espera-se que os dados sejam extraídos (Google Play, App Store ou ambas as opções).

* Número de resultados: define a quantidade de registros desejados. Para melhora de performance e teste da aplicação, sugere-se um número baixo. Caso contrário, o processo torna-se mais demorado e pode apresentar instabilidades, principalmente no momento de utilização do modelo de NLP.

* Nome da empresa: neste campo pode-se definir o nome da empresa (aplicativo) ao qual deseja-se extrair dados. A partir dessa definiçãoé que o processo começa a funcionar.

Após iniciar o processo, alguns gráficos e dados iniciais serão mostrados na tela, trazendo insights a respeito do sentimento geral do consumidor referente ao aplicativo. Posteriormente, o usuário tem contato com o dado bruto extraído das fontes selecionadas e possui a opção de baixar o arquivo csv para sua máquina e então aprofundar a análise. Além disso, ao final de todo o processo existe uma caixa no qual o usuário pode inserir uma pergunta. A partir desta etapa, um modelo baseado em Q&A é acionado, ou seja, não trata-se de uma IA generativa (ideal para o caso de uso). O modelo, pré-treinado e preparado para receber dados em português irá então se basear exclusivamente nos dados obtidos para retornar uma resposta que tenha maior sentido ao questionamento feito pelo usuário.

## Observações
A ideia deste projeto é desenhar uma solução. Não trata-se de algo escalável ou usual em grandes volumes de dados. A estratégia foi construir um esboço de solução que poderia ser melhor trabalhada para um cenário produtivo. Abaixo listo alguns pontos de melhoria:

* Estratégia de coleta de dados: foram utilizados pacotes e métodos que não levam em conta a possibilidade de filtro de data para a estração. Sempre que uma requisição é feita, todo o dado é captado, exceto quando enviado um número fixo de retornos que espera-se obter. Uma possível estratégia seria estudar se já existe e caso não exista, qual a complexidade em implementar processos que permitam um controle por data das respostas obtidas. Isto permite ganho de escala e processamento particionado e orquestrado.

* Visualização: o streamlit é uma importante ferramenta para esboçar interfaces e ideias de produtos e até entregar alguns projetos de baixa escala, mas no cenário ideal teríamos uma equipe de desenvolvedores construindo uma plataforma para suportar toda a operação.

* Modelo: foi utilizado para fins de teste um modelo razoavelmente simples e sem muita capacidade de generalização. Além disso, não há muito tratamento nos textos recebidos, o que pode prejudicar um pouco a performance. No cenário ideal, existe um trabalho de tratamento dessas informações de forma a passar como entrada apenas o essencial para a interpretação e captação de contexto. Além disso, em um cenário mais robusto, torna-se interessante utilizar algum LLM para processar e retornar respostas mais personalizadas e "humanas". Neste momento esta frente não foi realizada para testar um modelo grátis, disponível e que não necessitasse de grandes capacidades de hardware (o Llama 2 por exemplo em alguns modelos já configurados necessita de um espaço livre de RAM de 10 Gb).
