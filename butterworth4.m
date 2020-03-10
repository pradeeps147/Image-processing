fc1=45,fc2=55;
fs=1000;
order=5;
x = chirp(t,100,1,200,'quadratic');
[b,a] = butter(5,[0.45 0.55],'stop');
fvtool(b,a)