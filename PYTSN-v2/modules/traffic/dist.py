import random

class const():
 
    def __init__(self, inter_arr_time=1, size_in_bytes=100):
    	self.inter_arr_time = inter_arr_time
    	self.size_in_bytes = size_in_bytes
        
    def adist(self):
    	return (self.inter_arr_time)

    def sdist(self):
    	return (self.size_in_bytes)
        
class poisson():
 
    def __init__(self, rate_parameter=1, size_in_bytes=100):
    	self.rate_parameter = rate_parameter
    	self.size_in_bytes = size_in_bytes
        
    def adist(self):
    	result = random.expovariate(self.rate_parameter)
    	return (result)

    def sdist(self):
    	return (self.size_in_bytes)