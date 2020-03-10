obj=imread('mri.jpg')
%obj=[1 2;3 4]theta1=0:10:170;
theta2=0:5:175;
theta3=0:2:179;

   
ctimg=imread('mri.jpg');
ctimg=ctimg(:,:,1);
rad = radon(ctimg,theta2);

[R2,xp]=radon(ctimg,theta2);
[R3,xp]=radon(ctimg,theta3);
 
figure(1)
imagesc(theta3,xp,R3)
colormap(hot)
colorbar

p=size(obj)
for i=1:p(1)
    p012(i)=[sum(obj(i,:))];
end
for j=1:p(2)
    p034(j)=[sum(obj(:,j))];
end

p0=[p012;p034]
x=mean(mean(obj))
imshow(p0)
 
