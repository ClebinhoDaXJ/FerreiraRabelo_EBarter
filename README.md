# E-Barter
Ideia chave:
*criar uma simulação de ecônomia em um "mundo" com diversas sociedades.

Objetivo final:
O usuário do app vai poder ajustar valores de parametros para mudar a forma como o valor de uma moeda muda ao longo do tempo e, com isso, 
tentar ajustar o grafico valorXtempo com gráficos reais, aprendendo o que pode causar a variação do preço de uma moeda real. 

Fatores que levam à variação do valor da moeda:
*produtos originários da sociedade.
*negociação desses produtos dentro da própria sociedade.
*negociação dos produtos com outras sociedades.
*um indíviduo de determindada sociedade pode possuir parte de sua riqueza como moeda de outra sociedade.

OBS: 
a ideia com esse trabalho NÃO É PREVER preços de ações e moedas, mas sim observar como eles variam
de acordo com a mudança de certos parâmetros, a mudança destes parâmetros pode, ou não, se aproximar do que ocorre no mundo real, apesar do modelo se basear na economia estudada em sociedades reais. 


## Interface gráfica

Para interface gráfica do E-Barter será usada a biblioteca gráfica de Pyhon CustomTkinter.

Basta, instalá-la e importá-la no código. Funções como CTk() criam uma janela. O tamanho desta pode ser ajustada pela função geometry("dim1xdim2"). Para que a janela apareça é necessário criar um loop usando a função mainloop().

Para escrever algo na janela, basta usar a função CTklabel(janela,"text"), para adicionar uma imagem usa-se CTkImage(imagem = Image.open("imagem.png"). Cada texto ou atributo adicionado na janela pode ter sua posição ajustada pela função pack().

Pode-se adicionar um botão com CTkButton(janela,"text") e ele pode chamar uma função quando ativado: CTkButton(janela,"text",commad=function).
