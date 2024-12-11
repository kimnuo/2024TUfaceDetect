from tensorflow.keras.callbacks import Callback

class NBatchCallback(Callback):
    def __init__(self, n):
        super().__init__()
        self.n = n  # n번마다 콜백 수행
        self.batch_count = 0  # 현재 배치 카운트


    def on_batch_end(self, batch, logs=None):
        # 배치 종료 시 호출
        self.batch_count += 1
        if self.batch_count % self.n == 0:
            print(f"Batch {self.batch_count}: logs={logs}")

class NEpochCallback(Callback):
    def __init__(self, n, filepath):
        super().__init__()
        self.n = n  # n번마다 콜백 수행
        self.batch_count = 0  # 현재 배치 카운트
        self.filepath = filepath

    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % self.n == 0:
            self.model.save_weights(f"{self.filepath}_epoch_{epoch + 1}.weights.h5")
            print(f"Model weights saved for epoch {epoch + 1}")