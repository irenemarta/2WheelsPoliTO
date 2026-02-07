"""
Modelli dati per il sistema di assegnazione turni
"""

from dataclasses import dataclass  # decorator
from typing import List, Dict


@dataclass
class Persona:
    """Classe rappresentante una persona con le sue informazioni"""

    matricola: str
    nome: str
    cognome: str
    new_entry: bool

    def __str__(self):
        tipo = "Esperto" if self.new_entry == "NO" else "Nuovo"
        return f"{self.nome} {self.cognome} ({self.matricola}) [{tipo}]"


@dataclass
class Turno:
    """Classe che rappresenta un turno con le persone assegnate"""

    giorno: str
    fascia: str
    persone: List[Persona]

    def __str__(self):
        return f"{self.giorno} {self.fascia}"

    def get_dati_assegnati(self) -> List[str]:
        "Ritorna tutte le persone assegnate al turno"
        nomi = [f"{persona.nome} {persona.cognome}" for persona in self.persone]
        return sorted(nomi, key=lambda x: x.split()[1]) # ordine alfabetico per cognome

    def get_esperti(self) -> List[Persona]:
        """Ritorna solo gli esperti del turno"""
        return [persona for persona in self.persone if persona.new_entry == "NO"]

    def get_nuovi(self) -> List[Persona]:
        """Ritorna solo i nuovi del turno"""
        return [persona for persona in self.persone if persona.new_entry == "SI"]


class AssegnazioneTurni:
    """Classe per tutti i turni assegnati"""

    def __init__(self):
        self.turni: List[Turno] = []
        self.conteggio_turni: Dict[str, int] = {}
        # map = key: matricola -> value:numero turni assegnati

    def aggiungi_turno(self, turno: Turno):
        """Aggiunge un turno e aggiorna i conteggi"""
        self.turni.append(turno)
        for persona in turno.persone:
            self.conteggio_turni[persona.matricola] = (
                self.conteggio_turni.get(persona.matricola, default=0) + 1
            )

    def get_turni_persona(self, matricola: str) -> int:
        """Ritorna il numero di turni assegnati a una persona"""
        return self.conteggio_turni.get(matricola, default=0)
