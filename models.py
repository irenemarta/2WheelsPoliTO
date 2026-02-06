"""
Modelli dati per il sistema di assegnazione turni
"""
from dataclasses import dataclass # decorator
from typing import List, Dict


@dataclass
class Persona:
    """Rappresenta una persona con le sue informazioni"""
    matricola: str
    nome: str
    cognome: str
    is_esperto: bool
    
    def __str__(self):
        tipo = "Esperto" if self.is_esperto else "Nuovo"
        return f"{self.nome} {self.cognome} (s{self.matricola}) [{tipo}]"


@dataclass
class Turno:
    """Rappresenta un turno con le persone assegnate"""
    giorno: str
    fascia: str
    persone: List[Persona]
    
    def __str__(self):
        return f"{self.giorno} {self.fascia}"
    
    def get_esperti(self) -> List[Persona]:
        """Ritorna solo gli esperti del turno"""
        return [persona for persona in self.persone if persona.is_esperto]
    
    def get_nuovi(self) -> List[Persona]:
        """Ritorna solo i nuovi del turno"""
        return [persona for persona in self.persone if not persona.is_esperto]


class AssegnazioneTurni:
    """Container per tutti i turni assegnati"""
    
    def __init__(self):
        self.turni: List[Turno] = []
        self.conteggio_turni: Dict[str, int] = {}  
        # map = key: matricola -> value:numero turni assegnati
    
    def aggiungi_turno(self, turno: Turno):
        """Aggiunge un turno e aggiorna i conteggi"""
        self.turni.append(turno)
        for persona in turno.persone:
            self.conteggio_turni[persona.matricola] = self.conteggio_turni.get(persona.matricola, default=0) + 1
    
    def get_turni_persona(self, matricola: str) -> int:
        """Ritorna il numero di turni assegnati a una persona"""
        return self.conteggio_turni.get(matricola, default=0)
