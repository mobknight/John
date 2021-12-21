#!/bin/bash
# cloudfoundry.value.name 별 cloudfoundry.envelope.job 목록을 집계하기 위한 스크립트

TARGET_FILES=(cloudfoundry.value.name cloudfoundry.counter.name)
API_ADDR="https://127.0.0.1:9200/app_metric*/_search"

for T in ${TARGET_FILES[*]}; do
    echo "===== ${T} : $(cat ${T} | wc -l) lines"
    LIST=`cat ${T}`
    X=1
    for ITEM in ${LIST}; do
        echo "  === Item ${X} : ${ITEM}"
        echo '{"query":{"match":{"TARGET":"ITEM"}}}' | sed "s/TARGET/${T}/g" | sed "s/ITEM/${ITEM}/g" > tempfile
        cat tempfile
        # curl -s -XGET ${API_ADDR} -u 'user:password' -d @tempfile
        X=`expr ${X} + 1`
    done
done
