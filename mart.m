theta3=0:2:179;
ctimg=imread('mri.jpg');
[R3,xp]=radon(ctimg,theta3);
figure('Name','sinogram')
imagesc(theta3,xp,R3)
colormap(hot)
colorbar
[A b x] = parallelct(50,0:2:179,150);
e = randn(size(b)); e = e/norm(e);
b = b + 0.05*norm(b)*e;
X = kaczmarz(A,b,1:500);
imagesc(reshape(X(:,end),50,50))
colormap gray, axis image off
 N = 256;
theta = 1:180;
[A,b] = paralleltomo(N,theta);
x = fbp(A,b,theta);
imagesc(reshape(x,N,N))
colormap gray, axis image off 
 P = phantom('Modified Shepp-Logan',200);
 imshow(P)