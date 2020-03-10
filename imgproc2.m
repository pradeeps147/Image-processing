theta1=0:10:170; 
theta2=0:5:175;
theta3=0:1:179;

   
ctimg=imread('mri.jpg');
ctimg=ctimg(:,:,1);
[R1,xp]=radon(ctimg,theta1);
[R2,xp]=radon(ctimg,theta2);
[R3,xp]=radon(ctimg,theta3);
 
figure(1)
imagesc(theta3,xp,R3)
colormap(hot)
colorbar


output_size=max(size(ctimg));
 
dtheta1=theta1(2)-theta1(1);
I1=iradon(R1,dtheta1,'linear','shepp-logan',output_size);
 
dtheta2=theta2(2)-theta2(1);
 
 
dtheta3=theta3(2)-theta3(1);    
I2=iradon(R2,theta2,'linear','none',output_size);
I3=iradon(R3,dtheta3,'nearest','Ram-Lak',output_size);
figure(2)
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
