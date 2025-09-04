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

## 🔄 Update 1.6.1-BETA
Nach ausgiebigen Experimenten steht die Webseite nun endlich bereit und funktioniert weitgehend zuverlässig. Dennoch sind mir mehrere potenzielle Problempunkte aufgefallen:

Downloadpflichtiges Softwarepaket
Entgegen dem ursprünglichen Ziel liegt die neue Version weiterhin als Softwarepaket vor, das heruntergeladen werden muss.

Statische Assets
Die aus älteren Versionen übernommenen Assets sind unverändert statisch und an die jeweilige Software gebunden. Mein Ziel war es jedoch, sämtliche Assets online verfügbar zu machen, damit Änderungen (z. B. am Stundenplan) ohne erneutes Softwareupdate übernommen werden.

Mein erster Lösungsansatz scheiterte kläglich an den Sicherheitsprotokollen des Internets, die mir weiterhin Kopfzerbrechen bereiteten. Schließlich empfahl mir der Chatbot den Einsatz von Flask. Flask ermöglicht es, einen Server zu betreiben, der auf Internetanfragen eine Python-Funktion ausführt und deren Ergebnis zurückliefert. Zuvor hatte ich versucht, die entsprechende JSON-Datei direkt in die Webseite einzubinden.

Da das Flask-Skript problemlos auf einen von überall erreichbaren Server hochgeladen werden konnte, war der nächste Schritt, auch die Benutzeroberfläche über einen Webserver bereitzustellen.

## 🔄 Release 1.6.2
Nach dem Erwerb weiterer Programmierkenntnisse ist es nun soweit: Die neue Homework-Manager-Webseite ist online.

**Vorteile der Weblösung:**

Keine lokale Installation mehr erforderlich
Weder der Download einer Software noch manuelle Updates sind nötig, da alle Prozesse direkt auf dem Webserver ausgeführt werden.

Erweiterte Gestaltungsoptionen
Die Weboberfläche lässt sich deutlich flexibler designen.

Zentrale Speicherung
Stundenplandateien und weitere Assets liegen zentral auf dem Server und können dynamisch aktualisiert werden. Veränderte Stundenpläne werden nun automatisch angezeigt, ohne dass eine neue Version installiert werden muss.

Anfangs kam es vereinzelt zu Performance-Problemen: Die Webseite lief nicht durchgängig flüssig und hängte sich gelegentlich auf. Inzwischen konnten jedoch alle Fehler behoben werden.

Hinweis zum Hosting:
Der Server, der die Daten bereitstellt, benötigt aus dem Standby-Modus bis zu 80 Sekunden, um Anfragen zu beantworten. Ursache hierfür ist das kostenlose Hosting-Angebot, das ich derzeit nutze. Es steht jedoch zur Diskussion, für monatlich CHF 7 auf ein Paket mit sofortiger Verfügbarkeit umzusteigen.

## 🔄️ Update 1.6.3 & 1.6.4

Die Webseite hat in mehrere grafische so wie auch sicherheitstechnische Verbesserungen erhalten. Dazu gehören neue Overlays. Zudem habe ich aufgrund von Feedback von Benutzern ein neues Overlay erstellt, welches einem Administator ermöglicht Einträge zu bearbeiten oder zu löschen.

## 🔄️ Update 1.7 inkl Patch 00x1 & 00x2

Es wurden diverse kleinere Anpassung an der Benutzeroberfläche vorgenommen und es gibt nun die Möglichkeit, Einträge direkt im Kalender zu erfassen und zu bearbeiten

## ℹ️ Mehr Infos

Falls du **mehr über die Entstehung oder die Struktur** des Projekts erfahren möchtest, kannst du dich gerne bei mir melden. 😊

