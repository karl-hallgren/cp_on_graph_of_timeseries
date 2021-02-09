
# Changepoint detection on a graph of time series

Python code for the article: Hallgren K. L., Heard N. A. and Turcotte M. J (2021). "Changepoint detection on a graph of time series". In: arXiv e-prints. arXiv:2102.04112.

The novel graphical changepoint model, the simulation study and the datasets are introduced in the article.

The code was tested with Python 3.7, and it requires `numpy`, `pandas`, `scipy.special`, `networkx`, `matplotlib`, `pickle` 

Address for questions: karl.hallgren17@imperial.ac.uk

The code is organised into three folders as described below.

## model_and_sampler

Code to sample from the graphical changepoint model. 

* Class `ChangepointModel` in `changepoint_model.py`: an object corresponds to a graphical changepoint model given some some data.

* Class `MCMCsampler` from `mcmc_sampler.py`, which inherits from `ChangepointModel`: an object corresponds to an MCMC algorithm given a graphical changepoint model


## simulation_study

Code for the experiments described in Section 6 of the article. 

Run the experiments:
```
./simulation_study/star_run.sh
./simulation_study/cluster_run.sh
```

Process results:
```
./simulation_study/star_process.py
./simulation_study/cluster_process_lags.py
./simulation_study/cluster_process_nolags.py
```

Plot results (with R) into `simulation_study/plots/`:
```
Rscript simulation_study/plots/plot_star.R
Rscript simulation_study/plots/plot_cluster.R
Rscript simulation_study/plots/plot_auxi.R
Rscript simulation_study/plots/plot_lags.R
```

## cyber_application

Code for the application in cyber-security described in Section 3 and Section 7. 

Process the authentication data: 
```
./cyber_application/get_edgeset.py
./cyber_application/get_tseries.py
```

Fit standard model for the motivational example of Section 3.3: 
```
python3 cyber_application/fit_motivation.py
```

Plot results in `cyber_application/plots/`:
```
Rscript cyber_application/plots/plot_motivation.R
```

To fit graphical changepoint model for Section 7:
```
./cyber_application/fit_run.sh &
```

Process and plot results in `cyber_application/plots/`:
```
./cyber_application/process_results.py 
Rscript cyber_application/plots/plot_edgeset.R
Rscript cyber_application/plots/plot_results.R
```
