# Main
ConRepass
APP para consultar os repasses de convênios e contratos de repasses do MS

Consulta de Convênios
Aplicação em Python + Streamlit para consulta de convênios a partir de um arquivo CSV.
O campo principal de busca é o Instrumento (número do convênio), e o sistema exibe todos os dados relacionados.

🚀 Funcionalidades
Consulta de convênios pelo número do Instrumento.
Exibição automática de todos os campos presentes no CSV.
Organização dos dados em blocos (Identificação, Institucional, Valores/Vigência).
Possibilidade de edição em campos específicos (ex: Situação, Valor Liberado).
Salvamento das alterações diretamente no arquivo CSV.
📊 Estrutura do CSV
O arquivo convenios.csv deve conter pelo menos os seguintes campos:

Instrumento → número do convênio (chave de busca)
Município
Órgão Concedente
Objeto
CNPJ
Fundo de Saúde
Região de Saúde
Valor Total
Valor Liberado
Situação
Data de Início
Data de Fim
Você pode adicionar ou remover colunas conforme necessário. O app exibirá automaticamente todos os campos existentes.

🛠️ Instalação e Uso
Clone este repositório:
git clone https://github.com/seuusuario/consulta-convenios.git
cd consulta-convenios
