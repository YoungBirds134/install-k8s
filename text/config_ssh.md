
--CLIENT

    ssh-keygen -t rsa -b 4096 -C "huynguyen2913@gmail.com"
    cd ~/.ssh

    ssh-copy-id huynt@192.168.1.13

    cat ~/.ssh/id_rsa.pub | ssh huynt@192.168.1.13 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
    chmod 700 ~/.ssh
    chmod 600 ~/.ssh/id_rsa



--SERVER

        sudo nano /etc/ssh/sshd_config

-----------------------------------------------------

            UsePAM no
            IgnoreUserKnownHosts no
            PasswordAuthentication yes
-----------------------------------------------------

        chown -R $USER:$USER /home/$USER/.ssh

        sudo systemctl restart ssh
