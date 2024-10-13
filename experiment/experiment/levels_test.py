import os
import shutil
import subprocess

WORK_DIR = "./experiment/levels_test"
MODEL_DIR = f"{WORK_DIR}/models"
PROOF_DIR = f"{WORK_DIR}/proofs"
os.makedirs(WORK_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(PROOF_DIR, exist_ok=True)

def generate_file(dlevel, plevel, source, dest):
    cmd = f"python3 ./scripts/main.py {source} -o {dest} --derive-level={dlevel} --propagate-level={plevel}"
    subprocess.run(cmd, shell=True)

def prove_file(model_file, out_file):
    cmd = f'export LC_ALL=C.UTF-8 && tamarin-prover +RTS -N6 -RTS --derivcheck-timeout=0 {model_file} --prove --output={out_file} > {out_file}.tmp && echo "" >> {out_file} && cat {out_file}.tmp >> {out_file} && rm {out_file}.tmp'
    subprocess.run(cmd, shell=True)

def levels_test(source_file:str, dlevels=(1, 9), plevels=(1, 9)):
    name = source_file.split("/")[-1].split(".")[0]
    for dlevel in range(dlevels[0], dlevels[1]):
        for plevel in range(plevels[0], plevels[1]):
            dest = f"{MODEL_DIR}/{name}_d{dlevel}_p{plevel}.spthy"
            generate_file(dlevel, plevel, source_file, dest)
            proof_file = f"{PROOF_DIR}/{name}_d{dlevel}_p{plevel}.spthy"
            prove_file(dest, proof_file)


if __name__ == "__main__":
    levels_test("./experiment/source_models/BC_session_establishment2.spthy", (1, 6), (6, 9))
    levels_test("./experiment/source_models/BC_session_establishment2.spthy", (6, 9), (1, 9))
    levels_test("./experiment/source_models/BC_session_establishment4.spthy", (1, 3), (6, 9))
    levels_test("./experiment/source_models/BC_session_establishment4.spthy", (3, 4), (1, 2))
    levels_test("./experiment/source_models/BC_session_establishment4.spthy", (3, 4), (6, 9))
    # levels_test("./experiment/source_models/BC_session_establishment4.spthy", (4, 9), (1, 9))
