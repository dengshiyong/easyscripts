

# 说明:
#     直接执行 sh install.sh 进行安装。
#     安装脚本会重载 /etc/bash_completion 中 _file_dir和_file_dir_xspec 函数，将
#        COMPREPLY=( "${COMPREPLY[@]}" "${toks[@]}" )
#     变成 ( 其中chsdir为本脚的名字,注意指定路径和赋执行权限 )
#        chs=($(chsdir "x$1" "$cur"))
#        COMPREPLY=( "${COMPREPLY[@]}" "${toks[@]}" "${chs[@]}" )
#     将这段函数写入一个独立的文件并导入$HOME/.bashrc中,在引用/etc/bash_completion之后再覆盖性的定义一遍。


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


