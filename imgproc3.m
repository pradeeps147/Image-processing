theta1=0;
ctimg=imread('mri.jpg');
[R1,xp]=radon(ctimg,theta1)
figure
imagesc(theta1,xp,R1)
colormap(gray)






