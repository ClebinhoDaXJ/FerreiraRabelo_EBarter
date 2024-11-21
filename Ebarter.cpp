#include"Ebarter.h"
#include<iostream>
#include<vector>
#include<random>
#include<chrono>

Good::Good(World* mundo, string gname, vector<float> gqval, vector<float> gdval, vector<float> gnval){
    world = mundo;
    unsigned dim = world->n_s;
    if(gqval.size() != dim){
        cout << "Deve-se especificar uma quantidade do bem para cada sociedade.\n\n";
        return;
    }
    if(gdval.size() != dim){
        cout << "Deve-se especificar a dificuldade que cada sociedade tem para produzir esse bem.\n\n";
        return;
    }
    if(gnval.size() != dim){
        cout << "Deve-se especificar a necessidade que cada sociedade tem de possuir este bem.\n\n";
        return;
    }
    
    _gname = gname;
    index = world->n_g;

    int initialQtd = 0;
    for(int i=0; i<world->n_s; i++)
        initialQtd += gqval[i];
    totalGood = initialQtd;

    for(unsigned i=0; i<dim; i++){
        float* ptrq = new float(gqval[i]);
        float* ptrd = new float(gdval[i]);
        float* ptrn = new float(gnval[i]);
        float valor;
        if(gqval[i] == 0)
            valor = gdval[i]*gnval[i]/0.5; //aleatoriamente 0.5.
        else 
            valor = gdval[i]*gnval[i]/gqval[i]; //valor = dificuldade*necessidade/quantidade;
        float* ptrv = new float(valor);
        gqv.push_back(ptrq);
        gdv.push_back(ptrd);
        gnv.push_back(ptrn);
        gvv.push_back(ptrv);
    }
    if(dim != 0){
        //constroi a matriz do good.
        gm.push_back(gqv);
        gm.push_back(gdv);
        gm.push_back(gnv);
        gm.push_back(gvv);
    }
    else{
        //caso dim == 0 inicializa cada um dos vetores de bem com 1 elemento 0.
        gqv.push_back({});
        gdv.push_back({});
        gnv.push_back({});
        gvv.push_back({});
    }
    //fornece um valor inicial para o bem.
    int sum = 0;
    if(world->n_s != 0){
        for(int i=0; i<world->n_s; i++)
            sum += *gqv[i]**gvv[i];
        gvalue = sum/totalGood;
    }
    else{
        /*
        esse valor aqui é relevante, mas não sei o que ele afeta ainda, 
        então só coloquei 0.5 pra poder inicializar quando não houverem sociedades ainda.
        */ 
        gvalue = 0.5;
    }
}

Good::~Good(){
    for(unsigned i=0; i<world->n_s; i++){
        delete gqv[i];
        delete gdv[i];
        delete gnv[i];
        delete gvv[i];
    }
    //OBS: quando a instância é destruida seus vetores membros também são liberados.
}

inline void Good::atlzGValue(){
    float sum = 0;
    for(int i=0; i<world->n_s; i++){
        sum += (*world->vm[index][i])*(*world->qm[index][i]);
    }
    //valor intrínseco do bem é a média ponderada dos valores que ele tem em cada sociedade.
    gvalue = sum/totalGood;
}


Society::Society(World* mundo, string sname, string cname, vector<float> sqval, vector<float> sdval, vector<float> snval, int qtd_moedas){
    world = mundo;
    unsigned dim = world->n_g;
    int n_sociedades = world->n_s;
    if(sqval.size() != dim){
        cout << "Deve-se especificar o quanto de cada bem existente esta sociedade tem.\n\n";
        return;
    }
    if(sdval.size() != dim){
        cout << "Deve-se especificar a dificuldade que esta sociedade tem para produzir cada bem existente.\n\n";
        return;
    }
    if(snval.size() != dim){
        cout << "Deve-se especificar a necessidade que esta sociedade tem de possuir cada bem.\n\n";
        return;
    }

    _sname = sname;
    _cname = cname;
    _totalNativa = qtd_moedas;
    index = n_sociedades; 
    //inicializar os vetores de moeda.
    for(unsigned i=0; i<index; i++){
        ntvCoin.push_back(0);
        foreignCoins.push_back(0);
    }
    ntvCoin.push_back(_totalNativa);
    foreignCoins.push_back(_totalNativa);
    //inicializar os vestores de bens desta sociedade.
    for(unsigned i=0; i<dim; i++){
        float* ptrq = new float(sqval[i]);
        float* ptrd = new float(sdval[i]);
        float* ptrn = new float(snval[i]);
        float valor;
        if(sqval[i] == 0)
            valor = sdval[i]*snval[i]/0.5; //aleatoriamente 0.5.
        else  
            valor = sdval[i]*snval[i]/sqval[i]; //valor = dificuldade*necessidade/quantidade;
        float* ptrv = new float(valor);
        sqv.push_back(ptrq);
        sdv.push_back(ptrd);
        snv.push_back(ptrn);
        svv.push_back(ptrv); 
    }
    if(dim != 0){
        sm.push_back(sqv);
        sm.push_back(sdv);
        sm.push_back(snv);
    }
    //fornece um valor inicial para a moeda.
    float sum = 0;
    for(int i=0; i<world->n_g; i++)
            sum += *sqv[i]/(1+*svv[i]);
    cvalue = sum/_totalNativa;
    cout << _sname << ": valor inicial da moeda: " << cvalue << endl;
}

Society::~Society(){
    for(unsigned i=0; i<world->n_g; i++){
        delete sqv[i];
        delete sdv[i];
        delete snv[i];
        delete svv[i];
    }
    //OBS: quando a instância é destruida seus vetores membros também são liberados.
}

inline void Society::atlzCValue(){
    _totalNativa = convertForeignCoins();
    float sum = 0;
    /*
    o valor da moeda é inverso ao valor dos bens naquela sociedade,
    se um bem é muito valioso é porque minha moeda é fraca e eu não
    consigo comprá-lo tão facilmente.
    */
    for(int i=0; i<world->n_g; i++)
        sum += *world->qm[i][index]/(1 + *world->vm[i][index]);
    cvalue = sum/(1 + _totalNativa);  
    if(cvalue > 1000)
        cvalue = 1000;
    if(cvalue < 0.01)
        cvalue = 0.2;
}

inline int Society::convertForeignCoins(){
    /*
    Acho que essa função é meio problemática no sentido de converter
    todas as foreigcoins em moedas nativas de uma só vez e num tempo determinado
    pela negociação de bens, quer dizer, não é isso que acontece na realidade.
    OPORTUNIDADE DE MELHORIA NESSA FUNÇÃO AQUI!
    */
    int sum = foreignCoins[index];
    for(unsigned i=0; i<world->n_s; i++){
        if(i != index){ 
            sum += foreignCoins[i]*(world->societies[i]->cvalue)/(0.0001+cvalue);
            foreignCoins[i] = 0;
        }
    }
    foreignCoins[index] = sum;
    return sum;
}

/*
da forma que eu defini o construtor Society() não recomendo tentar declarar uma instância
de Society separadamente, isto é, fora do mundo e sem usar a função sadd.
*/

World::World(){
    n_s = 0; n_g = 0;
    gadd("firstGood", {}, {}, {});
    sadd("firstSociety", "firstCoin", {0.1}, {0.2}, {0.3});
    sadd("secondSociety", "secondCoin", {0.}, {0.}, {0.});
}

World::~World(){
    for(int i=0; i<n_g ;i++)
        delete goods[i];
    for(int i=0; i<n_s; i++)
        delete societies[i];
    goods.clear();
    societies.clear();
}

void World::gadd(string gname, vector<float> gqval, vector<float> gdval, vector<float> gnval){ 
    for(int i=0; i<n_g; i++){
        if(goods[i]->_gname == gname){
            cout << "Nome de bem já existente, escolha outro!\n";
            return;
        }
    }
    //necessário armazenar a informação no heap para não ser destruída ao fim de gadd.
    Good* new_good = new Good(this, gname, gqval, gdval, gnval);
    goods.push_back(new_good);
    //adiciona uma nova linha às matrizes de quantidade, dificuldade e necessidade.
    qm.push_back(new_good->gqv);
    dm.push_back(new_good->gdv);
    nm.push_back(new_good->gnv);
    vm.push_back(new_good->gvv);
    n_g++;
    //adiciona novos elementos ao vetores de sociedade.
    for(int i=0; i<n_s; i++){
        societies[i]->sqv.push_back(new_good->gqv[i]);
        societies[i]->sdv.push_back(new_good->gdv[i]);
        societies[i]->snv.push_back(new_good->gnv[i]);
        societies[i]->svv.push_back(new_good->gvv[i]);
    } 
}

void World::sadd(string sname, string cname, vector<float> sqval, vector<float> sdval, vector<float> snval, int qtd_moedas){   
    for(int i=0; i<n_s; i++){
        if(societies[i]->_sname == sname){
            cout << "Nome de sociedade já existente, escolha outro!\n";
            return;
        } 
    }
    //necessário armazenar a informação no heap para não ser destruída ao fim de gadd.
    Society* new_society = new Society(this, sname, cname, sqval, sdval, snval, qtd_moedas);
    societies.push_back(new_society);
    //cria o primeiro elemento de cada matriz, antes estes espaços estavam inicializados
    //e vazios pelo First good.
    if(n_s == 0){
        qm[0][0] = new_society->sqv[0];
        dm[0][0] = new_society->sdv[0];
        nm[0][0] = new_society->snv[0];
        vm[0][0] = new_society->svv[0];
        n_s++;
        goods[0]->gqv[0] = new_society->sqv[0];
        goods[0]->gdv[0] = new_society->sdv[0];
        goods[0]->gnv[0] = new_society->snv[0];
        goods[0]->gvv[0] = new_society->svv[0];
    }
    else{
        //adiciona uma nova coluna às matrizes de quantidade, dificuldade e necessidade.
        for(int i=0; i<n_g; i++){
            qm[i].push_back(new_society->sqv[i]);
            dm[i].push_back(new_society->sdv[i]);
            nm[i].push_back(new_society->snv[i]);
            vm[i].push_back(new_society->svv[i]);
        }
        n_s++;
        //asiciona os novos elemetos aos vetores de bens.
        for(int i=0; i<n_g; i++){
            goods[i]->gqv.push_back(new_society->sqv[i]);
            goods[i]->gdv.push_back(new_society->sdv[i]);
            goods[i]->gnv.push_back(new_society->snv[i]);
            goods[i]->gvv.push_back(new_society->svv[i]);
            goods[i]->totalGood += *new_society->sqv[i];
        }
    }
    //aumenta a dimensão dos vetores de moeda das demais sociedades.
    for(int i=0; i<n_s; i++){
        societies[i]->ntvCoin.push_back(0);
        societies[i]->foreignCoins.push_back(0);
    }
}

void World::grmv(string gname){
    //procura o ponteiro que guarda o bem a ser removido.
    for(unsigned i=0; i<n_g; i++){
        if(goods[i]->_gname == gname){
            //OBS: antes eu usei 'goods[i]->~Good();' mas não destruia pq o goods[i] é um ponteiro no heap.
            delete goods[i];
            //dá um shift para trás em todos os elementos após o eliminado.
            goods.erase(goods.begin()+i);
            //elimina uma linha de cada matriz.
            qm.erase(qm.begin()+i);
            dm.erase(dm.begin()+i);
            nm.erase(nm.begin()+i); 
            vm.erase(vm.begin()+i);
            //diminui um elemento de cada vetor de sociedade.
            for(int j=0; j<n_s; j++){
                societies[j]->sqv.erase(societies[j]->sqv.begin()+i);
                societies[j]->sdv.erase(societies[j]->sdv.begin()+i);
                societies[j]->snv.erase(societies[j]->snv.begin()+i);
                societies[j]->svv.erase(societies[j]->svv.begin()+i);
            }
            //diminui o numero total de bens em 1 unnidade.
            n_g--;
            //abaixa o indice dos bens apos o que foi eliminado em 1 unidade.
            for(int k=i; k<n_g; k++) 
                goods[k]->index--;
            return;
        }
        //caso chegue na última posição sem encontrar o nome.
        if(i == n_g-1){
            cout << "nao existe um bem com esse nome.\n";
            return;
        }
    }
}

void World::srmv(string sname){
    //procura o ponteiro que guarda a sociedade a ser removida.
    for(unsigned j=0; j<n_s; j++){
        if(societies[j]->_sname == sname){
            //OBS: usar 'societies[j]->~Society();' não dá certo pq a instancia está alocada no heap.
            delete societies[j];
            //dá um shift para trás em todos os elementos após o eliminado.
            societies.erase(societies.begin()+j);
            for(int i=0; i<n_g; i++){
                qm[i].erase(qm[i].begin()+j);
                dm[i].erase(dm[i].begin()+j);
                nm[i].erase(nm[i].begin()+j);
                vm[i].erase(vm[i].begin()+j);
                //elimina um elemento de cada vetor de bem.
                goods[i]->gqv.erase(goods[i]->gqv.begin()+j);
                goods[i]->gdv.erase(goods[i]->gdv.begin()+j);
                goods[i]->gnv.erase(goods[i]->gnv.begin()+j);
                goods[i]->gvv.erase(goods[i]->gvv.begin()+j);
                //elimina um elemento de cada vetor sociedade.
            }
            //diminui o numero total de sociedades em 1 unidade.
            n_s--;
            //diminui um elemento dos vetores moeda de cada sociedade.
            for(int i=0; i<n_s; i++){
                societies[i]->ntvCoin.erase(societies[i]->ntvCoin.begin()+j);
                societies[i]->foreignCoins.erase(societies[i]->foreignCoins.begin()+j);
            }
            //abaixa o indice das sociedades apos a que foi eliminada em 1 unidade. 
            for(int k=j; k<n_s; k++) 
                societies[k]->index--;
            return;
        }
        //dá um shift para trás em todos os elementos após o eliminado.
        if(j == n_s-1){
            cout << "nao existe uma socidade com esse nome.\n";
            return;
        }
    }
}

inline void World::atlzVM(){
    for(int i=0; i<n_g; i++){
        for(int j=0; j<n_s; j++)
            *vm[i][j] = ((*dm[i][j])*(*nm[i][j])/(*qm[i][j]))*goods[i]->gvalue; 
    }
}


Operation::Operation(World* mundo, int numero_op){
    world = mundo;
    if(world->n_s < 2){
        std::cout << "nao e possivel realizar operação alguma, o mundo possui apenas uma sociedade.";
        return;
    }
    n_op = numero_op;
    for(int i=0; i<n_op; i++){ 
    /*
    OpType == 0: compra de moedas, OpType == 1 compra de bens.
    A ideia é que os valores de bens e moedas são atualizados somente nas vezes em que ocorre 
    uma transação de bem. Pq na minh aconcepção o bem é que dá valor ao dinheiro kk.
    Quando uma transação de bem é realizada todos os valores das moedas estrangeiras que a sociedade
    possui são convertidos para valores de sua moeda nativa, como se ele consolidasse a compra da outra moeda,
    isso vai fazer o valor das moedas mudar ao longo do tempo. 
    */
        for(int j=0; j<world->n_s; j++)
            ivv.push_back(world->societies[j]->cvalue);
        opMatrix.push_back(ivv);
        ivv.clear();
        if(OpType()){ 
            cout << "op_de_bem" << endl;
            generateBuyerSeller();
            generateGood();
            atlzGood();
            good->atlzGValue();
            buyer->atlzCValue();
            seller->atlzCValue();
            world->atlzVM();
        }
        else{
            cout << "op_de_moeda" << endl;
            generateBuyerSeller();
            atlzCoin();
        }
    }
}

inline int Operation::generate(int sup_lim, int inf_lim){
    static int counter = 0;
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::mt19937 gen(seed + counter++);
    std::uniform_int_distribution<> dist(inf_lim, sup_lim);
    return dist(gen);
}

inline void Operation::generateBuyerSeller(){
    int sup_lim = world->n_s-1;
    int buyer_index = generate(sup_lim);
    int seller_index = generate(sup_lim);
    buyer = world->societies[buyer_index];
    seller = world->societies[seller_index];
    if(buyer_index == seller_index)
        generateBuyerSeller();
    else
        cout << buyer->_sname << "\t" << seller->_sname << endl;
    return;
}

inline bool Operation::OpType(){
    bool coinOrGood = generate(1);
    return coinOrGood;
}

inline void Operation::generateGood(){
    int sup_lim = world->n_g-1;
    int good_index = generate(sup_lim);
    good = world->goods[good_index];
    cout << good->_gname << endl;
}

inline int Operation::generateQtdG(){
    //o vendedor não pode vender mais bens do que possui.
    int totalInSeller = (int)*world->qm[good->index][seller->index];
    int qtd = generate(totalInSeller);
    return qtd;
}

inline int Operation::generateQtdC(){
    float cBv = buyer->cvalue;
    float cSv = seller->cvalue;
    int totalBueyer = buyer->ntvCoin[buyer->index];
    int totalSeller = seller->ntvCoin[seller->index];
    int sup_lim;
    cout << "---------------" << endl;
    cout << cBv << "  " << cSv << endl;
    cout << totalBueyer << "  " << totalSeller << endl;
    cout << "---------------" << endl;
    //deves-se converter os valores de sup_lim na moeda do comprador, pq é ela que eu estou usando no generate.
    if(totalBueyer*cBv >= totalSeller*cSv){
        sup_lim = totalSeller*cSv/cBv;
        cout << "sup_lim = " << totalSeller << "*" << cSv << "/" << cBv << endl;
    }
    else{
        sup_lim = totalBueyer; 
        cout << "sup_lim = " << totalBueyer << endl;
    }
    int qtd1 = generate(sup_lim);
    return qtd1;
}

inline void Operation::atlzCoin(){
    /*
    qtd1 é o valor da trnasação em moedas nativas do comprador.
    qtd2 é o valor da trnasação em moedas nativas do vendedor.
    note que qtd1 = qtd2 se convertermos seus preços para o referencial GOLD.
    */
    int qtd1 = generateQtdC(); //número de moedas cedidas pelo comprador.
    float qtd2 = qtd1*(buyer->cvalue/seller->cvalue); //número de moedas cedidas pelo vendedor.
    cout << "quantidade buyer: " << qtd1 << " quantidade seller: " << qtd1 << "*" << buyer->cvalue << "/" << seller->cvalue << endl;
    //atualizar os valores nos veotores de moeda de ambas as sociedades.
    buyer->ntvCoin[buyer->index] -= qtd1;
    buyer->ntvCoin[seller->index] += qtd1;
    buyer->foreignCoins[buyer->index] -= qtd1;
    buyer->foreignCoins[seller->index] += qtd2;
    seller->ntvCoin[seller->index] -= qtd2;
    seller->ntvCoin[buyer->index] += qtd2;
    seller->foreignCoins[seller->index] -= qtd2;
    seller->foreignCoins[buyer->index] += qtd1;
}

inline void Operation::atlzGood(){
    //calcula o preço de uma unidade do bem na moeda do comprador.
    float price = *world->vm[good->index][buyer->index]/buyer->cvalue;
    //sorteia a quantidade de bens na transação.
    int qtd = generateQtdG();
    //entra num loop para verificar se o comprador tem dinheiro pra pagar.
    cout << "numero de bens trocados: " << qtd << endl;
    //é realizada a troca dos bens.
    *(world->qm[good->index][buyer->index]) += qtd;
    *(world->qm[good->index][seller->index]) -= qtd;
    //é ralizado o pagamento.
    world->societies[buyer->index]->ntvCoin[buyer->index] -= qtd*price;
    world->societies[buyer->index]->foreignCoins[buyer->index] -= qtd*price;
    world->societies[seller->index]->foreignCoins[buyer->index] += qtd*price;
}
