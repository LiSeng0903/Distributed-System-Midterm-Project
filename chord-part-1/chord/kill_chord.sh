#!/bin/bash

# 找出所有執行 chord 的 processes 並將其 kill -9
ps aux | grep 'chord' | grep -v 'grep' | awk '{print $2}' | xargs -I {} kill -9 {}

wait