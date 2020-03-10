fc = 150;
fs = 1000;

[b,a] = butter(10,fc/(fs/2));%b and a are trasfer fuction coeficient
fvtool(b,a)
%dataIn = randn(1000,1);
%dataOut = filter(b,a,dataIn);
y=filter(b,a,VarName3)
subplot(2,1,1)
plot(VarName3);
subplot(2,1,2);
plot(y)
