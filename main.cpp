#include <iostream>
#include <string>
#include <cstring>
#include <windows.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <vector>
#include <sstream>
#include <typeinfo>
#include <cmath>
#include <fstream>
#include "Ebarter.h"

using namespace::std;

#pragma comment(lib, "ws2_32.lib")

// Variáveis globais
World mundo;
int x = 0;
int y = 0;
std::string sname, cname, gname, snametormv, gnametormv;
std::vector<float> qtds, difcs, necs;
int initialQtd = 0;
int numero_op = 0;
int z = 0;

void salvar_em_arquivo(const std::string& nome_arquivo, const std::string& conteudo) {
    // Criar ou abrir o arquivo em modo de escrita
    std::ofstream arquivo(nome_arquivo, std::ios::out);
    
    // Verificar se o arquivo foi aberto com sucesso
    if (arquivo.is_open()) {
        arquivo << conteudo;  // Escrever o conteúdo no arquivo
        arquivo.close();      // Fechar o arquivo
        std::cout << "Conteúdo salvo no arquivo: " << nome_arquivo << std::endl;
    } else {
        std::cerr << "Erro ao abrir o arquivo: " << nome_arquivo << std::endl;
    }
}

std::vector<float> parseLista(const std::string& str) {
    std::vector<float> lista;
    std::stringstream ss(str);
    std::string item;

    while (std::getline(ss, item, ';')) {
        try {
            lista.push_back(std::stof(item));
        } catch (const std::exception& e) {
            std::cerr << "Erro ao converter valor para float: " << item << std::endl;
        }
    }

    return lista;
}

void processarMensagemy1(const std::string& mensagem) {
    std::istringstream stream(mensagem);
    std::string token;

    while (std::getline(stream, token, '|')) {
        auto pos = token.find('=');
        if (pos != std::string::npos) {
            std::string chave = token.substr(0, pos);
            std::string valor = token.substr(pos + 1);

            if (chave == "sname") {
                sname = valor;
            } else if (chave == "cname") {
                cname = valor;
            } else if (chave == "qtds") {
                qtds = parseLista(valor);
            } else if (chave == "difcs") {
                difcs = parseLista(valor);
            } else if (chave == "necs") {
                necs = parseLista(valor);
            } else if (chave == "initialQtd") {
                initialQtd = std::stoi(valor);
            }
        }
    }

    // Exibir os valores recebidos
    std::cout << "Sociedade Criada: " << sname << std::endl;
    std::cout << "Moeda: " << cname << std::endl;
    std::cout << "Quantidade Inicial: " << initialQtd << std::endl;
    std::cout << "Bens: ";
    for (float q : qtds) std::cout << q << " ";
    std::cout << "\nDificuldades: ";
    for (float d : difcs) std::cout << d << " ";
    std::cout << "\nNecessidades: ";
    for (float n : necs) std::cout << n << " ";
    std::cout << std::endl;

    // Verificar os tipos das variáveis
    std::cout << "Tipo de qtds: " << typeid(qtds).name() << std::endl;
    std::cout << "Tipo de difcs: " << typeid(difcs).name() << std::endl;
    std::cout << "Tipo de necs: " << typeid(necs).name() << std::endl;

    std::cout << "qtds.size()" << qtds.size() << std::endl;
}

void processarMensagemy2(const std::string& mensagem) {
    std::istringstream stream(mensagem);
    std::string token;

    while (std::getline(stream, token, '|')) {
        auto pos = token.find('=');
        if (pos != std::string::npos) {
            std::string chave = token.substr(0, pos);
            std::string valor = token.substr(pos + 1);

            if (chave == "gname") {
                gname = valor;
            } else if (chave == "qtds") {
                qtds = parseLista(valor);
            } else if (chave == "difcs") {
                difcs = parseLista(valor);
            } else if (chave == "necs") {
                necs = parseLista(valor);
            }
        }
    }

    // Exibir os valores recebidos
    std::cout << "Bem criado: " << gname << std::endl;
    std::cout << "Vetor qtd bens: ";
    for (float q : qtds) std::cout << q << " ";
    std::cout << "\nVetor de dificuldades: ";
    for (float d : difcs) std::cout << d << " ";
    std::cout << "\nVetor de necessidades: ";
    for (float n : necs) std::cout << n << " ";
    std::cout << std::endl;

    // Verificar os tipos das variáveis
    std::cout << "Tipo de qtds: " << typeid(qtds).name() << std::endl;
    std::cout << "Tipo de difcs: " << typeid(difcs).name() << std::endl;
    std::cout << "Tipo de necs: " << typeid(necs).name() << std::endl;

    std::cout << "qtds.size() " << qtds.size() << std::endl;
}

void processarMensagemy3(const std::string& mensagem) {
    std::istringstream stream(mensagem);
    std::string token;

    while (std::getline(stream, token, '|')) {
        auto pos = token.find('=');
        if (pos != std::string::npos) {
            std::string chave = token.substr(0, pos);
            std::string valor = token.substr(pos + 1);

            if (chave == "snametormv") {
                snametormv = valor;
            } 
        }
    }

    // Exibir os valores recebidos
    std::cout << "Sociedade a ser removida: " << snametormv << std::endl;
    std::cout << std::endl;
}

void processarMensagemy4(const std::string& mensagem) {
    std::istringstream stream(mensagem);
    std::string token;

    while (std::getline(stream, token, '|')) {
        auto pos = token.find('=');
        if (pos != std::string::npos) {
            std::string chave = token.substr(0, pos);
            std::string valor = token.substr(pos + 1);

            if (chave == "gnametormv") {
                gnametormv = valor;
            } 
        }
    }

    // Exibir os valores recebidos
    std::cout << "Bem a ser removido: " << gnametormv << std::endl;
    std::cout << std::endl;
}

void processarMensagemy5(const std::string& mensagem) {
    std::istringstream stream(mensagem);
    std::string token;

    while (std::getline(stream, token, '|')) {
        auto pos = token.find('=');
        if (pos != std::string::npos) {
            std::string chave = token.substr(0, pos);
            std::string valor = token.substr(pos + 1);

            if (chave == "numero_op") {
                numero_op = std::stoi(valor);
            } else if (chave == "z"){
                z = std::stoi(valor);
            }
        }
    }

    // Exibir os valores recebidos
    std::cout << "Número de operações: " << numero_op << std::endl;
    std::cout << "Índice da sociedade: " << z << std::endl;
    std::cout << std::endl;
}


DWORD WINAPI tratarCliente(LPVOID clienteSocket) {
    SOCKET socket = *(SOCKET*)clienteSocket;
    char buffer[1024];

    while (true) {
        memset(buffer, 0, sizeof(buffer));
        int bytesRecebidos = recv(socket, buffer, sizeof(buffer) - 1, 0);

        if (bytesRecebidos <= 0) {
            std::cout << "Conexão encerrada pelo cliente." << std::endl;
            break;
        }

        std::string mensagem(buffer);
        std::cout << "Mensagem recebida: " << mensagem << std::endl;
        
        if (x==1 && y==1) {
            processarMensagemy1(mensagem);
            mundo.sadd(sname, cname, qtds, difcs, necs, initialQtd);
            y=0;
        } else if (x==1 && y==2) {
            processarMensagemy2(mensagem);
            mundo.gadd(gname, qtds, difcs, necs);
            y=0;
        } else if (x==1 && y==3) {
            processarMensagemy3(mensagem);
            mundo.srmv(snametormv);
            y=0;
        } else if (x==1 && y==4) {
            processarMensagemy4(mensagem);
            mundo.grmv(gnametormv);
            y=0;
        } else if (x==1 && y==5) {
            processarMensagemy5(mensagem);

            Operation operation(&mundo, numero_op);
            if(z < 0 || z >= mundo.n_s) continue;
            vector<float> coinValue;
            for(int i=0; i<numero_op; i++)
                coinValue.push_back(operation.opMatrix[i][z]);

            // Substituir "NaN" pelo valor anterior
            for (size_t i = 0; i < coinValue.size(); ++i) {
                if (std::isnan(coinValue[i]) && i > 0) {
                    coinValue[i] = coinValue[i - 1];
                }
            }
                        
            std::ostringstream oss;
            for (size_t i = 0; i < coinValue.size(); ++i) {
                oss << coinValue[i];
                if (i < coinValue.size() - 1) oss << ";";
            }
            std::string coinValueStr = oss.str();
            salvar_em_arquivo("simulacao.txt", coinValueStr);
            y=0;
        }
        

        // Atualiza as variáveis `x` e `y` conforme as mensagens recebidas
        if (mensagem == "x=1") {
            x = 1;
            std::cout << "Variável x alterada para: " << x << std::endl;
        } else if (mensagem == "y=1") {
            y = 1;
            std::cout << "Variável y alterada para: " << y << std::endl;
        } else if (mensagem == "y=2"){
            y = 2;
            std::cout << "Variável y alterada para: " << y << std::endl;
        } else if (mensagem == "y=3"){
            y = 3;
            std::cout << "Variável y alterada para: " << y << std::endl;
        } else if (mensagem == "y=4"){
            y = 4;
            std::cout << "Variável y alterada para: " << y << std::endl;
        } else if (mensagem == "y=5"){
            y = 5;
            std::cout << "Variável y alterada para: " << y << std::endl;
        }       
    }

    closesocket(socket);
    return 0;
}

int main() {
    const int porta = 12345;
    WSADATA wsaData;

    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "Erro ao inicializar o Winsock." << std::endl;
        return -1;
    }

    SOCKET servidorSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (servidorSocket == INVALID_SOCKET) {
        std::cerr << "Erro ao criar o socket." << std::endl;
        WSACleanup();
        return -1;
    }

    sockaddr_in enderecoServidor;
    enderecoServidor.sin_family = AF_INET;
    enderecoServidor.sin_addr.s_addr = INADDR_ANY;
    enderecoServidor.sin_port = htons(porta);

    if (bind(servidorSocket, (sockaddr*)&enderecoServidor, sizeof(enderecoServidor)) == SOCKET_ERROR) {
        std::cerr << "Erro ao vincular o socket." << std::endl;
        closesocket(servidorSocket);
        WSACleanup();
        return -1;
    }

    if (listen(servidorSocket, 5) == SOCKET_ERROR) {
        std::cerr << "Erro ao iniciar o modo de escuta." << std::endl;
        closesocket(servidorSocket);
        WSACleanup();
        return -1;
    }

    std::cout << "Servidor em execução na porta " << porta << "..." << std::endl;

    while (true) {
        sockaddr_in enderecoCliente;
        int tamanhoCliente = sizeof(enderecoCliente);
        SOCKET clienteSocket = accept(servidorSocket, (sockaddr*)&enderecoCliente, &tamanhoCliente);

        if (clienteSocket == INVALID_SOCKET) {
            std::cerr << "Erro ao aceitar conexão." << std::endl;
            continue;
        }

        std::cout << "Cliente conectado." << std::endl;

        // Cria uma thread para tratar o cliente usando WinAPI
        CreateThread(nullptr, 0, tratarCliente, &clienteSocket, 0, nullptr);
    }

    closesocket(servidorSocket);
    WSACleanup();
    return 0;
}
