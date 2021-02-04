import torch
import torch.nn as nn
import torchvision.datasets as normal_datasets
import torchvision.transforms as transforms
from torch.autograd import Variable
import time
 
num_epochs = 5
batch_size = 100
learning_rate = 0.001
start_time=time.time()
 
# 将数据处理成Variable, 如果有GPU, 可以转成cuda形式
def get_variable(x):
    x = Variable(x)
    return x.cuda() if torch.cuda.is_available() else x
 
 
# 从torchvision.datasets中加载一些常用数据集
train_dataset = normal_datasets.MNIST(
    root="C:\\Users\\daicong\\.spyder-py3",  # 数据集保存路径
    train=True,  # 是否作为训练集
    transform=transforms.ToTensor(),  # 数据如何处理, 可以自己自定义
    download=False)  # 路径下没有的话, 可以下载
 
# 见数据加载器和batch
test_dataset = normal_datasets.MNIST(root="C:\\Users\\daicong\\.spyder-py3",
                                     train=False,
                                     transform=transforms.ToTensor())
 
train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                           batch_size=batch_size,
                                           shuffle=True)
 
test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
                                          batch_size=batch_size,
                                          shuffle=False)
 
 
# 两层卷积
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        # 使用序列工具快速构建
        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=5, padding=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2))
        self.conv2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=5, padding=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2))
        self.dense = torch.nn.Sequential(
            torch.nn.Linear(7 * 7 * 32,1024),
            torch.nn.ReLU(),
            torch.nn.Dropout(p = 0.5),
            torch.nn.Linear(1024,10)
        #self.fc = nn.Linear(7 * 7 * 32, 10)
        )
    def forward(self, x):
        out = self.conv1(x)
        out = self.conv2(out)
        #print(out.size()) #torch.Size([100, 32, 7, 7])
        out = out.view(out.size(0), -1)  # reshape
        #print(out.size()) #torch.Size([100, 1568])
        #out = self.fc(out)
        out = self.dense(out)
        return out
 
 
cnn = CNN()
print(cnn)
if torch.cuda.is_available():
    cnn = cnn.cuda()
 
# 选择损失函数和优化方法
loss_func = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(cnn.parameters(), lr=learning_rate)
 
for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_loader):
        images = get_variable(images)
        labels = get_variable(labels)
 
        outputs = cnn(images)
        loss = loss_func(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
 
        if (i + 1) % 100 == 0:
            print('Epoch [%d/%d], Iter [%d/%d] Loss: %.4f'
                  % (epoch + 1, num_epochs, i + 1, len(train_dataset) // batch_size, loss.item()))

end_time=time.time()
#print("Totle Time: %s"%(start_time - end_time))
# Save the Trained Model
torch.save(cnn.state_dict(), 'cnn.pkl')
print("start_time;{},end_time{},totle_time:{:.2f}min".format(start_time,end_time,(end_time-start_time)/60))
