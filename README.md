# WRO-2025-SJADragons-futuros--ingenieros
Team Presentation – SJADragons
Saint John’s Academy
Participants in the Future Engineers Category – WRO 2025

Team Members and Roles

Alisson Ortega
Age: 18
She has an analytical and reflective personality. When faced with a problem, she prefers to explore solutions independently first, enjoying the process of discovery. However, she knows when it’s time to collaborate and merge ideas with the team.
Alisson is passionate about technology and loves immersing herself in the digital world—whether by programming, researching tools, or simply absorbing new knowledge. Her approach is balanced: she knows when to stay connected and when to focus on real-world responsibilities.
She tends to remain calm in complex situations, combining logical thinking with a sensitivity that brings harmony to the group.

Eudhannys Vargas
Reserved and calm, she is a steady and reliable presence within the team. She doesn’t need many words to show her commitment and support. She likes taking the necessary time to do things well and is always ready to collaborate when needed. Her serene attitude helps maintain the group’s stability, even under pressure.

Gabriel Rentería
He has strong knowledge in robotics and a great willingness to share what he knows with his teammates. He actively contributes to the project’s development, offering practical ideas in both design and technical analysis. His ability to adapt to technical challenges is key to the team’s progress.

Viviam Ortega
Team coach – a guiding and fundamental support throughout the process.

Our Path to Robotics

Our story began with something simple: curiosity. We’ve always felt a natural attraction to technology and discovering how things work. What started as a conversation full of ideas, dreams, and eagerness to learn, became a shared and meaningful challenge.

As we dove into the world of robotics, we realized it wasn’t just about connecting wires or writing lines of code. It was about facing real problems, seeking creative solutions, and watching our ideas come to life. Every obstacle we overcame—from learning new concepts to adapting to limited resources—helped us grow both as a team and as future engineers.

The path wasn’t easy. We had to research, make mistakes, try over and over… but every attempt brought us closer to a better version of our robot—and of ourselves.

Today, when we look back at what we’ve achieved, we feel proud. Because this project represents more than technical knowledge: it reflects friendship, commitment, and confidence in what we can accomplish when we work together.

Technology Core: Architecture and Components

We designed a powerful, stable, and modular system focused on efficiency and adaptability for the competition. These are the main components of our robot:

* Central Controller: Raspberry Pi 4 Model B – Handles core processing, vision, and decision-making. It manages overall logic and sends instructions to the microcontroller.
* Microcontroller: Arduino Uno – Executes commands from the Raspberry Pi and controls motors, sensors, and actuators.
* Motor Controller and Regulator: L298N H-Bridge – Manages motor speed and direction using PWM signals.
* System Actuators: 
    * DC Motor: Vehicle propulsion.
    * Servo Motor: Precise steering of the front wheels.
* Sensors and Perception: 
    * HC-SR04 Ultrasonic Sensor: Real-time obstacle detection.
    * Webcam: Provides computer vision for visual recognition and navigation.
* Power Supply: 7.4V Powerbank-style battery, offering stable and portable energy to the entire system.
* Connections: Jumpers allow clear and secure internal wiring between modules.


Navigation System and Autonomous Behavior

Based on a Finite State Machine (FSM) architecture, our robot makes autonomous decisions, adapting to multiple environmental scenarios:

* Obstacle detection and avoidance using the ultrasonic sensor.
* Blockage recovery through turning or reverse routines.
* Visual processing via the webcam, directed by the Raspberry Pi.
* Communication between Raspberry Pi and Arduino to synchronize actions.


Mechanical Design and Assembly

* Modular design for fast repairs and efficient modifications.
* Balanced weight distribution to improve stability during movement.
* Clean and safe wiring with well-organized jumpers to avoid interference.
* Accessible structure for easy maintenance and component assembly.


Code Organization and Software Architecture

* Sensor reading module with filtering for greater precision.
* Actuator controllers for smooth, controlled movements.
* FSM logic to adapt behaviors based on environmental input.
* Basic computer vision module using camera input.

Conclusion

This project is more than just wires, sensors, and code. It has been an experience that allowed us to grow, learn together, and build something real. We’ve combined robotics, programming, and mechanical design into a competitive, versatile, and functional autonomous vehicle.

We feel prepared and proud to represent Saint John’s Academy in the WRO 2025, carrying with us not only technical knowledge, but also values such as teamwork, perseverance, and a passion for innovation.
