# LEMMA="Executability"
# nohup bash ./experiment/prove_lemma.sh $LEMMA > output_$LEMMA.txt 2>&1 &

# LEMMA="IAuthRwithDHKey"
# nohup bash ./experiment/prove_lemma.sh $LEMMA > output_$LEMMA.txt 2>&1 &

# LEMMA="RAuthIwithDHKey"
# nohup bash ./experiment/prove_lemma.sh $LEMMA > output_$LEMMA.txt 2>&1 &

# LEMMA="IAuthRwithLTK"
# nohup bash ./experiment/prove_lemma.sh $LEMMA > output_$LEMMA.txt 2>&1 &

# LEMMA="RAuthIwithLTK"
# nohup bash ./experiment/prove_lemma.sh $LEMMA > output_$LEMMA.txt 2>&1 &

# LEMMA="MITMP"
# bash ./experiment/prove_lemma.sh $LEMMA > output_$LEMMA.txt 2>&1 

# LEMMA="LTKCP"
# nohup bash ./experiment/prove_lemma.sh $LEMMA > output_$LEMMA.txt 2>&1 &

LEMMA="SecAuthLTK"
bash ./experiment/prove_lemma.sh $LEMMA > output_$LEMMA.txt 2>&1 

LEMMA="SecrecySK"
bash ./experiment/prove_lemma.sh $LEMMA > output_$LEMMA.txt 2>&1 
