

library(latex2exp)
library(RColorBrewer)


###########################################
#########     AUXILIARY variables expriment 




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


theta = 1050

pdf(paste0(pwdout,"FigClustInf.pdf"), height=11, width=14)


graphs = c('rchain', 'rchain', 'lattice', 'lattice')
clusters = c(0,1,0,1)
n_col = length(graphs)


logit_indices = 3:7

nf <- layout(matrix(1:(n_col*length(logit_indices)), byrow=TRUE, nrow=n_col))


for (col_j in 1:length(graphs)){
  
  graph = graphs[col_j]
  cluster = clusters[col_j]
  results = list()
  
  for (delta in c('no', 'yes')) {
    results[[delta]] = read.csv(paste0(pwd, 'simulation_cluster_res_',theta, '_graph_', graph, '_cluster_', cluster, ifelse(delta=='no', '_no_delta', ''), '.csv'), header=TRUE)
    results[[delta]]= as.matrix(results[[delta]][, 2:length( results[[delta]][1, ])])
  }
  
  for (logit_i in logit_indices){
    
    
    if (col_j == 1){
      partbottom = 0.9
      partop = 3.9
    } else if (col_j == 2) {
      partbottom = 1.9
      partop = 2.9
    } else if (col_j == 3) {
      partbottom = 2.9
      partop = 1.9
    } else if (col_j == n_col) {
      partbottom = 3.9
      partop = 0.9
    }
    
    if (logit_i == logit_indices[1]){
      parleft=5
      parright=0.2
    }
    else if ( logit_i == logit_indices[length(logit_indices)]){
      parleft = 5
      parright = 0.2
    } else {
      parleft=5
      parright=0.2
    }
    
    par(mar=c(partbottom,parleft,partop,parright))
    
    
    plot( 0, -300, type = 'b', lty = 2,
          ylab = ifelse(logit_i ==logit_indices[1],
                        TeX(paste0('prob. for $', "C_", clusters[col_j]+1, '$, ', ifelse(graphs[col_j]=='rchain', '$r$-chain', 'lattice'))  ),
                        #TeX(paste0(ifelse(graphs[col_j]=='rchain', '$r$-chain', 'lattice'), ", $C_", clusters[col_j]+1, '$')  ),
                        ''),
          xlab = ifelse(col_j == n_col, TeX("$\\lambda_s$"), ""),
          main = ifelse(col_j == 1, TeX(paste0('logit($p)=',logit_ps[logit_i], '$')), ''  ),
          ylim = c(0, 1), #c(ifelse(cluster == 'loss', -40, 0), ifelse(cluster == 'loss', 0, 1) ),
          mgp=c(2.9,0.8,0),
          cex.lab = 2.4,
          cex.axis = 1.5,
          cex.main =2.4,
          xlim = c(0, 0.8) )
    
    for (delta in c('no', 'yes')) {
      lines(lambdas,  results[[delta]][logit_i, ],
            #col = brewer.pal(n = 3, name = "Dark2")[which( windows  == windw)],
            col = ifelse(delta == 'no', 'red', 'blue'),
            type = 'b',
            pch = ifelse(delta == 'no', 17, 15), #c(17, 15, 19)[which( windows  == windw)], 
            cex = 1.8,
            lty = 2)
    }
    
  }
}


dev.off()


