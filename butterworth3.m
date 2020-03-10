fc1=1,fc2=100;
fs=1000;

[A,B,C,D] = butter(20,[fc1 fc2]/500);
% d = designfilt('bandpassiir','FilterOrder',20, ...
%     'HalfPowerFrequency1',fc1,'HalfPowerFrequency2',fc2, ...
%     'SampleRate',1000);
sos = ss2sos(A,B,C,D);
fvt = fvtool(sos,'fs',1000);
legend(fvt,'butter')