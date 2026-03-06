/*
Il programma gestisce una mini rubrica di massimo 10 contatti (nome max 30 char, telefono max 15 char). 
Deve: 
1. Leggere N contatti dall'utente; 
2. Ordinarli alfabeticamente per nome (ricorda: scambia anceh i telefoni); 
3. Stampare la rubrica ordinata; 
4. Chiedere un nome da cercare e stampare il risultato 
*/ 

#include <stdio.h>
#include <string.h>
#define MAX_CONTATTI 10
#define MAX_NOME 30
#define MAX_TELEFONO 15