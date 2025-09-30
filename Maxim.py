import csv # type: ignore

class Hello:
    def hello(self):
        print("Hello World")


class Rechner:
    """Ein einfacher Rechner mit den 4 Grundrechenarten"""
    def __init__(self, csv_datei="rechner_log.csv"):
        self.csv_datei = csv_datei
        # CSV vorbereiten (Kopfzeile schreiben, falls Datei leer ist)
        with open(self.csv_datei, mode="a", newline="") as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["Zahl 1", "Operator", "Zahl 2", "Ergebnis"])

    def _speichern(self, a, operator, b, result):
        """Hilfsmethode: speichert die Berechnung in der CSV-Datei"""
        with open(self.csv_datei, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([a, operator, b, result])
            
    
    def add(self, a, b):
        try:
            a = float(a)
            b = float(b)
        except (TypeError, ValueError) as e:
            print("Fehler:", e)
            return None
        result= a+b
        self._speichern(a, "+", b, result)
        return result

    def subtract(self, a: float, b: float)->float |None:
        """_summary_

        Args:
           - a (float): Minuend(Erste Zahl)
           - b (float): Subtrahend(Zweite Zahl)

        Returns:
           - float: Die Differenz als Float
           - |None: Bei fehlerhafter Eingabe 
        """
        try:
            a = float(a)
            b = float(b)
        except (TypeError, ValueError) as e:
            print("Fehler:", e)
            return None
        result= a-b
        self._speichern(a, "-", b, result)
        return result
        

    def multiply(self, a, b):
        try:
            a = float(a)
            b = float(b)
        except (TypeError, ValueError) as e:
            print("Fehler:", e)
            return None
        result= a*b
        self._speichern(a, "*", b, result)
        return result

    def divide(self, a, b):
        try:
            a = float(a)
            b = float(b)
        except (TypeError, ValueError) as e:
            print("Fehler:", e)
            return None
        if b == 0:
            print("Fehler: Division durch 0 nicht erlaubt!")
            return None
        result= a/b
        self._speichern(a, "/", b, result)
        return result

class Waerungsrechner:
    @staticmethod
    def eur_in_usd(eur):
        try:
            eur = float(eur)
        except (TypeError, ValueError) as e:
            print("Error", e)
            return None
        result = eur * 1.17
        return round(result,2)
    
    @staticmethod
    def usd_in_eur(usd):
        try:
            usd = float(usd)
        except (TypeError, ValueError) as e:
            print("Error", e)
            return None
        result = usd/1.17
        return round(result,2)
    
    @staticmethod
    def eur_in_bp(eur):
        try:
            eur = float(eur)
        except (TypeError, ValueError) as e:
            print("Error", e)
            return None
        result = eur*0.87
        return round(result,2)
    
    @staticmethod
    def bp_in_eur(bp):
        try:
            bp = float(bp)
        except (TypeError, ValueError) as e:
            print("Error", e)
            return None
        result = bp/0.87
        return round(result,2)
    
    @staticmethod
    def eur_in_yen(eur:float)->float|None:
        """Die Funktion macht was tolles
        - asd 
        - asdf 
        """
        try:
            eur = float(eur)
        except (TypeError, ValueError) as e:
            print("Error", e)
            return None
        result = eur * 173.84
        return round(result,2)
    @staticmethod
    def yen_in_euro(yen:float)->float|None:
        try:
            yen = float(yen)
        except (TypeError, ValueError) as e:
            print("Error", e)
            return None
        result = yen / 173.84
        return round(result,2)
    