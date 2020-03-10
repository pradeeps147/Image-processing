p=phantom(255)
theta1 =19;
[R1,xp]=radon(p,theta1)
output_size=max(size(p))
figure(1)
colormap(hot)
imagesc(theta1,xp,R1)


I1=iradon(R1,theta1,'nearest','Ram-lak',output_size)
figure(2)
imagesc(I1)
colormap(gray)
theta2 =1:10:180;
[R2,xp]=radon(p,theta2)
figure(1)
colormap(hot)
imagesc(theta2,xp,R2);
theta2=theta2(2)-theta2(1)
I2=iradon(R2,theta2,'linear','Ram-lak',output_size)
figure(3)
imagesc(I2)
colormap(gray)
theta3 =1:1:180;
[R3,xp]=radon(p,theta3)
figure(1)
colormap(hot)
imagesc(theta2,xp,R2)
theta3=theta3(2)-theta3(1)
I3=iradon(R3,theta3,'nearest','none',output_size);
figure(4)
imagesc(I3)
colormap(gray)