import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('model_full_batch_25000_mix_Batch_16_decay_droupout.txt')

x = data["iteration_no"].tolist()
y = data["losses"].tolist()

# plt.plot(x[2500:5000],y[2500:5000])
plt.plot(x,y)
plt.xlabel('Iterations')
plt.ylabel('Lossess')

plt.title('Itn Vs Losses')

plt.show()
# plt.save()
print (data["iteration_no"])
