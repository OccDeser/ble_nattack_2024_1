# cmd = 'export LC_ALL=C.UTF-8'
# cmd += f' && {tamarin} +RTS -N6 -RTS --stop-on-trace=SEQDFS --derivcheck-timeout=0'
# cmd += f' {i} {lemma_opt} --output={o} > {o}.tmp'
# cmd += f' && echo "" >> {o} && cat {o}.tmp >> {o} && rm {o}.tmp'

OUTDIR="./experiment/proofs"
if [ ! -d $OUTDIR ]; then
    mkdir -p $OUTDIR > /dev/null 2>&1
    mkdir -p "$OUTDIR/entropy" > /dev/null 2>&1
    mkdir -p "$OUTDIR/orginal" > /dev/null 2>&1
fi

################################################################################################
# ENTROPY MODELS
################################################################################################
# MODEL="BC_session_establishment2.spthy"
# OUTFILE="$OUTDIR/entropy/$MODEL"
# MODELFILE="./experiment/entropy_models/$MODEL"
# echo "Verifying $MODEL"
# export LC_ALL=C.UTF-8 && \
#     tamarin-prover +RTS -N6 -RTS --derivcheck-timeout=0 $MODELFILE \
#     --prove --output=$OUTFILE > $OUTFILE.tmp \
#     && echo "" >> $OUTFILE && cat $OUTFILE.tmp >> $OUTFILE && rm $OUTFILE.tmp

# MODEL="BC_session_establishment4.spthy"
# OUTFILE="$OUTDIR/entropy/$MODEL"
# MODELFILE="./experiment/entropy_models/$MODEL"
# echo "Verifying $MODEL"
# export LC_ALL=C.UTF-8 && \
#     tamarin-prover +RTS -N6 -RTS --derivcheck-timeout=0 $MODELFILE \
#     --prove --output=$OUTFILE > $OUTFILE.tmp \
#     && echo "" >> $OUTFILE && cat $OUTFILE.tmp >> $OUTFILE && rm $OUTFILE.tmp

MODEL="BLE_SC-KeyboardDisplay_KeyboardDisplay.spthy"
OUTFILE="$OUTDIR/entropy/$1""_$MODEL"
MODELFILE="./experiment/entropy_models/$MODEL"
export LC_ALL=C.UTF-8 && \
    tamarin-prover +RTS -N6 -RTS --derivcheck-timeout=0 $MODELFILE \
    --prove=$1 --output=$OUTFILE > $OUTFILE.tmp \
    && echo "" >> $OUTFILE && cat $OUTFILE.tmp >> $OUTFILE && rm $OUTFILE.tmp

################################################################################################
# ORIGINAL MODELS
################################################################################################
# MODEL="BC_session_establishment2.spthy"
# OUTFILE="$OUTDIR/original/$MODEL"
# MODELFILE="./experiment/original_models/$MODEL"
# echo "Verifying $MODEL"
# export LC_ALL=C.UTF-8 && \
#     tamarin-prover +RTS -N6 -RTS --derivcheck-timeout=0 $MODELFILE \
#     --prove --output=$OUTFILE > $OUTFILE.tmp \
#     && echo "" >> $OUTFILE && cat $OUTFILE.tmp >> $OUTFILE && rm $OUTFILE.tmp

# MODEL="BC_session_establishment4.spthy"
# OUTFILE="$OUTDIR/original/$MODEL"
# MODELFILE="./experiment/original_models/$MODEL"
# echo "Verifying $MODEL"
# export LC_ALL=C.UTF-8 && \
#     tamarin-prover +RTS -N6 -RTS --derivcheck-timeout=0 $MODELFILE \
#     --prove --output=$OUTFILE > $OUTFILE.tmp \
#     && echo "" >> $OUTFILE && cat $OUTFILE.tmp >> $OUTFILE && rm $OUTFILE.tmp

# MODEL="BLE_SC-KeyboardDisplay_KeyboardDisplay.spthy"
# OUTFILE="$OUTDIR/original/$MODEL"
# MODELFILE="./experiment/original_models/$MODEL"
# export LC_ALL=C.UTF-8 && \
#     tamarin-prover +RTS -N6 -RTS --derivcheck-timeout=0 $MODELFILE \
#     --prove --output=$OUTFILE > $OUTFILE.tmp \
#     && echo "" >> $OUTFILE && cat $OUTFILE.tmp >> $OUTFILE && rm $OUTFILE.tmp
