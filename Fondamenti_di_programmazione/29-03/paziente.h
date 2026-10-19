#ifndef PAZIENTE_H
#define PAZIENTE_H

struct paziente
{
    char cognome[50], nome[50];
    int codice;       /* 1=rosso; 2=arancione; 3=giallo; 4=verde */
    int oraArrivo;
    int minutoArrivo;
    int visitato;     /* 0=in attesa; 1=visitato */
};

void bubleSortPazienti(struct paziente *pazienti, int count, int ordine);
void registraPaziente(struct paziente *p);
void rimuoviPazienteVisitato(struct paziente **pazienti, int *count, int indice);
void cercaPaziente(struct paziente *pazienti, int count, const char *cognome);
void stampaSalaAttesa(struct paziente *pazienti, int count);
void statistichePazienti(struct paziente *pazienti, int count);
void durataAttesa(struct paziente *pazienti, int count);

#endif /* PAZIENTE_H */
