# image-processing
#GRADIENT DECENT 
import numpy as np,sys,os
from scipy.signal import convolve
from skimage.measure import block_reduce
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from scipy.ndimage import imread
from matplotlib.pyplot import plot, draw, show,ion
np.random.randn(6789)


def tanh(x):
    return np.tanh(x)
def d_tanh(x):
    return 1 - np.tanh(x) ** 2
def ReLu(x):
    mask = (x>0) * 1.0
    return mask *x
def d_ReLu(x):
    mask = (x>0) * 1.0
    return mask 
def log(x):
    return 1 / (1 + np.exp(-1 * x))
def d_log(x):
    return log(x) * ( 1 - log(x))
def arctan(x):
    return np.arctan(x)
def d_arctan(x):
    return 1 / (1 + x ** 2)
def softmax(x):
    shiftx = x - np.max(x)
    exp = np.exp(shiftx)
    return exp/exp.sum()



uploaded = files.upload()
for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(name=fn, length=len(uploaded[fn])))
  
temp = uploaded[list(uploaded.keys())[0]]
f = io.BytesIO(temp)
archive = zipfile.ZipFile(f, 'r')

one = np.zeros((119,512,512))
for image_index in range(len(one)):
  file = archive.read('lung_data/DOI/NoduleLayout_1/1.2.840.113704.1.111.1664.1186756141.2/1.2.840.113704.1.111.4116.1186756880.24/'+str(image_index)+'.jpg')
  one[image_index,:,:]   = np.array(dicom.read_file(io.BytesIO(file)).pixel_array)
  

training_data = one
# training_data = np.vstack((one,two,three))

num_epoch = 100
learn_rate_e = 0.0000007
learn_rate_d = 0.0000001
cost_array = []
total_cost = 0 

beta_1,beta_2 = 0.9,0.999
adam_e = 0.00000001

# 2. Build Class for Encoder and Decoder
class Encoder():
    
    def __init__(self):
        self.w1 = np.random.randn(7,7)* 0.01
        self.w2 = np.random.randn(5,5)* 0.01
        self.w3 = np.random.randn(3,3)* 0.01
        self.w4 = np.random.randn(4096,1000)* 0.1

        self.input,self.output = None,None

        self.l1,self.l1A,self.l1M = None, None, None
        self.l2,self.l2A,self.l2M = None, None, None
        self.l3,self.l3A,self.l3M = None, None, None
        
        self.l4Input  = None
        self.l4,self.l4A = None, None

        self.v1,self.v2,self.v3,self.v4 = 0,0,0,0
        self.m1,self.m2,self.m3,self.m4 =  0,0,0,0
        

    def feed_forward(self,input):
        
        self.input = input
        self.l1  = convolve2d(input,self.w1,'same')
        self.l1M = block_reduce(self.l1,(2,2), np.mean)
        self.l1A = tanh(self.l1M)

        self.l2  = convolve2d(self.l1A,self.w2,'same')
        self.l2M = block_reduce(self.l2,(2,2), np.mean)
        self.l2A = arctan(self.l2M)

        self.l3  = convolve2d(self.l2A,self.w3,'same')
        self.l3M = block_reduce(self.l3,(2,2), np.mean)
        self.l3A = tanh(self.l3M)

        self.l4Input = np.reshape(self.l3A,(1,-1))
        self.l4 = self.l4Input.dot(self.w4)
        self.l4A = self.output = arctan(self.l4)

        return self.output

    def back_propagation(self,gradient):

        grad_4_part_1 = gradient
        grad_4_part_2 = d_arctan(self.l4)
        grad_4_part_3 = self.l4Input
        grad_4 = grad_4_part_3.T.dot(grad_4_part_1 * grad_4_part_2)

        grad_3_part_1 = np.reshape((grad_4_part_1 * grad_4_part_2).dot(self.w4.T),(64,64))
        grad_3_part_2 = d_tanh(self.l3M)
        grad_3_part_M = (grad_3_part_1 * grad_3_part_2).repeat(2,axis=0).repeat(2,axis=1)
        grad_3_part_3 = np.pad(self.l2A,1,'constant')
        grad_3 = np.rot90(convolve2d(grad_3_part_3,    np.rot90( grad_3_part_M ,2),'valid')  ,2)

        grad_2_part_1 = convolve2d( self.w3  , np.rot90(np.pad(grad_3_part_M,1,'constant')    ,2)  ,'valid')
        grad_2_part_2 = d_arctan(self.l2M)
        grad_2_part_M = (grad_2_part_1 * grad_2_part_2).repeat(2,axis=0).repeat(2,axis=1)
        grad_2_part_3 = np.pad(self.l1A,2,'constant')
        grad_2 = np.rot90(convolve2d(grad_2_part_3,    np.rot90( grad_2_part_M ,2),'valid')  ,2)
                
        grad_1_part_1 = convolve2d( self.w2  , np.rot90(np.pad(grad_2_part_M,2,'constant')    ,2)  ,'valid')
        grad_1_part_2 = d_tanh(self.l1M)
        grad_1_part_M = (grad_1_part_1 * grad_1_part_2).repeat(2,axis=0).repeat(2,axis=1)
        grad_1_part_3 = np.pad(self.input,3,'constant')
        grad_1 = np.rot90(convolve2d(grad_1_part_3,    np.rot90( grad_1_part_M ,2),'valid')  ,2)

        self.m4 = self.m4 * beta_1 + (1 - beta_1) * grad_4
        self.m3 = self.m3 * beta_1 + (1 - beta_1) * grad_3
        self.m2 = self.m2 * beta_1 + (1 - beta_1) * grad_2
        self.m1 = self.m1 * beta_1 + (1 - beta_1) * grad_1

        self.v4 = self.v4 * beta_2 + (1 - beta_2) * grad_4** 2
        self.v3 = self.v3 * beta_2 + (1 - beta_2) * grad_3** 2
        self.v2 = self.v2 * beta_2 + (1 - beta_2) * grad_2** 2
        self.v1 = self.v1 * beta_2 + (1 - beta_2) * grad_1** 2

        m4_hat = self.m4 / ( 1- beta_1)
        m3_hat = self.m3 / ( 1- beta_1)
        m2_hat = self.m2 / ( 1- beta_1)
        m1_hat = self.m1 / ( 1- beta_1)
      
        v4_hat = self.v4 / ( 1- beta_2)
        v3_hat = self.v3 / ( 1- beta_2)
        v2_hat = self.v2 / ( 1- beta_2)
        v1_hat = self.v1 / ( 1- beta_2)  

        self.w4 = self.w4 - (learn_rate_e/( np.sqrt(v4_hat)  + adam_e  )) *    m4_hat
        self.w3 = self.w3 - (learn_rate_e/( np.sqrt(v3_hat)  + adam_e  )) *    m3_hat  
        self.w2 = self.w2 - (learn_rate_e/( np.sqrt(v2_hat)  + adam_e  )) *    m2_hat   
        self.w1 = self.w1 - (learn_rate_e/( np.sqrt(v1_hat)  + adam_e  )) *    m1_hat   
             
class Decoder():
    
    def __init__(self):
        self.w1 = np.random.randn(1000,4096) * 0.1
        self.w2 = np.random.randn(3,3)* 0.01
        self.w3 = np.random.randn(5,5)* 0.01
        self.w4 = np.random.randn(7,7)* 0.01

        self.input,self.output = None, None

        self.l1,self.l1A = None,None

        self.l2Input = None
        self.l2,self.l2A,self.l2M = None, None, None
        self.l3,self.l3A,self.l3M = None, None, None
        self.l4,self.l4A,self.l4M = None, None, None

        self.v1,self.v2,self.v3,self.v4 =  0,0,0,0
        self.m1,self.m2,self.m3,self.m4 =  0,0,0,0

    def feed_forward(self,input):
        
        self.input = input
        
        self.l1 = self.input.dot(self.w1)
        self.l1A = arctan(self.l1)

        self.l2Input = np.reshape(self.l1A,(64,64))
        self.l2M   =   self.l2Input.repeat(2,axis=0).repeat(2,axis=1)
        self.l2    =   convolve2d(self.l2M,self.w2,'same')
        self.l2A   =   arctan(self.l2)

        self.l3M   = self.l2A.repeat(2,axis=0).repeat(2,axis=1)
        self.l3    = convolve2d(self.l3M,self.w3,'same')
        self.l3A   = arctan(self.l3)
        
        self.l4M   = self.l3A.repeat(2,axis=0).repeat(2,axis=1)
        self.l4    = convolve2d(self.l4M,self.w4,'same')
        self.l4A = self.output = log(self.l4)

        return self.output

    def back_propagation(self,gradient):

        grad_4_part_1 = gradient
        grad_4_part_2 = d_log(self.l4)
        grad_4_part_3 = np.pad(self.l4M,3,'constant')
        grad_4 = np.rot90(convolve2d(grad_4_part_3,np.rot90(grad_4_part_1 * grad_4_part_2,2),'valid'),2)

        grad_3_part_1 = convolve2d( self.w4,  np.rot90(np.pad(grad_4_part_1 * grad_4_part_2,3,'constant') ,2), 'valid'  )[::2,::2]  
        grad_3_part_2 = d_arctan(self.l3)
        grad_3_part_3 = np.pad(self.l3M,2,'constant')
        grad_3 = np.rot90(convolve2d(grad_3_part_3,np.rot90(grad_3_part_1 * grad_3_part_2,2),'valid'),2)

        grad_2_part_1 = convolve2d( self.w3,  np.rot90(np.pad(grad_3_part_1 * grad_3_part_2,2,'constant') ,2), 'valid'  )[::2,::2]  
        grad_2_part_2 = d_arctan(self.l2)
        grad_2_part_3 = np.pad(self.l2M,1,'constant')
        grad_2 = np.rot90(convolve2d(grad_2_part_3,np.rot90(grad_2_part_1 * grad_2_part_2,2),'valid'),2)

        grad_1_part_1 = np.reshape(convolve2d( self.w2,  np.rot90(np.pad(grad_2_part_1 * grad_2_part_2,1,'constant') ,2), 'valid'  )[::2,::2],(1,-1))
        grad_1_part_2 = d_arctan(self.l1)
        grad_1_part_3 = self.input
        grad_1 = grad_1_part_3.T.dot(grad_1_part_1 * grad_1_part_2)

        grad_passon = (grad_1_part_1 * grad_1_part_2).dot(self.w1.T)

        self.m4 = self.m4 * beta_1 + (1 - beta_1) * grad_4
        self.m3 = self.m3 * beta_1 + (1 - beta_1) * grad_3
        self.m2 = self.m2 * beta_1 + (1 - beta_1) * grad_2
        self.m1 = self.m1 * beta_1 + (1 - beta_1) * grad_1

        self.v4 = self.v4 * beta_2 + (1 - beta_2) * grad_4** 2
        self.v3 = self.v3 * beta_2 + (1 - beta_2) * grad_3** 2
        self.v2 = self.v2 * beta_2 + (1 - beta_2) * grad_2** 2
        self.v1 = self.v1 * beta_2 + (1 - beta_2) * grad_1** 2

        m4_hat = self.m4 / ( 1- beta_1)
        m3_hat = self.m3 / ( 1- beta_1)
        m2_hat = self.m2 / ( 1- beta_1)
        m1_hat = self.m1 / ( 1- beta_1)
      
        v4_hat = self.v4 / ( 1- beta_2)
        v3_hat = self.v3 / ( 1- beta_2)
        v2_hat = self.v2 / ( 1- beta_2)
        v1_hat = self.v1 / ( 1- beta_2)  

        self.w4 = self.w4 - (learn_rate_e/( np.sqrt(v4_hat)  + adam_e  )) *    m4_hat
        self.w3 = self.w3 - (learn_rate_e/( np.sqrt(v3_hat)  + adam_e  )) *    m3_hat  
        self.w2 = self.w2 - (learn_rate_e/( np.sqrt(v2_hat)  + adam_e  )) *    m2_hat   
        self.w1 = self.w1 - (learn_rate_e/( np.sqrt(v1_hat)  + adam_e  )) *    m1_hat  
        
        return grad_passon

# 3. Define Each Layer object
encoder = Encoder()
decoder = Decoder()

# 4. Training both the encoder and decoder
for iter in range(num_epoch):
    for image_index in range(len(training_data)):
        
        current_data = training_data[image_index,:,:]
        current_data_noise =  current_data + 0.3 * current_data.max() *np.random.randn(current_data.shape[0],current_data.shape[1])

        encoded_vector = encoder.feed_forward(current_data_noise)
        decoded_image  = decoder.feed_forward(encoded_vector)

        naive_cost = np.square(decoded_image - current_data).sum() * 0.25
        print("Current Iter :",iter,"  Current Image Index:  ",image_index ," Real Time Update Cost: ", naive_cost,end='\r')
        total_cost+= naive_cost
        
        gradient = decoder.back_propagation((decoded_image - current_data)*0.5)
        encoder.back_propagation(gradient)

    if iter % 1 == 0 :
        print('\n======================================')
        print("current Iter: ", iter, " Current Total Cost :", total_cost/len(training_data))

        for test_index in range(5):
            
            temp = shuffle(training_data)

            current_data = temp[test_index,:,:]
            current_data_noise =  current_data + 0.3 * current_data.max() *np.random.randn(current_data.shape[0],current_data.shape[1])

            encoded_vector = encoder.feed_forward(current_data_noise)
            decoded_image  = decoder.feed_forward(encoded_vector)
 
        print('======================================')

    cost_array.append(total_cost/len(training_data))
    total_cost = 0
# ---------------------------------
for test_index in range(30):
    
    temp = shuffle(training_data)

    current_data = temp[test_index,:,:]
    current_data_noise =  current_data + 0.3 * current_data.max() *np.random.randn(current_data.shape[0],current_data.shape[1])

    encoded_vector = encoder.feed_forward(current_data_noise)
    decoded_image  = decoder.feed_forward(encoded_vector)

    f, axarr = plt.subplots(2, 2)
    axarr[0, 0].imshow(current_data,cmap='gray')
    axarr[0, 0].set_title('Original : ' + str(test_index))
    axarr[0, 1].imshow(current_data_noise,cmap='gray')
    axarr[0, 1].set_title('Add noise: ' + str(test_index))
    axarr[1, 0].imshow(decoded_image,cmap='gray')
    axarr[1, 0].set_title('Decoded: ' + str(test_index))
    plt.show()

plt.title("Cost over time")
plt.plot(np.arange(len(cost_array)), cost_array)
plt.show()
