from numpy import linspace, sqrt, array, zeros
import tensorflow as tf
from tensorflow.python.ops.gen_math_ops import select
import matplotlib.pyplot as plt

class brownian_bridge:
    def __init__(self, length, variance):
        self.length = length
        self.variance = variance
        print("TensorFlow version:", tf.__version__)
        print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
        tf.config.set_visible_devices([], 'GPU')
        self.simulate()

    def simulate(self):
        self.X=linspace(0,1,self.length)
        self.tf_random()
        self.calculate_bounds()

    def calculate_bounds(self):
        print("S")
    
    def plot(self):
        fig, ax = plt.subplots()
        ax.plot(self.X, self.Y)
        plt.show()

    def tf_random(self):
        g1 = tf.random.Generator.from_non_deterministic_state()
        dt = 1.0 / (self.length -1)   
        self.dw=tf.math.scalar_mul(sqrt(dt),g1.normal(shape=[self.length-1])).numpy()
        self.Y=zeros(self.length)
        for i in range(len(self.Y)-1):
            self.Y[i+1]= self.Y[i]*(1-dt/(1-i*dt))+self.dw[i]
        self.Y[-1]=0.
