
--CLIENT

    ssh-keygen -t rsa -b 4096 -C "huynguyen2913@gmail.com"
    cd ~/.ssh

    ssh-copy-id huynt@192.168.1.13
    ssh-copy-id huynt@congcu24h.ddns.net


    cat ~/.ssh/id_rsa.pub | ssh huynt@192.168.1.13 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

        cat ~/.ssh/id_rsa.pub | ssh huynt@congcu24h.ddns.net "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
    chmod 700 ~/.ssh
    chmod 600 ~/.ssh/id_rsa



--SERVER

        sudo nano /etc/ssh/sshd_config

-----------------------------------------------------

            UsePAM yes
            PermitRootLogin no
            PubkeyAuthentication yes
            IgnoreUserKnownHosts no
            PasswordAuthentication yes
-----------------------------------------------------

        chown -R $USER:$USER /home/$USER/.ssh

        chmod 0700 /home/$USER

        chmod 0700 /home/$USER/.ssh

        chmod 0600 /home/$USER/.ssh/authorized_keys


        sudo systemctl restart ssh
