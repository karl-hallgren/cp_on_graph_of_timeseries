
#!/bin/bash


python3 simulation_study/cluster_part00.py &
python3 simulation_study/cluster_part01.py &
python3 simulation_study/cluster_part02.py &
python3 simulation_study/cluster_part03.py &
python3 simulation_study/cluster_part04.py &

python3 simulation_study/cluster_lag_part00.py &
python3 simulation_study/cluster_lag_part01.py &
python3 simulation_study/cluster_lag_part02.py &
python3 simulation_study/cluster_lag_part03.py &
python3 simulation_study/cluster_lag_part04.py &
python3 simulation_study/cluster_lag_part05.py &

python3 simulation_study/cluster_auxi.py &





