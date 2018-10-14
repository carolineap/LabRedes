/*
	Laboratório de Redes de Computadores - Implementação RIP
	Caroline Aparecida de Paula Silva - 726506
	Isabela Sayuri Matsumoto - 726539
*/

#include <stdio.h>

typedef struct rtpkt {
	int source_id;
	int dest_id;
	int minCost[4];
} Pkt;


typedef struct nodes {
	int distTable[4][4];
} Node;

void rtinit0();
void rtupdate0(Pkt *p);
void rtinit1();
void rtupdate1(Pkt *p);
void rtinit2();
void rtupdate2(Pkt *p);
void rtinit3();
void rtupdate3(Pkt *p);
void printTable(int distTable[4][4]);

int main () {
	
	Node node[4];
	/* inicializa com os custos */
	int connCosts[4][4] = {0, 1, 3, 7, 1, 0, 1, 999, 3, 1, 0, 2, 7, 999, 2, 0};


	return 0;
}

void rtinit0() {
	
}

void rtupdate0(Pkt *p) {

}

void rtinit1() {

}

void rtupdate1(Pkt *p) {

}

void rtinit2() {

}

void rtupdate2(Pkt *p) {

}

void rtinit3() {

}

void rtupdate3(Pkt *p) {

}

void printTable(int distTable[4][4]){

}
