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

## Classes - chave:

SOCIETY: Consiste de uma lista de bens e seus valores. Ela possui uma moeda característica, esta tem um preço em Gold que depende da quantidade de moedas e do poder de compra dela: preçoMoeda = poder/qtd. Novos bens podem ser gerados em uma sociedade. Sociedades diferentes dão valores diferentes a mesmos bens, por exemplo, o valor de um computador no Brasil é mais alto que nos Estados Unidos devido à dificuldade de produção.     

BENS: Possui Nome, quantidade disponível em certa sociedade, o valor que ele possui na sociedade em questão dependerá de três parâmetros: quantidade atual de bens, necessidade dos bens, dificuldade de produção. Também contém uma lista de preços desse bem em todas as sociedades.

OPERAÇÃO_BENS: Responsável por englobar todas as características de uma operação de bens: a sociedade compradora, a sociedade vendedora, o bem que foi transacionado. Em seguida o valor dos bens e da moeda são atualizados em ambas as sociedades.    

OPERAÇÃO_MOEDAS: Responsável por englobar todas as características de uma operação de medas: a sociedade compradora, a sociedade vendedora, o bem que foi transacionado. Aqui há apenas atualização no valor das moedas, não dos bens. Quando uma moeda é comprada do exterior seu valor é mantido ainda na sociedade compradora, contudo esse valor deve ser atualizado conforme as mudanças no valor da moeda comprada. Uma consequência interessante disso é que se não houver uma transação de bens o valor de uma moeda nunca é atualizado, mesmo que hajam transação de moedas, pois a atualização no valor de uma moeda é consequência da atualização do valor de outra.

## Dinâmica do programa

O valor de uma moeda é intimamente relacionado com o preço dos bens em uma sociedade, quanto menor o preço dos bens, maior o valor da moeda (porque é possível comprar mais com menos) e vice-versa.
Haverá um referencial de valor. O referencial é uma constante global chamada Gold, os valores tanto dos bens quanto das moedas serão definidos por meio desse padrão.

A princípio as transações ocorrerão aleatoriamente entre duas sociedades, há  um número predeterminado de transações que podem ser realizadas.  
O preço atual da moeda de cada sociedade é armazenado numa matriz. 
Antes da transação seguinte, ou após um certo número de transações, o valores das moedas e bens de uma sociedade devem ser atualizados, assim como suas quantidades. 
Esse ciclo se repete até que o número de transações previamente selecionado seja atingido. Ao final do processo serão plotados gráficos com os dados dos preços das moedas de cada sociedade em função da transação realizada. Número da transação no eixo x, preço da moeda no eixo y.
