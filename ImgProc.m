
theta1=0:10:170;
theta2=0:5:175;
theta3=0:1:179;

ctimg=imread('mri.jpg');
ctimg=ctimg(:,:,1);
[R1,xp]=radon(ctimg,theta1);
[R2,xp]=radon(ctimg,theta2);
[R3,xp]=radon(ctimg,theta3);

figure('Name','sinogram')
imagesc(theta3,xp,R3)
colormap(gray)
colorbar

output_size=max(size(ctimg));

dtheta1=theta1(2)-theta1(1);
I1=iradon(R1,dtheta1,'nearest','none',output_size);

dtheta2=theta2(2)-theta2(1);


dtheta3=theta3(2)-theta3(1);
I2=iradon(R2,dtheta2,'linear','Hamming',output_size);
I3=iradon(R3,dtheta3,'nearest','linear','Ram-lak',output_size);
dtheta2 = num2str(dtheta2);
str = strcat('Reconstrcuted image, dtheta =',dtheta2);
figure('Name','num');
imagesc(I1)
colormap(gray)
title('Reconstruction from Parallel Beam Projection with 18 Projection Angles')

figure(3)
imagesc(I2)
colormap(gray)
title('Reconstruction from Parallel Beam Projection with  24 Projection Angles')

figure(4)
imagesc(I3)
colormap(gray)
title('Reconstruction from Parallel Beam Projection with  90 Projection Angles')

