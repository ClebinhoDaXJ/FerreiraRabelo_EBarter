# E-Barter
Ideia chave:
*criar uma simulação de ecônomia em um "mundo" com diversas sociedades.

Objetivo final:
*printar gráficos valor X tempo da moeda de cada sociedade.

Fatores que levam à variação do valor da moeda:
*produtos originários da sociedade.
*negociação desses produtos dentro da própria sociedade.
*negociação dos produtos com outras sociedades.
*um indíviduo de determindada sociedade pode possuir parte de sua riqueza como moeda de outra sociedade.

OBS: 
a ideia com esse trabalho NÃO É PREVER preços de ações e moedas, mas sim observar como eles variam
de acordo com a mudança de certos parâmetros, a mudança destes parâmetros pode, ou não, se aproximar do que ocorre no mundo real, apesar do modelo se basear na economia estudada em sociedades reais.

# Classes - chave:

TRADER: pertence a uma sociedade e possui determinada quantidade de moedas daquela sociedade. Pode comprar fazer operações de compra e venda de bens ou moedas dentro da própria sociedade ou em outras sociedades.

SOCIETY: consiste de uma lista de bens e traders, assim como de seus respectivos valores e riquezas. Ela possui uma moeda característica. Novos bens podem ser gerados em uma sociedade.  O valor de um bem na 
sociedade em questão dependerá de três parâmetros: quatidade atual de bens, necessidade dos bens, dificuldade de produção.    

BENS: possui nome, quantidade disponível em certa sociedade, o valor que ele possui na sociedade em em questão dependerá de três parâmetros: quatidade atual de bens, necessidade dos bens, dificuldade de produção. Também contém uma lista de preços desse bem em todas as sociedades.  

MOEDA: é a característica especial de uma sociedade, uma sociedade não pode ter duas moedas diferentes. A classe possui a quantidade total de moedas existentes, além do valor e preço da moeda em comparação com o de outras moedas. preço = valor/quantidade.

Conceitos importantes:
O valor de uma moeda é intimamente relacionado com o preço dos bens em uma sociedade, quanto menor o preço dos bens, maior o valor da moeda (porque é possível comprar mais com menos) e vice-versa.
Haverá um referencial de valor, algo análogo ao padrão ouro. O referencial é uma constante global chamada GOLD. Os valores tanto dos bens como das moedas serão definidos por meio desse padrão.

Fluxo das transações:
Será definido um número específico de transações entre dois traders quaisquer que, a princípio, são selecionados aleatoriamente e não têm conhecimento nenhum do que significa um bom negócio, isto é, o bem ou moeda a ser transacionada também é selecionada aleatoriamente. Dessa forma, um trader pode gastar todas as suas economias comprando uma bomba nuclear de outra sociedade, por exemplo.
Após a transação ser realizada, o bem é adicionado no inventário da sociedade do comprador, a moeda é convertida instantâneamente para moedas da compradora e depositadas na carteira do trader. O preço pago pelo bem é acrescido à carteira do trader vendedor na forma de moedas da sociedade vendedora.
O preço atual da moeda de cada sociedade é armazenado numa matriz. 
Antes da transação seguinte, ou após um certo número de transações, o valores das moedas e bens de uma sociedade devem ser atualizados, assim como suas quantidades. 
Esse ciclo se repete até que o número de transações previamente selecionado seja atingido. Ao final do processo serão plotados gráficos com os dados dos preços das moedas de cada sociedade em função da transação realizada. Número da transação no eixo x, preço da moeda no eixo y.
