if [ -d "./experiment/entropy_models" ]; then
    rm -rf ./experiment/entropy_models
    mkdir ./experiment/entropy_models
fi


python3 ./scripts/main.py ./experiment/source_models/BC_session_establishment2.spthy -o ./experiment/entropy_models/BC_session_establishment2.spthy --derive-level=3 --propagate-level=3
python3 ./scripts/main.py ./experiment/source_models/BC_session_establishment4.spthy -o ./experiment/entropy_models/BC_session_establishment4.spthy --derive-level=3 --propagate-level=3
python3 ./scripts/main.py ./experiment/source_models/BLE_SC-KeyboardDisplay_KeyboardDisplay.spthy -o ./experiment/entropy_models/BLE_SC-KeyboardDisplay_KeyboardDisplay.spthy --derive-level=2 --propagate-level=1
python3 ./scripts/main.py ./experiment/source_models/wpa2_four_way_handshake_unpatched.spthy -o ./experiment/entropy_models/wpa2_four_way_handshake_unpatched.spthy --derive-level=3 --propagate-level=3

# python3 ./scripts/main.py ./experiment/source_models/BC_session_establishment2.spthy -o ./experiment/entropy_models/BC_session_establishment2.spthy --derive_level 3 --propagate_level 3
# python3 ./scripts/main.py ./experiment/source_models/BC_session_establishment4.spthy -o ./experiment/entropy_models/BC_session_establishment4.spthy --derive_level 3 --propagate_level 3
# python3 ./scripts/main.py ./experiment/source_models/BLE_SC-KeyboardDisplay_KeyboardDisplay.spthy -o ./experiment/entropy_models/BLE_SC-KeyboardDisplay_KeyboardDisplay.spthy 
