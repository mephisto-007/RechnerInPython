import subprocess
while True:
    print("1: Rechner")
    print("2: Währungsumrechner")
    print("3: Beenden")
    choice = int(input("Bitte wählen Sie eine Option: "))
    match choice:
        case 1:
            subprocess.run(["python", "Rechner.py"])

        case 2:
            uvicorn_process = subprocess.Popen(["uvicorn", "api:app"])

        case 3:
            print("Programm wird beendet.")
            break
        
        case _:
            print("Ungültige Auswahl. Bitte erneut versuchen.")
            continue