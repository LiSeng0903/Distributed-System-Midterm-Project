#!/bin/bash

# 檢查是否提供了參數 n
if [ -z "$1" ]; then
  echo "請輸入參數 n（要啟動的節點數量）"
  exit 1
fi

n=$1
base_port=5057

# 啟動 n 個 chord 節點
for ((i=0; i<n; i++));
do
  port=$((base_port + i))
  ./chord 127.0.0.1 $port &
done
