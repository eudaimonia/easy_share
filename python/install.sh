#!/bin/bash -x
cwd=`pwd`
lib_dir=$HOME/MyBin/lib/easy_share
bin_dir=$HOME/MyBin/sh_bin

mkdir -p $lib_dir

cat << eof > $lib_dir/config.py 
TEMPLATE_DIR="$lib_dir/templates"
eof

cp -R $cwd/* $lib_dir
rm -f $bin_dir/easy_share
ln -s $lib_dir/main.py $bin_dir/easy_share
