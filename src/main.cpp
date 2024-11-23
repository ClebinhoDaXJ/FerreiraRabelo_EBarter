#include"Ebarter.h"
#include<iostream>

using namespace::std;

int main(){
    World world;
    world.sadd("joquebede", "suado", {2}, {0.78}, {0.4});
    world.gadd("cao", {23, 11, 2}, {0.13, 0.5, 0.6}, {0.1, 0.1, 1.});
    world.srmv("secondSociety");
    world.gadd("picole", {2, 4}, {0.1, 1.}, {0.1, 0.1});
    world.grmv("firstGood");
    world.sadd("china", "cruzadochines", {10, 10}, {15, 5}, {20, 2});
    world.gadd("palito", {11, 1, 20}, {1, 3, 0.5}, {0.2, 1, 0.9});
    world.sadd("tailandia", "bitcoin", {90, 33, 2}, {0.1, 0.2, 0.3}, {0.1, 5, 6});
    world.srmv("china");
    Operation operation(&world, 12);
    cout << "\n\n\n";
    for(int i=0; i<20; i++){
        cout << operation.opMatrix[i][0] << "   " ;
        cout << operation.opMatrix[i][1] << "   " ;
        cout << operation.opMatrix[i][2] << "   " ;
        cout << "\n";
    }
}
