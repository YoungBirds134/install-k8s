#1. Create service


    sudo nano /etc/systemd/system/<name>.service

        ------CONTENT----------
        [Unit]
        After=network.target

        [Service]
        ExecStart=/usr/local/bin/<name>.sh

        [Install]
        WantedBy=default.target

        ------CONTENT----------


#2. Create bash file
    
    
    sudo nano  /usr/local/bin/<name>.sh

        ------CONTENT----------
        #!/bin/bash

        date > /root/<name>.txt
        du -sh /home/ >> /root/<name>.txt

        ------CONTENT----------


#3. Grant permission

    sudo chmod 744 /usr/local/bin/<name>.sh
    sudo chmod 664 /etc/systemd/system/<name>.service

#4. Reload daemon


    sudo systemctl daemon-reload
    sudo systemctl enable <name>.service

#5. View log


    sudo ls /root/




