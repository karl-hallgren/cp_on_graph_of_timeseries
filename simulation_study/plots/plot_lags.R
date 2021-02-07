

library(latex2exp)
library(RColorBrewer)


###########################################
#########     LAGS expriment 



pwd = "simulation_study/simulations_cluster_results/"
pwdout = "simulation_study/plots/"


logit_ps = read.csv(paste0(pwd, 'simulation_clust_logits.csv'), header=TRUE)
logit_ps = logit_ps$X0

lambdas = read.csv(paste0(pwd, 'simulation_clust_lambdas.csv'),  header=TRUE)
lambdas = lambdas$X0

graphtype = read.csv(paste0(pwd, 'simulation_clust_graph_type.csv'),  header=TRUE)
graphtype = as.character(graphtype$X0)

thetas = read.csv(paste0(pwd, 'simulation_clust_thetas.csv'),  header=TRUE)
thetas = thetas$X0

windows = read.csv(paste0(pwd, 'simulation_clust_windows.csv'),  header=TRUE)
windows = as.character(windows$X0)




pdf(paste0(pwdout,"FigClustLag.pdf"), height=9, width=14)


restype = c('prob1', 'loss')[2]

lags = c(15, 10, 5)
graph = 'rchain'
cluster = 0
logit_indices = 2:6

n_col = 3


nf <- layout(matrix(1:(n_col*length(logit_indices)), byrow=TRUE, nrow=n_col))


for (col_j in 1:length(lags)){
  
  lag = lags[col_j]
  results = list()
  
  for (windw in windows) {
    results[[windw]] = read.csv(paste0(pwd, 'simulation_clusterlagged_', restype, '_', windw, '_graph_', graph, '_cluster_', cluster, '_lag_', lag,'.csv'), header=TRUE)
    results[[windw]] = as.matrix(results[[windw]][, 2:length( results[[windw]][1, ])])
  }
  
  
  for (logit_i in logit_indices){
    
    if (col_j == 1){
      partbottom = 1
      partop = 4
    } else if (col_j == 2) {
      partbottom = 2.5
      partop = 2.5
      
    } else if (col_j == n_col) {
      partbottom = 4
      partop = 1
    }
    
    if (logit_i == logit_indices[1]){
      parleft=4.9
      parright=0.2
    }
    else if ( logit_i == logit_indices[length(logit_indices)]){
      parleft=4.9
      parright=0.2
    } else {
      parleft=4.9
      parright=0.2
    }
    
    par(mar=c(partbottom,parleft,partop,parright))
    
    
    plot( 0, -300, type = 'b', lty = 2,
          ylab = ifelse( logit_i == logit_indices[1] ,TeX(paste0('$v=', lag, '$')), ''),
          xlab = ifelse(col_j == n_col, TeX("$\\lambda_s$"), ""),
          main = ifelse(col_j == 1, TeX(paste0('logit($p)=',logit_ps[logit_i], '$')), ''  ),
          #ylim = c(ifelse(restype == 'loss', -40, 0), ifelse(restype == 'loss', 0, 1) ),
          ylim = c(ifelse(restype == 'loss', 0, 0), ifelse(restype == 'loss', 40, 1) ),
          #ylim = c(-5, 20),
          mgp=c(2.9,0.8,0),
          cex.lab = 2.2,
          cex.axis = 1.5,
          cex.main =2.2,
          xlim = c(0, 0.8) )
    
    box()
    for (windw in windows) {
      lines(lambdas,
            ifelse(restype == 'loss', 1, 1)*results[[windw]][logit_i, ],
            #-ifelse(restype == 'loss', 1, 1)*results[[windw]][logit_i, ]+ifelse(restype == 'loss', 1, 1)*results[['no']][logit_i, ],
            #col = brewer.pal(n = 3, name = "Dark2")[which( windows  == windw)],
            col = c('red', 'blue', 'black')[which( windows  == windw)],
            type = 'b',
            pch = c(17, 15, 19)[which( windows  == windw)], 
            cex = 1.8,
            lty = 2)
    }
    
  }
}

dev.off()

