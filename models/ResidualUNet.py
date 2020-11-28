import torch.nn as nn
import torch.nn.functional as F


class PreConv(nn.Module):

    def __init__(self, in_c, out_c, k, s, p):
        """Full Pre-Activation Convolutional Layer"""
        super(PreConv, self).__init__()
        self.conv = nn.Sequential(
            nn.BatchNorm3d(in_c),
            nn.ReLU(),
            nn.Conv3d(in_c, out_c, k, s, p, bias=False)
        )

    def forward(self, x):
        return self.conv(x)


class ResidualBlock(nn.Module):

    def __init__(self, in_c, out_c):
        """Full Pre-activation Residual Block"""
        super(ResidualBlock, self).__init__()
        self.conv_1 = PreConv(in_c, out_c, 3, 1, 1)
        self.conv_2 = PreConv(out_c, out_c, 3, 1, 1)
        self.linear = nn.Conv3d(in_c, out_c, 1, 1)

    def forward(self, x):
        skip = self.linear(x)
        return skip + self.conv_2(self.conv_1(x))


class DoubleConv(nn.Module):

    def __init__(self, in_c, out_c):
        """(Conv ==> BatchNorm ==> ReLU)^2"""
        super(DoubleConv, self).__init__()
        self.double_conv = nn.Sequential(
            nn.Conv3d(in_c, out_c, 3, 1, 1),
            nn.BatchNorm3d(out_c),
            nn.ReLU(),
            nn.Conv3d(out_c, out_c, 3, 1, 1),
            nn.BatchNorm3d(out_c),
            nn.ReLU()
        )

    def forward(self, x):
        return self.double_conv(x)


class ResidualUNet(nn.Module):

    def __init__(self):
        """Residual U-Net with Full pre-activation residual encoder and standard double convolution
        decoder. Addition skip connections rather than concatenation to reduce memory requirements."""
        super(ResidualUNet, self).__init__()
        self.conv1 = nn.Conv3d(1, 16, 1, 1)
        self.res_1 = ResidualBlock(16, 32)
        self.res_2 = ResidualBlock(32, 64)
        self.res_3 = ResidualBlock(64, 128)
        self.res_4 = ResidualBlock(128, 256)

        self.dec_1 = DoubleConv()
        self.dec_2 = DoubleConv()
        self.dec_3 = DoubleConv()
        self.dec_4 = DoubleConv()

    def forward(self, x):
        return x