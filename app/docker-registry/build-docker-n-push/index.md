--Login Docker registry

--run script
    docker build -t congcu24h-ui .

    docker tag congcu24h-ui registry.congcu24h.com/congcu24h-ui

    docker push registry.congcu24h.com/congcu24h-ui

    docker rmi congcu24h-ui