

# ˵��:
#     ֱ��ִ�� sh install.sh ���а�װ��
#     ��װ�ű������� /etc/bash_completion �� _file_dir��_file_dir_xspec ��������
#        COMPREPLY=( "${COMPREPLY[@]}" "${toks[@]}" )
#     ��� ( ����chsdirΪ���ŵ�����,ע��ָ��·���͸�ִ��Ȩ�� )
#        chs=($(chsdir "x$1" "$cur"))
#        COMPREPLY=( "${COMPREPLY[@]}" "${toks[@]}" "${chs[@]}" )
#     ����κ���д��һ���������ļ�������$HOME/.bashrc��,������/etc/bash_completion֮���ٸ����ԵĶ���һ�顣


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


