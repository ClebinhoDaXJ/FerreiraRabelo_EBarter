#ifndef __EBARTER_H__
#define __EBARTER_H__

#include<vector>
#include<string>

using namespace::std;

class World;

class Good{
        World* world; //o mundo no qual o bem existe.
    public: 
        Good(){} //default so serve para declaração na classe operation.
        Good(World* mundo, string gname, vector<float> gqval, vector<float> gdval, vector<float> gnval);
        ~Good();
        string _gname;
        unsigned index;
        int totalGood;
        float gvalue;
        vector<vector<float*>> gm; //good matrix.
        vector<float*> gqv; //good quantity vector.
        vector<float*> gdv; //good difficulty vector.
        vector<float*> gnv; //good necessity vector.
        vector<float*> gvv; //good value vector.
        inline void atlzGValue();
        void makeGood(int n_new);
};

class Society{
        World* world; //o mundo no qual a sociedade existe.
    public:
        Society(){} //default so serve para declaração na classe operation.
        Society(World* mundo, string sname, string cname, vector<float> sqval, vector<float> sdval, vector<float> snval, int qtd_moedas=10);
        ~Society();
        string _sname;
        unsigned index;
        string _cname;
        int _totalNativa; //qtd total existente no mundo da moeda nativa.
        float cvalue;
        vector<int> ntvCoin; //vetor de como minha moeda (moeda nativa) está distribuida em cada sociedade, insclusive a minha.
        vector<int> foreignCoins; //vetor de todas as moedas estrangeiras, e própeia moeda, na minha sociedade.
        vector<vector<float*>> sm; //society matrix.
        vector<float*> sqv; //society quantity of the goods vector.
        vector<float*> sdv; //society difficulty of the goods vector.
        vector<float*> snv; //society necessity of the goods vector.
        vector<float*> svv; //society values that are given to the goods.
        inline void atlzCValue();
        inline int convertForeignCoins();
        void makeCoin(int n_new);
};

class World{ //reune todas as sociedades e bens existentes no mundo.
    public:
        World();
        ~World();
        vector<Society*> societies; 
        vector<Good*> goods;
        /*
        Nas matrizes a seguir linhas representam bens
        e colunas representam sociedades. qm[2][3] representa a quantidade 
        do bem da linha 2 na sociedade da coluna 3.
        */
        vector<vector<float*>> qm; //quantity matrix
        vector<vector<float*>> dm; //difficulty matrix
        vector<vector<float*>> nm; //necessity matrix 
        vector<vector<float*>> vm; //value matrix, guarda o valor em GOLD 
        int n_g;
        int n_s;
        void gadd(string name, vector<float> gqval, vector<float> gdval, vector<float> gnval); 
        void sadd(string sname, string cname, vector<float> sqval, vector<float> sdval, vector<float> snval, int qtd_moedas=10);
        void grmv(string name);
        void srmv(string name);
        inline void atlzVM();
}; 

class Operation{
        int n_op; 
        World* world;
        Society* buyer;
        Society* seller;
        Good* good;
        //funções auxiliares de geração aleatória:
        inline int generate(int sup_lim, int inf_lim=0);
        inline int generateQtdG();
        inline int generateQtdC();
        //funções auxiliares de calculo de valor:
    public:
        Operation(World* mundo, int numero_op = 100);
        vector<float> ivv; //instant value vector: guarda os valores de cada moeda em um determindado instante
        vector<vector<float>> opMatrix; 
        //funções principais:
        inline bool OpType();
        inline void generateBuyerSeller();
        inline void generateGood();
        inline void atlzCoin();
        inline void atlzGood();
};

#endif