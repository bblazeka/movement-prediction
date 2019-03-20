import pickle
import csv
import calendar
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import  MultipleLocator, FormatStrFormatter
from scipy.interpolate import spline
from IPython.core.display import display_html
from keras.models import load_model
from utils import np_haversine, density_map, get_clusters, plot_embeddings
from data import load_data
from training import full_train, start_new_session, process_features, create_model

def training():
    full_train(n_epochs=100, batch_size=200, save_prefix='mymodel')

def plotting():
    with open('cache/mymodel-history.pickle', 'rb') as handle:
        history = pickle.load(handle)

    # Interpolate a smooth curve from the raw validation loss
    n_epochs = len(history['val_loss'])
    x_smooth = np.linspace(0, n_epochs-1, num=10)
    y_smooth = spline(range(n_epochs), history['val_loss'], x_smooth)

    plt.figure(figsize=(7.5,4))
    plt.plot(history['loss'])
    plt.plot(history['val_loss'])
    plt.plot(x_smooth, y_smooth)
    plt.title('Evolution of loss values during training')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.xticks(fontsize=9)
    plt.axes().xaxis.set_major_locator(MultipleLocator(10))
    plt.legend(['train', 'validation', 'smoothened validation'], loc='upper right')
    plt.show()

def evaluating():
    data = load_data()
    clusters = get_clusters(data.train_labels)
    start_new_session()
    model = create_model(data.metadata, clusters)
    model.load_weights('cache/mymodel-100-2.1949.hdf5')

    input = data.validation
    validation_predictions = model.predict(process_features(input))
    print(type(input))
    print(np_haversine(validation_predictions, data.validation_labels).mean())

if __name__ == '__main__':
    evaluating()