
######################
##     自动安装     ##
######################
##   直接执行 bash install.sh 进行安装。
##   运行完成后关闭终端,在新终端中测试


######################
##     手动安装     ##
######################
##
## 以ROOT权限安装
##   1. 复制 to 到 /usr/bin/to ，修改权限为 755
##   2. 复制 to_completion 到 /etc/bash_completion.d/to_completion
##   3. 安装完成
##
## 以普通用户安装
##  1. 复制 to 到 $PATH 指定的目录, 修改权限为 755
##  2. 确认系统已经完装 bash_completion 包, 并复制 to_completion 到
##     任意位置,在 $HOME/.bashrc 尾加入一行
##  ~~~~~~~~~ ( 注意开头的"点" )
##  . to_completion
##  ~~~~~~~~~
##  3. 复制 to.hosts 到与 to 相同的目录，或复制为 $HOME/.to.hosts
##  4. 手工修改 to.hosts 文件，添加自定义主机
##  5. 安装完成
##


######################
##     注意事项     ##
######################
##
## 1. 如果系统未安装 python-pexpect 组件，运行时会提示安装
## 2. 命令行按 TAB 自动补全主机名功能，需要 bash_completion 支持
## 3. to.hosts 文件中保存有明文的密码，建议置权限为 600
##


if [ ! -f "/etc/bash_completion" ]
then
	printf "\n\tWARNNING : bash-completion not found :( \n\n"
fi

if [ `id -u` -eq 0 ]
then
	# INSTALL AS ROOT
	[ ! -d "/etc/bash_completion.d" ] && mkdir -m 755 -p /etc/bash_completion.d
	cp to /usr/bin/to
	chmod 755 /usr/bin/to
	cp to_completion /etc/bash_completion.d/to_completion
	chmod 644 /etc/bash_completion.d/to_completion
else
	# INSTALL AS NORMAL USER
	mkdir -p $HOME/bin
	cp to $HOME/bin/
	cp to_completion $HOME/bin/
	chmod +x $HOME/bin/to
	[ $? -ne 0 ] && echo "FAIL!" && exit 3

	CONF=$HOME/.bashrc
	echo '### remote_to start ###'                      >> $CONF
	echo '. $HOME/bin/to_completion'                    >> $CONF
	echo 'PATH=$PATH:$HOME/bin'                         >> $CONF
	echo '### remote_to finish. ###'                    >> $CONF
fi

echo "Install finished."
echo "Open new terminal to use it."

