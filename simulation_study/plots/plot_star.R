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


