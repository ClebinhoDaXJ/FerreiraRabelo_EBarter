#include"Ebarter.h"
#include<iostream>
#include<vector>
#include<string>

using namespace::std;

int main(){
    //janela inicial.
    int x = 100;
    do{
        int y = 100;
        x = getfrompy();

        //criar nova simulação;
        if(x==1){
            do{
                y = getfrompy();

                World mundo;

                //adicionar nova sociedade.
                if(y==1){
                    //envia o numero de bens (dim. dos vetores de sociedade).
                    sendtopy(world.n_g);
                    //recebe os inputs.
                    string sname = getfrompy();
                    string cname = getfrompy();
                    int initialCQtd = getfrompy();
                    vector<float> qtds = getfrompy();
                    vector<float> difs = getfrompy();
                    vector<float> necs = getfrompy();
                    //adiciona a socedade ao mundo (simulação).
                    mundo.sadd(sname, cname, qtds, difs, necs, initialCQtd);
                }

                //adicionar novo bem.
                if(y==2){
                    //envia o numero de sociedades (dim. dos vetores de bem).
                    sendtopy(world.n_s);
                    //recebe os inputs.
                    string gname = getfrompy();
                    vector<float> qtds = getfrompy();
                    vector<float> difs = getfrompy();
                    vector<float> necs = getfrompy();
                    //adiciona a socedade ao mundo (simulação).
                    mundo.gadd(gname, qtds, difs, necs);
                }

                //remover sociedade.
                if(y==3){
                    if(mundo.n_s <= 2){
                        //mandar esse texto para frontend de alguma forma.
                        cout << "nao é possível remover mais sociedades, só existem duas." << endl;
                    }
                    else{
                        string snametormv = getfrompy();
                        mundo.srmv(snametormv);
                    }
                }

                //remover bem.
                if(y==4){
                    if(mundo.n_g <= 1){
                        //mandar esse texto para frontend de alguma forma.
                        cout << "nao é possível remover mais bem, só existe um." << endl;
                    }
                    else{
                        string gnametormv = getfrompy();
                        mundo.grmv(gnametormv);
                    }
                }

                //realizar a simulação.
                if(y==5){
                    int z = 10000;
                    do{
                        //recebe o numero de transações a serem feitas.
                        int numero_op = getfrompy();
                        //realiza as operações.
                        Operation operation(&mundo, numero_op);
                        //recebe o indice da sociadade que se deseja visualizar o grafico.
                        z = getfrompy();
                        //encerra a iteração se o indice recebido for inválido.
                        if(z < 0 || z >= mundo.n_s) continue;
                        //gera o vetor de cvalues ao longo das transações
                        vector<float> coinValue;
                        for(int i=0; i<numero_op; i++)
                            coinValue.push_back(operation.opMatrix[i][z]);
                        //envia esse vetor para o front, para ser transformado em grafico.
                        sendtopy(coinValue);
                    }
                    while(z < 0 || z >= mundo.n_s);
                }
            }
            while(y);
        }

        //entrar em simulações arquivadas.
        if(x==2){
            //...
        }
    }
    while(x)
}