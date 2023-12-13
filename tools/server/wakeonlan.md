    wakeonlan 9c:6b:00:0a:ed:1f

---------PM2-------------


    pm2 start /home/huynt/bin/src/script/cloudflare/index.js  --name change-ip-auto  --cron-restart= "*/2 * * * *" --watch && pm2 save

    pm2 start /home/huynt/bin/src/script/cloudflare/index.js  --name change-ip-auto  --cron-restart= "*/1 * * * *" --watch && pm2 save

---------SERVER-----------


    sudo apt install ethtool -y &&
    sudo ethtool -s enp2s0 wol g &&
    sudo --preserve-env systemctl edit --force --full wol-enable.service &&
    sudo systemctl daemon-reload &&
    sudo systemctl enable wol-enable.service &&
    sudo apt search wakeonlan


---------CLIENT-----------


    install wakeonlan

    sudo wakeonlan 30:5a:3a:0d:ac:0d (take in enp2s0 -> link/ether)

    2: enp2s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
        link/ether 30:5a:3a:0d:ac:0d brd ff:ff:ff:ff:ff:ff
        inet 192.168.1.10/24 brd 192.168.1.255 scope global dynamic noprefixroute enp2s0
        valid_lft 67502sec preferred_lft 67502sec
        inet6 fe80::40ab:d219:c23e:abfb/64 scope link noprefixroute 
        valid_lft forever preferred_lft forever



