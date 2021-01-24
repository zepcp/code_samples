import argparse
from enum import Enum
from typing import List, Optional
import numpy

import torch
import torchvision
import torchvision.transforms as transforms
from matplotlib import pyplot
from torch import nn
from torch.nn import functional
from torch import optim


class TorchContent(Enum):
    EMPTY = torch.empty
    ZEROS = torch.zeros
    RANDOM = torch.rand
    ONES = torch.ones


def numpy_ones(size: int) -> numpy:
    return numpy.ones(size)


def numpy_to_tensor(np: numpy) -> torch.Tensor:
    return torch.from_numpy(np)


def numpy_add(np: numpy, value: float) -> None:
    return numpy.add(np, value, out=np)


def tensor_new(length: int, height: int, content: TorchContent,
               dtype: torch.dtype = None) -> torch.Tensor:
    if height == 1:
        return content.value(length, dtype=dtype if dtype else torch.float)
    return content.value(length, height, dtype=dtype if dtype else torch.float)


def tensor_duplicate(tensor: torch.Tensor, dtype: torch.dtype = None,
                     resize: Optional[List[int]] = None, random: bool = False
                     ) -> torch.Tensor:
    if random:
        if dtype:
            return torch.randn_like(tensor, dtype=dtype)
        return torch.randn_like(tensor)
    if resize:
        if dtype:
            return tensor.new_ones(resize, dtype=torch.double)
        return tensor.new_ones(resize)


def tensor_from_array(array: List[float]) -> torch.Tensor:
    return torch.tensor(array)


def tensor_add(tensor_1: torch.Tensor, tensor_2: torch.Tensor,
               output: torch.Tensor = None) -> torch.Tensor:
    if tensor_1.size() != tensor_2.size():
        raise

    if type(output) == torch.Tensor:
        # if output==tensor_1 => return tensor_1.add_(tensor_2)
        return torch.add(tensor_1, tensor_2, out=output)
    return torch.add(tensor_1, tensor_2)  # == tensor_1 + tensor_2


def tensor_to_numpy(tensor: torch.Tensor) -> numpy:
    return tensor.numpy()


def get_started():
    # Tensor Create
    print(tensor_new(5, 3, TorchContent.EMPTY))
    print(tensor_new(5, 3, TorchContent.RANDOM))
    print(tensor_new(5, 3, TorchContent.ZEROS))

    # Tensor Create From (re-use properties)
    x = tensor_from_array([5.5, 3])
    print(x)
    x = tensor_duplicate(x, resize=[5, 3], dtype=torch.double)
    print(x)
    x = tensor_duplicate(x, random=True, dtype=torch.float)
    print(x)

    # Tensor Operations - Sum
    x = torch.rand(5, 3)
    y = torch.rand(5, 3)
    print(tensor_add(x, y))
    print(tensor_add(x, y, output=x))

    # Tensor Operations - Resize
    x = torch.randn(4, 4)
    y = x.view(16)
    z = x.view(-1, 8)  # the size -1 is inferred from other dimensions
    print(x.size(), y.size(), z.size())

    # Tensor Operations - 1 element tensor to number
    x = torch.randn(1)
    print(x.item())

    # Tensor - NumPy
    a = tensor_new(5, 1, TorchContent.ONES)
    b = tensor_to_numpy(a)
    a.add_(1)
    print(a, b)

    a = numpy_ones(5)
    b = numpy_to_tensor(a)
    numpy_add(a, 1)
    print(a, b)


def download_data() -> (torchvision.datasets.CIFAR10, torchvision.datasets.CIFAR10,
                        List[str]):
    transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                            download=True, transform=transform)
    testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                           download=True, transform=transform)

    return (
        torch.utils.data.DataLoader(
            trainset, batch_size=4, shuffle=True, num_workers=2),
        torch.utils.data.DataLoader(
            testset, batch_size=4, shuffle=False, num_workers=2),
        ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
    )


def show_image(image: torch.Tensor) -> None:
    img = image / 2 + 0.5  # Unnormalize
    npimg = img.numpy()
    pyplot.imshow(numpy.transpose(npimg, (1, 2, 0)))
    pyplot.show()


def show_random_images(loader: torchvision.datasets.CIFAR10, labels: List[str]
                       ) -> torch.Tensor:
    dataiter = iter(loader)
    images, labels = dataiter.next()

    # show images
    show_image(torchvision.utils.make_grid(images))

    # print labels
    print('Ground Truth: ', ' '.join('%s' % labels[labels[j]] for j in range(4)))
    return images


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(functional.relu(self.conv1(x)))
        x = self.pool(functional.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = functional.relu(self.fc1(x))
        x = functional.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def train(net: Net, path: str) -> None:
    # Define Loss Function & Optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    # Train Network
    for epoch in range(2):  # loop over the dataset multiple times
        running_loss = 0.0
        for i, data in enumerate(train_loader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 2000 == 1999:  # print every 2000 mini-batches
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / 2000))
                running_loss = 0.0

    print('Finished Training')

    # Store trained data
    torch.save(net.state_dict(), path)


def accuracy(test_loader: torchvision.datasets.CIFAR10) -> (int, int):
    correct, total = 0, 0
    with torch.no_grad():
        for data in test_loader:
            images, labels = data
            outputs = neural_network(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    return correct, total


def accuracy_by_label(test_loader: torchvision.datasets.CIFAR10, nr_labels: int
                      ) -> (List[int], List[int]):
    class_correct = list(0. for _ in range(nr_labels))
    class_total = list(0. for _ in range(nr_labels))
    with torch.no_grad():
        for data in test_loader:
            images, labels = data
            outputs = neural_network(images)
            _, predicted = torch.max(outputs, 1)
            c = (predicted == labels).squeeze()
            for i in range(4):
                label = labels[i]
                class_correct[label] += c[i].item()
                class_total[label] += 1

    return class_correct, class_total


def train_net(net: Net, save_to: str):
    train(net, save_to)


def load_net(net: Net, load_from: str):
    net.load_state_dict(torch.load(load_from))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", '-d', choices=["train, load"], default="load")
    parser.add_argument("--save", '-s', type=str, default="./cifar_net.pth")
    args = parser.parse_args()

    # get_started()
    train_loader, test_loader, classes = download_data()

    # Define Convolutional Neural Network
    neural_network = Net()

    # Train or load trained data
    train_net(neural_network, args.save) if args.data == "train" \
        else load_net(neural_network, args.save)

    # images = show_random_images(test_loader, classes)
    # outputs = neural_network(images)
    # _, predicted = torch.max(outputs, 1)
    # print('Predicted: ', ' '.join('%s' % classes[predicted[j]] for j in range(4)))

    correct, total = accuracy(test_loader)
    print("Accuracy of the network: %d %%" % (100 * correct / total))

    # correct, total = accuracy_by_label(test_loader, len(classes))
    # for x in range(len(classes)):
    #     print('Accuracy of %s : %d %%' % (classes[x], 100 * correct[x] / total[x]))
