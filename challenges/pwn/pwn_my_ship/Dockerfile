FROM alpine:3.17.3


WORKDIR /config

ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1
ENV PATH="$PATH:/root/.dotnet/"

RUN apk update && \
    apk add --no-cache socat bash ncurses-libs libstdc++ && \
    wget https://dot.net/v1/dotnet-install.sh && \
    chmod +x dotnet-install.sh && \
    ./dotnet-install.sh --channel 7.0


WORKDIR /app/

COPY src/Chip8.cs .
COPY src/Program.cs ./tmp.cs

RUN dotnet new console \
    && mv tmp.cs Program.cs \
    && dotnet build -r win-x64 --self-contained \
    && dotnet build --self-contained \
    && echo '#!/usr/bin/env sh' > /app/entrypoint.sh ;\
    echo 'while true; do socat TCP-LISTEN:55555,fork,reuseaddr EXEC:"/app/bin/Debug/net7.0/linux-musl-x64/app _bUg_EZ_WiTh__YoU_",stderr; done' >> /app/entrypoint.sh

CMD ["/bin/sh","/app/entrypoint.sh"]