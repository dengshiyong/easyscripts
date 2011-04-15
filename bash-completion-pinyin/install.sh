
######################
##     自动安装     ##
######################
##   直接执行 bash install.sh 进行安装。
##   运行完成后关闭终端,在新终端中测试


######################
##     手工安装     ##
######################
##
## 以ROOT权限安装
##   1. 复制 chsdir 到 /usr/bin/chsdir ,修改权限为 755
##   2. 复制 chs_completion 到 /etc/bash_completion.d/chs_completion
##   3. 安装完成
##
## 以普通用户安装
##   1. 复制 chsdir 到 $PATH 路径，修改权限为 755
##   2. 复制 chs_completion 到任意位置，在 $HOME/.bashrc 中导入
##   3. 按需要配置模糊拼音、命令扩展等
##   4. 安装完成

if [ "$SHELL" != "/bin/bash" ]
then
	printf "\n\tsupport bash only !\n\n" && \
	exit 1
fi

if [ ! -f "/etc/bash_completion" ]
then
	printf "\n\tbash-completion not found :( \n\n" && \
	exit 1
fi

if [ `id -u` -eq 0 ]
then
	# INSTALL AS ROOT
	[ ! -d "/etc/bash_completion.d" ] && mkdir -m 755 -p /etc/bash_completion.d
	cp chsdir /usr/bin/chsdir
	chmod 755 /usr/bin/chsdir
	cp chs_completion /etc/bash_completion.d/chs_completion
	chmod 644 /etc/bash_completion.d/chs_completion
else
	# INSTALL AS NORMAL USER
	mkdir -p $HOME/bin
	cp chsdir chs_completion $HOME/bin/
	chmod +x $HOME/bin/chsdir
	[ $? -ne 0 ] && echo "FAIL!" && exit 3

	CONF=$HOME/.bashrc
	echo '### chsdir start ###'                         >> $CONF
	echo '. $HOME/bin/chs_completion'                   >> $CONF
	echo 'PATH=$PATH:$HOME/bin'                         >> $CONF
	echo "#export CHSDIR=\"{'n':'l'}\""                 >> $CONF
	echo "complete -o filenames -F _filedir_xspec file" >> $CONF
	echo '### chsdir finish. ###'                       >> $CONF
fi

echo "Install finished."
echo "Open new terminal to use it."

