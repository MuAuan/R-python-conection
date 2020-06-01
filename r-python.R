library(cubature)
library(tuneR, pos=4)
library(tuneR)

#make a simple sine wave and play
t = seq(0, 3, 1/8000)
u = (2^15-1)*sin(2*pi*440*t)
w = Wave(u, samp.rate = 8000, bit=16)
play(w)
writeWave(w, 'w.wav')

wp <- "mywave.wav"
#wp <- "w.wav"
wave <- readWave(wp)
mono <- wave@left
spec <- fft(mono)
plot(spec,type='h',col='orange',ylab='FFT')
#dev.off()
plot(Re(spec),type='h',col='red', ylab='Re')
#dev.off()
plot(Im(spec),type='h',col='blue', ylab='Im')
#dev.off()
 
pspec = Re(spec)^2+Im(spec)^2 
 
#オイラー法
y<-pspec
x<-0
i<-1
Y<-numeric(0)
X<-numeric(0)
while(x<=10){
  Y[i]<-y
  X[i]<-x
  y<-y+y*0.01
  x<-x+0.01
  i<-i+1
}
plot(X,Y,type="l")
#dev.off()
 
#フーリエ級数（サイン波）
y2<-function(n,x){sin(n*x*2*pi)}
m.f<-function(m,k,c=0){
  f<-function(m,x,a,c){
    re<-0
    for(n in 1:a)re<-re+m(n,x)
    return(c+re)
  }
  y<-seq(-2*pi,2*pi,by=4*pi/1000)
  return(plot(y,f(m,y,k,c),type="l",xlab="x",ylab="y"))
}
m.f(y2,10,pi)
#dev.off()
 
#フーリエ級数（ノコギリ波、矩形波）
select<-T #セレクト用フラグ T(or TRUE) F(or FALSE)
ff<-function(n){
  function(x){
    sum<-0
    #sapply 1からnに対してfunction(n)の演算
    sum(sapply(1:n,function(n){
 
      if(select){
        sin(n*(x-floor(x))-1)    #ノコギリ波
      }
      else
      floor(sin(n*x)+1)    #矩形波
           
    }))
  }
}
pngFileName <- paste("./wine/fft_0.png",sep="")
png(file=pngFileName)
if(select) x<-seq(-pi,pi,length.out=100)    #ノコギリ波用
if(!select) x<-seq(0,8*pi,length.out=100)    #矩形波用
par(mfrow=c(2,2))    #グラフを分割して表示
for(n in seq(2,12,length.out=4)){
  plot(x,sapply(x,ff(n)),type="l")
}
dev.off()
 