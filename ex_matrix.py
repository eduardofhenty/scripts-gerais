import numpy as np
#import numpy.ma as ma 
a = np.array([[0,1],[2,3]])
b = np.array([[1,3],[3,5]])
c = np.array([[0,1],[4,2]])
d = np.array([[3,2],[2,3]])
e = np.array([[4,2],[1,1]])
print(a)
print(a.shape)

dado=[]
dado.append(a)
dado.append(b)
dado.append(c)
dado.append(d)
dado.append(e)



#A = ma.zeros((5,2,2))
#A.mask = np.zeros_like(A)
#A[1,:,:]=a


res=np.max(dado,axis=0)
print("valor Maximo")
print(res)

res=np.min(dado,axis=0)
print("valor Mínimo")
print(res)

res=np.mean(dado,axis=0)
print("valor Médio")
print(res)

def gerafig (gr,file):
    


