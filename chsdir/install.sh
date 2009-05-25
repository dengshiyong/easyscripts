

# ˵��:
#   ֱ��ִ�� sh install.sh ���а�װ��
#   ������ɺ�ر��ն�,�����ն��в���

mkdir -p $HOME/bin
cp chsdir chs_completion $HOME/bin/

if [ "$SHELL" != "/bin/bash" ]
then
	printf "\n\tnot using bash? insall it youself ! \n\n" && \
	exit 1
fi

CONF=$HOME/.bashrc
[ $? -ne 0 ] && echo "FAIL!" && exit 3

echo '### chsdir start ###'       >> $CONF
echo '. $HOME/bin/chs_completion' >> $CONF
echo 'PATH=$PATH:$HOME/bin'       >> $CONF
echo '### chsdir finish. ###'     >> $CONF

echo "Install finished."
echo "Open new terminal to use it."


