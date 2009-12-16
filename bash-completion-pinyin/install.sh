

# 说明: (以当前用户运行)
#   直接执行 sh install.sh 进行安装。
#   运行完成后关闭终端,在新终端中测试

if [ "$SHELL" != "/bin/bash" ]
then
	printf "\n\tsupport bash only !\n\n" && \
	exit 1
fi

if [ ! -f "/etc/bash_completion" ]
then
	printf "\n\tbash_completion not found :( \n\n" && \
	exit 1
fi

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

echo "Install finished."
echo "Open new terminal to use it."


