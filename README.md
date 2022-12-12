# Wolly
## Installazione preliminare

### Modifica IP
* Collegare Wolly ad una rete wifi
* Identificare l'indirizzo ip del Raspberry inserirendo nel terminale il comando 

    `hostname -I`
        
* Inserire l'indirizzo IP nel file *db_connection.py* nella variabile

        `host_name = '<indirizzo IP>'`
        
        **N.B:** la porta di default è settata a 8000

### Installazione delle librerie

* #### CircuitPython
    Seguire la procedura descritta in questo link
    
    https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

* #### Adafruit PCA9685
    Eseguire nel terminale il comando 
    
    `pip3 install adafruit-circuitpython-pca9685` 

* #### Appwrite
     Eseguire nel terminale il comando\
     
    `pip3 install appwrite`
