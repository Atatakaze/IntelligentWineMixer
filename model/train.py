import pandas as pd
import numpy as np
import joblib
import argparse

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from progress.bar import Bar

# ================ User passing arguments ================ #
parser = argparse.ArgumentParser(
        prog="train.py.",
        description="Training Random Forest model for intelligent wine mixer."
    )
parser.add_argument('-d', '--data', type=str, default='./winequality.csv', required=False,
                    help="Path to wine quality dataset.")
parser.add_argument('-s', '--save', type=str, default='./RF_model_32bit.joblib', required=False,
                    help="Save name of the RF model.")

args = parser.parse_args()

PATH_TO_CSV = args.data
SAVE_NAME = args.save

# ======================================================== #

df = pd.read_csv(PATH_TO_CSV)

state = np.random.get_state()
np.random.seed(531)
ds = df.values
np.random.shuffle(ds)
np.random.set_state(state)

data = ds[:, 0:9]    # 取出所有資料列的第 0 到 8 欄資料做為樣本資料
label = ds[:, 9]     # 取出所有資料列的第 9 欄資料做為標籤資料

split_ratio = 0.7
x_train = data[:int(data.shape[0] * split_ratio), :]
y_train = label[:int(label.shape[0] * split_ratio)]

x_test = data[int(data.shape[0] * split_ratio):, :]
y_test = label[int(label.shape[0] * split_ratio):]

print('Data shape : {}, {}'.format(data.shape, label.shape))
print('\n-------------------------------------------')
print('Training data')
print('x_train, y_train = {}, {}'.format(x_train.shape, y_train.shape))
print('Testing data')
print('x_test, y_test = {}, {}\n'.format(x_test.shape, y_test.shape))

# training with different number of trees
mse_history = []
nTreeList = np.arange(50, 500, 10)
with Bar('Training ...') as bar:
    for iTrees in nTreeList:
        depth = None
        
        model = RandomForestRegressor(n_estimators=iTrees, max_depth=depth, random_state=531)
        model.fit(x_train, y_train)

        #Accumulate mse on test set
        prediction = model.predict(x_test)
        mse_history.append(mean_squared_error(y_test, prediction))

        bar.next()

print('MSE: {}'.format(mse_history[-1]))

# save model
print('Save model ...')
joblib.dump(model, SAVE_NAME)