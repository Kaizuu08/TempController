# TempController
Project Overview
This project addresses critical issues related to the overheating and security of server rooms, essential for the stability and success of organizations. The proposed solution involves using raspberry pi technology to maintain optimal conditions and secure the server room environment.

Problem Statement
Server rooms are vital to organizational operations, housing expensive and sensitive equipment. Overheating can lead to hardware damage, expensive repairs, and pose health risks to personnel. Current security measures are inadequate, lacking alert systems for unauthorized access and environmental monitoring.

Solution Summary
We developed a server room cooling system with added safety and security features. The system includes:

Temperature and Humidity Monitoring: A sensor continuously monitors server room conditions. If temperatures exceed a set threshold, a fan is activated to cool the room.
Notification System: Alerts are sent to relevant personnel when the cooling system activates.
Visual Indicators: An LED provides a visual cue of increased temperature and system activation.
Security Enhancement: A distance sensor detects unauthorized access near the server room entrance, triggering faster LED flashes and sending notifications.
Graphical Output: A plot of Temperature vs. Time during the cooling process is generated to assess efficiency.
Hardware Components
Sensors: DHT11 (Temperature and Humidity), HC-SR04 (Ultrasonic Distance)
Actuators: LED, Servomotor, Twilio for text notifications, Matplotlib for graphical output
Controller: Raspberry Pi Model 3
Programming Overview
Main Loop: Continuously monitors temperature and distance.
Threading: Simultaneously controls LED flashing and fan activation.
Alert System: Sends notifications when temperature exceeds thresholds or unauthorized access is detected.
Graphical Monitoring: Displays cooling efficiency upon reaching safe temperature levels.