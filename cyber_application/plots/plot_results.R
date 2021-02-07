
library(latex2exp)
library(RColorBrewer)
library(scales)


pwd = "cyber_application/"
#pwd = "/Users/karlh/Documents/PhD/multi_cp/cp_graph_tseries_code/cyber_application/"


logit_ps = read.csv(paste0(pwd, '/results/logit_p_s.csv'), header=TRUE)
logit_ps = logit_ps$X0
logit_i_s = c(2, 4, 6) #c(1, 2, 3, 4, 5, 6, 7)#


collines = colorRampPalette(brewer.pal(8, "Dark2"))(length(logit_i_s)) 

lambdas = c(0, 0.5, 0.6, 0.7, 0.8)
lambdas_i = c(1, 2, 3, 4, 5)



###########
##### number of changepoints two plots

pdf(paste0(pwd, 'plots/KENTcpnum.pdf'), height=9, width=14)


nf <- layout(matrix(1:2, byrow=FALSE, nrow=1))

partbottom = 4
partop = 0.5

for (type_i in c('notred', 'red')) {
  
  
  parleft = ifelse(type_i == 'notred', 4, 1.5)
  parright = ifelse(type_i == 'red', 4, 1.5)
  
  par(mar=c(partbottom,parleft,partop,parright))
  
  plot( 0, -300,
        type = 'b',
        lty = 2,
        xaxt = "n",
        cex.axis = 1.5,
        cex.lab = 2,
        ylab = ifelse( type_i == 'notred', TeX("$k_i$"), ""),
        xlab = TeX("$\\lambda_s$"),
        mgp=c(2.5,0.8,0),
        ylim = c(0.9, 4.7), #ylim =c(0.8, 4.5),
        xlim = c(0, length(lambdas_i)-1) )
  axis(side = 1, at = 0:(length(lambdas_i)-1), cex.axis = 1.5, labels = lambdas[lambdas_i], mgp=c(2.5,0.8,0))
  
  grid(col = 'gray')
  for (wind in c('nw', 'uw')){
  #for (wind in c('nw')){
    if (wind == 'nw'){
      pch_wind = 19
      lty_wind = 3
      alpha_wind = 0.5
    } else if ( wind == 'fw12'){
      pch_wind = 17
      lty_wind = 2
      alpha_wind = 0.7
    } else {
      pch_wind = 17
      lty_wind = 5
      alpha_wind = 1
    }
    
    
    cp_num = read.csv(paste0(pwd, 'results/num_cp_',type_i,'_', wind,'.csv'), header=TRUE)
    
    for (p in 1:length(logit_i_s) ){
      
      lines(0:(length(lambdas_i)-1),  cp_num[logit_i_s[p], lambdas_i],
            col = alpha(collines[p], alpha_wind),
            type = 'b',
            pch = pch_wind,
            lwd = ifelse(wind == 'nw', 3, 3),
            cex = 1.8,
            lty = lty_wind
      )
      
    }
  }
  
  if (type_i == 'notred'){
    
    legend("topleft",
           inset=c(0.05,0.05),
           legend= logit_ps[logit_i_s],
           bty = "n",
           cex = 1.5,
           horiz = FALSE,
           fill = collines,
           title=TeX("$\\bar{p}$"))
  }
}

dev.off()



##############################
########################


### average m_i

pdf(paste0(pwd, 'plots/KENTcpni.pdf'),height=9, width=14)


nf <- layout(matrix(1:2, byrow=FALSE, nrow=1))

partbottom = 4
partop = 0.5

for (type_i in c('notred', 'red')) {
  
  parleft = ifelse(type_i == 'notred', 4, 1.5)
  parright = ifelse(type_i == 'red', 4, 1.5)
  
  par(mar=c(partbottom,parleft,partop,parright))
  
  plot(0, -300,
       type = 'b',
       lty = 2,
       xaxt = "n",
       cex.axis = 1.5,
       cex.lab = 2,
       ylab = ifelse( type_i == 'notred', TeX("$m_i$"), ""),
       xlab = TeX("$\\lambda_s$"),
       mgp=c(2.5,0.8,0),
       ylim = c(0.35, 1.45),
       xlim = c(0, (length(lambdas_i)-1))
  )
  axis(side = 1, at = 0:(length(lambdas_i)-1), cex.axis = 1.5, labels = lambdas[lambdas_i], mgp=c(2.5,0.8,0))
  
  grid(col = 'gray')
  

  for (wind in c('nw', 'uw')){
    
    
    if (wind == 'nw'){
      pch_wind = 19
      lty_wind = 3
      alpha_wind = 0.5
    } else if ( wind == 'fw12'){
      pch_wind = 17
      lty_wind = 2
      alpha_wind = 0.7
    } else {
      pch_wind = 17
      lty_wind = 5
      alpha_wind = 1
    }
    
    
    cp_num = read.csv(paste0(pwd, 'results/sum_ni_dd_',type_i,'_', wind,'.csv'), header=TRUE)
    
    for (p in 1:length(logit_i_s) ){
      
      lines(0:(length(lambdas_i)-1),  cp_num[logit_i_s[p], lambdas_i],
            col = alpha(collines[p], alpha_wind),
            type = 'b',
            pch = pch_wind,
            lwd = 3,
            cex = 1.8,
            lty = lty_wind
      )
    }
  }
  
  if (type_i == 'notred'){
    
    legend("topleft",
           inset=c(0.05,0.05),
           legend= logit_ps[logit_i_s],
           bty = "n",
           cex = 1.5,
           horiz = FALSE,
           fill = collines,
           title=TeX("$\\bar{p}$"))
  }
}

dev.off()
