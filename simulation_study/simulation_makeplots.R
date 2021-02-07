library(latex2exp)
library(RColorBrewer)


### Make plots for the simulation section


#####################################
#########     STAR expriment

pwd = "simulation_study/simulations_star_results/"
pwdout = "simulation_study/plots/"

logit_ps = read.csv(paste0(pwd, 'simulation_star_logits.csv'), header=TRUE)
logit_ps = logit_ps$X0

lambdas = read.csv(paste0(pwd, 'simulation_star_lambdas.csv'),  header=TRUE)
lambdas = lambdas$X0

C2card = read.csv(paste0(pwd, 'simulation_star_C2card.csv'),  header=TRUE)
C2card = C2card$X0

thetas = read.csv(paste0(pwd, 'simulation_star_thetas.csv'),  header=TRUE)
thetas = thetas$X0


pdf( paste0(pwdout,"FigStar.pdf"), height=10, width=14)

nf <- layout(matrix(1:12, byrow=TRUE, nrow=3))

for (theta in thetas[c(2, 3, 4)]){
  
  for (C2 in  C2card){
    
    
    if (C2 == 0){
      parleft = 7
      parright = 1
    } else if (C2==27){
      parleft = 1
      parright = 7
    } else if (C2 ==9) {
      parleft = 5
      parright = 3
    } else {
      parleft = 3
      parright = 5
    }
    
    if (theta == 1040){
      partop = 4
      partbottom = 1
    } else if (theta == 1050){
      partop = 2.5
      partbottom = 2.5
    } else {
      partop = 1
      partbottom = 4
    }
    
    par(mar=c(partbottom,parleft,partop,parright))
    
    
    results = read.csv(paste0(pwd, 'simulation_star_res_',theta, '_card_', C2,'.csv'), header=TRUE)
    results = results[,2:dim(results)[2]]
    results <- apply(as.matrix(results), 2, rev)
    results <- t(results)
    
    
    image(1:dim(results)[1], 1:dim(results)[2], results,
          xlab= ifelse( theta == 1060, TeX("$\\lambda_s$"), ""),
          ylab = ifelse( C2 ==0 , TeX(paste0("logit($p$), with $\\theta = $", theta)), ""),
          main = ifelse(theta == 1040, TeX(paste0('$|C_2| = $',C2)), "" ),
          cex.lab = 2,
          cex.axis = 2.5,
          cex.main =2,
          zlim = c(0, 1),
          col=colorRampPalette(brewer.pal(9, "Blues"))(30),
          axes = FALSE)
    axis(side = 1, at = 1:dim(results )[1], cex.axis = 1.5, labels = lambdas, mgp=c(2.5,0.8,0))
    axis(side = 2, at = 1:dim(results )[2], cex.axis = 1.5, labels = rev(logit_ps), mgp=c(1.9,0.8,0))
    box()
    
    for ( i in 1:dim(results)[1]){
      abline(v = i+0.5, lty = 2, col = "black", lwd = 0.5)
    }
    for ( j in 1:dim(results)[2]){
      abline(h = j+0.5, lty = 2, col = "black", lwd = 0.5)
    }
    
    if (theta == 1050 && C2 == 27){
      par(xpd=TRUE)
      legend("right",
             inset=c(-0.4,-0.4),
             legend= rev(c(0.0,0.2,0.4,0.6,0.8,1.0) ),
             bty = "n",
             cex = 2.2,
             horiz = FALSE,
             fill = rev(brewer.pal(6, "Blues") ),
             title="")
      par(xpd=FALSE)
    }
  }
  
}

dev.off()







#####################################
#########     CLUSTER expriment 


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



pdf(paste0(pwdout,"FigClust.pdf"), height=9, width=14)

theta = 1050
nf <- layout(matrix(1:6, byrow=TRUE, nrow=2))

for (graph in graphtype){
  for (cluster in c(0, 1, 2) ){
    
    
    if (graph == 'rchain'){
      partbottom = 2
      partop = 4
    } else {
      partbottom = 4
      partop = 2
    }
    
    if (cluster == 0){
      parleft = 7
      parright = 1
    } else if (cluster == 1){
      parleft = 4
      parright = 4
    } else {
      parleft = 1
      parright = 7
    }
    
    
    par(mar=c(partbottom,parleft,partop,parright))
    
    results = read.csv(paste0(pwd, 'simulation_cluster_res_',theta, '_graph_', graph, '_cluster_', cluster,  '.csv'), header=TRUE)
    results = results[,2:dim(results)[2]]
    results <- apply(as.matrix(results), 2, rev)
    results <- t(results)
    
    
    image(1:dim(results)[1], 1:dim(results)[2], results,
          xlab= ifelse( graph == 'lattice', TeX("$\\lambda_s$"), ""),
          ylab = ifelse( cluster ==0 , TeX(paste0("logit($p$), with ", graph, ' graph')), ""),
          main = ifelse(graph == 'rchain', TeX(paste0('$C_',cluster+1,'$') ), "" ),
          cex.lab = 2.5,
          cex.axis = 1.6,
          cex.main =2.5,
          zlim = c(0, 1),
          col=colorRampPalette(brewer.pal(9, "Blues"))(50),
          axes = FALSE)
    axis(side = 1, at = 1:dim(results )[1], cex.axis = 1.6, labels = lambdas, mgp=c(2.5,0.8,0))
    axis(side = 2, at = 1:dim(results )[2], cex.axis = 1.6, labels = rev(logit_ps), mgp=c(1.9,0.8,0))
    box()
    
    
    for ( i in 1:dim(results)[1]){
      abline(v = i+0.5, lty = 2, col = "black", lwd = 0.5)
    }
    for ( j in 1:dim(results)[2]){
      abline(h = j+0.5, lty = 2, col = "black", lwd = 0.5)
    }
    
    if (cluster == 2 && graph == 'rchain'){
      par(xpd=TRUE)
      legend("right",
             inset=c(-0.25,-0.25),
             legend= rev(c(0.0,0.2,0.4,0.6,0.8,1.0)),
             bty = "n",
             cex = 1.8,
             horiz = FALSE,
             fill = rev(brewer.pal(6, "Blues")),
             title="")
      par(xpd=FALSE)
    }
    
    
  }
}


dev.off()




pdf(paste0(pwdout,"FigClust1.pdf"), height=9, width=14)

graph = 'rchain'
cluster_s = c(2, 0)
nf <- layout(matrix(1:6, byrow=TRUE, nrow=2))

thetas_p = thetas[c(1, 3, 5)]

for (cluster in cluster_s){
  for (theta in thetas_p ){
  
    if (cluster == cluster_s[1]){
      partbottom = 2
      partop = 4
    } else {
      partbottom = 4
      partop = 2
    }
    
    if (theta == thetas_p[1]){
      parleft = 7
      parright = 1
    } else if (theta == thetas_p[2]){
      parleft = 4
      parright = 4
    } else {
      parleft = 1
      parright = 7
    }
    
    
    par(mar=c(partbottom,parleft,partop,parright))
    
    results = read.csv(paste0(pwd, 'simulation_cluster_res_',theta, '_graph_', graph, '_cluster_', cluster,  '.csv'), header=TRUE)
    results = results[,2:dim(results)[2]]
    results <- apply(as.matrix(results), 2, rev)
    results <- t(results)
    
    
    image(1:dim(results)[1], 1:dim(results)[2], results,
          xlab= ifelse( cluster == cluster_s[2], TeX("$\\lambda_s$"), ""),
          ylab = ifelse( theta ==thetas_p[1] , TeX(paste0("logit($p$), for $i \\in C_", cluster+1, "$")), ""),
          main = ifelse(cluster == cluster_s[1], TeX(paste0('$\\theta =',theta,'$') ), "" ),
          #mgp=c(2.2,3,0),
          cex.lab = 2.5,
          cex.axis = 1.6,
          cex.main =2.5,
          zlim = c(0, 1),
          col=colorRampPalette(brewer.pal(9, "Blues"))(50),
          axes = FALSE)
    axis(side = 1, at = 1:dim(results )[1], cex.axis = 1.6, labels = lambdas, mgp=c(2.5,0.8,0))
    axis(side = 2, at = 1:dim(results )[2], cex.axis = 1.6, labels = rev(logit_ps), mgp=c(1.9,0.8,0))
    box()
    
    
    for ( i in 1:dim(results)[1]){
      abline(v = i+0.5, lty = 2, col = "black", lwd = 0.5)
    }
    for ( j in 1:dim(results)[2]){
      abline(h = j+0.5, lty = 2, col = "black", lwd = 0.5)
    }
    
    if (theta ==thetas_p[3] && cluster == cluster_s[1]){
      par(xpd=TRUE)
      legend("right",
             inset=c(-0.25,-0.25),
             legend= rev(c(0.0,0.2,0.4,0.6,0.8,1.0)),
             bty = "n",
             cex = 1.8,
             horiz = FALSE,
             fill = rev(brewer.pal(6, "Blues")),
             title="")
      par(xpd=FALSE)
    }
    
  }
}

dev.off()








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






