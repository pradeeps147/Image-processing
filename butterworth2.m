fc=.1;
fs=1000;

[z,p,k] = butter(4,fc/500,'high');%zeroes,pole and gain(k)
sos = zp2sos(z,p,k);
fvtool(sos,'Analysis','freq')
