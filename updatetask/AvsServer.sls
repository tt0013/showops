{% if True == grains['File'] %}

{% for num in grains['avsnum'].split() %}

/data0/{{ num }}/AvsServer.conf:
  file.managed:
    - makedirs: True
    - source: salt://Sinashow/files/AvsServer.conf
    - mode: 644
    - template: jinja

{% endfor %}

AvsServer_Sinashow:
    file.managed:
      - makedirs: True
      - name: /home/maintain/AllChatService/Program/AvsServer-2.2.2.2.tar.gz
      - source: salt://Sinashow/files/AvsServer-2.2.2.2.tar.gz
      - source_hash: md5
      - mode: 600
      - template: jinja

{% if 0 != grains['empty'] %}
/home/maintain/AllChatService/confing.py:
    file.managed:
      - makedirs: True
      - name: /home/maintain/AllChatService/confing.py
      - source: salt://Sinashow/files/confing.py
      - source_hash: md5
      - mode: 755
      - template: jinja
    cmd.run:
      - cwd: /home/maintain/AllChatService/Program/
      - name: /usr/bin/python /home/maintain/AllChatService/confing.py
{% endif %}
#####IP CHANGE####
{% if grains['eth0'] not in [''] %}

{% if '2.2.2.2' != grains['avsversion'] %}
{% if '' != grains['PID'] %}
KillAvsServer:
    cmd.run:
      - name: /usr/bin/killall AvsServer && rm -rf /tmp/Chat_AllServiceMonitor_pid
{% endif %}
      - template: jinja
{% endif %}

{% for num in grains['avsnum'].split() %}
{% if '2.2.2.2' != grains['avsversion'] %}
/data0/{{ num }}:
    cmd.run:
      - cwd: /home/maintain/AllChatService/Program/
      - names :
        -  tar xf AvsServer-2.2.2.2.tar.gz -C /data0/{{ num }}/
      - template: jinja
{% endif %}
{% endfor %}

{% else %}

{% if '2.2.2.2' != grains['avsversion'] %}
{% if '' != grains['PID'] %}
Killprogram:
    cmd.run:
      - name: /usr/bin/killall AvsServer
{% endif %}
      - template: jinja
{% endif %}

{% for num in grains['avsnum'].split() %}
{% if '2.2.2.2' != grains['avsversion'] %}
/data0/{{ num }}:
    cmd.run:
      - cwd: /home/maintain/AllChatService/Program/
      - names :
        -  tar xf AvsServer-2.2.2.2.tar.gz -C /data0/{{ num }}/
      - template: jinja
{% endif %}
{% endfor %}
{% endif %}

{% endif %}

{% if True == grains['File'] %}

{% for num in salt['cmd.run']("cat /home/maintain/AllChatService/ChatList|grep -v '#'|grep 'ChatServer'|awk -F/ '{print $3}'").split() %}

/data0/{{ num }}/ChatServer.conf:
  file.managed:
    - makedirs: True
    - source: salt://FengBo_PhoneChat/files/ChatServer.conf
    - source_hash: md5
    - mode: 644
    - template: jinja
{% endfor %}

ChatServer_Sinashow:
    file.managed:
      - makedirs: True
      - name: /home/maintain/AllChatService/Program/ChatServer-2.2.2.2.tar.gz
      - source: salt://FengBo_PhoneChat/files/ChatServer-2.2.2.2.tar.gz
      - source_hash: md5
      - mode: 600
      - template: jinja

{% if 0 != grains['empty'] %}
Crsconfing.sh_Sinashow:
    file.managed:
      - makedirs: True
      - name: /home/maintain/AllChatService/confing.py
      - source: salt://FengBo_PhoneChat/files/confing.py
      - source_hash: md5
      - mode: 755
      - template: jinja
    cmd.run:
      - cwd: /home/maintain/AllChatService/Program/
      - name: /usr/local/bin/python /home/maintain/AllChatService/confing.py
{% endif %}
###IP变动
{% if grains['eth0'] not in [''] %}

{% if '2.2.2.2' != grains['phonecrsversion'] %}
Killprogram:
    cmd.run:
      - name: /usr/bin/killall room && /usr/bin/killall room_manager
{% endif %}
{% for num in salt['cmd.run']("cat /home/maintain/AllChatService/ChatList|grep -v '#'|grep 'ChatServer'|awk -F/ '{print $3}'").split() %}
{% if '2.2.2.2' != grains['phonecrsversion'] %}
/data0/{{ num }}/:
    cmd.run:
      - cwd: /home/maintain/AllChatService/Program/
      - names :
        -  tar xf ChatServer-2.2.2.2.tar.gz -C /data0/{{ num }}/
      - template: jinja
{% endif %}
{% endfor %}

{% else %}

{% if '2.2.2.2' != grains['phonecrsversion'] %}
Killprogram:
    cmd.run:
      - name: /usr/bin/killall room && /usr/bin/killall room_manager
{% endif %}
{% for num in salt['cmd.run']("cat /home/maintain/AllChatService/ChatList|grep -v '#'|grep 'ChatServer'|awk -F/ '{print $3}'").split() %}
{% if '2.2.2.2' != grains['phonecrsversion'] %}
/data0/{{ num }}:
    cmd.run:
      - cwd: /home/maintain/AllChatService/Program/
      - names :
        -  tar xf ChatServer-2.2.2.2.tar.gz -C /data0/{{ num }}/
      - template: jinja
{% endif %}
{% endfor %}
{% endif %}

{% endif %}


