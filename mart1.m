theta3=0:2:179;
ctimg=imread('mri.jpg');
[R3,xp]=radon(ctimg,theta3);
figure('Name','sinogram')
imagesc(theta3,xp,R3)
colormap(hot)
colorbar