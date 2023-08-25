#!/bin/bash

username="jeff"
username="lengxiao"
username="jiangbo"
userdel -r ${username}
echo -e "创建-指定主目录"
useradd -m -d /home/${username} ${username}
echo -e "设定密码"
passwd ${username}
echo -e "设定bash"
usermod -s /bin/bash ${username}
echo -e "设定group"
usermod -g ${username} ${username}

