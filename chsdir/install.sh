
mkdir -p $HOME/bin
cp chsdir chs_completion $HOME/bin/
[ $? -ne 0 ] && echo "FAIL!" && exit 3
echo '. $HOME/bin/chs_completion' >> $HOME/.bashrc
echo 'PATH=$PATH:$HOME/bin' >>  $HOME/.bashrc

echo "Install finished."
echo "Open new terminal to use it."
