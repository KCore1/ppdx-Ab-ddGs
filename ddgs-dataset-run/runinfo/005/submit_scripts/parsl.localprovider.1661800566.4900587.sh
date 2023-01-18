
export JOBNAME=$parsl.localprovider.1661800566.4900587
set -e
export CORES=$(getconf _NPROCESSORS_ONLN)
[[ "1" == "1" ]] && echo "Found cores : $CORES"
WORKERCOUNT=1
FAILONANY=0
PIDS=""

CMD() {
process_worker_pool.py  --max_workers=12 -a 10.225.104.65,10.225.8.65,128.138.64.27,bhpc-c5-u7-16.rc.int.colorado.edu,127.0.0.1 -p 0 -c 1 -m None --poll 10 --task_port=54457 --result_port=54609 --logdir=/projects/brpe7306/ppdx/example-flu/runinfo/005/htex_Local --block_id=0 --hb_period=30  --hb_threshold=120 --cpu-affinity none 
}
for COUNT in $(seq 1 1 $WORKERCOUNT); do
    [[ "1" == "1" ]] && echo "Launching worker: $COUNT"
    CMD $COUNT &
    PIDS="$PIDS $!"
done

ALLFAILED=1
ANYFAILED=0
for PID in $PIDS ; do
    wait $PID
    if [ "$?" != "0" ]; then
        ANYFAILED=1
    else
        ALLFAILED=0
    fi
done

[[ "1" == "1" ]] && echo "All workers done"
if [ "$FAILONANY" == "1" ]; then
    exit $ANYFAILED
else
    exit $ALLFAILED
fi
