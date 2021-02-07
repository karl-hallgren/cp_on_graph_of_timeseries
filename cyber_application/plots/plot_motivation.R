# plot of ecp for motivation

pwd = "cyber_application/"


library(latex2exp)
library(RColorBrewer)
library(scales)



#####################
#########  Display the data for two users


logit_ps = read.csv(paste0(pwd, 'results/motivation_logit_p.csv'), header=FALSE)
logit_ps = logit_ps$V1[2:length(logit_ps$V1)]

transparencies = c(0.2, 0.5, 1.0)
coloursforplot = c('black')



pdf(paste0(pwd, 'plots/FigMotivDataKENT.pdf'), height=11, width=14)


nf <- layout(matrix(c(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                      2,2,2,2,2,2,2,2,2,2,2,2,2,2,2), byrow=TRUE, nrow=6))

set.seed(11)
patients = c('U342@DOM1','U86@DOM1')
for (patient in 1:2){
  
  X = read.csv(paste0(pwd, 'data/tseries/x_',patients[patient],'.csv'), header=TRUE)

  X_plot = as.matrix(t(X[1:720,names(sort(colSums(X), decreasing = TRUE))]))
  colnames(X_plot) <- NULL
  at_tick <- c(1, 100, 200, 300, 400, 500, 600, 700)
  
  par(mar=c(3.8,4.5,0.5,0.5))
  
  barplot(X_plot,
          border = NA,
          space=0,
          width = 1,
          ylim = c(0, 155),
          ylab = TeX("$x_{i, t}$"),
          xlab = ifelse(patient == 2, TeX("$t$"), ""),
          axes = FALSE,
          cex.lab = 2.5,
          xaxs = 'i',
          mgp=c(2.5,1.1,0),
          col = colorRampPalette(brewer.pal(12, "Paired")[1:12])(30)
  )
  box()
  axis(side = 1, at = at_tick - 1, labels = at_tick, mgp=c(2.5,1.1,0), cex.axis=1.9)
  axis(side = 2, at = seq(0, 150, 50), labels = seq(0, 150, 50), mgp=c(2.5,1.1,0), cex.axis=1.9)
  
}

dev.off()







#####################
#########  Display the data for two users with Bayes estimates




#pdf(paste0(pwd, 'plots/FigMotivBayesKENT.pdf'), height=13, width=14)
pdf(paste0(pwd, 'plots/FigMotivBayesKENT.pdf'), height=12, width=14)

nf <- layout(matrix(c(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4), byrow=TRUE, nrow=8))


for (patient in 1:2){
  
  # bayes estimate
  post_bayes_tau = read.csv(paste0(pwd, 'results/motivation_bayes_tau_',patients[patient],'.csv'), header=FALSE)
  post_bayes_tau = post_bayes_tau[2:dim(post_bayes_tau)[1],]
  
  X = read.csv(paste0(pwd, 'data/tseries/x_',patients[patient],'.csv'), header=TRUE)
  
  X_plot = as.matrix(t(X[1:720,names(sort(colSums(X), decreasing = TRUE))]))
  colnames(X_plot) <- NULL
  at_tick <- c(1, 300, 600, 900, 1200)
  
  
  p_s = c(1, 5, 9)
  
  if (patient ==1){
    par(mar=c(0,4.5,1,0.3))
  } else {
    par(mar=c(0,4.5,0,0.3))
  }
  
  barplot(X_plot,
          border = NA,
          space=0,
          width = 1,
          ylim = c(0, 155),
          ylab = TeX("$x_{i, t}$"),
          xlab = ifelse(patient == 2, TeX("$t$"), ""),
          axes = FALSE,
          cex.lab = 2.5,
          xaxs = 'i',
          mgp=c(2.5,1.1,0),
          col = colorRampPalette(brewer.pal(12, "Paired")[1:12])(30) 
  )
  
  axis(side = 1, at = at_tick - 1, labels = rep('', length(at_tick)), mgp=c(2.5,1.1,0), cex.axis=1.9)
  axis(side = 2, at = seq(50, 150, 50), labels = seq(50, 150, 50), mgp=c(2.5,1.1,0), cex.axis=1.9)
  
  
  for (p in 1:3){
    ypos = 4-p
    
    for (j in as.numeric(post_bayes_tau[p_s[p], ])){
      if (j > 0){
        
        abline(v = j, lty = 2, lwd = 1.5, col = alpha(coloursforplot[1], transparencies[p]))
        
      }
    }
  }
  box()
  
  if (patient ==1){
    par(mar=c(2,4.5,0,0.3))
  } else {
    par(mar=c(4,4.5,0,0.3))
  }
  
  
  plot(10,
       ylab = TeX("logit($p$)"),
       mgp=c(2.4,0.8,0),
       yaxt="n",
       xlab = ifelse(patient==1, "", "t"),
       #ylim = c(0, 4),
       cex.axis=1.4,
       cex.lab = 2.2,
       ylim = c(0.7, 4-0.7),
       xlim = c(1, dim(X_plot)[2]),xaxs = "i")
  
  for (p in 1:3){
    ypos = 4-p
    abline(h=ypos, lty = 1, col = "gray")
    for (j in as.numeric(post_bayes_tau[p_s[p], ])){
      if (j > 0){
        #abline(v = j, lty = 3)
        lines(x=c(j, j), y = c(ypos, 5), lty = 2, lwd = 1.5,
              col = alpha(coloursforplot[1], transparencies[p]))
        points(x = c(j), y = c(ypos), pch = 4, cex=2)
      }
    }
  }
  for (p in 1:3){
    ypos = 4-p
    for (j in as.numeric(post_bayes_tau[p_s[p], ])){
      if (j > 0){
        points(x = c(j), y = c(ypos), pch = 4, cex=2)
      }
    }
  }
  
  axis(2, at = 1:3, labels = rev(logit_ps[p_s]), mgp=c(2.4,0.8,0), cex.axis=1.4)
  box()
  
}

dev.off()









#####################
#########  Display posterior distribution of changepoints



pdf(paste0(pwd, 'plots/FigMotivPostkKENT.pdf'), height=6.5, width=14)

par(mfrow=c(1,2))
for (patient in 1:2){
  post_k = read.csv(paste0(pwd, 'results/motivation_post_k_',patients[patient],'.csv'), header=FALSE)
  k_s = as.numeric(post_k[1,])
  prob_s = post_k[2:(dim(post_k)[1]),]
  prob_s[is.na(prob_s)] = 0
  prob_s <- apply(as.matrix(prob_s), 2, rev)
  prob_s <- t(prob_s)
  
  if (patient ==1){
    par(mar=c(3,4,0.3,2))
  } else {
    par(mar=c(3,0,0.3,5))
  }
  
  image(1:dim(prob_s)[1], 1:dim(prob_s)[2], prob_s,
        xlab= TeX("$k_i$"),
        ylab = TeX("logit($p$)"),
        mgp=c(2,0.6,0),
        cex.lab = 1.5,
        col=colorRampPalette(brewer.pal(9, "Reds"))(30),
        axes = FALSE)
  axis(side = 1, at = 1:dim(prob_s)[1], labels = k_s, mgp=c(1,0.4,0))
  axis(side = 2, at = 1:dim(prob_s)[2], labels = rev(logit_ps), mgp=c(1,0.6,0))
  box()
  
  for ( i in 1:dim(prob_s)[1]){
    abline(v = i+0.5, lty = 2, col = "lightgrey", lwd = 0.5)
  }
  for ( j in 1:dim(prob_s)[2]){
    abline(h = j+0.5, col = "lightgrey", lwd = 0.5)
  }
  
  if (patient == 2){
    par(xpd=TRUE)
    legend("right",
           inset=c(-0.17,-0.17),
           legend= rev( c(0.0,0.2,0.4,0.6,0.8,1.0) ),
           bty = "n",
           cex = 1.3,
           horiz = FALSE,
           fill = rev( brewer.pal(6, "Reds")),
           title="Prob.")
    par(xpd=FALSE)
  }
  
}

dev.off()





