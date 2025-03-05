from machine import I2C, Pin
import time

# 初始化I2C接口
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# RDA5807M模块的I2C地址
RDA5807M_ADDR = 0x1E


# 初始化RDA5807M模块
def init_rda5807m():
    # 发送初始化命令
    i2c.writeto(RDA5807M_ADDR, b'\x02\x00\x00\x00\x00')  # 关闭静音
    i2c.writeto(RDA5807M_ADDR, b'\x03\x00\x00\x00\x00')  # 设置音量
    i2c.writeto(RDA5807M_ADDR, b'\x04\x10\x00\x00\x00')  # 设置频率范围（76MHz-108MHz）
    i2c.writeto(RDA5807M_ADDR, b'\x07\x00\x00\x00\x00')  # 开启搜索模式


# 设置频率
def set_frequency(freq):
    freq_reg = int((freq * 10) - 870)  # 将频率转换为寄存器值
    i2c.writeto(RDA5807M_ADDR, b'\x02\x10\x00\x00\x00')  # 取消静音
    i2c.writeto(RDA5807M_ADDR, bytes([0x04, freq_reg >> 8, freq_reg & 0xFF, 0x00, 0x00]))  # 设置频率


# 主程序
def main():
    init_rda5807m()
    print("RDA5807M FM Radio Initialized.")

    # 设置频率到93.7MHz
    set_frequency(100.3)
    print("Tuning to 93.7MHz...")

    while True:
        time.sleep(1)  # 保持运行


if __name__ == "__main__":
    main()