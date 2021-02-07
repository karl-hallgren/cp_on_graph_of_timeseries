
library(latex2exp)
library(RColorBrewer)


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



