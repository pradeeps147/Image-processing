fs = 4410;%sampling frequency
t = 0:1/fs:2;
x = chirp(t,100,1,200,'quadratic');
subplot(3,1,1)
plot(t,x)
title('analysed signal')
filteredsignal=filter(blpf,x);
subplot(3,1,2);
plot(t,filteredsignal);
title('band reject filtered signal')
fft1=fft(x);
subplot(3,1,3);
plot(abs(fft1))
