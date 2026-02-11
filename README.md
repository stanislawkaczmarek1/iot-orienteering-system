# IoT Orienteering System 

An IoT-based orienteering race tracking system that uses smart checkpoints to record participants’ progress in real-time. The system provides a user-friendly interface for race management and live race monitoring.

The main function of the system is to use Raspberry Pi devices as checkpoints, where participants register themselves by scanning an RFID card. When a participant scans their card, the checkpoint communicates with the central server to log the visit. Visual and auditory feedback is provided via a buzzer and a programmable RGB LED strip, confirming successful scans. 

Raspberry Pi devices can also be used to add new participants to the system if needed. Each device also has an OLED display showing its unique ID for easy identification.

The PyQt6 desktop UI allows organizers to add and manage participants, create races and assign checkpoints in the desired order, and monitor race results in real-time.

The FastAPI backend handles data from all devices and stores it in a SQLite database.

---

## **Technologies Used**

- Python
- FastAPI
- SQLAlchemy
- SQLite
- PyQt6
- Raspberry Pi
  
---

## **Team**

- [Jakub](https://github.com/jakubwesta)
- [Łukasz](https://github.com/Barabasz1)
- [Mateusz](https://github.com/HavilMal)
- [Stanisław](https://github.com/stanislawkaczmarek1)

---

