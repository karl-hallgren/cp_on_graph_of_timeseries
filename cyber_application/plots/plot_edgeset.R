

library(latex2exp)
library(RColorBrewer)


pwd = "cyber_application/"

nodes = read.csv(paste0(pwd, 'results/nodes.csv'), header=TRUE)


pdf(paste0(pwd, 'plots/KENTdegree.pdf'), height=7.0, width=16)

nf <- layout(matrix(1:2, byrow=FALSE, nrow=1))

br = seq(0, 103, by=1)


Xblue = nodes[nodes$X1 == 'False', ]$X2
Xred = nodes[nodes$X1 == 'True', ]$X2

histblue = hist(Xblue, br, plot = FALSE)
histred = hist(Xred, br, plot = FALSE)

X_plot = matrix(data = histblue$breaks[2:(length(histblue$breaks)-0)])
X_plot = cbind(X_plot,  histblue$counts)
X_plot = cbind(X_plot, histred$counts)

X_plot = t(X_plot[, c(2, 3)])

at_tick = c(1, 20, 40, 60, 80, 100)

par(mar=c(partbottom=4, parleft=4, partop=1, parright=2))

for (i in 1:2) {
barplot(X_plot[i, ],
        border = NA,
        space=0.1,
        width = 1,
        ylim = c(0, 10.5),
        xlim = c(0, 112.3),
        ylab = ifelse(i==1 , 'Frequency', ''),
        xlab = 'Degree',
        cex.axis = 1.5,
        cex.lab = 2,
        axes = FALSE,
        mgp=c(2.5,0.8,0),
        main ='',
        xaxs = 'i',
        col = c('#1f78b4')
)
box()
axis(side = 1, at = at_tick-0.5 + at_tick*0.1, labels = at_tick, mgp=c(2.5,0.7,0), cex.axis=1.5)
axis(side = 2, at = seq(0, 15, 3), labels = seq(0, 15, 3), mgp=c(2.5,0.7,0), cex.axis=1.5)

}

dev.off()
