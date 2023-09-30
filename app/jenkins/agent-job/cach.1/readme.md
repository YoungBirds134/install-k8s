------*Cài Agent Job bằng Inbount

    1. Cài Java 
    2. Làm theo Jenkins Agent Overview
    3. Làm theo Jenkins slave cannot connect with master_ Incorrect acknowledgement sequence - Stack Overflow (cấu hình dùng websocket solution in short: just tick the "Use WebSocket" option in the agent node config (Manage Jenkins ==> Manage nodes and clouds ==> choose your inbound agent node ==> Configure ==> tick the "Use WebSocket"))
    4. Tạo service để giữ connection agent 
    5. Làm theo shell - Run java jar file on a server as background process - Stack Overflow

    ------*
         systemctl status jenkins-agent-huynt-13.service # starts the service

         systemctl start jenkins-agent-huynt-13.service # starts the service
         systemctl enable jenkins-agent-huynt-13.service # auto starts the service
         systemctl disable jenkins-agent-huynt-13.service # stops autostart
         systemctl stop jenkins-agent-huynt-13.service # stops the service
         systemctl restart jenkins-agent-huynt-13.service # restarts the service

    ------*

