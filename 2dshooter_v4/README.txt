Semesterprojekt Pygame von Christopher Hübner und Allan Fodi

Name des Spiels: Hunting Terrorist

Infos zur Dateistruktur:
-   sprites: Alle Sprite und Eventklassen.
-   sounds: Alle sounds die in das Spiel geladen werden.(Werden in main.py geladen)
-   img: Alle Bilder die in das Spiel geladen werden.(Werden in main.py geladen)
-   scores: Die Highscoreliste mit der Datenbank (Wird verwendet in Enemy.py und ActionEvent.py)
-   main.py: Enthält die Game Klasse die alle erforderlichen Objekte erzeugt,lädt und verwaltet. (update,load,initialize,ect...)
-   map.py: Enthält einen Teil des Map-parsers und die Camera Klasse, welche dafür sorgt dass nur ein Teil der ganzen Karte gezeichnet wird.
-   timeunit.py: Für spätere Implementationen nützlich (nicht relevant für die jetzige Version, nicht zu beachten)
-   mapfile.txt/mapfile2.txt: Die mapfiles, mit denen die Spielwelt in der Game Klasse erzeugt wird.

Ziel des Spiels:
Ziel ist es alle Gegner zu eliminieren und mögliche Hindernisse zu bewältigen (Gate öffnen).

HowTo Map:
Die Map funktioniert ganz einfach. Gespeichert werden die Mapdaten in einer Textdatei, bei der folgende Zeichen bedeutend sind.
"." = Ein leeres Feld.
"T" = Ein Baum.
"S" = Der Spawn des Spielers (Die Kamera passt sich dem Spawnpunkt entsprechend an).
"E" = Die Enemy-Spawnpunkte. Die Anzahl der zu tötenden Enemies hängt von der Anzahl Enemys in der Map ab.
"1" = Wände, durch die man nicht durchlaufen kann.
"C" = Control Box, an der man E drücken muss damit das Gate sich öffnet.
"W" = Woodboxes, die man zerstören muss um am Weg weiter zu kommen.
"G" = Das Gate, welches durch betätigen von E an der Control Box geöffnet wird.
