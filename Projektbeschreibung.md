# 📚 Homework-Manager

## 📝 Projektbeschreibung

Der **Homework-Manager** entstand aus einem einfachen, aber frustrierenden Problem:  
Ich hatte es satt, im Klassenchat nach den Hausaufgaben zu fragen und keine Antwort zu bekommen.  

Natürlich könnte man sich die Hausaufgaben einfach auf **Papier** notieren oder in einen **persönlichen digitalen Kalender** eintragen.  
Aber das wäre mir zu langweilig gewesen – und hätte nur mir selbst geholfen.  

Daher wollte ich eine **Lösung entwickeln**, die auch meinen Klassenkameraden etwas bringt.  
So entstand der **Homework-Manager**:  
Ein Programm, das einen **Hausaufgaben- und Prüfungs-Kalender** bietet und einige zusätzliche Features mitbringt.  

## 🔄️ Update 1.5 
Die Benutzeroberfläche wurde angepasst um eine höhere Benutzerfreundlichkeit zu garantieren, zudem wurde der "Noterechner" implementiert.

## 🔄️ Update 1.6.x
Aktuell versuche ich die Benutzeroberfläche zu überarbeiten, jedoch ist mir schnell klar geworden, dass die Möglichkeiten einer reinen Python Benutzenoberfläche sehr beschränkt sind bzw. viel zu komplieziert um ein gutes Resulat zu erzielen. Die Folge davon war, dass ich mir alternativen überlegen musste. Die Lösung war schnell gefunden, ich wollte die Benutzeroberfläche mit HTML und CSS gestalten (so wie jede Webseite auch programmiert ist). Für die Funktionalitäten wollte ich weiterhin auf Python setzen. 

## 🔄️ Update 1.6.1-BETA
Nach einigem experimentieren steht endlich die Webseite und funktioniert so weit auch einigermassen. Leider sind mir jedoch einige mögliche Problempunkte aufgefallen.
Entgegen dem Ursprünglichen Ziel ist die neue Version immer noch ein Softwarepacket, welches mann sich herunterladen muss. Das eigentlich grössere Problem, welches mich am meisten nervte, war jdeoch ein Anderes. Denn die Assets die unverändert aus den alten Versionen übernommen wurden, waren immernoch statisch und an die jeweilige Software gebunden. Mein Ziel war jedoch, die Assets online verfügbar zu machen, so dass bei allfälligen Änderungen (wie z.B. dem Stundenplan) die Änderungen ohne ein Softwareupdate übernommen werden.

Der erste Lösungsansatz scheiterte jedoch kläglich an den Sicherheitsprotokollen des Internets, welche mir weiterhin Kopfschmerzen bereiteten. Jedoch wusste der Chatbot die Lösung für mein Problem. Sie hiess FLASK.
Für alle diejenigen die nicht verstehen was genau FLASK ist: FLASK ermöglichte es mier eine Art Server zu erschaffen der auf Internetanfragen eine Pythonfunktion ausführt und deren Funktionswert zurückgibt. Zuvor hatte ich versucht dass entsprchende JSON-File dirket in die Webseite einzuspeisen.

Da es ein leichtes war das FLASK Skript auf einen Server zu Uploaden, der von überall erreichbar ist, war nun der Plan auch die Benutzeroberfläche über einen Webserver verfügbar zu machen.

## 🔄️ Release 1.6.2
Nach dem erlernen einiger neuer Programmierskills ist es endlich so weit, die neue Homework-Manager Webseite ist da.

Der Vorteil der neuen Webseite ist, dass man sich keine Software mehr herunterladen muss und dass man die Software auch nicht mehr ständig manuell Updaten muss, da alles direkt auf dem Web-Server geschieht. Zudem bietet die Webseitenlösung mehr Gestaltungsoptionen für das Design der Benutzeroberfläche und des weiteren eine Zentale Speicherlösung für die Stundenplan Files und weiteren Assets die auch bereits zuvor in den alten Versionen eingebunden waren. Jedoch waren dieses Files zuvor fest eigebunden und so konnten die alten Versionen nicht veränderte Stundenpläne anzeigen, was inzwischen möglich ist. Zu beginn hatte ich noch einige Probleme damit, dass die Webseite nicht wirklich flüssig lief und sich zeitweise selber aufhängte, inzwischen konnten jedoch alle Fehler behoben werden.

Was noch wichtig zu erwähnen ist, ist dass der Server, welcher die Daten für die Seite bereitstellt, bis zu 80 Sekunden braucht um aus dem Standby zu kommen und die Daten zu liefern. Der Grund dafür ist, dass ich aktuell auf ein kostenloses Angebot für das Hostting setzte, welches diese Einschränkungen mit sich bringt. Aktuell stehen jedoch die überlegungen im Raum für monatlich 7 Fr. auf ein sofort verfügabres Paket zu setzen.

## ℹ️ Mehr Infos

Falls du **mehr über die Entstehung oder die Struktur** des Projekts erfahren möchtest, kannst du dich gerne bei mir melden. 😊
