FROM ubuntu:22.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/kr.archive.ubuntu.com/g" /etc/apt/sources.list
RUN sed -i "s/http:\/\/security.ubuntu.com/http:\/\/kr.archive.ubuntu.com/g" /etc/apt/sources.list


RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y perl python3 curl && \
    curl -LO https://github.com/radareorg/radare2/releases/download/6.1.8/radare2_6.1.8_amd64.deb && \
    apt-get install -y ./radare2_6.1.8_amd64.deb && \
    rm radare2_6.1.8_amd64.deb && \
    rm -rf /var/lib/apt/lists/*

#Adduser
RUN useradd -u 1158 -m pwnsandbox_pwn

#Copy Binary
COPY pwnsandbox /home/pwnsandbox_pwn/pwnsandbox
COPY flag /home/pwnsandbox_pwn/flag
COPY super.pl /super.pl

#Set Privilege
RUN chown -R root:pwnsandbox_pwn /home/pwnsandbox_pwn
RUN chmod 551 /home
RUN chmod 755 /home/pwnsandbox_pwn/pwnsandbox
RUN chmod 440 /home/pwnsandbox_pwn/flag
RUN chmod 755 /super.pl

USER pwnsandbox_pwn
WORKDIR /home/pwnsandbox_pwn
CMD ["perl", "/super.pl"]
EXPOSE 10058
