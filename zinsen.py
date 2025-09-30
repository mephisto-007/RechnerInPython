from datetime import datetime # type: ignore

def tageszins(kapital: float, zinssatz: float, startdatum: str, enddatum: str, methode: str = "act/365") -> float:
    """
    Berechnet die Zinsen nach Tageszinsmethode zwischen zwei Daten.
    """
    zinssatz_dez = zinssatz / 100
    d1 = datetime.strptime(startdatum, "%d.%m.%Y")
    d2 = datetime.strptime(enddatum, "%d.%m.%Y")

    if methode == "30/360":
        tage = (d2.year - d1.year) * 360 + (d2.month - d1.month) * 30 + (d2.day - d1.day)
        jahr = 360
    else:
        tage = (d2 - d1).days
        if methode == "act/360":
            jahr = 360
        elif methode in ("act/365", "act/act"):
            jahr = 365
        else:
            raise ValueError("Unbekannte Methode. Erlaubt: '30/360', 'act/360', 'act/365', 'act/act'")

    zinsen = kapital * zinssatz_dez * (tage / jahr)
    return round(zinsen, 2)


# --- Benutzer-Eingabe ---
print("📊 Tageszins-Berechnung\n")

kapital = float(input("Kapital (€): "))
zinssatz = float(input("Zinssatz (% pro Jahr): "))
startdatum = input("Startdatum (TT.MM.JJJJ): ")
enddatum = input("Enddatum (TT.MM.JJJJ): ")
methode = input("Zinsmethode (30/360, act/360, act/365, act/act): ")

# Berechnung
zinsen = tageszins(kapital, zinssatz, startdatum, enddatum, methode)

print("\n💰 Ergebnis:")
print(f"Kapital: {kapital:,.2f} €")
print(f"Zeitraum: {startdatum} bis {enddatum}")
print(f"Methode: {methode}")
print(f"Zinsen: {zinsen:,.2f} €")

